import signal
import sys
import math

from toio.simple import SimpleCube 

LOOP = True
toio_sensor_distance = 13  # this is mat sacale, not mm.

def ctrl_c_handler(_signum, _frame):
    global LOOP
    print("Ctrl-C")
    LOOP = False

signal.signal(signal.SIGINT, ctrl_c_handler)

def convert_to_sensor_position(pos, orientation):
    if pos == None:
        print("mat not found")
    else:
        orientation = orientation + 180
        print( int(math.sin(math.radians(orientation + 43)) * toio_sensor_distance), 
               int(math.cos(math.radians(orientation + 43)) * toio_sensor_distance))
        pos = (int(math.sin(math.radians(orientation + 43)) * toio_sensor_distance + pos[0]), 
               int(math.cos(math.radians(orientation + 43)) * toio_sensor_distance + pos[1]))
    return pos, orientation

def test():
    with SimpleCube() as cube:
        while LOOP:
            pos = cube.get_current_position()
            orientation = cube.get_orientation()
            converted_pos, converted_orientation = convert_to_sensor_position(pos, orientation)
            print("pos:", pos, orientation , " / converted pos:", converted_pos, converted_orientation)
            cube.sleep(0.5)

if __name__ == "__main__":
    sys.exit(test())