local json = require("json")
local http = require("socket.http")
local url = require("socket.url")

http.PROXY="http://localhost:7890"

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
    local sl = "zh_TW"
    local tl = "en"
    return 'http://translate.googleapis.com/translate_a/single?client=gtx&sl=' .. sl .. '&tl=' .. tl .. '&dt=t&q=' ..
               urlencode(input)
end

local function translator(input, seg, env)
    local S = env.focus_text
    -- print(env.max_quality)
    -- local reply = io.popen('curl -s "' .. make_url(S) .. '"'):read("*all")
    local reply = http.request(make_url(S))
    local data = json.decode(reply)

    for i, v in ipairs(data) do
        -- get the output string
        local output = v[1][1]
        -- print(output)
        local c = Candidate("translation", seg.start, seg._end, output, "翻译")
        c.quality = 2
        -- c.quality = env.selected_candidate.quality
        -- c.quality = tonumber(tostring(env.max_quality):match('(%d+).')) + 1
        yield(c)
    end
end

return translator
