local json = require("json")
local http = require("socket.http")
local url = require("socket.url")

http.PROXY = "http://localhost:7890"

local char_to_hex = function(c)
    return string.format("%%%02X", string.byte(c))
end

local function urlencode(url)
    if url == nil then
        return
    end
    url = url:gsub("\n", "\r\n")
    url = url:gsub("([^%w ])", char_to_hex)
    url = url:gsub(" ", "+")
    return url
end

local function make_url(input)
    local sl = "en"
    local tl = "zh_TW"
    return 'http://translate.googleapis.com/translate_a/single?client=gtx&sl=' .. sl .. '&tl=' .. tl .. '&dt=t&q=' ..
               urlencode(input)
end

local function translator(input, seg)
    local context = input
    -- 'as space key
    local string = context:gsub("%'", " ")

    -- local reply = io.popen('curl -s "' .. make_url(string) .. '"'):read("*all")
    local reply = http.request(make_url(string))
    local data = json.decode(reply)

    for i, v in ipairs(data) do
        -- get the output string
        local output = v[1][1]
        local c = Candidate("translate", seg.start, seg._end, output, "翻译")
        c.quality = 2
        -- add to Candidate
        yield(c)
        yield(Candidate("translate", seg.start, seg._end, string, "原文"))
    end
end

return translator
