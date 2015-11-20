class State:
    
    def __init__(self, production, pos, origin, end):
        self.production = production
        self.origin = origin
        self.pos = pos
        self.end = end
        self.completed = list()
        
    def incomplete(self):
        return self.pos < len(self.production.body)
        
    def next_cat(self):
        return self.production.body[self.pos]

    def __str__(self):
        s  = self.production.head+" -> "
        for i,symbol in enumerate(self.production.body):
            if i == self.pos:
                s += '*'
            
            s += symbol+' '
        
        if not self.incomplete():
            s += '* '
        
        s += str(self.production.prob)
        s += " ["+str(self.origin)+"] "
            
        return s
    
    def __eq__(self, other):
        return self.__str__() == other.__str__()
    
    def __repr__(self):
        return self.__str__()
    
    
    def __hash__(self):
        self_string = str(self.production)+str(self.pos)+str(self.origin)
        return hash(self_string)
    
    def increment(self, arg):
        new_state = State(self.production, self.pos+1, self.origin)
        new_state.completed = copy(self.completed)
        new_state.completed.append(arg)
        return new_state
    
class Production:
    
    def __init__(self, head, body, prob):
        self.head = head
        self.body = body
        self.prob = prob
        
    def __str__(self):
        return self.head+' -> '+' '.join(self.body)+' '+str(self.prob)
    
class ParseNode:
    def __init__(self, val):
        self.children = list()
        self.value = val

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

def parse(g, words):
        s = [list()]
        top = State(Production('BETA',['TOP'], 1.0), 0, 0, 0)
        s[0].append(top)
        
        for i in range(0, len(words)+1):
            if i==len(s):
                return []
            
            curr = list()
            scanned = list()
            
            while(s[i]):
                state = s[i].pop()
                
                if state.incomplete():
                    if state.next_cat() in g.non_terminals:
                        predictions = predictor(g, state, i)
                        for p in predictions:
                            if p not in curr and p not in s[i]:
                                if not p.__eq__(state):
                                    s[i].append(p)
                    elif i<len(words) and state.next_cat() == words[i]:
                        scan_state = state.increment(words[i])
                        scan_state.end = i
                        scanned.append(scan_state)
                else:
                    s[i].extend(completer(state, i, s))
                
                curr.append(state)
                    
            s[i] = curr
            if len(scanned):
                s.append(scanned)
        
        def isHead(state):
            return state.production.head == 'TOP'
        
        heads = filter(isHead, s[-1])
  
        return [ParseNode(x.completed[0]) for x in heads]
        
def predictor(g, state, i):
    print state
    predictions = set()
    head = state.next_cat()
    
    for body,prob in g.rules[head].items():
        if body == body.upper():
            body = body.split()
        else:
            body = [body,]
        
        p = Production(head, body, prob)
        predictions.add(State(p, 0, i, i))

    return predictions
    
def completer(state, i, s):
    past_states = [ps for ps in s[state.origin] if ps.incomplete()]
    completed = list()
    head = state.production.head
    for p_state in past_states:
        if head == p_state.next_cat():
            x = p_state.increment(state)
            x.end = i
            completed.append(x)


    return completed