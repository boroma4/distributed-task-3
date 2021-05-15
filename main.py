import sys
import util

if __name__ == "__main__":
    # Entrypoint
    print(sys.argv[1])
    processes, history = util.read_input(sys.argv[1])
    print(processes, history)
    choice = ""

    while choice != "exit":
        try:
            choice = input("\nPlease, enter your next action:\n").strip()
            args = choice.split(" ")

            if args[0] == "exit":
                print("\nCiao")
            else:
                print('Unsupported command')

        except KeyboardInterrupt:
            print("Please, do not use Ctrl+C. Try again with \'exit\' command")
        except:
            print("Please try again")
