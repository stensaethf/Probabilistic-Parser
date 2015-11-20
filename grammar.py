'''
grammar.py
Frederik Roenn Stensaeth, Phineas Callahan
'''

# NOTES TO SELF:
# Format:
# LHS , RHS , prob
# Example: S , NP VP , 0.5

import re

def storeGrammar(prob_dict):
	"""
	storeGrammar() takes a probabilities dictionary and stores all the
	grammar rules with their associated probabilities in grammar.txt.

	@params: probabilities dictionary.
	@return: n/a.
	"""
	f = open('cfg.txt', 'w')

	for lhs in prob_dict:
		for rhs in prob_dict[lhs]:
			rule = lhs + ' , ' + rhs + ' , ' + str(prob_dict[lhs][rhs])
			f.write(rule + '\n')

	f.close()

def convertToCNF(filename):
	"""
	convertToCNF() takes a filename and converts the grammar to CNF.
	Result is stored in cnf.txt.

	@params: grammar file.
	@return: n/a.
	"""
	f = open('cnf.txt', 'w')

	cfg = open(filename, 'r')
	count = 1
	for line in cfg:
		# LHS , RHS , PROB\n
		info = re.sub('\n' , '', line)
		# LHS , RHS , PROB
		info = info.split(' , ')

		lhs = info[0]
		rhs = info[1]
		prob = info[2]

		rhs_split = rhs.split(' ')

		if len(rhs_split) > 2:
			rhs_temp = rhs_split
			lhs_temp = lhs

			while len(rhs_temp) > 1:
				new_rhs = rhs_temp[0] + ' x' + str(count)

				# Only the initial rule should have the 
				if lhs_temp == lhs:
					rule = lhs_temp + ' , ' + new_rhs + ' , ' + str(prob)
				elif len(rhs_temp) == 2:
					new_rhs = ' '.join(rhs_temp)
					rule = lhs_temp + ' , ' + new_rhs + ' , ' + str(1)
				else:
					rule = lhs_temp + ' , ' + new_rhs + ' , ' + str(1)

				f.write(rule + '\n')

				rhs_temp = rhs_temp[1:]
				lhs_temp = 'x' + str(count)
				count += 1
		else:
			rule = lhs + ' , ' + rhs + ' , ' + str(prob)
			f.write(rule + '\n')

	cfg.close()
	f.close()

# TEST
def main():
	d = {}
	d['a'] = {}
	d['b'] = {}
	d['a']['aa aa aa bb'] = 0.5
	d['a']['bb bb bb'] = 0.9

	storeGrammar(d)
	convertToCNF('cfg.txt')

if __name__ == '__main__':
	main()