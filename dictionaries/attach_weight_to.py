#! /usr/bin/env python3
weight_map = {}

weight = "thuocl_it.txt"
to = "jsj.txt"

with open(weight, "r") as f:
    for l in f.readlines():
        s = l.strip().split('\t')
        weight_map[s[0]] = int(s[1])

with open(to, "r") as f:
    for l in f.readlines():
        s = l.strip()
        if s in weight_map.keys():
            print("%s\t%d" % (s, weight_map[s]))
        else:
            print("%s" % (s))
