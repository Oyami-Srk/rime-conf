#! /usr/bin/env python3
weight_map = {}

with open("base_singal_char_weight.txt", "r") as f:
    for l in f.readlines():
        s = l.strip().split('\t')
        weight_map[s[0]] = int(s[1])

with open("zrm_pinyin.dict.yaml", "r") as f:
    for l in f.readlines():
        s = l.strip().split('\t')
        if s[0] in weight_map.keys():
            print("%s\t%s\t%d"%(s[0],s[1],weight_map[s[0]]))
        else:
            print("%s\t%s"%(s[0], s[1]))
