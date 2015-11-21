import sys, os, types, counts, grammar, parse

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
        
    
    return node
        
def main():
    trees = []
    for path in os.listdir(sys.argv[1]):
        if path.split('.')[1] != 'prd':
            continue
            
        file_path = sys.argv[1]+'/'+path
        f = open(file_path, 'rb')
        trees.extend(read_trees(f))
    
    g = grammar.Grammar(trees)
    g = g.convertToCNF()
    
    print len(g.terminals)
    words = ['The', 'dog', 'jumps']
    parsed_trees = parse.parse(g, words)
    for tree in parsed_trees:
        print tree
    
if __name__=='__main__':
    main()
