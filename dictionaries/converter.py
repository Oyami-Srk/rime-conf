#! /usr/bin/env python3
raw_dict = "zrm_pinyin.dict.yaml"
char_dict = "base_singal_char_weight.txt"
output = "zrm_pinyin.weight.dict.yaml"
additional_codec = "additional_codec_for_zrm.txt"

zrm_table = {}

Initials_translation_table = {
    u'zh': 'v',
    u'sh': 'u',
    u'ch': 'i'
}

Reverse_Initials_translation_table = {
    u'v': 'zh',
    u'u': 'sh',
    u'i': 'ch'
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


Reverse_Finals_translation_table = {
    u'q': 'iu',
    u'w': 'ia',
    u'w': 'ua',
    u'r': 'uan',
    u't': 'ue',
    u't': 've',
    u'y': 'ing',
    u'y': 'uai',
    u'o': 'uo',
    u'p': 'un',
    u's': 'iong',
    u's': 'ong',
    u'd': 'iang',
    u'd': 'uang',
    u'f': 'en',
    u'g': 'eng',
    u'h': 'ang',
    u'j': 'an',
    u'k': 'ao',
    u'l': 'ai',
    u'z': 'ei',
    u'x': 'ie',
    u'c': 'iao',
    u'v': 'ui',
    u'b': 'ou',
    u'n': 'in',
    u'm': 'ian',
}


def convert_zrm_to_py(zrm: str):
    py = ""
    if zrm[0] in Reverse_Initials_translation_table.keys():
        py += Reverse_Initials_translation_table[zrm[0]]
    else:
        py += zrm[0]

    if zrm[1] in Reverse_Finals_translation_table.keys():
        py += Reverse_Finals_translation_table[zrm[1]]
    else:
        py += zrm[1]
    return py


manually_map = {
    u'a': ['oa', 'aa'],
    u'e': ['oe', 'ee'],
    u'o': ['oo'],
    u'an': ['an', 'oj'],
    u'en': ['en', 'of'],
    u'ou': ['ou', 'ob'],
    u'ang': ['ah', 'oh'],
    u'eng': ['eg', 'og'],
}


def convert_py_to_zrm(py: str):
    if py in manually_map.keys():
        return manually_map[py]

    zrm = ""

    if py[0] in "zcs" and py[1] == "h":
        zrm += Initials_translation_table[py[:2]]
        final = py[2:]
    else:
        zrm += py[0]
        final = py[1:]

    if final in Finals_translation_table.keys():
        zrm += Finals_translation_table[final]
    else:
        zrm += final

    assert(len(zrm) == 2)
    return [zrm]


class py_char:
    def __init__(self, char: str):
        self.char = char
        self.pinyin = []
        self.code = []

    def push_pinyin(self, py: str, freq: float):
        if py not in dict(self.pinyin).keys():
            self.pinyin.append((py, freq))

    def push_code(self, code: str):
        if code not in self.code:
            self.code.append(code)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        s = "[" + self.char + "\t"
        for p in self.pinyin:
            s += p[0] + ", "
        s = s.rstrip(', ')
        s += "\t"
        for c in self.code:
            s += c + ", "
        s = s.rstrip(', ')
        s += "]"
        return s


def read_from_dict():
    meet = False
    with open(raw_dict, 'r') as f:
        for line in f.readlines():
            line = line.rstrip()
            if meet:
                try:
                    if len(line) == 0:
                        continue
                    s = line.split('\t')
                    char = s[0]
                    pc = s[1].strip().split(';')
                    py = pc[0].strip()
                    py = convert_zrm_to_py(py)
                    code = pc[1].strip()
                    freq = 1.00
                    if len(s) > 2:
                        freq = float(s[2].strip(' %'))*100

                    if char not in zrm_table.keys():
                        zrm = py_char(char)
                        zrm.push_pinyin(py, freq)
                        zrm.push_code(code)
                        zrm_table[char] = zrm
                    else:
                        zrm = zrm_table[char]
                        zrm.push_pinyin(py, freq)
                        zrm.push_code(code)

                except Exception as e:
                    print(e)
                    print(s)
                    exit(-1)
            else:
                if line == "...":
                    meet = True


read_from_dict()
print(f"Loaded totally {len(zrm_table)} Zrm codes")

chars = {}

with open(char_dict, 'r') as f:
    for line in f.readlines():
        line = line.rstrip()
        s = line.split('\t')
        char = s[0]
        py = s[1]
        freq = int(s[2])
        if char not in chars.keys():
            c = py_char(char)
            c.push_pinyin(py, freq)
            chars[char] = c
        else:
            c = chars[char]
            c.push_pinyin(py, freq)

print(f"Loaded totally {len(chars)} Characters")

uncoded = []
min_freq = 2

for _, char in chars.items():
    has = False
    for py in char.pinyin:
        if py[1] >= min_freq:
            has = True
            break
    if not has:
        continue

    if char.char not in zrm_table.keys():
        uncoded.append(char)
        continue

print(f"There are totally {len(uncoded)} uncoded chars.")
print("Load additional codec for zrm.")
uncoded = []

with open(additional_codec, 'r') as f:
    for line in f.readlines():
        s = line.strip().split(',')
        if s[0] in zrm_table.keys():
            continue
        zrm = py_char(s[0])
        for code in s[1:]:
            zrm.push_code(code)
        zrm_table[s[0]] = zrm

result = []
enable_f1 = False

for _, char in chars.items():
    has = False
    for py in char.pinyin:
        if py[1] >= min_freq:
            has = True
            break
    if not has:
        continue

    if char.char not in zrm_table.keys():
        uncoded.append(char)
        continue
    cc = char.char
    codes = zrm_table[cc].code
    for py in char.pinyin:
        if py[1] < min_freq:
            continue
        for code in codes:
            for p in convert_py_to_zrm(py[0]):
                if not enable_f1:
                    ot = f"{cc}\t{p};{code}\t{py[1]}"
                    result.append(ot)
                else:
                    head = f"{cc}\t{p}"
                    # result.append(head)
                    result.append(head+f"\t{py[1]}")
                    # result.append(head+f";{code[0]}\t{py[1]}")
                    # result.append(head+f";{code}\t{py[1]}")
            if enable_f1:
                break


print(f"There are totally {len(uncoded)} uncoded chars.")
print(f"Converted result: totally {len(result)} codec.")

header = """# Rime dictionary: zrm_pinyin.weight
# encoding: utf-8
---
name: zrm_pinyin.weight
version: "1.0"
sort: by_weight
use_preset_vocabulary: true
columns:
  - text
  - code
  - weight
...
"""

with open(output, 'w') as f:
    f.write(header)
    f.writelines(list(map(lambda x: x+'\n', result)))
