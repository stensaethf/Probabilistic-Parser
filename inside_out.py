'''
inside_out.py
Frederik Roenn Stensaeth, Phineas Callahan
11.20.15
'''

# Grammar.rules -> dict
# dict[lhs][rhs] -> prob (float form)

from math import log
import parse

def potential(tree, grammar):
	"""
	potential() xx

	@params: xx
	@return: xx
	"""
	potential = 0

	if tree.status:
		# Potential of a leaf is 0 (log scale).
		return potential
	else:
		left = tree.left
		right = tree.right

		potential += potential(left, grammar)
		potential += potential(right, grammar)

		prob = 1
		# Probability of root going to its children.
		for rule in grammar.NR[tree.root].values():
			derivation = rule.rhs
			if len(derivation) == 2:
				B = derivation[0]
				C = derivation[1]
				if B == left.root and C == right.root:
					prob = log(rule.prob)
		# child_list = []
		# for child in root.children:
		# 	child_list.append(child.value)
		# 	potential += potential(child, grammar)

		# prob = grammar.rules[root.value][' '.join(child_list)]

		potential += log(prob)

	return potential

def calculateInsideProbabilities(sentence_list, grammar):
	"""
	calculateInsideProbabilities() xx

	@params: xx
	@return: xx
	"""
	alpha = {}
	rules = gramamr.rules
	j = xx 

	for lhs in rules:
		total = 0
		for rhs in rules[lhs]:
			for i in range(1, n - 1):
				for j in range(1, n):
					for k in range(i, j - 1):
						parse.parse(grammar, words)
						pot = potential(xx)

	return None

def insideOutside(xx):
	"""
	insideOutside() xx

	@params: xx
	@return: xx
	"""
	inside = calculateInsideProbabilities(sentence_list, grammar)
	outside = getOutsideProbabilties(x)

	return None