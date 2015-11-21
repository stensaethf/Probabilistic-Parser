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

class Rule:
    
    def __init__(self, l = None, r = None, p = 0.0, *vals):
        if len(vals):
            self.lhs = l[0]
            self.rhs = l[1:-1]
            self.prob = l[-1]
        else:
            self.lhs = l
            self.rhs = r
            self.prob = p
        
    def __str__(self):
        return self.lhs+' -> '+'|'.join(self.rhs)+' '+str(self.prob)

class Grammar:
    
    def __init__(self, E = None, N = None, R = None, S = 'TOP', nodes = None):
        if len(nodes):
            E, N, R = self.transform_nodes(nodes)
            
        self.rules = R
        self.non_terminals = N
        self.terminals = E
        self.start_symbol = S
        self.count = 0
        
    def convertToCNF(self):
        for lhs_dict in self.rules.keys():
            cnf_rules = []
            print lhs_dict
            while len(lhs_dict):
                rule = lhs_dict.popitem()
                cnf_rules.extend(self.cnf(rule))
            
            lhs_dict = cnf_rules
        
        for lhs in self.rules.keys():
            for key in self.rules[lhs]:
                rule = lhs_dict[key]
                if len(rule.rhs) == 1 and rule.rhs[0] not in self.terminals:
                    del lhs_dict[key]
                    for x in self.rules[rule.rhs[0]]:
                        prob = x.prob*rule.prob
                        new_rule = Rule(l = lhs,r = x.rhs,p = prob)
                        lhs_dict[' '.join(x.rhs)] = new_rule
                     
                
    def cnf(self, rule):
        new_rules = []
        body = rule.lhs
        head = rule.rhs
        
        if len(body) >= 2:
            for i, symbol in enumerate(body):
                if symbol in self.terminals:
                    new_rule = [self.new_symbol(),]
                    new_rule.append(symbol)
                    new_rule.append(1.0)
                    new_rules.append(Rule(new_rule))
                    
                    body[i] = new_rule[0]
        
        while len(rhs)>2:
            new_head = self.new_symbol()
            new_rule = [head, rhs.pop(0), new_head, 1.0]
            new_rules.append(Rule(new_rule))
            head = new_head
            
        new_rule = [head,]
        new_rule.extend(body)
        new_rule.append(1.0)
        
        new_rules.append(Rule(new_rule))
                
        return new_rules
                
    def new_symbol(self):
        while 'X'+str(self.count) in self.non_terminals:
            self.count += 1
                
        return 'X'+str(self.count)
    
    def write(self, output_file):
        for lhs in self.rules:
            for rule in self.rules[lhs].keys():
                output_file.write(rule)
    
    def transform_nodes(self, nodes):
        non_terminals = set()
        terminals = set()
        rules = {}
        
        count = {}
        for node in nodes:
            self.recursive_count(node, count)
            
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
                rule = lhs + ' | ' + rhs + ' | ' + str(prob_dict[lhs][rhs])
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
