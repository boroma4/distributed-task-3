import sys
import util
import random
import copy
from process import Process
from ticker import Ticker

def voting(_processes, new_value, rollback_count):

    if (new_value is None and rollback_count is None) or (new_value is not None and rollback_count is not None):
        print('Incorrect voting, it\'s a bug')
        return _processes

    # Processes without coordinator
    normal_processes = copy.deepcopy(list(filter(lambda p: not p.is_coordinator,_processes.copy())))
    # Coordinator
    coordinator = copy.deepcopy(list(filter(lambda p: p.is_coordinator, _processes.copy()))[0])

    if new_value:
        coordinator.history.append(new_value)

    if rollback_count:
        if len(coordinator.history) - rollback_count <= 0:
            print('Rollback too long')
            return _processes

        coordinator.history = coordinator.history[: len(coordinator.history) - rollback_count]

    # coordinator time failed
    if coordinator.is_time_failed:
        print('Coordinator is failed, aborting')
        return _processes

    messages = []

    for i in range(len(normal_processes)):
        # check for time failure
        if normal_processes[i].is_time_failed:
            # just do nothing
            continue

        # Coordinator sends new value to other processes and it's own history
        if new_value:
            normal_processes[i].history.append(new_value)

        if rollback_count:
            # erase everything if rollback is too long
            if len(normal_processes[i].history) - rollback_count <= 0:
                normal_processes[i].history = []
            else:
                normal_processes[i].history = normal_processes[i].history[: len(normal_processes[i].history) - rollback_count]

        # Didn't see anything about history condition in slides

        # Basically sending the message back to coordinator for it to perform voting
        # if normal_processes[i].history == coordinator.history:
        #     # flip
        #     msg = 'OK' if not normal_processes[i].is_arbitrary_failed else 'CANCEL'
        #     messages.append('OK')
        # else:
        #     # flip
        #     msg = 'CANCEL' if not normal_processes[i].is_arbitrary_failed else 'OK'
        #     messages.append('CANCEL')

        # Basically sending the message back to coordinator for it to perform voting
        # flip
        msg = 'OK' if not normal_processes[i].is_arbitrary_failed else 'CANCEL'
        messages.append(msg)
    
    # Voting
    oks = list(filter(lambda p: p=='OK',messages))
    cancels = list(filter(lambda p: p=='CANCEL',messages))
    
    # if all are VOTE-COMMIT, it sends GLOBAL COMMIT to all participants, otherwise it sends GLOBAL-ABORT
    # Flip coordinator decision if arbitrary failed

    if (len(cancels) == 0 and not coordinator.is_arbitrary_failed) or (len(cancels) != 0 and coordinator.is_arbitrary_failed):
        normal_processes.append(coordinator)
        # Commit
        return normal_processes
    else:
        print(f'Value {new_value} will not be added to history. Commit failed')
        # No commit
        return _processes.copy()


def set_val(_processes, val):
    return voting(_processes, val, None)


def rollback(_processes, n):
    return voting(_processes, None, int(n))


def add_process(_processes, name):
    coord_history = list(filter(lambda p: p.is_coordinator, _processes))[0].history
    matches = list(filter(lambda p: p.name == name, _processes))

    if len(matches) != 0:
        print('Proc with this name is already in the list')
        return _processes

    new_proc = Process(name, False, coord_history)
    copy_proc = _processes.copy()
    copy_proc.append(new_proc)
    return copy_proc


def remove_process(_processes, name):
    if not util.check_name_match(_processes, name):
        return _processes

    copy_proc = _processes.copy()
    matches = list(filter(lambda p: p.name == name, _processes))

    proc_to_remove = matches[0]

    if proc_to_remove.is_coordinator:
        random.choice(copy_proc).is_coordinator = True

    copy_proc.remove(proc_to_remove)
    return copy_proc


def time_fail(_processes, name, time):
    if not util.check_name_match(_processes, name):
        return _processes

    copy_proc = _processes.copy()
    matches = list(filter(lambda p: p.name == name, _processes))
    
    proc_to_fail = matches[0]
    proc_to_fail.set_time_failed_for(int(time))

    return copy_proc


def arbitrary_fail(_processes, name, time):
    if not util.check_name_match(_processes, name):
        return _processes

    copy_proc = _processes.copy()
    matches = list(filter(lambda p: p.name == name, _processes))
    
    proc_to_fail = matches[0]
    proc_to_fail.set_arbitrary_failed_for(int(time))

    return copy_proc

if __name__ == "__main__":
    # Entrypoint
    print(sys.argv[1])
    processes, history = util.read_input(sys.argv[1])
    print(processes, history)
    # Initializing. Each process stores the value state.
    for i,process in enumerate(processes):
        processes[i].history = history.copy()
    choice = ""

    ticker = Ticker(processes)
    ticker.start()

    while choice != "exit":
        try:
            choice = input("\nPlease, enter your next action:\n").strip()
            args = choice.split(" ")

            if args[0] == "exit":
                print("\nCiao")
            elif args[0] == "debug":
                util.assert_arg_len(args, 1)
            elif args[0] == "set-value":
                util.assert_arg_len(args, 2)
                processes = set_val(processes, args[1])
            elif args[0] == "rollback":
                util.assert_arg_len(args, 2)
                processes = rollback(processes, args[1])                
            elif args[0] == "add":
                util.assert_arg_len(args, 2)
                processes = add_process(processes, args[1])
            elif args[0] == "remove":
                util.assert_arg_len(args, 2)
                processes = remove_process(processes, args[1])
            elif args[0] == "time-failure":
                util.assert_arg_len(args, 3)
                processes = time_fail(processes, args[1], args[2])
            elif args[0] == "arbitrary-failure":
                util.assert_arg_len(args, 3)
                processes = arbitrary_fail(processes, args[1], args[2])
            else:
                print('Unsupported command')
            
            ticker.upd_list(processes)
            print('\n')
            for p in processes:
                p.history_print()

        except KeyboardInterrupt:
            print("Please, do not use Ctrl+C. Try again with \'exit\' command")
        # debug
        except Exception as e:
            print("Please try again")

    ticker.stop()

