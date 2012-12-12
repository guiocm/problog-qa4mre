#!/usr/bin/env python
import sys, re
from nltk import stem

def string_to_tree(s):
    s = s.replace("(", "( ")
    s = s.replace(")", " )")
    s = s.split()
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


'''
    01-12-2012
        My first idea is to process the syntax tree produced by the
        Stanford Parser, extracting relations from the main verb
        phrases of the sentences, and grouping the nested noun 
        phrases and prepositional phrases in word sets, so that
        their similarity with the hypothesis can be analyzed.

        Another possibility would be to use the generated dependencies
        to find the main verb (it'll be associated with the root of 
        the sentence), and just proceed processing the dependencies to
        generate the word sets.
'''

dep_re = re.compile(r'(\w+).(\w+).(\d+)..(\w+).(\d+)')
ignore_deps = ["aux", "auxpass", "attr", "det"]

def parse_dependencies(deps):
    words = {}
    rels = {}

    for d in deps:
        s = dep_re.search(d)
        if s:
            rel, gov, gov_idx, dep, dep_idx = s.groups()
            gov_idx = int(gov_idx)
            dep_idx = int(dep_idx)
            
            words[gov_idx] = gov
            words[dep_idx] = dep

            if gov_idx not in rels:
                rels[gov_idx] = []

            rels[gov_idx].append((rel, dep_idx))

    return words, rels

def get_subtree(rels, dependant):
    elems = set([dependant])
    try:
        for dep_class, dep in rels[dependant]:
            if dep_class not in ignore_deps:
                elems.update(get_subtree(rels, dep))
    except:
        pass
    return elems

stemmer = stem.LancasterStemmer()
    
def get_words(wds, words):
    return map(lambda x: stemmer.stem(words[x]), wds)

def extract_relation(deps):
    words, rels = parse_dependencies(deps)

    main = rels[0][0][1]
    groups = []

    for dep_class, dependant in rels[main]:
        if dep_class in ignore_deps:
            continue

        wds = get_subtree(rels, dependant)
        group = get_words(wds, words)

        groups.append((dep_class, group))

    return words[main], groups

'''
    02-12-2012
        This works, and produces a tuple with the main verb, and a 
        list of the structures associated to it. These list is
        composed of tuples with the dependency between the structure
        and the verb, and a list of the relevant words within the
        structure.

        This sort of processing could be enhanced to calculate the
        tf-idf of the words, if that proves useful.

        It could also associate the POS tags with the words, so that
        further semantic analysis could be done using that information.

        Another idea would be to utilize a stemming algorithm in the
        extracted words. 
'''

'''
    10-12-2012
        Start to process whole files, split groups of relations about
        the same sentence, and work on each group.
'''




test = \
''' attr(is-2, What-1)
    root(ROOT-0, is-2)
    det(objective-4, the-3)
    nsubj(is-2, objective-4)
    det(Program-10, the-6)
    amod(Program-10, Brazilian-7)
    nn(Program-10, National-8)
    nn(Program-10, Biodiesel-9)
    prep_of(objective-4, Program-10)
'''

another_test = \
''' nsubj(plays-2, Brazil-1)
    root(ROOT-0, plays-2)
    det(role-7, an-3)
    amod(role-7, important-4)
    conj_and(important-4, unique-6)
    amod(role-7, unique-6)
    dobj(plays-2, role-7)
    nn(change-10, climate-9)
    prep_in(role-7, change-10)
'''


if __name__ == "__main__":
    with open(sys.argv[1], "r") as infile:
        lines = [l.rstrip("\n") for l in infile.readlines()]

    sentences = []
    while "" in lines:
        sentences.append(lines[:lines.index("")])
        lines = lines[lines.index("")+1:]

    relations = []
    for s in sentences:
        print s
        relations.append(extract_relation(s))
    
    print relations
    for r in relations:
        print len(r[1]), r
    # print extract_relation(test.splitlines())
    # print extract_relation(another_test.splitlines())
    # print parse_dependencies(test.splitlines())
    # print dep_re.search(test).groups()
    # print string_to_tree(open(sys.argv[1], "r").read())


