import sys

from toio.simple import SimpleCube
import signal

turn_speed = 10
move_speed = 10
count_timer = 2.0
motor_param_dict = {"first_move"   : [10, 10, 1.5],
                    "straight"     : [10, 10, 4],
                    "turn_right"   : [10,  2, 4],
                    "turn_left"    : [ 2, 10, 4]}

LOOP = True
panels = [[   7,  33,  64,  38],[  35,  63,  64,  38],[  64,  89,  65,  37],[  92, 120,  64,  37],
          [   6,  33,  36,   8],[  34,  63,  36,   9],[  64,  90,  36,   9],[  92, 119,  36,   9],
          [   6,  32,   8,  19],[  34,  62,   8, -20],[ -79, -53,   7, -19],[-108, -80,   7, -19],
          [   6,  33, -21, -48],[  35,  61, -21, -49],[ -78, -53, -22, -48],[   0,   0,   0,   0]]

panel_type = ["cross",  "cross",  "cross",   "cross",
              "wcurve", "wcurve", "wcurve",  "wcurve",
              "wcurve", "wcurve", "scurve",  "scurve",
              "scurve", "scurve", "straight","straight"]



#def read_position():


def check_panel_No(x,y):
    #print(x,y)
    for index, panel in enumerate(panels):
        if x > panel[0] and x < panel[1]:
            if y < panel[2] and y > panel[3]:
                return index

def gate_check():
    print("gate check")


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
    target_angle = [0, 90, 180, 270]
    orientation = cube.get_orientation() + 180
    print("before = ", orientation - 180)
    if orientation > 315 :
        orientation = orientation - 360
    
    for angle in target_angle:
        if orientation > angle - 45 and orientation <= angle + 45:
            print("turn angle = ", angle - orientation)
            cube.turn(speed = turn_speed, degree = angle - orientation)
    orientation = cube.get_orientation()
    print("after = ", orientation)

def move_cube(cube, mode):
    param = motor_param_dict[mode]
    cube.run_motor(left_speed = param[0] ,right_speed = param[1], duration = param[2])

signal.signal(signal.SIGINT, ctrl_c_handler)

def main():
    
    with SimpleCube() as cube:

        wait_mat(cube)
        #set_orientation(cube)
        count_down(cube)
        set_orientation(cube)
        move_cube(cube,"first_move")
        set_orientation(cube)

        while LOOP:
            pos = cube.get_current_position()
            orientation = cube.get_orientation()
            print("POSITION:", pos, orientation)
            #print("orientation:" )
            cube.sleep(0.5)
            if pos != None:
                panel_no = check_panel_No(pos[0], pos[1])
            else:
                panel_no = None
            print(panel_no)


if __name__ == "__main__":
    sys.exit(main())