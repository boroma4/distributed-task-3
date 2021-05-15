class Process:
    def __init__(self, name, is_coordinator):
        self.name = name
        self.is_coordinator = is_coordinator

    def __str__(self):
        ending = 'Coordinator' if self.is_coordinator else ''
        return f'{self.name} {ending}'

    def __repr__(self):
        return self.__str__()