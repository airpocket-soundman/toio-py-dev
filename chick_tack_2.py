import sys

from toio.simple import SimpleCube
import signal
from math import sin, cos, radians


toio_sensor_distance = 14  # this is mat sacale, not mm.
turn_speed = 10
move_speed = 10
count_timer = 2.0
motor_param_dict = {"first_move"   : [ 10, 10, 1.5],
                    "straight"     : [ -8, -8, 1.6],
                    "turn_right"   : [  0, -8, 1.7, -8, -8, 0.5],
                    "turn_left"    : [ -8,  0, 1.7, -8, -8, 0.5]}

LOOP = True
panels = [[  33,   6,  64,  37],[  62,  34,  64,  37],[  90,  64,  64,  37],[ 120,  92,  64,  37],
          [  33,   6,  36,   9],[  62,  34,  36,   9],[  90,  64,  36,   9],[ 120,  92,  36,   9],
          [  33,   6,   8,  20],[  62,  34,   8, -20],[ -53, -79,   8, -20],[ -80,-108,   9, -20],
          [  33,   6, -21, -48],[  62,  34, -21, -48],[ -53, -79, -21, -48],[   0,   0,   0,   0]]

panel_type = ["cross",  "cross",  "cross",   "cross",
              "wcurve", "wcurve", "wcurve",  "wcurve",
              "wcurve", "wcurve", "scurve",  "scurve",
              "scurve", "scurve", "straight","straight"]

def convert_to_sensor_position(pos, direction):
    if pos == None:
        print("mat not found")
    else:
        pos = (int(sin(radians(direction + 43)) * toio_sensor_distance + pos[0]), 
               int(cos(radians(direction + 43)) * toio_sensor_distance + pos[1]))
    return pos

def check_panel_No(x,y):
    #print(x,y)
    for index, panel in enumerate(panels):
        if panel[0] > x and x > panel[1]:
            if panel[2] > y and y > panel[3]:
                return index

def ctrl_c_handler(_signum, _frame):
    global LOOP
    print("Ctrl_C")
    LOOP = False

def wait_mat(cube):
    print("waiting mat")
    DETECT_MAT = True
    while DETECT_MAT:
        pos = cube.get_current_position()
        print(pos)
        if pos != None:
            print("detect mat")
            DETECT_MAT = False
        cube.sleep(0.5)
    
def count_down(cube):
    cube.turn_on_cube_lamp(r=0, g=255, b=0, duration=count_timer)
    cube.sleep(0.5)
    cube.turn_on_cube_lamp(r=0, g=255, b=0, duration=count_timer)
    cube.sleep(0.5)
    cube.turn_on_cube_lamp(r=255, g=0, b=0, duration=count_timer)
    cube.sleep(0.5)

def set_direction(cube):
    target_angle = [0, 90, 180, 270]
    direction = cube.get_orientation() + 180
    print("before = ", direction)
    if direction > 315 :
        direction = direction - 360
    
    for angle in target_angle:
        if direction > angle - 45 and direction <= angle + 45:
            print("turn angle = ", angle - direction)
            cube.turn(speed = turn_speed, degree = angle - direction)
    direction = cube.get_orientation() + 180
    print("after = ", direction)

def move_cube(cube, mode):
    param = motor_param_dict[mode]
    cube.run_motor(left_speed = param[0] ,right_speed = param[1], duration = param[2])

signal.signal(signal.SIGINT, ctrl_c_handler)
 
def main():
    
    with SimpleCube() as cube:

        wait_mat(cube)
        count_down(cube)
        set_direction(cube)
        move_cube(cube, "straight")

        """ #main loop
        while LOOP:
            pos = cube.get_current_position()
            direction = cube.get_orientation() + 180
            sensor_pos = convert_to_sensor_position(pos, direction)
            
            print("POSITION:", pos, direction)
            #print("direction:" )
        """

if __name__ == "__main__":
    sys.exit(main())