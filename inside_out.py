'''
inside_out.py
Frederik Roenn Stensaeth, Phineas Callahan
11.20.15
'''

# Grammar.rules -> dict
# dict[lhs][rhs] -> prob (float form)

from math import log
import parse, cky

def potential(tree, grammar):
	"""
	potential() xx

	@params: xx
	@return: xx
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
		# Probability of root going to its children.

		# check = False
		for rule in grammar.NR[tree.root].values():
			derivation = rule.rhs
			if len(derivation) == 2:
				B = derivation[0]
				C = derivation[1]
				if B == left.root and C == right.root:
					prob = rule.prob
					# check = True
		# child_list = []
		# for child in root.children:
		#   child_list.append(child.value)
		#   potential += potential(child, grammar)

		# prob = grammar.rules[root.value][' '.join(child_list)]
		# print(check)
		pot += log(prob)

	return pot

def getAlpha(sentence, grammar, trees):
	"""
	calculateInsideProbabilities() xx

	@params: xx
	@return: xx
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
	n = len(sentence)
	beta = {lhs: [[0]*n]*n for lhs in grammar.non_terminals}
	
	# print(grammar.start_symbol)

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
	
def insideOutside(sentence, grammar):
	"""
	insideOutside() xx

	@params: xx
	@return: xx
	"""
	n = len(sentence)
	
	print 'Parsing'
	trees = cky.cky(grammar, sentence)
	print 'Inside'
	inside = getAlpha(sentence, grammar, trees)
	# print(inside)
	print 'Outside'
	outside = getBeta(sentence, grammar, trees, inside)
	
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
			for i in range(n):
				for j in range(i+1, n):
					for k in range(i,j):
						gamma[rule][i][k][j] = outside[rule.lhs][i][j]*rule.prob*inside[rule.rhs[0]][i][k]*inside[rule.rhs[1]][k+1][j]
					
	print gamma
	
def main():
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
    
    g.write(open('cfg', 'wb'))
    g.convertToCNF()
    
    
    print 'Parsing Sentence'
    words = ['He', 'glowered', 'down', 'at', 'her']
    inside_out.insideOutside(words, g)
    

if __name__=='__main__':
	main()