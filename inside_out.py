'''
inside_out.py
Frederik Roenn Stensaeth, Phineas Callahan
11.20.15
'''

# Grammar.rules -> dict
# dict[lhs][rhs] -> prob (float form)

from math import log
import parse

def potential(root, grammar):
	"""
	potential() xx

	@params: xx
	@return: xx
	"""
	potential = 0

	if root.children == []
		return potential
	else:
		child_list = []
		for child in root.children:
			child_list.append(child.value)
			potential += potential(child, grammar)

		prob = grammar.rules[root.value][' '.join(child_list)]

		potential += log(prob)

	return potential

def alpha(sentence, grammar, trees):
	"""
	calculateInsideProbabilities() xx

	@params: xx
	@return: xx
	"""
    n = len(sentence)
    
    alpha = {lhs: [[0]*n]*n for lhs in g.non_terminals}
    
    #BASE CASE
    for lhs in grammar.non_terminals:
        for i in range(n):
            word = sentence[i]
            if word in grammar.TR and lhs in grammar.TR[word]:
                alpha[lhs][i][i] = grammar.TR[word][lhs].prob
            else:
                alpha[lhs][i][i] = 0
    
    for lhs in grammar.non_terminals:
		for rule in rules[lhs].values():
			for i in range(n - 1):
				for j in range(1, n):
					for k in range(i+1, j):
						prod = 1
                        prod *= rule.prob
                        prod *= alpha[rule.rhs[0]][i][k]
                        prod *= alpha[rule.rhs[1]][k+1][j]
                        alpha[lhs][i][j] += prod

	return alpha

def beta(sentence, grammar, trees):
    
    beta = {lhs: [[0]*n]*n for lhs in g.non_terminals}
    n = len(sentence)
    
    beta[grammar.start_symbol][0][n-1]
    
    for lhs in grammar.non_terminals:
        for rule in rules[lhs].values():
            rrhs = '|'.join(rule.rhs[::-1])
            if rrhs not in rules[lhs]:
                continue
            
            r_rule = rules[lhs][rrhs]
            
            for i in range(n-1):
                for j in range(1, n):
                    if i==0 and j==n-1:
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
                        prod *= alpha[r.rhs[0][i][k]]
                        prod *= beta[lhs][i][k]
                        beta[rule.rhs[1]][i][j] += prod
                        
    return beta
                        
def insideOutside(xx):
	"""
	insideOutside() xx

	@params: xx
	@return: xx
	"""
	inside = calculateInsideProbabilities(sentence_list, grammar)
	outside = getOutsideProbabilties(x)

	return None