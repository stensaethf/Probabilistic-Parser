'''
grammar.py
Frederik Roenn Stensaeth, Phineas Callahan
11.19.15
'''

# NOTES TO SELF:
# Format:
# LHS , RHS , prob
# Example: S , NP VP , 0.5

import re, string

class Grammar:
    
    def __init__(self, E, N, R, S = 'TOP'):
        self.rules = R
        self.non_terminals = N
        self.terminals = E
        self.start_symbol = S
        
def read_grammar(input_file):
    rules = {}
    non_terminals = set()
    terminals = set()
    
    for line in input_file:
        rule = map(string.strip, line.split('|'))
        
        entry = {}
        if rule[0] in rules:
            entry = rules[rule[0]]
        else:
            rules[rule[0]] = entry
        
        entry[rule[1]] = rule[-1]
        
        non_terminals.add(rule[0])
        if rule[1] == rule[1].upper():
            non_terminals.update(rule[1].split())
        else:
            terminals.add(rule[1])
        
    return Grammar(terminals, non_terminals, rules)

def storeGrammar(prob_dict):
    """
    storeGrammar() takes a probabilities dictionary and stores all the
    grammar rules with their associated probabilities in grammar.txt.
    
    @params: probabilities dictionary.
    @return: n/a.
    """
    with open('cfg.txt', 'w') as f:
        for lhs in prob_dict:
            for rhs in prob_dict[lhs]:
                rule = lhs + ' | ' + rhs + ' | ' + str(prob_dict[lhs][rhs])
                f.write(rule + '\n')

def convertToCNF(filename):
    """
	convertToCNF() takes a filename and converts the grammar to CNF.
	Result is stored in cnf.txt.

	@params: grammar file.
	@return: n/a.
	"""
    with open('cnf.txt', 'w') as f:
        with open(filename, 'r') as cfg:
            count = 1
            rule_dict = {}
            # count_unit = 1
            for line in cfg:
                # LHS , RHS , PROB\n
                info = line.strip()
                # LHS , RHS , PROB
                info = info.split(' | ')

                lhs = info[0]
                rhs = info[1]
                prob = info[2]

                rhs_split = rhs.split(' <br> ')

                rhs_temp = rhs_split
                lhs_temp = lhs

                if len(rhs_temp) <= 2: # aka length is 1 or 2.
                    rhs_0_change = re.sub(' ', '-', rhs_temp[0])
                    if rhs_0_change != rhs_0_change.upper():
                        rhs_0_change = rhs_0_change.upper()

                    if rhs_temp[0] != rhs_0_change:
                        rhs_0_change = rhs_0_change + '_NEW'
                        rule = rhs_0_change + ' | ' + rhs_temp[0] + ' | ' + str(1)
                        if rule not in rule_dict:
                            rule_dict[rule] = True
                            f.write(rule + '\n')

                        rhs_temp[0] = rhs_0_change


                    if len(rhs_temp) == 2:
                        rhs_1_change = re.sub(' ', '-', rhs_temp[1])
                        if rhs_1_change != rhs_1_change.upper():
                            rhs_1_change = rhs_1_change.upper()

                        if rhs_temp[1] != rhs_1_change:
                            rhs_1_change = rhs_1_change + '_NEW'
                            rule = rhs_1_change + ' | ' + rhs_temp[1] + ' | ' + str(1)
                            if rule not in rule_dict:
                                rule_dict[rule] = True
                                f.write(rule + '\n')

                            rhs_temp[1] = rhs_1_change

                    rule = lhs_temp + ' | ' + ' '.join(rhs_temp) + ' | ' + str(prob)
                    f.write(rule + '\n')
                else:
                    # > 2
                    while len(rhs_temp) > 1:
                        rhs_0_change = re.sub(' ', '-', rhs_temp[0])
                        if rhs_0_change != rhs_0_change.upper():
                            rhs_0_change = rhs_0_change.upper()

                        if rhs_temp[0] != rhs_0_change:
                            rhs_0_change = rhs_0_change + '_NEW'
                            rule = rhs_0_change + ' | ' + rhs_temp[0] + ' | ' + str(1)
                            if rule not in rule_dict:
                                rule_dict[rule] = True
                                f.write(rule + '\n')

                            rhs_temp[0] = rhs_0_change

                        if len(rhs_temp) == 2:
                            rhs_1_change = re.sub(' ', '-', rhs_temp[1])
                            if rhs_1_change != rhs_1_change.upper():
                                rhs_1_change = rhs_1_change.upper()

                            if rhs_temp[1] != rhs_1_change:
                                rhs_1_change = rhs_1_change + '_NEW'
                                rule = rhs_1_change + ' | ' + rhs_temp[1] + ' | ' + str(1)
                                if rule not in rule_dict:
                                    rule_dict[rule] = True
                                    f.write(rule + '\n')

                                rhs_temp[1] = rhs_1_change

                            rule = lhs_temp + ' | ' + ' '.join(rhs_temp) + ' | ' + str(1)
                            f.write(rule + '\n')

                        else:
                            new_rhs = rhs_temp[0] + ' X' + str(count)

                            if lhs_temp == lhs:
                                rule = lhs_temp + ' | ' + new_rhs + ' | ' + str(prob)
                            else:
                                rule = lhs_temp + ' | ' + new_rhs + ' | ' + str(1)
                            f.write(rule + '\n')

                        rhs_temp = rhs_temp[1:]
                        lhs_temp = 'X' + str(count)
                        count += 1

# TEST
#def main():
#	d = {}
#	d['A'] = {}
#	d['B'] = {}
#	d['A']['aa zz <br> aa <br> aa <br> bb <br> aa zz <br> aa <br> bb'] = 0.5
#	# d['B']['BB BB'] = 0.9
#
#	storeGrammar(d)
#	convertToCNF('cfg.txt')


if __name__ == '__main__':
	main()
