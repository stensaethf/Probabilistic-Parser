import sys, os, types, counts, grammar, parse
from collections import Counter

def read_trees(f):
    tokens = []
    for line in f:
        line = line.replace('(', ' ( ')
        line = line.replace(')', ' ) ')
        tokens.extend(line.split())
    
    return recursiveParse(tokens).children
    
def recursiveParse(tokens):
    nodeValue = tokens.pop(0)
    if nodeValue == '(':
        nodeValue = 'TOP'
        tokens.insert(0, '(')
    
    node = parse.ParseNode(nodeValue)
    while len(tokens):
        token = tokens.pop(0)
        if token == ')':
            return node
        elif token == '(':
            node.append(recursiveParse(tokens))
        else:
            node.append(parse.ParseNode(token))
        
    if len(node.children)==1 and node.children[0].isLeaf():
        print node
        if node.value == node.children[0].value:
            node.children = list()
    
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
    
#    for tree in trees:
#        if '``' in tree:
#            print tree
        
#    print 'Converting trees to grammar'
#    g = grammar.Grammar(nodes = trees)
#    g.write(open('cfg.txt', 'wb'))
#    print 'Converting grammar to CNF'
#    g.convertToCNF()
##    for rule in g.NR['NAC'].values():
##        print rule
#    g.write(open('cnf.txt', 'wb'))
    
#    print 'Parsing Sentence'
#    words = ['the', 'dog', 'showed']
#    parsed_trees = parse.parse(g, words)
#    print len(parsed_trees)
#    for tree in parsed_trees:
#        l=tree.__str__()
#        print
#    
if __name__=='__main__':
    main()
