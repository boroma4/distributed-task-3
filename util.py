import process

def read_input(path):
    processes = []
    history = []

    with open(path, 'r') as f:
        isSystem = False
        isState = False
        for line in f.readlines():
            line = line.strip()

            if '#System' in line:
                isSystem = True
                isState = False
                continue

            if '#State' in line:
                isState = True
                isSystem = False
                continue

            if len(line) == 0:
                continue

            if isSystem:
                is_coord = False
                name = line

                if 'Coordinator' in line:
                    name = line[0:2]
                    is_coord = True

                processes.append(process.Process(name, is_coord))

            if isState:
                # taking the left side from 
                # Consistency-history; 4,5,6,7,8,9

                data = line.split(';')[1]
                history = [e.strip() for e in data.split(',')]

        return processes, history
