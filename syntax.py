#!/usr/bin/env python
import sys

def string_to_tree(s):
    print s
    s = s.replace("(", "( ")
    print s
    s = s.replace(")", " )")
    print s
    s = s.split()
    print s
    return rec_parse(s)

def rec_parse(syntax):
    elem = []
    syntax.pop(0)

    while syntax[0] != ")":
        if syntax[0] == "(":
            elem.append(rec_parse(syntax))
        else:
            elem.append(syntax.pop(0))

    syntax.pop(0)
    return elem

if __name__ == "__main__":
    print string_to_tree(open(sys.argv[1], "r").read())
