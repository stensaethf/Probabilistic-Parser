import sys, os, types

class ParseNode:
    def __init__(self, val):
        self.children = list()
        self.value = val

    def append(self, node):
        self.children.append(node)
        
    def __str__(self):
        return self.recursive_print(0)
    
    def recursive_print(self, indent):
        if len(self.children):
            all_terminal = True
            for child in self.children:
                if len(child.children):
                    all_terminal = False
            
            s = '('+self.value+' '
            indent = indent+len(s)
            for child in self.children[:-1]:
                s += child.recursive_print(indent)
                if all_terminal:
                    s+= ' '
                else:
                    s += '\n'+' '*indent
        
            s += self.children[-1].recursive_print(indent)+')'
        else:
            s = self.value
        
        return s
            
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
    
    node = ParseNode(nodeValue)
    while len(tokens):
        token = tokens.pop(0)
        if token == ')':
            return node
        elif token == '(':
            node.append(recursiveParse(tokens))
        else:
            node.append(ParseNode(token))
        
    
    return node
        
def main():
    trees = []
    for path in os.listdir(sys.argv[1]):
        if path.split('.')[1] != 'prd':
            continue
            
        file_path = sys.argv[1]+'/'+path
        f = open(file_path, 'rb')
        trees.extend(read_trees(f))
    
    print len(trees)
    
if __name__=='__main__':
    main()