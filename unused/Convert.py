from pypinyin.contrib.tone_convert import to_normal, to_tone, to_initials, to_finals
import re
all_list = ['gu', 'qiao', 'qian', 'qve', 'ge', 'gang', 'ga', 'lian', 'liao', 'rou', 'zong',
            'tu', 'seng', 'yve', 'ti', 'te', 'jve', 'ta', 'nong', 'zhang', 'fan', 'ma', 'gua', 'die', 'gui',
            'guo', 'gun', 'sang', 'diu', 'zi', 'ze', 'za', 'chen', 'zu', 'ba', 'dian', 'diao', 'nei', 'suo',
            'sun', 'zhao', 'sui', 'kuo', 'kun', 'kui', 'cao', 'zuan', 'kua', 'den', 'lei', 'neng', 'men',
            'mei', 'tiao', 'geng', 'chang', 'cha', 'che', 'fen', 'chi', 'fei', 'chu', 'shui', 'me', 'tuan',
            'mo', 'mi', 'mu', 'dei', 'cai', 'zhan', 'zhai', 'can', 'ning', 'wang', 'pie', 'beng', 'zhuang',
            'tan', 'tao', 'tai', 'song', 'ping', 'hou', 'cuan', 'lan', 'lao', 'fu', 'fa', 'jiong', 'mai',
            'xiang', 'mao', 'man', 'a', 'jiang', 'zun', 'bing', 'su', 'si', 'sa', 'se', 'ding', 'xuan',
            'zei', 'zen', 'kong', 'pang', 'jie', 'jia', 'jin', 'lo', 'lai', 'li', 'peng', 'jiu', 'yi', 'yo',
            'ya', 'cen', 'dan', 'dao', 'ye', 'dai', 'zhen', 'bang', 'nou', 'yu', 'weng', 'en', 'ei', 'kang',
            'dia', 'er', 'ru', 'keng', 're', 'ren', 'gou', 'ri', 'tian', 'qi', 'shua', 'shun', 'shuo', 'qun',
            'yun', 'xun', 'fiao', 'zan', 'zao', 'rang', 'xi', 'yong', 'zai', 'guan', 'guai', 'dong', 'kuai',
            'ying', 'kuan', 'xu', 'xia', 'xie', 'yin', 'rong', 'xin', 'tou', 'nian', 'niao', 'xiu', 'fo',
            'kou', 'niang', 'hua', 'hun', 'huo', 'hui', 'shuan', 'quan', 'shuai', 'chong', 'bei', 'ben',
            'kuang', 'dang', 'sai', 'ang', 'sao', 'san', 'reng', 'ran', 'rao', 'ming', 'tei', 'lie', 'lia',
            'min', 'pa', 'lin', 'mian', 'mie', 'liu', 'zou', 'miu', 'nen', 'kai', 'kao', 'kan', 'ka', 'ke',
            'yang', 'ku', 'deng', 'dou', 'shou', 'chuang', 'nang', 'feng', 'meng', 'cheng', 'di', 'de', 'da',
            'bao', 'gei', 'du', 'gen', 'qu', 'shu', 'sha', 'she', 'ban', 'shi', 'bai', 'nun', 'nuo', 'sen', 'lve',
            'kei', 'fang', 'teng', 'xve', 'lun', 'luo', 'ken', 'wa', 'wo', 'ju', 'tui', 'wu', 'le', 'ji', 'huang',
            'tuo', 'cou', 'la', 'mang', 'ci', 'tun', 'tong', 'ca', 'pou', 'ce', 'gong', 'cu', 'lv', 'dun', 'pu',
            'ting', 'qie', 'yao', 'lu', 'pi', 'po', 'suan', 'chua', 'chun', 'chan', 'chui', 'gao', 'gan', 'zeng',
            'gai', 'xiong', 'tang', 'pian', 'piao', 'cang', 'heng', 'xian', 'xiao', 'bian', 'biao', 'zhua', 'duan',
            'cong', 'zhui', 'zhuo', 'zhun', 'hong', 'shuang', 'juan', 'zhei', 'pai', 'shai', 'shan', 'shao', 'pan',
            'pao', 'nin', 'hang', 'nie', 'zhuai', 'zhuan', 'yuan', 'niu', 'na', 'miao', 'guang', 'ne', 'hai', 'han',
            'hao', 'wei', 'wen', 'ruan', 'cuo', 'cun', 'cui', 'bin', 'bie', 'mou', 'nve', 'shen', 'shei', 'fou', 'xing',
            'qiang', 'nuan', 'pen', 'pei', 'rui', 'run', 'ruo', 'sheng', 'dui', 'bo', 'bi', 'bu', 'chuan', 'qing',
            'chuai', 'duo', 'o', 'chou', 'ou', 'zui', 'luan', 'zuo', 'jian', 'jiao', 'sou', 'wan', 'jing', 'qiong',
            'wai', 'long', 'yan', 'liang', 'lou', 'huan', 'hen', 'hei', 'huai', 'shang', 'jun', 'hu', 'ling', 'ha', 'he',
            'zhu', 'ceng', 'zha', 'zhe', 'zhi', 'qin', 'pin', 'ai', 'chai', 'qia', 'chao', 'ao', 'an', 'qiu', 'ni', 'zhong',
            'zang', 'nai', 'nan', 'nao', 'chuo', 'tie', 'you', 'nu', 'nv', 'zheng', 'leng', 'zhou', 'lang', 'e', 'jue', 'xue',
            'yue', 'eng', 'lue', 'nue', 'que', 'rua']
