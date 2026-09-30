local _M = {}

local Initial_Table = {
    v = 'zh',
    i = 'ch',
    u = 'sh'
}

-- Zero-initial syllables (a/o/e...): typed as their literal pinyin
-- (ai, ei, ao, ou, an, en, er), as a doubled vowel (aa, oo, ee),
-- as a doubled vowel plus final key (ah, eg, os), or via the
-- mspy-style aliases (oa, oe).
local Zero_Initial_Table = {
    aa = 'a',
    oa = 'a',
    oo = 'o',
    ee = 'e',
    oe = 'e',
    ai = 'ai',
    ei = 'ei',
    ao = 'ao',
    ou = 'ou',
    an = 'an',
    en = 'en',
    er = 'er',
    ah = 'ang',
    eg = 'eng',
    os = 'ong',
}

local Special_Final_Table = {
    -- if initial in second string, use first string, else use third string
    t = { 'ue', 'jqxy', 've' },
    y = { 'uai', 'gkhviu', 'ing' },
    s = { 'iong', 'jxq', 'ong' },
    d = { 'iang', 'nljqx', 'uang' },
    w = { 'ia', 'jxqdnl', 'ua' },
    v = { 'v', 'ln', 'ui' },
    o = { 'o', 'bfmpwy', 'uo' }
}

local Final_Table = {
    q = 'iu',
    r = 'uan',
    p = 'un',
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

local function translate_one(initial, following)
    -- Zero-initial / special syllables must be resolved from the raw pair
    -- first, otherwise "er" would expand as "e" + "uan", "an" as "a" + "in",
    -- and "oo" as "o" + "uo".
    local special = Zero_Initial_Table[initial .. following]
    if special ~= nil then
        return special
    end

    local result = ""

    -- Process initial character (vowel)
    result = Initial_Table[initial] or initial

    if Initial_Table[initial] == nil then
        result = initial
    else
        result = Initial_Table[initial]
    end

    -- Process following character (final)
    if Final_Table[following] ~= nil then
        result = result .. Final_Table[following]
    elseif Special_Final_Table[following] ~= nil then
        local st = Special_Final_Table[following]
        if st[2]:find(initial) ~= nil then
            result = result .. st[1]
        else
            result = result .. st[3]
        end
    else
        result = result .. following
    end

    return result
end


function _M:expand(input, delimiter)
    local delimiter = delimiter or ""
    local result = ""
    for i = 1, #input, 2 do
        local initial = input:sub(i, i)
        local following = input:sub(i + 1, i + 1)
        result = result .. delimiter .. translate_one(initial, following)
    end
    return result
end

return _M