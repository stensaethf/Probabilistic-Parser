'''
grammar.py
Frederik Roenn Stensaeth, Phineas Callahan
11.19.15
'''

import re, string

class Rule:
    """
    Rule is a class for containing rules. An instance of the class has a
    left hand side, a right hand side and probability.
    """
    
    def __init__(self, l = None, r = None, p = 0.0, vals = None):
        if vals:
            self.lhs = vals[0]
            self.rhs = vals[1:-1]
            self.prob = vals[-1]
        else:
            self.lhs = l
            self.rhs = r
            self.prob = p

    def __hash__(self):
        return hash(self.lhs)+hash(tuple(self.rhs))
        
    def __str__(self):
        return self.lhs+' -> '+'|'.join(self.rhs)+' '+str(self.prob)

    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs == self.rhs

class Grammar:
    """
    Grammar is a class for containing grammars. An instance of the class has
    both a set for terminals and non terminals, and dictionaries that contain
    the NR and TR rules.
    """
    
    def __init__(self, E = None, N = None, R = None, S = 'TOP', nodes = None):
        if len(nodes):
            count = self.transform_nodes(nodes)
            E, N, R = self.from_count(count)
        
        self.non_terminals = N
        self.terminals = E
        self.NR = {}
        self.TR = {}
        
        for lhs in R:
            while len(R[lhs]):
                self.add_rule(R[lhs].popitem()[1])
                
        self.start_symbol = S
        self.count = 0

    def incrementCount(self):
        """
        incrementCount() increments the count of the grammar by one.

        @params: n/a.
        @return: n/a.
        """
        self.count = self.count + 1
        
    def convertToCNF(self):
        """
        convertToCNF() converts the grammar to CNF from CFG.

        @params: n/a.
        @return: n/a.
        """
        curr_rules = []
        for lhs in self.NR:
            curr_dict = self.NR[lhs]
            while len(curr_dict):
                curr_rules.append(curr_dict.popitem()[1])
        for rhs in self.TR:
            curr_dict = self.TR[rhs]
            while len(curr_dict):
                curr_rules.append(curr_dict.popitem()[1])
        
        curr_rules = self.TERM(curr_rules)
        curr_rules = self.BIN(curr_rules)
        curr_rules = self.UNIT(curr_rules)
        
        for rule in curr_rules:
            # if rule.lhs == 'NAC':
            #     print rule
            self.add_rule(rule)
            
        self.non_terminals = set(self.NR.keys())
        for lhs in self.NR:
            for rule in self.NR[lhs].values():
                self.non_terminals.update(rule.rhs)
                
        self.terminals = set(self.TR.keys())
        
        
    def UNIT(self, rules):
        """
        UNIT() removes all unit productions in the grammar.

        @params: rules.
        @return: new rules.
        """
        new_rules = []

        rule_lookup = {x.lhs : {} for x in rules}
        for rule in rules:
            rule_lookup[rule.lhs]['|'.join(rule.rhs)] = rule

        processed = set()

        while len(rules):
            rule = rules.pop()
            # print rule
            if self.isUnit(rule):
                processed.add(rule)
                # print rule
                # print rule in processed
                for x in rule_lookup[rule.rhs[0]].values():
                    prob = x.prob*rule.prob
                    new_rule = Rule(l = rule.lhs,r = x.rhs,p = prob)
                    if new_rule not in processed:
                        if not self.isUnit(new_rule):
                            new_rules.append(new_rule)
                        else:
                            rules.append(new_rule)
                            # print '    '+str(new_rule),
                            # print new_rule in processed
                        
            else:
                new_rules.append(rule)
                
        return new_rules
                     
                
    def TERM(self, rules):
        """
        TERM() removes any rule that contains a terminal and something else.
        Can be other terminals or other non-terminals.

        @params: rules.
        @return: new rules.
        """
        new_rules = []
        
        while(len(rules)):
            rule = rules.pop()
            body = rule.rhs
            head = rule.lhs
            
            if len(body) >= 2:
                for i, symbol in enumerate(body):
                    if symbol in self.terminals:
                        new_rule = [self.new_symbol(),]
                        new_rule.append(symbol)
                        new_rule.append(1.0)
                        new_rules.append(Rule(vals = new_rule))
                    
                        body[i] = new_rule[0]
            
            new_rules.append(rule)
        return new_rules
    
    def BIN(self, rules):
        """
        BIN() makes sure that everything is a binary. Anything with more than
        two non-terminals are made into a sequence of rules that converts them
        to binary form.

        @params: rules.
        @return: new rules.
        """
        new_rules = []
        
        while(len(rules)):
            rule = rules.pop()
            body = rule.rhs
            head = rule.lhs
            
            if len(body) > 2:
                prev = body.pop()
                while len(body) >= 2:
                    new_head = self.new_symbol()
                    new_rule = [new_head, body.pop(), prev, 1.0]
                    new_rules.append(Rule(vals = new_rule))
                    prev = new_head
            
                new_rule = [head, body[0], prev, rule.prob]
                new_rules.append(Rule(vals = new_rule))
            else:
                new_rules.append(rule)
                
        return new_rules    
        
    def isUnit(self, rule):
        """
        isUnit() checks whether a rule is a unit production.

        @params: rule.
        @return: boolean.
        """
        return len(rule.rhs) == 1 and rule.rhs[0] not in self.terminals
    
    def new_symbol(self):
        """
        new_symbol() creates a new symbol.

        @params: n/a.
        @return: new symbol.
        """
        n_symbol = 'X'+str(self.count)
        self.incrementCount()
                
        return n_symbol

    def add_rule(self, rule):
        """
        add_rule() adds the given rule to the grammar.

        @params: rule.
        @return: n/a.
        """
        entry = {}
        if len(rule.rhs) == 1 and rule.rhs[0] in self.terminals:
            terminal = rule.rhs[0]
            if rule.rhs[0] in self.TR:
                entry = self.TR[terminal]
            else:
                self.TR[terminal] = entry
                
            entry[rule.lhs] = rule
        else:
            if rule.lhs in self.NR:
                entry = self.NR[rule.lhs]
            else:
                self.NR[rule.lhs] = entry
        
            key = '|'.join(rule.rhs)
            entry[key] = rule
    
    def write(self, output_file):
        """
        write() writes the grammar to the given output file.

        @params: name of output file.
        @return: n/a.
        """
        for lhs in self.NR:
            for rule in self.NR[lhs].values():
                rule_str = rule.lhs+'|'+'|'.join(rule.rhs)+'|'+str(rule.prob)
                output_file.write(str(rule)+'\n')
                
        output_file.write('\n')
        for lhs in self.TR:
            for rule in self.TR[lhs].values():
                rule_str = rule.lhs+'|'+'|'.join(rule.rhs)+'|'+str(rule.prob)
                output_file.write(str(rule)+'\n')
        
        output_file.close()
    
    def transform_nodes(self, nodes):
        """
        transform_nodes() takes a set of nodes and calls recursive_count() to
        count the number of times each rule is seen in the nodes.

        @params: nodes.
        @return: count dictionary.
        """
        count = {}
        for node in nodes:
            self.recursive_count(node, count)
                
        return count
    
    def from_count(self, count):
        """
        from_count() creates terminal and non terminal sets and a dictionary
        of rules from the given count dictionary.

        @params: count dictionary.
        @return: terminals (set), non terminals (set), rules.
        """
        non_terminals = set()
        terminals = set()
        rules = {}
        
        for lhs in count:
            lhs_sum = sum(count[lhs].values())
            for key,val in count[lhs].items():
                count[lhs][key] = val/lhs_sum
        
        for lhs in count:
            for rhs in count[lhs]:
                prob = count[lhs][rhs]
                body = map(string.strip, rhs.split('|'))
                
                terminals.update(body)
                non_terminals.add(lhs)
                
                entry = {}
                if lhs in rules:
                    entry = rules[lhs]
                else:
                    rules[lhs] = entry
        
                entry[rhs] = Rule(l = lhs, r = body, p = prob)
        
        terminals -= non_terminals
        return terminals, non_terminals, rules
            
    def recursive_count(self, node, count):
        """
        recursive_count() recusively counts the number of times a rule is seen,
        given a root node of a tree.

        @params: node, count dictionary.
        @return: n/a.
        """
        if len(node.children):
            entry = {}
            if node.value in count:
                entry = count[node.value]
            else:
                count[node.value] = entry

            children = [child.value for child in node.children]
            child_string = '|'.join(children)
            if child_string in entry:
                entry[child_string] += 1.0
            else:
                entry[child_string] = 1.0
                
            for child in node.children:
                self.recursive_count(child, count)
                                
def read_grammar(input_file):
    """
    read_grammar() takes the contents of a file and reads in the grammar from
    that file.

    @params: contents of file were grammar is stored.
    @return: grammar object.
    """
    rules = {}
    non_terminals = set()
    terminals = set()
    
    for line in input_file:
        rule = map(string.strip, line.split('|'))
        
        non_terminals.add(rule[0])
        terminals.update(rule[1:-1])
        
        entry = {}
        if rule[0] in rules:
            entry = rules[rule[0]]
        else:
            rules[rule[0]] = entry
        
        entry[' '.join(rule[1:-1])] = Rule(rule)
        
    terminals -= non_terminals
    return Grammar(E = terminals, N = non_terminals, R = rules)

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
                rule = lhs + '|' + rhs + '|' + str(prob_dict[lhs][rhs])
                f.write(rule + '\n')



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
