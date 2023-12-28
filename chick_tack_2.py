import sys

from toio.simple import SimpleCube
import signal
from math import sin, cos, radians


toio_sensor_distance = 13  # this is mat sacale, not mm.
panel_size = 29
turn_speed = 10
move_speed = 10
count_timer = 0.5
direction = 0
target_direction = 0
distance = 0
bias = 0

motor_param_dict = {"first_move"   : [ 10, 10, 1.5],
                    "straight"     : [ -8, -8, 1.8],
                    "turn_right"   : [  0, -8, 1.8, -8, -8, 0.4],
                    "turn_left"    : [ -8,  0, 1.8, -8, -8, 0.4]}

LOOP = True
panel_area_sensor       = [[ 22,  54,  78, 110],[ 55,  86,  78, 110],[ 87, 119,  78, 110],[ 120, 152,  78, 110],
                           [ 22,  54,  34,  66],[ 55,  86,  34,  66],[ 87, 119,  34,  66],[ 120, 152,  34,  66],
                           [ 22,  54,  -8,  24],[ 55,  86,  -8,  24],[ 87, 119,  -8,  24],[ 120, 152,  -8,  24],
                           [ 22,  54, -52, -20],[ 55,  86, -52, -20],[ 87, 119, -52, -20],[ 120, 152, -52, -20]]

#x - 9,y -9
panel_area_sensor_raw    = [[ 24, 54,  79, 108],[ 57, 84, 79, 108],[ 88, 118, 79, 109],[ 122, 152, 78, 108],
                            [ 23, 54,  35,  65],[  0,  0,  0,   0],[  0,   0,  0,   0],[   0,   0,  0,   0],
                            [ 22, 55,  -8,  23],[  0,  0,  0,   0],[  0,   0,  0,   0],[   0,   0,  0,   0],
                            [ 23, 54, -21, -51],[  0,  0,  0,   0],[  0,   0,  0,   0],[   0,   0,  0,   0]]

panel_center            = [[  39,  94],[  72,  94],[ 104,  94],[ 137,  94],
                           [  39,  51],[  72,  51],[ 104,  51],[ 137,  51],
                           [  39,   8],[  72,   8],[ 104,   8],[ 137,   8],
                           [  39, -37],[  72, -37],[ 104, -37],[ 137, -37]]

panel_type = ["cross",  "cross",  "cross",   "cross",
              "wcurve", "wcurve", "wcurve",  "wcurve",
              "wcurve", "wcurve", "scurve",  "scurve",
              "scurve", "scurve", "straight","straight"]

def convert_to_sensor_position(pos):
    if pos == None:
        print("mat not found")
    else:
        pos = (int(sin(radians(direction + 43)) * toio_sensor_distance + pos[0]), 
               int(cos(radians(direction + 43)) * toio_sensor_distance + pos[1]))
    return pos

def check_panel_No(sensor_pos):
    for index, panel in enumerate(panel_area_sensor):
        if panel[0] <= sensor_pos[0] and sensor_pos[0] <= panel[1]:
            if panel[2] <= sensor_pos[1] and sensor_pos[1] <= panel[3]:
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
    global direction, target_direction
    target_angle = [0, 90, 180, 270]
    try:
        direction = cube.get_orientation() + 180
        print("before = ", direction)
        if direction > 315 :
            direction = direction - 360
        
        for angle in target_angle:
            if direction > angle - 45 and direction <= angle + 45:
                print("turn angle = ", angle - direction)
                cube.turn(speed = turn_speed, degree = angle - direction)
                target_direction = angle
        direction = cube.get_orientation() + 180
        print("after = ", direction)
        return True
    except:
        return False

def get_target_distance(cube):
    try:
        direction = cube.get_orientation() + 180
    except:
        pass

    pos = cube.get_current_position()
    print("pos = ",pos)
    if pos == None:
        print("mat not found")
        return False
    else:
        sensor_pos = convert_to_sensor_position(pos)
        panel_No = check_panel_No(sensor_pos)
        print("sensor_Pos = " ,sensor_pos, " / panel_No = ", panel_No)

        if target_direction == 0:
            distance = (panel_center[panel_No][1] - 6) - pos[1] + panel_size
            bias = pos[0] - panel_center[panel_No][0]
        elif target_direction == 90:
            distance = pos[0] - (panel_center[panel_No][0] - 6) + panel_size
            bias = panel_center[panel_No][1] - pos[1]
        elif target_direction == 180:
            distance = pos[1] - (panel_center[panel_No][1] + 6) + panel_size
            bias = panel_center[panel_No][0] - pos[0]
        elif target_direction == 270:
            distance = (panel_center[panel_No][0] + 6) - pos[0] + panel_size
            bias = pos[1] - panel_center[panel_No][1]
        
        print("panel = ", panel_No, " / sensor pos = ", sensor_pos, " / direction = ", direction, " / target_direction = ", target_direction, " / distance = ", distance, " / bias = ", bias)
        return True

def move_cube(cube, mode):
    param = motor_param_dict[mode]
    cube.run_motor(left_speed = param[0] ,right_speed = param[1], duration = param[2])

signal.signal(signal.SIGINT, ctrl_c_handler)
 
def main():
    
    with SimpleCube() as cube:

        wait_mat(cube)
        count_down(cube)

        #set_direction(cube)
    
        while LOOP:
            set_direction(cube)
            if get_target_distance(cube):
                print("go go go")
            
            cube.sleep(0.5)

        #move_cube(cube, "straight")

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