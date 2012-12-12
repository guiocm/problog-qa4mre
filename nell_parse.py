#!/usr/bin/env python

import sys


class Parser:
    def __init__(self, input, output):
        self.input = open(input, "r")
        self.output = open(output, "w")
        self.concepts = set()
        self.relations = set()

    def close(self):
        self.input.close()
        self.output.close()

    def add_concept(self, parent, concept):
        if concept not in self.concepts:
            self.concepts.add(concept)
            self.output.write("isA(" + parent + ", " + concept + ").\n")

    def add_relation(self, relation):
        if relation not in self.relations:
            self.relations.add(relation)
            self.output.write("isA(relation, " + relation + ").\n")

    def parse(self):
        self.output.write(":- use_module(library(problog)).\n")
        for line in self.input.readlines():
            sp = line.split("\t")
            entity = sp[0]
            relation = sp[1]
            value = sp[2]
            prob = sp[4]
            
            entity = self.parse_concept(entity)
            relation = self.parse_concept(relation)
            value = self.parse_concept(value)

            self.parse_relation(entity, relation, value, prob)

    def parse_concept(self, concept):
        if concept.find("concept") == 0:
            parts = concept.split(":")
            for i in range(len(parts)-1):
                self.add_concept(parts[i], parts[i+1])
            return parts[-1]
        else:
            return "'" + concept.replace("'", "\'") + "'"

    def parse_relation(self, entity, relation, value, prob):
        self.add_relation(relation)
        self.output.write(str(prob) + " :: " + relation + "(" + entity + ", " + value + ").\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: " + sys.argv[0] + " <source>.csv <dest>.pl"
        exit(1)

    Parser(sys.argv[1], sys.argv[2]).parse()


