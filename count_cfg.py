import sys, os, types, counts, grammar, parse, time
from collections import Counter

import cky, node
import pickle
import inside_out

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
    g.convertToCNF()
    
    
    print 'Parsing Sentence'
    words = ['He', 'glowered', 'down', 'at', 'her']
    inside_out.insideOutside(words, g)

    #  (TOP (S (NP (PRP He)) (VP (VBD glowered) (ADVP (RP down)) 
    # (PP (IN at) (NP (PRP her))))))
    
    # pickle.dump(g, open('grammar.p', 'wb'))
    # g = pickle.load(open('grammar.p', 'rb'))

#    nodes_back = cky.cky(g, words)
#    print 'Parsed'
    # best_pot = 0
    # best_tree = None
    # for node in nodes_back:
    #     if node.root == 'TOP':
    #         if best_tree == None:
    #             best_tree = node
    #             best_pot = inside_out.potential(node, g)
    #         pot = inside_out.potential(node, g)
    #         print(pot)
    #         print(best_pot)
    #         print(pot > best_pot)
    #         if pot > best_pot:
    #             best_pot = pot
    #             best_tree = node

#    def isTop(node):
#        return node.root == 'TOP'
#
#    print(len(nodes_back))
#    node_back = filter(isTop, nodes_back)
#    print(len(node_back))
#    node_back = [(node, inside_out.potential(node, g)) for node in node_back]
#    node_back.sort(key=lambda node: -1*node[1])
#    print(cky.getParseTree(node_back[1][0], 5))
#    print(cky.getParseTree(node_back[2][0], 5))
#    print(cky.getParseTree(node_back[3][0], 5))

    # print(cky.getParseTree(best_tree, 5))

    
if __name__=='__main__':
    main()
