class Process:
    def __init__(self, name, is_coordinator, history=[]):
        self.name = name
        self.is_coordinator = is_coordinator
        self.history = history
        self.is_time_failed = False
        self.is_arbitrary_failed = False
        self.time_fail_sec_left = 0
        self.arbitrary_fail_sec_left = 0

    def __str__(self):
        ending = 'Coordinator' if self.is_coordinator else ''
        return f'{self.name} {ending}'
    
    def history_print(self):
        status = ' (Coordinator)' if self.is_coordinator else ''
        time_error_info = '' if not self.is_time_failed else f', Time failure, Time left: {self.time_fail_sec_left}s'
        arb_error_info = '' if not self.is_arbitrary_failed else f', Arbitrary failure, Time left: {self.arbitrary_fail_sec_left}s'
        print(f'PName: {self.name}{status}. PHistory: {self.history}{time_error_info}{arb_error_info}')

    def __repr__(self):
        return self.__str__()

    def is_failed(self):
        return self.is_time_failed or self.is_arbitrary_failed

    def set_time_failed_for(self, time):
        if self.is_time_failed:
            print('Process already failing')
            return 

        self.is_time_failed = True
        self.time_fail_sec_left = time

    def set_arbitrary_failed_for(self, time):
        if self.is_time_failed:
            print('Process already failing')
            return  

        self.is_arbitrary_failed = True
        self.arbitrary_fail_sec_left = time


    # happens every second, triggered by Ticker class
    def tick(self):
        if self.is_time_failed:
            self.time_fail_sec_left -= 1

        if self.is_arbitrary_failed:
            self.arbitrary_fail_sec_left -= 1
        
        if self.time_fail_sec_left == 0:
            self.is_time_failed = False
        
        if self.arbitrary_fail_sec_left == 0:
            self.is_arbitrary_failed = False
