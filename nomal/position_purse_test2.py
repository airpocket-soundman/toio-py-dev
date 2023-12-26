import asyncio
import signal
from toio import *

panel_size = 29
turn_speed = 10
move_speed = 10
count_timer = 0.5
target_direction = 0
distance = 0
bias = 0


motor_param_dict = {"first_move"   : [ 10, 10, 1.5],
                    "straight"     : [ -8, -8, 1.8],
                    "turn_right"   : [  0, -8, 1.8, -8, -8, 0.4],
                    "turn_left"    : [ -8,  0, 1.8, -8, -8, 0.4]}

LOOP = True

panels        = [[ 276, 304, 143, 171],[ 309, 336, 143, 171],[ 340, 368, 143, 171],[ 374, 401, 143, 171],
                 [ 276, 304, 185, 213],[ 309, 336, 185, 213],[ 340, 368, 185, 213],[ 374, 401, 185, 213],
                 [ 276, 304, 229, 257],[ 309, 336, 229, 257],[ 340, 368, 229, 257],[ 374, 401, 229, 257],
                 [ 276, 304, 272, 300],[ 309, 336, 272, 300],[ 340, 368, 272, 300],[ 374, 401, 272, 300]]

panel_center = [[  11,  43],[  41,  43],[  70,  43],[  99,  43],
                [  11,  14],[  41,  14],[  70,  14],[  99,  14],
                [  11, -14],[  40, -14],[ -73, -14],[-102, -14],
                [  11, -43],[  40, -43],[ -73, -43],[   0,   0]]

panel_type = ["cross",  "cross",  "cross",   "cross",
              "wcurve", "wcurve", "wcurve",  "wcurve",
              "wcurve", "wcurve", "scurve",  "scurve",
              "scurve", "scurve", "straight","straight"]

def ctrl_c_handler(_signum, _frame):
    global LOOP
    print("Ctrl-C")
    LOOP = False

signal.signal(signal.SIGINT, ctrl_c_handler)

def check_panel_No(pos):
    for index, panel in enumerate(panels):
        if panel[0] <= pos[0] and pos[0] <= panel[1]:
            if panel[2] <= pos[1] and pos[1] <= panel[3]:
                return index

async def cube_connect():
    device_list = await BLEScanner.scan(1)
    assert len(device_list) > 0
    cube = ToioCoreCube(device_list[0].interface)
    await cube.connect()
    return cube

async def cube_disconnect(cube):
    await cube.disconnect()
    await asyncio.sleep(2)

async def get_position(cube):
    #global read_data
    read_data = await cube.api.id_information.read()
    if read_data is not None:
        if str(read_data) == "Position ID missed":
            read_data = None
        else:
            read_data = str(read_data.sensor).split(",")
            read_data[0] = int(read_data[0][27:])
            read_data[1] = read_data[1][3:]
            read_data[1] = int(read_data[1][:-1])
            read_data[2] = read_data[2][7:]
            read_data[2] = int(read_data[2][:-1])

    return read_data

async def set_direction(cube, pos):
    global target_direction
    target_angle = [0, 90, 180, 270]
    direction = pos[2]
    print("before = ", pos[2])
    if direction > 315 :
        direction = direction - 360
    
    for angle in target_angle:
        if direction > angle - 45 and direction <= angle + 45:
            turn_angle = angle - direction
            
            print("turn angle = ", angle - direction)
            """
            if turn_angle > 0:
                x_speed =  20
                y_speed = -20
            else:
                x_speed = -20
                y_speed =  20

            await cube.api.motor.motor_control(x_speed, y_speed)
            await asyncio.sleep(turn_angle/20)
            await cube.api.motor.motor_control(0, 0)
            """

            target_direction = angle
    pos = await get_position(cube)
    return pos




async def move_cube(cube, mode):
    param = motor_param_dict[mode]
    await cube.api.motor.motor_control(param[0],param[1])
    await asyncio.sleep(param[2])
    await cube.api.motor.motor_control(0, 0)


async def main():
    cube = await cube_connect()
    while LOOP:
 
        pos = await get_position(cube)
        if pos == None:
            print("None")
            continue
       
        panel = check_panel_No(pos)
        print("panel = ", panel, " / position = ", pos)

        pos = await set_direction(cube, pos)
        if pos == None:
            print("after = None")
            continue
        print("after = ", pos[2])
        print("panel = ", panel, " / position = ", pos, "target dirction = ", target_direction)
        
        
    await cube_disconnect(cube)
    print("cube disconnected.")

asyncio.run(main())