-- easy_en_enhance_filter: 连续输入增强
-- 详见 `lua/easy_en.lua`
local easy_en = require("easy_en")
easy_en_enhance_filter = easy_en.enhance_filter

-- custom translator
function date_translator(input, seg)
    if (input == "date") then
        --- Candidate(type, start, end, text, comment)
        yield(Candidate("date", seg.start, seg._end, os.date("%Y-%m-%d"), ""))
        yield(Candidate("date", seg.start, seg._end, os.date("%Y年%m月%d日"), ""))
        yield(Candidate("date", seg.start, seg._end, os.date("%m-%d"), ""))
        yield(Candidate("date", seg.start, seg._end, os.date("%Y/%m/%d"), ""))
    end
    if (input == "time") then
        --- Candidate(type, start, end, text, comment)
        yield(Candidate("time", seg.start, seg._end, os.date("%H:%M"), ""))
        yield(Candidate("time", seg.start, seg._end, os.date("%H:%M:%S"), ""))
    end
    if (input == "week") then
        local weakTab = {'日', '一', '二', '三', '四', '五', '六'}
        yield(Candidate("week", seg.start, seg._end, "周" .. weakTab[tonumber(os.date("%w") + 1)], ""))
        yield(Candidate("week", seg.start, seg._end, "星期" .. weakTab[tonumber(os.date("%w") + 1)], ""))
        yield(Candidate("week", seg.start, seg._end, "礼拜" .. weakTab[tonumber(os.date("%w") + 1)], ""))
    end
end

-- custom filter
--- 过滤器：单字在先
function single_char_first_filter(input)
    local l = {}
    for cand in input:iter() do
        if (utf8.len(cand.text) == 1) then
            yield(cand)
        else
            table.insert(l, cand)
        end
    end
    for cand in ipairs(l) do
        yield(cand)
    end
end

local charset = require("charset")
charset_filter = charset.filter
charset_comment_filter = charset.comment_filter

-- select_character_processor: 以词定字
-- 详见 `lua/select_character.lua`
select_character_processor = require("select_character")

--- 百度云拼音，Control+t 为云输入触发键
--- 使用方法：
--- 将 "lua_translator@baidu_translator" 和 "lua_processor@baidu_processor"
--- 分别加到输入方案的 engine/translators 和 engine/processors 中
baidu_require = require("baidu")
local baidu = require("trigger")("Control+b", baidu_require.func)
baidu_translator = {
    init = baidu_require.init,
    func = baidu.translator
}
baidu_processor = baidu.processor

local c2e = require("trigger")("Control+t", require("c2e"))
c2e_translator = c2e.translator
c2e_processor = c2e.processor

local e2c = require("trigger")("Control+e", require("e2c"))
e2c_translator = e2c.translator
e2c_processor = e2c.processor

--- xnumber
number_translator = require("numberx")
