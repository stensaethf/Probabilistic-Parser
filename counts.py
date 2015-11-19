'''
counts.py
Frederik Roenn Stensaeth, Phineas Callahan
11.19.15
'''

# NOTES TO SELF:
# node
# -> node.children -> list
# first one is left child

# end:
# node.children == []

# node.value

def getCounts(counts_dict, root):
	"""
	getCounts() takes a tree and updates the counts dictionary based on what
	is seen in the given tree.

	@params: counts dictionary and tree (root node).
	@return: updated counts dictionary.
	"""
	# If the root has been seen before we increment the count, if not we
	# set the count to 1.
	if root.value in counts_dict:
		# Root seen before.
		counts_dict[0] += 1
	else:
		# Root not seen before.
		counts_dict[root.value] = {}
		counts_dict[root.value][0] = 1

	# If the root has children we also want to count these.
	if root.children != []:
		# Gets the list of children (their values).
		child_list = []
		for child_node in root.children:
			child_list.append(child_node.value)

		# If the grammar rule has been seen before we increment the count, if
		# not we set the count to 1.
		if child_list in counts_dict[root.value]:
			# Grammar rule seen before.
			counts_dict[root.value][child_list] += 1
		else:
			# Grammar rule not seen before.
			counts_dict[root.value][child_list] = 1

		# Calls getCounts on each child in order to consider the entire tree.
		for child_node in root.children:
			counts_dict = getCounts(counts_dict, child_node)

	return counts_dict







