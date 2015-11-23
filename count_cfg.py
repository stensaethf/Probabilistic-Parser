import sys, os, types, counts, grammar, parse, time
from collections import Counter

def read_trees(f):
    tokens = []
    for line in f:
        line = line.replace('(', ' ( ')
        line = line.replace(')', ' ) ')
        tokens.extend(line.split())

    if tokens[0] == '(':
        tokens.insert(0, 'BETA')
    return recursiveParse(tokens).children
    
def recursiveParse(tokens):
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
        # print node.children
        if node.value == node.children[0].value:
            # node.children = list()
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
    
    
    start = time.time()
    print 'Parsing Sentence'
    words = ['He', 'glowered', 'down', 'at', 'her']
#      (TOP (S (NP (PRP He)) (VP (VBD glowered) (ADVP (RP down)) 
#     (PP (IN at) (NP (PRP her))))))
    parsed_trees = parse.parse(g, words)
    end = time.time()
    print end-start
    
    for tree in parsed_trees:
        print tree
#    
#    
if __name__=='__main__':
    main()
