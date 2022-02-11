
class State:
    
    def __init__(self, *args, **kwargs):
        self.attr_count = 0
        self.current_state = None
        self._define_states(args)
        
    def _define_states(self, states):        
        for i, s in enumerate(states):
            self.add_state(s)
            if i == 0:
                self.set_state(s)
            
    def set_state(self, state):
        try:
            self.current_state = getattr(self, state)
        except:
            raise ValueError("This state is not defined: '{}'".format(state))
            
    def __len__(self):
        return self.attr_count

    def add_state(self, new_state):
        setattr(self, new_state.upper(), self.attr_count)
        self.attr_count += 1

    def get_current_state(self):
        return self.current_state
    
    def __getitem__(self, name):
        return getattr(self, name.upper())
    
    def __setitem__(self, name, value):
        raise NotImplementedError("You can't change an enum item's value")

state = State()

def add_state(new_state):
    state.add_state(new_state)

def define_states(*states):
    state._define_states(states)

def get_state():
    return state.get_current_state()

def set_state(new_state):
    state.set_state(new_state)

