'''
counts.py
Frederik Roenn Stensaeth, Phineas Callahan
11.19.15
'''

def getCounts(counts_dict, root):
	"""
	getCounts() takes a tree and updates the counts dictionary based on what
	is seen in the given tree.

	@params: counts dictionary and tree (root node).
	@return: updated counts dictionary.
	"""
	# If the root is a terminal value we do not do anything.
	if root.children != []:
		# If the root has been seen before we increment the count, if not we
		# set the count to 1.
		if root.value in counts_dict:
			# Root seen before.
			counts_dict[root.value][0] += 1
		else:
			# Root not seen before.
			counts_dict[root.value] = {}
			counts_dict[root.value][0] = 1

		# # If the root has children we also want to count these.
		# if root.children != []:
		# Gets the list of children (their values).
		child_list = []
		for child_node in root.children:
			child_list.append(child_node.value)
		child_str = ' '.join(child_list)

		# If the grammar rule has been seen before we increment the count, if
		# not we set the count to 1.
		if child_str in counts_dict[root.value]:
			# Grammar rule seen before.
			counts_dict[root.value][child_str] += 1
		else:
			# Grammar rule not seen before.
			counts_dict[root.value][child_str] = 1

		# Calls getCounts on each child in order to consider the entire tree.
		for child_node in root.children:
			counts_dict = getCounts(counts_dict, child_node)

	return counts_dict

def getProbabilities(counts_dict):
	"""
	getProbabilities() takes a counts_dict and converts the counts to 
	probabilities. A new dictionary containing the probabilities is returned.

	@params: counts dictionary.
	@return: probabilities dictionary.
	"""
	prob_dict = {}

	# Loops over every entry in the counts dictionary and converts to
	# probability.
	for lhs in counts_dict:
		prob_dict[lhs] = {}

		for rhs in counts_dict[lhs]:
			if rhs != 0:
				# Calculates the probability of the given grammar rule by
				# dividing the counts of left hand side by the count of
				# the grammar rule.
				prob = counts_dict[lhs][rhs] / counts_dict[lhs][0]
				prob_dict[lhs][rhs] = prob

		if prob_dict[lhs] == {}:
			del prob_dict[lhs]

	return prob_dict

# # TEST
# def main():
# 	d = {}
# 	d['a'] = {}
# 	d['b'] = {}
# 	d['a'][0] = 10
# 	d['a']['aa aa'] = 5
# 	d['a']['bb'] = 6
# 	d['d'] = {}

# 	prob = getProbabilities(d)

# 	print(prob)

# if __name__ == '__main__':
# 	main()







