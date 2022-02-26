
class State:
    
    def __init__(self, *args, **kwargs):
        self.attr_count = 0
        self.globals = kwargs.get('globals', None)
        self.current_state = None
        self.define_states_already_called = False
        
        for i, s in enumerate(args):
            if i == 0:
                self.set_state(s)
            self.add_state(s)
            
    def set_state(self, state):
        if state in self.__dict__.keys():
            self.current_state = state
        else:
            raise ValueError("This state is not defined: '{}'".format(state))
            
    def __len__(self):
        return self.attr_count

    def add_state(self, new_state):
        setattr(self, new_state.upper(), self.attr_count)
        if self.globals:
            self.globals['STATE_' + new_state.upper()] = self.attr_count
        self.attr_count += 1

    def get_current_state(self):
        return self.current_state
    
    def __getitem__(self, name):
        return getattr(self, name.upper())
    
    def __setitem__(self, name, value):
        raise NotImplementedError("You can't change an enum item's value")

state = State()
_define_states_already_called = False


def add_state(new_state):
    state.add_state(new_state)

def define_states(*args):
    global _define_states_already_called
    global state

    if _define_states_already_called:
        raise Exception("Unable to call define_states twice")

    _define_states_already_called = True
    for i, s in enumerate(args):
        if i == 0:
            state.current_state = s
        state.add_state(s)

def get_state():
    return state.get_current_state()

def set_state(new_state):
    state.set_state(new_state)
