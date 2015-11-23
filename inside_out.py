'''
inside_out.py
Frederik Roenn Stensaeth, Phineas Callahan
11.20.15
'''

# Grammar.rules -> dict
# dict[lhs][rhs] -> prob (float form)
import count_cfg
from math import log
import parse, cky, grammar, os, sys
import os.path
import pickle

def potential(tree, grammar):
    """
    potential() takes a tree and a grammar and returns the potential of that
    tree (log form). The potential of a tree is the probability of the rules
    in the tree multiplied with each other.

    @params: tree and grammar.
    @return: potential of the tree (log form).
    """
    pot = 0

    if tree.status:
        # Potential of a leaf is 0 (log scale).
        return pot
    else:
        left = tree.left
        right = tree.right

        pot += potential(left, grammar)
        pot += potential(right, grammar)

        prob = 1

        for rule in grammar.NR[tree.root].values():
            derivation = rule.rhs
            if len(derivation) == 2:
                B = derivation[0]
                C = derivation[1]
                if B == left.root and C == right.root:
                    prob = rule.prob

        if prob == 0:
            pot += -20000
        else:
            pot += log(prob)

    return pot

def getAlpha(sentence, grammar, trees):
    """
    getAlpha() finds the inside probabilities for all the non-terminals in our
    grammar, given a sentence and possible trees.

    @params: sentence (list of strings), grammar and list of trees.
    @return: inside matrix.
    """
    n = len(sentence)
    
    alpha = {lhs: [[0]*n]*n for lhs in grammar.non_terminals}
    
    #BASE CASE
    for lhs in grammar.non_terminals:
        for i in range(n):
            word = sentence[i]
            if word in grammar.TR and lhs in grammar.TR[word]:
                alpha[lhs][i][i] = grammar.TR[word][lhs].prob
            else:
                alpha[lhs][i][i] = 0
    
    for lhs in grammar.NR:
        for rule in grammar.NR[lhs].values():
            for i in range(n - 1):
                for j in range(i, n):
                    for k in range(i, j):
                        prod = 1
                        prod *= rule.prob
                        prod *= alpha[rule.rhs[0]][i][k]
                        prod *= alpha[rule.rhs[1]][k+1][j]
                        alpha[lhs][i][j] += prod

    return alpha

def getBeta(sentence, grammar, trees, alpha):
    """
    getBeta() finds the outside probabilities for all the non-terminals in our
    grammar, given a sentence and possible trees.

    @params: sentence (list of strings), grammar and list of trees.
    @return: outside matrix.
    """
    n = len(sentence)
    beta = {lhs: [[0]*n]*n for lhs in grammar.non_terminals}
    
    beta[grammar.start_symbol][0][n-1] = 1
    
    for lhs in grammar.NR:
        for rule in grammar.NR[lhs].values():
            rrhs = '|'.join(rule.rhs[::-1])
            if rrhs not in grammar.NR[lhs]:
                continue
            
            r_rule = grammar.NR[lhs][rrhs]
            
            for i in range(n-1):
                for j in range(1, n):
                    if i==0 and j==(n-1):
                        continue
                        
                    for k in range(i):
                        prod = 1
                        prod *= rule.prob
                        prod *= alpha[rule.rhs[0]][k][i-1]
                        prod *= beta[lhs][k][j]
                        beta[rule.rhs[1]][i][j] += prod
                        
                    for k in range(j+1, n):
                        prod = 1
                        prod *= r_rule.prob
                        prod *= alpha[rule.rhs[0]][i][k]
                        prod *= beta[lhs][i][k]
                        beta[rule.rhs[1]][i][j] += prod
                        
    return beta
    
def insideOutside(sentence, grammar, count):
    """
    insideOutside() finds the expected number of counts for rules in our
    grammar, given a sentence.

    @params: sentence (list of strings), grammar and count dictionary.
    @return: n/a (updates count dictionary).
    """
    n = len(sentence)
    
    trees = cky.cky(grammar, sentence)
    trees_top = []
    for tree in trees:
        if tree.root == 'TOP':
            trees_top.append(tree)

    # cky.printParseTrees(trees_top)
    inside = getAlpha(sentence, grammar, trees_top)
    # print(inside)
    outside = getBeta(sentence, grammar, trees_top, inside)
    
    Z = inside[grammar.start_symbol][0][n-1]
    mu = {lhs:[[0]*n]*n for lhs in inside}
    
    for lhs in mu:
        for i in range(n):
            for j in range(n):
                mu[lhs][i][j] = inside[lhs][i][j]*outside[lhs][i][j]
    
    gamma = {}
    for lhs in grammar.NR:
        for rule in grammar.NR[lhs].values():
            gamma[rule] = [[[0]*n]*n]*n
            for i in range(n-1):
                for j in range(i+1, n):
                    for k in range(i,j):
                        gamma[rule][i][k][j] = outside[rule.lhs][i][j]*rule.prob*inside[rule.rhs[0]][i][k]*inside[rule.rhs[1]][k+1][j]
    
    for lhs in grammar.NR:
        if lhs not in count:
            count[lhs] = {}
        for rule in grammar.NR[lhs].values():
            if tuple(rule.rhs) not in count[lhs]:
                count[lhs][tuple(rule.rhs)] = 0
            for i in range(n-1):
                for j in range(i+1, n):
                    for k in range(i, j):
                        count[lhs][tuple(rule.rhs)] += gamma[rule][i][k][j]/Z
    
    for term in grammar.TR:
        for lhs in grammar.TR[term]:
            if lhs not in count:
                count[lhs] = {}
              
    for i in range(n):
        for lhs in grammar.TR[sentence[i]]:
            if tuple([sentence[i]]) in count[lhs]:
                count[lhs][tuple([sentence[i]])] += mu[lhs][i][i]/Z
            else:
                count[lhs][tuple([sentence[i]])] = mu[lhs][i][i]/Z
    
