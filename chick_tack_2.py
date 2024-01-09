import sys

from toio.simple import SimpleCube
import signal
from math import sin, cos, radians


toio_sensor_distance = 13  # this is mat sacale, not mm.
panel_size = 29
turn_speed = 10
move_speed = 10
count_timer = 0.1
speed = -8

def set_motor_param():
    motor_param_dict = {"straight"      : [ speed, speed, 0.45 / speed * -1],                   # 右速度, 左速度, 単位動作時間
                        "turn_right"    : [ speed, speed, 17 / speed * -1 - 0.1, 5.6 / speed * -1, 0.45 / speed * -1],    # 右速度, 左速度, 旋回時間, 旋回前直進時間, 単位動作時間
                        "turn_left"     : [ speed, speed, 17 / speed * -1 - 0.1, 5.6 / speed * -1, 0.45 / speed * -1],    # 同上
                        "clush"         : [-50, 50, 2.0]}                    # 右速度, 左速度, スピン時間
    return motor_param_dict

LOOP = True
panel_area_sensor       = [[ 22,  54,  76, 110],[ 55,  86,  76, 110],[ 87, 119,  76, 110],[ 120, 152,  76, 110],
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
                           [  39,   8],[  71,   7],[ 104,   8],[ 137,   8],
                           [  39, -37],[  72, -37],[ 104, -37],[ 137, -37]]

panel_type_list         = ["cross",  "cross",  "cross",   "cross",
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

def get_panel_No(sensor_pos):
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

def get_target_direction(direction):
    target_direction_list = [0, 90, 180, 270]
    # print("direction = ", direction)
    if direction > 315:
        direction = direction - 360
    for angle in target_direction_list:
        #print("angle = ", angle, " / direction = ", direction)
        if direction > angle - 45 and direction <= angle + 45:
            #print("angle offset = ", angle - direction)
            angle_offset = angle - direction
            target_direction = angle

    return target_direction, angle_offset

def get_offset(pos_center, panel_No, target_direction):
    if target_direction == 0:
        forward_offset = pos_center[1] - (panel_center[panel_No][1] - 18)
        LR_offset = pos_center[0] - panel_center[panel_No][0]
    elif target_direction == 90:
        forward_offset = pos_center[0] - (panel_center[panel_No][0] - 18)
        LR_offset = panel_center[panel_No][1] - pos_center[1]
    elif target_direction == 180:
        forward_offset = (panel_center[panel_No][1] + 18) - pos_center[1]
        LR_offset = panel_center[panel_No][0] - pos_center[0] 
    elif target_direction == 270:
        forward_offset = (panel_center[panel_No][0] + 18) - pos_center[0]
        LR_offset = pos_center[1] - panel_center[panel_No][1]
    #print(target_direction, forward_offset)
    return forward_offset, LR_offset

def set_direction(cube, angle_offset, LR_offset):
    cube.turn(speed = turn_speed, degree = angle_offset - LR_offset)

def get_panel_type(panel_No):
    return panel_type_list[panel_No] 

def get_move_type(panel_type, target_direction):
    if panel_type == "cross":
        move_type = "straight"
    elif panel_type == "wcurve":
        if target_direction == 0 or target_direction == 180:
            move_type = "turn_left"
        else:
            move_type = "turn_right"

    elif panel_type == "scurve":
        if target_direction == 0:
            move_type = "turn_left"
        elif target_direction == 90:
            move_type = "turn_right"
        else:
            move_type = "clush" 

    elif panel_type == "straight":
        if target_direction == 0:
            move_type = "straight"
        elif target_direction == 180:
            move_type = "straight"
        else:
            move_type = "clush" 

    return move_type
       
def move_cube(cube, move_type, forward_offset):
    motor_param_dict = set_motor_param()
    param = motor_param_dict[move_type]
    if move_type == "straight":
        cube.run_motor(left_speed = param[0] ,right_speed = param[1], duration = param[2] * (panel_size - forward_offset))
    elif move_type == "turn_left":
        cube.run_motor(left_speed = param[0] ,right_speed = param[1], duration = param[3] - (forward_offset * param[4]))
        cube.run_motor(left_speed = param[0] ,right_speed = 0, duration = param[2])
    elif move_type == "turn_right":
        cube.run_motor(left_speed = param[0] ,right_speed = param[1], duration = param[3] - (forward_offset * param[4]))
        cube.run_motor(left_speed = 0 ,right_speed = param[1], duration = param[2])
    elif move_type == "clush":
        cube.run_motor(left_speed = param[0] ,right_speed = param[1], duration = param[2])
        

    else:
        print("move type is none")

signal.signal(signal.SIGINT, ctrl_c_handler)
 
def main():
    global speed
    
    with SimpleCube() as cube:

        wait_mat(cube)
        count_down(cube)

        #set_direction(cube)
    
        while LOOP:
            print("loop")
            # センターポジションを取得
            pos_center = cube.get_current_position()
            #print("pos_center = ", pos_center)
            if pos_center == None:
                print("can not read center position")
                move_cube(cube, "clush", forward_offset)
                cube.sleep(0.5)
                continue
            else:
                pass
            
            # 現在の方位を取得
            direction = cube.get_orientation()
            #print("direction = ", direction)            
            if direction == None:
                print("can not read direction")
                cube.sleep(0.5)
                continue
            else:
                # 現在の方位を180°シフト
                
                direction = direction +180
                # センサーポジションを取得
                pos_sensor = convert_to_sensor_position(pos_center, direction)
                # 現在のパネル番号を取得
                print("pos_sensor = ", pos_sensor, "/ pos_center = ", pos_center, "/ direction = ", direction)
                panel_No = get_panel_No(pos_sensor)
                # パネルタイプを取得
                #print(pos_sensor)
                panel_type = get_panel_type(panel_No)

            # 目的方位を取得
            target_direction, angle_offset = get_target_direction(direction)

            # 理想位置からのオフセット量を取得
            forward_offset, LR_offset = get_offset(pos_center, panel_No, target_direction)

            # 左右位置のオフセット量を勘案して、cube方位を修正
            set_direction(cube, angle_offset, LR_offset)

            # 現在パネルと侵入方向から、移動タイプを決定
            move_type = get_move_type(panel_type, target_direction)

            print   (    "panel = ",              panel_No,
                       "/ panel_type = ",         panel_type, 
                       #"/ pos sensor = ",         pos_sensor,
                       #"/ pos center = ",         pos_center,
                       #"/ panel center = ",       panel_center[panel_No],
                       "/ move_type = ",          move_type,
                       #"/ direction = ",          direction, 
                       "/ target_direction = ",   target_direction, 
                       #"/ angle_offset = ",       angle_offset,
                       "/ forward_offset = ",     forward_offset, 
                       #"/ LR_offset = ",          LR_offset
                    )
            move_cube(cube, move_type, forward_offset)
            #if move_type == "clush":
            #    return
            speed -= 1
            print(speed)
            cube.sleep(0.1)


if __name__ == "__main__":
    sys.exit(main())