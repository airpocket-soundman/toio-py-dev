import sys
import signal

from toio.simple import SimpleCube

LOOP = True
def ctrl_c_handler(_signum, _frame):
    global LOOP
    print("Ctrl-C")
    LOOP = False


signal.signal(signal.SIGINT, ctrl_c_handler)

def test():
    with SimpleCube() as cube:
        while LOOP:
            angle = cube.get_3d_angle()
            print(angle)
            cube.sleep(0.01)


if __name__ == "__main__":
    sys.exit(test())