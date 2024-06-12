local json = require("json")
-- local http = require("socket.http")
local http = require("simplehttp")

local Initial_Table = {
    v = 'zh',
    i = 'ch',
    u = 'sh'
}

local Special_Final_Table = {
    t = { 'ue', 'jqx', 've' },
    y = { 'uai', 'gkhviu', 'ing' },
    s = { 'iong', 'jxq', 'ong' },
    d = { 'iang', 'nljqx', 'uang' },
    w = { 'ia', 'jxqdl', 'ua' },
    v = { 'v', 'ln', 'ui' }
}

local Final_Table = {
    q = 'iu',
    -- w = 'ia',
    -- w = 'ua',
    r = 'uan',
    -- t = 'ue',
    -- t = 've',
    -- y = 'ing,uai',
    -- y = 'uai',
    o = 'uo',
    p = 'un',
    -- s = 'iong,ong',
    -- s = 'ong',
    -- d = 'iang,uang',
    -- d = 'uang',
    f = 'en',
    g = 'eng',
    h = 'ang',
    j = 'an',
    k = 'ao',
    l = 'ai',
    z = 'ei',
    x = 'ie',
    c = 'iao',
    b = 'ou',
    n = 'in',
    m = 'ian'
}

local function trans_double(input)
    local p = 0
    local result = ''
    local initial = ''
    for i = 1, #input do
        local s = input:sub(i, i)
        if p == 0 then
            initial = s
            if Initial_Table[s] == nil then
                result = result .. s
            else
                result = result .. Initial_Table[s]
            end
            p = 1
        else
            if Final_Table[s] ~= nil then
                result = result .. Final_Table[s]
            elseif Special_Final_Table[s] ~= nil then
                st = Special_Final_Table[s]
                if st[2]:find(initial) ~= nil then
                    result = result .. st[1]
                else
                    result = result .. st[3]
                end
            else
                result = result .. s
            end
            p = 0
        end
    end
    return result
end

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
    log.info(trans_double(input))
    local reply = http.request(make_url(trans_double(input), 0, 5))
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
