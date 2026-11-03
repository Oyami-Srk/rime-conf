local http = require("simplehttp")
local iconv = require("iconv")
local double_pinyin = require("double_pinyin")
local request_timeout = 2 -- seconds; cloud lookup runs on the input thread

function rc(x)
    local start = 0
    for i = 1, #x do
        start = start ~ string.byte(x, i)
    end
    return string.char(start)
end

function serial_keys(keys)
    local token = "\0\5\0\0\0\0\1"
    local total_len = #token + #keys + 3
    local data = string.char(total_len) .. token .. string.char(#keys) .. keys
    return data .. rc(data)
end

function key_from_serial(data)
    local token = "\0\5\0\0\0\0\1"
    local total_len = string.byte(data, 1)
    local key_len = total_len - #token - 3
    return string.sub(data, -key_len - 1, -2)
end

function open_sogou(keys, durtot, version)
    durtot = durtot or 0
    version = version or "3.7"
    local url = string.format(
        "http://shouji.sogou.com/web_ime/mobile.php?durtot=%d&h=000000000000000&r=store_mf_wandoujia&v=%s", durtot,
        version)
    local data = serial_keys(keys)
    -- simplehttp has no default timeout. Restore the shared setting because
    -- the Baidu translator also uses this module.
    local previous_timeout = http.TIMEOUT
    http.TIMEOUT = request_timeout
    log.info("[sougou] request started: " .. keys)
    local ok, response, status = pcall(http.request, url, data)
    http.TIMEOUT = previous_timeout
    if not ok then
        log.error("[sougou] request failed: " .. tostring(response))
        return nil, response
    end
    log.info("[sougou] request finished, status: " .. tostring(status))
    return response, status
end

function parse_result(result)
    local words = {}

    if type(result) ~= "string" or #result < 0x14 then
        log.error("[sougou] empty or truncated response")
        return words
    end

    if string.byte(result, 1) + 2 ~= #result then
        log.error("[sougou] invalid size, expected", string.byte(result, 1) + 2, "got", #result)
        return words
    end

    local num_words = string.unpack("<H", string.sub(result, 0x12 + 1, 0x12 + 2))
    if num_words == 0 or num_words > 32 then
        log.warning("[sougou] invalid word count: " .. tostring(num_words))
        return words
    end

    local pos = 0x14 -- data packet starts at 0x14

    for i = 1, num_words do
        local str_len = string.unpack("<H", string.sub(result, pos + 1, pos + 2))
        if str_len == 0 or str_len > 0xFF then
            log.error("[sougou] Invalid string length")
        end
        pos = pos + 2

        if str_len == 0 then
            -- Skip empty string
        else
            local word = string.sub(result, pos + 1, pos + str_len)
            local cd, err = iconv.new("utf-8", "utf-16le")
            if not cd then
                log.error(string.format("[sougou] word %s can't convert to utf-8: %s", word, err))
            else
                word, err = cd:iconv(word)
                if not word then
                    log.error(string.format("[sougou] word can't convert to utf-8: %s", err))
                end
            end
            table.insert(words, word)
        end
        pos = pos + str_len

        -- unknown part, like 0x12c, 0x12b, etc.
        str_len = string.unpack("<H", string.sub(result, pos + 1, pos + 2))
        pos = pos + str_len + 2

        -- unknown part, like 0x01, 0x02, etc.
        str_len = string.unpack("<H", string.sub(result, pos + 1, pos + 2))
        pos = pos + str_len + 2 + 1
    end

    if pos ~= #result then
        log.warning("[sougou] buffer not exhausted!")
    end

    return words
end

function get_cloud_words(keys)
    local resp, code = open_sogou(keys)
    if code ~= 200 then
        log.error(string.format("[sougou] invalid response for input <%s>: status: %s", keys, tostring(code)))
        return {}
    end

    local ok, words = pcall(parse_result, resp)
    if not ok then
        log.error("[sougou] cannot parse response: " .. tostring(words))
        return {}
    end
    return words
end

local function get_user_code(input)
    -- Only learn complete double-pinyin syllables. Apostrophes/spaces may
    -- separate syllables; auxiliary codes and abbreviations are not decoded.
    if not input:match("^[a-z' ]+$") then
        return nil
    end

    local parts = {}
    local syllable_count = 0
    for part in input:gmatch("[a-z]+") do
        if #part % 2 ~= 0 then
            return nil
        end
        -- expand() prefixes each syllable with the delimiter, including the first.
        parts[#parts + 1] = double_pinyin:expand(part, " "):gsub("^ +", "")
        syllable_count = syllable_count + #part / 2
    end
    if syllable_count == 0 then
        return nil
    end

    -- Rime user-dictionary keys need a space after every full-pinyin syllable.
    return table.concat(parts, " ") .. " ", syllable_count
end

local function remember(context, env)
    local entries = {}
    for _, seg in ipairs(context.composition:toSegmentation():get_segments()) do
        local candidate = seg:get_selected_candidate()
        local genuine = candidate and candidate:get_genuine()
        if genuine and genuine.type == "sougou" then
            local input = context.input:sub(genuine.start + 1, genuine._end)
            local code, syllable_count = get_user_code(input)
            -- The cloud service may complete/correct the input. Do not attach
            -- the typed reading to a result with a different character count.
            if code and utf8.len(genuine.text) == syllable_count then
                local entry = DictEntry()
                entry.text = genuine.text
                entry.custom_code = code
                entries[#entries + 1] = entry
            end
        end
    end
    if #entries == 0 then
        return
    end

    -- Open the main user dictionary only when actually committing a cloud
    -- candidate, and release it before returning to the input loop.
    local memory = Memory(env.engine, env.engine.schema, "translator")
    local ok, err = pcall(function()
        memory:start_session()
        for _, entry in ipairs(entries) do
            if memory:update_userdict(entry, 1, "") then
                log.info("[sougou] remembered: " .. entry.text .. " / " .. entry.custom_code)
            else
                log.error("[sougou] failed to remember: " .. entry.text)
            end
        end
    end)
    memory:finish_session()
    memory:disconnect()
    if not ok then
        log.error("[sougou] cannot update user dictionary: " .. tostring(err))
    end
end

local function init(env)
    -- Keep cloud candidates simple: Phrase candidates without numeric codes
    -- would also be learned by script_translator with an empty/partial code.
    env.commit_connection = env.engine.context.commit_notifier:connect(function(context)
        remember(context, env)
    end)
end

local function fini(env)
    if env.commit_connection then
        env.commit_connection:disconnect()
        env.commit_connection = nil
    end
end

local function translator(input, seg)
    local code = get_user_code(input)
    local pinyin = code and code:gsub(" ", "") or double_pinyin:expand(input)
    local list = get_cloud_words(pinyin)
    local yielded_candidates = 0
    local max_candidates = 5
    for i, v in ipairs(list) do
        if yielded_candidates >= max_candidates then
            break
        end

        local c = Candidate("sougou", seg.start, seg._end, v, "(搜狗云拼音)")
        c.quality = 2
        yield(c)

        yielded_candidates = yielded_candidates + 1
    end
end

return {
    init = init,
    func = translator,
    fini = fini
}
