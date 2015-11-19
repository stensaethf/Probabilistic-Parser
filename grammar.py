'''
grammar.py
Frederik Roenn Stensaeth, Phineas Callahan
'''

# NOTES TO SELF:
# Format:
# LHS , RHS , prob
# Example: S , NP VP , 0.5

def storeGrammar(prob_dict):
	"""
	storeGrammar() takes a probabilities dictionary and stores all the
	grammar rules with their associated probabilities in grammar.txt.

	@params: probabilities dictionary.
	@return: n/a.
	"""
	f = open('grammar.txt', 'w')

	for lhs in prob_dict:
		for rhs in prob_dict[lhs]:
			rule = lhs + ' , ' + rhs + ' , ' + str(prob_dict[lhs][rhs])
			f.write(rule + '\n')

	f.close()

# # TEST
# def main():
# 	d = {}
# 	d['a'] = {}
# 	d['b'] = {}
# 	d['a']['aa aa'] = 0.5
# 	d['a']['bb'] = 0.9

# 	storeGrammar(d)

# if __name__ == '__main__':
# 	main()