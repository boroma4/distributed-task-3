import sys
import util

def voting(_processes, new_value):
    # Processes without coordinator
    processes = list(filter(lambda p: not p.is_coordinator,_processes.copy()))
    # Coordinator
    coordinator = list(filter(lambda p: p.is_coordinator, _processes.copy()))[0]
    coordinator.history.append(new_value)

    messages = []

    for i in range(len(processes)):
        # Coordinator sends new value to other processes and it's own history
        processes[i].history.append(new_value)
        # Basically sending the message back to coordinator for it to perform voting
        if processes[i].history == coordinator.history:
            messages.append('OK')
        else:
            messages.append('CANCEL')
    
    # Voting
    oks = list(filter(lambda p: p=='OK',messages))
    cancels = list(filter(lambda p: p=='CANCEL',messages))

    if len(cancels) < len(oks):
        print(f'Value {new_value} will not be added to history. Commit failed')
        # No commit
        return _processes.copy()
    else:
        processes.append(coordinator)
        # Commit
        return processes

if __name__ == "__main__":
    # Entrypoint
    print(sys.argv[1])
    processes, history = util.read_input(sys.argv[1])
    print(processes, history)
    # Initializing. Each process stores the value state.
    for i,process in enumerate(processes):
        processes[i].history = history
    choice = ""

    while choice != "exit":
        try:
            choice = input("\nPlease, enter your next action:\n").strip()
            args = choice.split(" ")

            if args[0] == "exit":
                print("\nCiao")
            elif args[0] == "add":
                processes = util.add_process(processes, args[1])
            else:
                print('Unsupported command')
            
            for p in processes:
                p.history_print()

        except KeyboardInterrupt:
            print("Please, do not use Ctrl+C. Try again with \'exit\' command")
        except:
            print("Please try again")