__removetone_dict = {
    'ā': 'a',
    'á': 'a',
    'ǎ': 'a',
    'à': 'a',
    'ē': 'e',
    'é': 'e',
    'ě': 'e',
    'è': 'e',
    'ī': 'i',
    'í': 'i',
    'ǐ': 'i',
    'ì': 'i',
    'ō': 'o',
    'ó': 'o',
    'ǒ': 'o',
    'ò': 'o',
    'ū': 'u',
    'ú': 'u',
    'ǔ': 'u',
    'ù': 'u',
    'ü': 'v',
    'ǖ': 'v',
    'ǘ': 'v',
    'ǚ': 'v',
    'ǜ': 'v',
    'ń': 'n',
    'ň': 'n',
    '': 'm',
}
__pinyin = set(all_list)


def all_pinyin():
    for _ in __pinyin:
        yield _


def remove_tone(one_py):
    """ 删除拼音中的音调
    lǔ -> lu
    """
    one_py = as_text(one_py)
    r = as_text('')
    for c in one_py:
        if c in __removetone_dict:
            r += __removetone_dict[c]
        else:
            r += c
    return r


def as_text(v):  # 生成unicode字符串
    if v is None:
        return None
    elif isinstance(v, bytes):
        return v.decode('utf-8', errors='ignore')
    elif isinstance(v, str):
        return v
    else:
        raise ValueError('Unknown type %r' % type(v))


def py_result(result_list):
    for item in range(0, len(result_list)):
        item_list = list(result_list[item])
        num_list, res_list, num = [], [], 0
        for i in range(0, len(item_list)):
            one_py = item_list[i]
            num_list.append(one_py in __removetone_dict)
            if one_py in __removetone_dict:
                res_list.append("%s、" % one_py)
                num += 1
            else:
                res_list.append("%s" % one_py)
        if num > 1:
            py_ok = ' '.join(''.join(res_list).split("、")[:-2])
            py_end_ok = ''.join(''.join(res_list).split("、")[-2:])
            py_res = "%s %s" % (py_ok, py_end_ok)
            result_list[item] = py_res


def get_split_py(text):
    result_list = []
    py_text = remove_tone(text)

    def get_py(y):
        py_list = []
        for i in range(y, len(py_text) + 1):
            if y == 1:
                y = y - 1
            nr = py_text[y:i]
            y_nr = text[y:i]
            if nr in all_pinyin():
                py_list.append([y_nr, y, i])
        result = py_list[-1][0]

        if py_list[-1][2] < len(text):
            nr = py_text[py_list[-1][2]-1:py_list[-1][2]+1]
            anr = py_text[py_list[-1][2]:py_list[-1][2]+2]
            if nr in all_pinyin() and anr not in all_pinyin():
                result = py_list[-2][0]
        return result

    py_str = get_py(1)
    while 1:
        result_list.append(py_str)
        num = len(''.join(result_list))
        if num < len(text):
            py_str = get_py(num)
        else:
            py_result(result_list)
            break
    return ' '.join(result_list)


Initials_translation_table = {
    u'zh': 'v',
    u'sh': 'u',
    u'ch': 'i'
}

