import grammar
from copy import copy

class State:
    
    def __init__(self, rule, pos, origin, end):
        self.rule = rule
        self.origin = origin
        self.pos = pos
        self.end = end
        self.completed = list()
        
    def incomplete(self):
        return self.pos < len(self.rule.rhs)
        
    def next_cat(self):
        return self.rule.rhs[self.pos]

    def __str__(self):
        s  = self.rule.lhs+" -> "
        for i,symbol in enumerate(self.rule.rhs):
            if i == self.pos:
                s += '*'
            
            s += symbol+' '
        
        if not self.incomplete():
            s += '* '
        
        s += str(self.rule.prob)
        s += " ["+str(self.origin)+","+str(self.end)+"] "
            
        return s
    
    def __eq__(self, other):
        return self.__str__() == other.__str__() 
    
    def __repr__(self):
        return self.__str__()
    
    
    def __hash__(self):
        self_string = str(self.rule)+str(self.pos)+str(self.origin)+str(self.end)
        return hash(self_string)
    
    def increment(self, arg):
        new_state = State(self.rule, self.pos+1, self.origin, self.end)
        new_state.completed = copy(self.completed)
        new_state.completed.append(arg)
        return new_state
    

class ParseNode:
    def __init__(self, val):
        self.children = list()
        self.value = val

        self.prob = 0.0
        self.start = None
        self.end = None

    def append(self, node):
        self.children.append(node)
        
    def __str__(self):
        return self.recursive_print(0)
    
    def recursive_print(self, indent):
        if len(self.children):
            all_terminal = True
            for child in self.children:
                if len(child.children):
                    all_terminal = False
            
            s = '('+self.value+' '
            indent = indent+len(s)
            for child in self.children[:-1]:
                s += child.recursive_print(indent)
                if all_terminal:
                    s+= ' '
                else:
                    s += '\n'+' '*indent
        
            s += self.children[-1].recursive_print(indent)+')'
        else:
            s = self.value
        
        return s
    
    def __contains__(self, item):
        if not len(self.children):
            return self.value == item
        else:
            if self.value == item:
                return True
            else:
                child_has = [x.__contains__(item) for x in self.children]
                return any(child_has)
            
    def list_rules(self, rules):
        if len(self.children):
            rule = self.value+'|'
            children = [child.value for child in self.children]
            rule += '|'.join(children)
            rules.append(rule)
            for child in self.children:
                child.list_rules(rules)
                
    def isLeaf(self):
        return len(children)==0

def parse(g, words):
        s = [list()]
        top = State(grammar.Rule(vals = ['BETA', 'TOP', 1.0]), 0, 0, 0)
        s[0].append(top)
        
        for i in range(0, len(words)+1):
            if i==len(s):
                return []
            
            curr = set()
            scanned = list()
            nt_scanned = set()
            if i < len(words):
                print words[i]
            while(s[i]):
                state = s[i].pop()
                
                if state.incomplete():
                    nsymbol = state.next_cat()
                    
                    if nsymbol in g.NR and nsymbol not in nt_scanned:
                        
                        predictions = predictor(g, state, i)
                        nt_scanned.add(nsymbol)
                        for p in predictions:
                            if p not in curr and not p.__eq__(state):
                                s[i].append(p)
                                curr.add(p)
                else:   
                    completed = completer(state, i, s)
                    for c in completed:
                        if c not in curr:
                           s[i].append(c)
                            
                    curr.update(completed)
                    
                curr.add(state)
            
            scanned = []
            if i<len(words) and words[i] in g.TR:
                for rule in g.TR[words[i]].values():
                    scanned.append(State(rule, 1, i, i+1))
                                         
            if len(scanned):
                s.append(scanned)
                    
            s[i] = curr
            print len(s[i])
#            for state in s[i]:
#                print state
        
        def isHead(state):
            return state.rule.lhs == 'BETA'
        
        heads = filter(isHead, s[-1])
    
        print len(heads)
        return [recursive_tree(x.completed[0]) for x in heads]
        
def predictor(g, state, i):
    #print state
    predictions = set()
    head = state.next_cat()
    if head in g.NR:
        for r in g.NR[head].values():
            predictions.add(State(r, 0, i, i))
    
    return predictions
    
def completer(state, i, s):
    past_states = [ps for ps in s[state.origin] if ps.incomplete()]
    completed = list()
    head = state.rule.lhs
    for p_state in past_states:
        if head == p_state.next_cat():
            x = p_state.increment(state)
            x.end = i
            completed.append(x)

    return completed

def recursive_tree(state):
    node = ParseNode(state.rule.lhs)
    node.prob = state.rule.prob
    node.start = state.origin
    node.end = state.end

    if len(state.completed):
        for child in state.completed:
            node.append(recursive_tree(child))
    else:
        node.append(ParseNode(state.rule.rhs[0]))

    return node




