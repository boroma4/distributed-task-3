# Abstracted 2PC implementation

Running the program only requires python 3.

To start run:
```
py main.py 2PC.txt
```

Available commands:
```
debug - just printing the info

set-value X - committing a new value, example: set-value 5

rollback X - rolling the state back X steps, example: rollback 3

add PX - add a new process, example: add P100

remove PX - remove a process, example: remove P100

time-failure PX N - time-failure process PX for N seconds, example: time-failure P10 60

arbitrary-failure PX N - arbitrary-failure process PX for N seconds, example: arbitrary-failure P10 60
```