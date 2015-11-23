import sys, os, types, counts, grammar, parse, time
from collections import Counter

import cky, node
import pickle
import inside_out

def read_trees(f):
    """
    read_trees() takes the contents of a file (trees in string form) and
    recursively parses them based on where open and close parenthesis are
    located in the file.

    @params: contents of a file (trees in string form).
    @return: parsed trees (list).
    """
    tokens = []
    for line in f:
        line = line.replace('(', ' ( ')
        line = line.replace(')', ' ) ')
        tokens.extend(line.split())

    if tokens[0] == '(':
        tokens.insert(0, 'BETA')

    return recursiveParse(tokens).children
    
def recursiveParse(tokens):
    """
    recursiveParse() takes a list of tokens and recursively parses them based
    on where open and close parenthesis are located in the list of tokens.

    @params: list of tokens.
    @return: node.
    """
    nodeValue = tokens.pop(0)

    if nodeValue == '(':
        nodeValue = tokens.pop(0)
        tokens.pop()

    node = parse.ParseNode(nodeValue)
    while len(tokens):
        token = tokens.pop(0)
        if token == ')':
            return node
        elif token == '(':
            node.append(recursiveParse(tokens))
        else:
            node.append(parse.ParseNode(token))

    if len(node.children)==1: #and node.children[0].isLeaf():
        if node.value == node.children[0].value:
            node.children = node.children[0].children
    
    return node
        
def main():
    trees = []
    print 'Parsing trees'
    for path in os.listdir(sys.argv[1]):
        if path.split('.')[1] != 'prd':
            continue
            
        file_path = sys.argv[1]+'/'+path
        f = open(file_path, 'rb')
        trees.extend(read_trees(f))

    print 'Converting trees to grammar'
    g = grammar.Grammar(nodes = trees)
    
    g.write(open('cfg', 'wb'))
    g.convertToCNF()
    
    
    print 'Parsing Sentence'
    words = ['He', 'glowered', 'down', 'at', 'her']
    inside_out.insideOutside(words, g)


    
if __name__=='__main__':
    main()
