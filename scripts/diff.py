#!/usr/bin/env python

import codecs
import io
import operator
import re
import sys

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

enc_re = re.compile(r"^ENCODING (\d+)")

def die(msg):
    sys.exit(msg)

def parse_glyphs(lines):
    glyphs = {}
    while lines:
        ls = []
        while True:
            l = lines.pop(0)
            ls.append(l)
            if l == "ENDCHAR\n":
                break
        enc = re.search(enc_re, ls[1]).group(1)
        glyphs[int(enc)] = ls
    return glyphs

props = []
glyphs1 = {}
glyphs2 = {}

with io.open(sys.argv[1], encoding="utf-8") as f:
    lines = f.readlines()
i = lines.index("ENDPROPERTIES\n")
props = lines[:i+1]
lines = lines[i+1:]
lines.pop(0) # CHARS ...\n
lines.pop() # ENDCHARS\n
glyphs1.update(parse_glyphs(lines))

with io.open(sys.argv[2], encoding="utf-8") as f:
    lines = f.readlines()
i = lines.index("ENDPROPERTIES\n")
props = lines[:i+1]
lines = lines[i+1:]
lines.pop(0) # CHARS ...\n
lines.pop() # ENDCHARS\n
glyphs2.update(parse_glyphs(lines))

glyphs3 = {}
for k, v in glyphs2.items():
    if not k in glyphs1 or glyphs1.get(k) != v:
        glyphs3[k] = v

for l in props:
    sys.stdout.write(l)

print("CHARS {}".format(len(glyphs3)))

for l in sorted(glyphs3.items(), key=operator.itemgetter(0)):
    for l in l[1]:
        sys.stdout.write(l)

print("ENDCHARS")