Finals_translation_table = {
    u'iu': 'q',
    u'ia': 'w',
    u'ua': 'w',
    u'uan': 'r',
    u'ue': 't',
    u've': 't',
    u'ing': 'y',
    u'uai': 'y',
    u'uo': 'o',
    u'un': 'p',
    u'iong': 's',
    u'ong': 's',
    u'iang': 'd',
    u'uang': 'd',
    u'en': 'f',
    u'eng': 'g',
    u'ang': 'h',
    u'an': 'j',
    u'ao': 'k',
    u'ai': 'l',
    u'ei': 'z',
    u'ie': 'x',
    u'iao': 'c',
    u'ui': 'v',
    u'ou': 'b',
    u'in': 'n',
    u'ian': 'm'
}

errs = []


def proc(strs):
    strs = strs.strip()
    print(strs)

    pys = list(get_split_py(strs).split(' '))
    results = []
    if len(pys) > 2:
        print(strs + " is not splited into two pinyin")
        raise Exception("err")
    for p in pys:
        print(p)
        s = ''
        y = ''
        if p == 'a':
            results.append('a')
            continue
        if p == 'e':
            results.append('e')
            continue
        if p[1] == 'h' and (p[0] == 'z' or p[0] == 'c' or p[0] == 's'):
            s = Initials_translation_table[p[:2]]
            y = p[2:]
        else:
            s = p[0]
            y = p[1:]
        if y in Finals_translation_table.keys():
            y = Finals_translation_table[y]
        elif len(y) != 1:
            print("Error with pinyin: " + p + " with remaining as " + y)
        results.append(s+y)
    return results


