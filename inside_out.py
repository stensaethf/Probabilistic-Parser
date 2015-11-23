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
    for lhs in rules:
        for i in range(n):
            word = sentence[i]
            if word in grammar.TR and lhs in grammar.TR[word]:
                alpha[lhs][i][i] = grammar.TR[word][lhs].prob
            else:
                alpha[lhs][i][i] = 0
    
    for lhs in rules:
		total = 0
		for rule in rules[lhs].values():
			for i in range(n - 1):
				for j in range(1, n):
					for k in range(i+1, j):
						prod = 1
                        prod *= rule.prob
                        prod *= alpha[rule.rhs[0]][i][k]
                        prod *= alpha[rule.rhs[1]][k+1][j]

	return alpha

def beta(sentence, grammar, trees):
    
    beta = {lhs: [[0]*n]*n for lhs in g.non_terminals}
    
    

def insideOutside(xx):
	"""
	insideOutside() xx

	@params: xx
	@return: xx
	"""
	inside = calculateInsideProbabilities(sentence_list, grammar)
	outside = getOutsideProbabilties(x)

	return None