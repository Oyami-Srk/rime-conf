local json = require("json")
-- local http = require("socket.http")
local http = require("simplehttp")
local double_pinyin = require("double_pinyin")

-- local function make_url(input, bg, ed)
--     return 'http://olime.baidu.com/py?input=' .. input .. '&inputtype=py&bg=' .. bg .. '&ed=' .. ed ..
--         '&result=hanzi&resultcoding=utf-8&ch_en=0&clientinfo=web&version=1'
-- end

local function make_url(input, bg, ed)
    return 'https://olime.baidu.com/py?input=' .. input ..
        '&inputtype=py&bg=' .. bg .. '&ed=' .. ed ..
        '&result=hanzi&resultcoding=utf-8&ch_en=0&clientinfo=web&version=1'
end

local function memoryCallback(memory, commit)
    for i, dictentry in ipairs(commit:get()) do
        -- memory:update_userdict(dictentry, 0, "") -- do nothing to userdict
        if dictentry.comment == "(百度云拼音)" then
            log.info("Remember: " .. dictentry.text .. " " .. dictentry.weight .. " " .. dictentry.comment .. "")
            local result = memory:update_userdict(dictentry, 1, "") -- update entry to userdict
            log.info("Remember reuslt: " .. tostring(result))
        end
        -- memory:update_userdict(dictentry,1,"") -- delete entry to userdict
    end
    return true
end

local function init(env)
    log.info("Schema: " .. env.engine.schema.schema_id)
    env.mem = Memory(env.engine, env.engine.schema) --  ns= "translator"
    -- env.mem = Memory(env.engine, Schema("zrm_pinyin")) --  ns= "translator"
    env.mem:memorize(function(commit)
        memoryCallback(env.mem, commit)
    end)
end

local function translator(input, seg, env)
    -- local handle = io.popen('curl -s "' .. make_url(trans_double(input), 0, 5) .. '"')
    local pinyin = double_pinyin:expand(input)
    local reply = http.request(make_url(pinyin, 0, 5))
    log.error("Request for online pinyin for `" .. pinyin .. "`, result is: " .. reply)
    -- local reply = handle:read('*all')
    local _, j = pcall(json.decode, reply)

    if j.status == "T" and j.result and j.result[1] then
        for i, v in ipairs(j.result[1]) do
            local c = Candidate("simple", seg.start, seg.start + v[2], v[1], "(百度云拼音)")
            c.quality = 2
            if string.gsub(v[3].pinyin, "'", "") == string.sub(input, 1, v[2]) then
                c.preedit = string.gsub(v[3].pinyin, "'", " ")
            end
            local dict_entry = DictEntry()
            dict_entry.text = v[1]
            dict_entry.comment = "(百度云拼音)"
            code = string.gsub(v[3].pinyin, "'", " ") .. " " -- I did't know why
            -- code = input
            dict_entry.custom_code = code
            local ph = Phrase(env.mem, "baiduyun", seg.start, seg.start + v[2], dict_entry)
            ph.quality = 2
            ph.text = v[1]
            ph.comment = "(百度云拼音)"
            ph.code = code
            local candidate = ph:toCandidate()
            yield(candidate)
        end
    end
end

return {
    init = init,
    func = translator
}