manually_remap = {
    "alai": "aall",
    "anv": "aanv",
    "aru": "aaru",
    "atu": "aatu",
    "axia": "aaxw",
    "ayin": "aayn",
    "azeng": "aazg",
    "biankz": "bmkb",
    "binong": "bins",
    "changong": "ijgs",
    "cherong": "iers",
    "cherou": "ierb",
    "ebao": "eebk",
    "echu": "eeiu",
    "edao": "eedk",
    "eer": "eeer",
    "ege": "eege",
    "ejian": "eejm",
    "emu": "eemu",
    "eniao": "eenc",
    "eqian": "eeqm",
    "equan": "eeqr",
    "ese": "eese",
    "eshu": "eeuu",
    "eye": "eeye",
    "eyi": "eeyi",
    "ezhui": "eevv",
    "gangong": "gjgs",
    "gengong": "gfgs",
    "gerong": "gers",
    "gerou": "gerb",
    "guao": "guao",
    "gunong": "guns",
    "henong": "hens",
    "heran": "herj",
    "herong": "hers",
    "herou": "herb",
    "jiangong": "jmgs",
    "jingong": "jngs",
    "juerou": "jtrb",
    "mengong": "mfgs",
    "miang": "miah",
    "nangong": "njgs",
    "pangong": "pjgs",
    "pinong": "pins",
    "rengong": "rfgs",
    "ruao": "ruao",
    "shangong": "ujgs",
    "shengong": "ufgs",
    "sheran": "uerj",
    "sherou": "uerb",
    "shunong": "uuns",
    "tuang": "tuah",
    "tunong": "tuns",
    "xingong": "xngs",
    "xinong": "xins",
    "xuenong": "xtns",
    "xueran": "xtrj",
    "xuerong": "xtrs",
    "xuerou": "xtrb",
    "yangong": "yjgs",
    "yingong": "yngs",
    "yinong": "yins",
    "yuang": "yuah",
    "yuenong": "ytns",
    "yueran": "ytrj",
    "yuerao": "ytrk",
    "yuerong": "ytrs",
    "yuerou": "ytrb",
    "yunong": "yuns",
    "zhuao": "vuao",
    "zhunong": "vuns",
    "zuang": "zuah",
    "zunong": "zuns",
    "renang": "rfah",
    "rene": "rfee",
    "renge": "rfge",
    "rengeng": "rfgg",
    "daoe": "dkee",
    "koue": "kbee",
    "angtu": "ahtu",
    "angwa": "ahwa",
    "angye": "ahye",
    "bana": "bana",
    "bange": "bjge",
    "binang": "binh",
    "binga": "byaa",
    "binge": "byee",
    "caoang": "ckah",
    "caoe": "cke",
    "change": "ijge",
    "cheang": "ieah",
    "chee": "ieee",
    "chenge": "ifge",
    "chie": "iiee",
    "chongang": "igah",
    "chonge": "isee",
    "chue": "iuee",
    "daie": "dlee",
    "dana": "dana",
    "dange": "djge",
    "erang": "eerh",
    "ere": "eree",
    "geang": "geah",
    "gee": "geee",
    "guanga": "gdaa",
    "guange": "gdee",
    "gue": "guee",
    "guna": "guna",
    "hange": "hjge",
    "huange": "hdee",
    "huoang": "hoah",
    "huoe": "hoee",
    "jiange": "jmge",
    "jiaoe": "jkee",
    "jina": "jnaa",
    "jinang": "jnah",
    "jine": "jnee",
    "jingang": "jngh",
    "jinge": "jnge",
    "jingeng": "jngg",
    "kange": "kjge",
    "kenge": "kfge",
    "koua": "kbaa",
    "kouang": "kbah",
    "kuanga": "kdaa",
    "kue": "kuee",
    "lange": "ljge",
    "liange": "ldge",
    "linge": "lnge",
    "maang": "maah",
    "mae": "maee",
    "mana": "mana",
    "mena": "mfaa",
    "mengang": "mfgh",
    "menge": "mfge",
    "mina": "mina",
    "muang": "muah",
    "mue": "muee",
    "nange": "njge",
    "niange": "nmge",
    "niaoang": "ncah",
    "niue": "nqee",
    "nva": "nvaa",
    "pange": "pjge",
    "pineng": "pins",
    "qiange": "qmge",
    "quane": "qree",
    "rengang": "rfgh",
    "riang": "riah",
    "rie": "riee",
    "sange": "sjge",
    "shana": "ujaa",
    "shanang": "ujah",
    "shane": "ujee",
    "shangang": "ujgh",
    "shange": "ujge",
    "shangeng": "ujgg",
    "shene": "ufee",
    "shenge": "ufge",
    "shia": "uiaa",
    "shiang": "uiah",
    "shie": "uiee",
    "shouang": "ubah",
    "shoue": "ubee",
    "shuia": "uvaa",
    "shuiang": "uvah",
    "shuie": "uvee",
    "sia": "siaa",
    "tue": "tuee",
    "tuna": "tuna",
    "tunang": "tunh",
    "tuneng": "tung",
    "waang": "waah",
    "weie": "wzee",
    "xiange": "xmge",
    "xinang": "xnah",
    "xine": "xnee",
    "xineng": "xing",
    "xingang": "xngh",
    "xinge": "xnge",
    "xingeng": "xngg",
    "xionge": "xsee",
    "yanang": "yjah",
    "yane": "yjee",
    "yange": "yjge",
    "yangeng": "yjgg",
    "yie": "yiee",
    "yina": "yina",
    "yinang": "yinh",
    "yineng": "ying",
    "yinge": "ynge",
    "youang": "ybah",
    "yueang": "ytah",
    "yuee": "ytee",
    "yuna": "yuna",
    "yunang": "yunh",
    "yuneng": "yung",
    "zenga": "zgaa",
    "zhange": "vjge",
    "zhonge": "vsee",
    "zhue": "vuee",
    "zhuna": "vuna",
    "zhunang": "vunh",
    "zhuneng": "vung",
    "zouang": "zbah",
    "zoue": "zbee",
    "zue": "zuee",
    "zuna": "zuna",
    "zunang": "zunh",
    "zuneng": "zung",
    "caoe": "ckee"
}

i = 0
with open('aaaaa', 'r') as f:
    with open('b', 'w') as w:
        for line in f.readlines():
            pyaaa = line[2:].strip()
            try:
                if pyaaa in manually_remap.keys():
                    zrm = manually_remap[pyaaa]
                    if len(zrm) == 0:
                        rr += line
                else:
                    zrm = ''.join(proc(pyaaa))
            except:
                errs.append(pyaaa)
            if len(zrm) != 4 and len(zrm) != 2:
                print("Pinyin " + pyaaa + " not converted into 4 char zrm.")
                exit(0)
            result = line[:2] + zrm
            print(result)
            w.write(result+"\n")
            i += 1
            print("============================" + str(i))
