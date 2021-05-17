class Process:
    def __init__(self, name, is_coordinator, history=[]):
        self.name = name
        self.is_coordinator = is_coordinator
        self.history = history

    def __str__(self):
        ending = 'Coordinator' if self.is_coordinator else ''
        return f'{self.name} {ending}'
    
    def history_print(self):
        status = ' (Coordinator)' if self.is_coordinator else ''
        print(f'PName: {self.name}{status}. PHistory: {self.history}')

    def __repr__(self):
        return self.__str__()