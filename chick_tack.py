import sys

from toio.simple import SimpleCube
import signal

target_direction = 0
turn_speed = 10
move_speed = 10
count_timer = 0.2
motor_param_dict = {"first_move"   : [ -8,  -8, 1.0],
                    "straight"     : [ -8,  -8, 1.8],
                    "turn_right"   : [  0,  -8, 1.8, -8, 0.4],
                    "turn_left"    : [ -8,   0, 1.8, -8, 0.4]}
distance = 0
panel_size = 29


LOOP = True
panels = [[   6,  33,  64,  38],[  34,  63,  64,  38],[  64,  89,  65,  38],[  92, 120,  64,  38],
          [   6,  33,  36,   9],[  34,  63,  36,   9],[  64,  90,  36,   9],[  92, 119,  36,   9],
          [   6,  33,   8, -20],[  34,  62,   8, -20],[ -79, -53,   8, -20],[-108, -80,   8, -20],
          [   6,  33, -22, -49],[  34,  61, -22, -49],[ -78, -53, -22, -49],[   0,   0,   0,   0]]

panel_type = ["cross",  "cross",  "cross",   "cross",
              "wcurve", "wcurve", "wcurve",  "wcurve",
              "wcurve", "wcurve", "scurve",  "scurve",
              "scurve", "scurve", "straight","straight"]

panel_center = [[  11,  43],[  41,  43],[  70,  43],[  99,  43],
                [  11,  14],[  41,  14],[  70,  14],[  99,  14],
                [  11, -14],[  40, -14],[ -73, -14],[-102, -14],
                [  11, -43],[  40, -43],[ -73, -43],[   0,   0]]



#def read_position():


def check_panel_No(pos):
    #print(x,y)
    for index, panel in enumerate(panels):
        if pos[0] >= panel[0] and pos[0] <= panel[1]:
            if pos[1] <= panel[2] and pos[1] >= panel[3]:
                return index
            
def check_gate(cube):
    pos = cube.get_current_position()
    panel = check_panel_No(pos)
    print("panel no = ", panel, " / target_direction = ", target_direction)
    
def ctrl_c_handler(_signum, _frame):
    global LOOP
    print("Ctrl_C")
    LOOP = False

def wait_button(cube):
    BUTTON = True
    while BUTTON:
        if cube.is_button_pressed() == 128:
            BUTTON = False
        cube.sleep(0.5)
        cube.turn_on_cube_lamp(r=0, g=0, b=255, duration=0.1)

    cube.turn_on_cube_lamp(r=0, g=255, b=0, duration=0.5)
    cube.sleep(0.5)
    cube.turn_on_cube_lamp(r=0, g=255, b=0, duration=0.5)
    cube.sleep(0.5)
    cube.turn_on_cube_lamp(r=255, g=0, b=0, duration=0.5)
    cube.sleep(0.5)

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


def set_orientation(cube):
    global distance
    global target_direction
    target_angle = [0, 90, 180, -90]

    direction = cube.get_orientation()
    print("before = ", direction)
    if direction < -135 :
        direction = 360 + direction 
    for angle in target_angle:
        if direction > angle - 45 and direction <= angle + 45:
            print("turn angle = ", angle - direction)
            degree = angle - direction
            target_direction = angle

    pos = cube.get_current_position()
    panel_No = check_panel_No(pos)
    print("panel no = ", panel_No, " / pos = ", pos, " / panel_center = ",panel_center[panel_No])
    if target_direction == 180:
        distance = (panel_center[panel_No][1] - 12) - pos[1] + panel_size
        bias = pos[0] - panel_center[panel_No][0]
    elif target_direction == -90:
        distance = pos[0] - (panel_center[panel_No][0] - 12) + panel_size
        bias = panel_center[panel_No][1] - pos[1]
    elif target_direction == 0:
        distance = pos[1] - (panel_center[panel_No][1] + 12) + panel_size
        bias = panel_center[panel_No][0] - pos[0]
    elif target_direction == 90:
        distance = (panel_center[panel_No][0] + 12) - pos[0] + panel_size
        bias = pos[1] - panel_center[panel_No][1]
    
    print("distance = ", distance, " / bias = ", bias)

    degree -= bias

    cube.turn(speed = turn_speed, degree = degree)
    direction = cube.get_orientation()
    print("after = ", direction)


def move_cube(cube, mode):
    #print("mode = ", mode)
    param = motor_param_dict[mode]
    #print("param = ", param)

    if mode == "straight":
        cube.run_motor(left_speed = param[0] ,right_speed = param[1], duration = (param[2] * distance/panel_size))
    elif mode == "turn_right" or mode == "turn_left":
        cube.run_motor(left_speed = param[3], right_speed = param[3], duration = param[4])
        cube.run_motor(left_speed = param[0] ,right_speed = param[1], duration = param[2])
        cube.run_motor(left_speed = param[3], right_speed = param[3], duration = param[4])
    

signal.signal(signal.SIGINT, ctrl_c_handler)


    


def main():
    
    with SimpleCube() as cube:

        wait_mat(cube)
        set_orientation(cube)
        count_down(cube)

        #move_cube(cube,"first_move")
       
        
        while LOOP:
            check_gate(cube)
            move_cube(cube,"straight")
            set_orientation(cube)
        
            #check_gate(cube)
            #move_cube(cube,"turn_right")
            #set_orientation(cube)


        print("finished")

if __name__ == "__main__":
    sys.exit(main())