def main():
    if len(sys.argv) == 3:
        sentences = sys.argv[2].split(' ')

        # Get the grammar.
        file_path = sys.argv[1]

        trees = []
        print 'Parsing trees in file...'
        f = open(file_path, 'rb')
        trees.extend(count_cfg.read_trees(f))

        print 'Converting trees to grammar...'
        g = grammar.Grammar(nodes = trees)

        print 'Converting to CNF...'
        g.convertToCNF()

        # Parse and get nodes back.
        print 'Running CKY...'
        nodes_back = cky.cky(g, sentences)

        # Only get the nodes back that have a TOP.
        nodes_back_top = []
        for tree in nodes_back:
            if tree.root == 'TOP':
                nodes_back_top.append(tree)

        print 'Getting best and worst tree...'
        if nodes_back_top == []:
            print('No tree could be constructed for the sentence.')
            sys.exit()
        elif len(nodes_back_top) == 1:
            print('Only one valid tree found for the sentence.')
            print(cky.getParseTree(nodes_back_top[0], 5))

        max_pot = float('-inf')
        min_pot = float('inf')
        max_tree = nodes_back_top[0]
        min_tree = nodes_back_top[0]

        for tree in nodes_back_top:
            pot_tree = potential(tree, g)
            if pot_tree > max_pot:
                max_pot = pot_tree
                max_tree = tree
            elif pot_tree < min_pot:
                min_pot = pot_tree
                min_tree = tree

        print('Max tree:')
        print(cky.getParseTree(max_tree, 5))

        print('Min tree:')
        print(cky.getParseTree(min_tree, 5))
    else:
        if os.path.isfile('grammar.p'):
            g = pickle.load(open('grammar.p', 'rb'))
        else:
            trees = []
            print 'Parsing trees'
            for path in os.listdir(sys.argv[1]):
                if path.split('.')[1] != 'prd':
                    continue
                    
                file_path = sys.argv[1]+'/'+path
                f = open(file_path, 'rb')
                trees.extend(count_cfg.read_trees(f))

            print 'Converting trees to grammar'
            g = grammar.Grammar(nodes = trees)

            print 'Converting to CNF'
            g.convertToCNF()

            pickle.dump(g, open('grammar.p', 'wb'))
        

        print 'Parsing Sentence'

        sentences = [['His', 'tall', 'frame'], 
                     ['the', 'dog', 'saved'], 
                     ['discover', 'the', 'first', 'snail'],
                     ['it', 'is', 'juxtaposed', 'well'],
                     ['Her', 'handling', 'of', 'paint'],
                     ['He', 'glowered', 'down', 'at', 'her']]

        for t in range(5):
            num_t = [len(g.TR[lhs]) for lhs in g.TR]
            num_n = [len(g.NR[lhs]) for lhs in g.NR]

            print sum(num_t), sum(num_n)
            to_del = []
            count = {}
            for sent in sentences:
                insideOutside(sent, g, count)      
            
            for lhs in count:
                lhs_sum = sum(count[lhs].values())
                if lhs_sum == 0:
                    to_del.append(lhs)
                else:
                    for key,val in count[lhs].items():
                        count[lhs][key] = val/lhs_sum

            for lhs in to_del:
                del count[lhs]
            
            for lhs in count:
                for key,val in count[lhs].items():
                    rule_dat = [lhs,]
                    rule_dat.extend(list(key))
                    rule_dat.append(val)
                    g.add_rule(grammar.Rule(vals = rule_dat))

        def isTop(node):
           return node.root == 'TOP'

        for s in sentences:
            nodes_back = cky.cky(g, s)
            node_back = filter(isTop, nodes_back)
            node_back = [(node, potential(node, g)) for node in node_back]
            node_back.sort(key=lambda node: -1*node[1])
            cky.printParseTrees([node_back[0][0]])




if __name__=='__main__':
    main()