import signal
import sys

LOOP = True
valid_signals = signal.valid_signals()
print(valid_signals)


def print_param(_signum, _frame):
    print("_signmu = ", _signum)
    print("_frame = ", _frame)

def ctrl_c_handler(_signum, _frame):
    global LOOP
    LOOP = False
    print_param(_signum, _frame)


signal.signal(signal.SIGINT, ctrl_c_handler)

def test():
    print("LOOP start.")
    while LOOP:
        a = 5
    print("LOOOP finished.")

if __name__ == "__main__":
    sys.exit(test())
        