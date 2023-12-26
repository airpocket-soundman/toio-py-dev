import asyncio
import signal
from toio.scanner import BLEScanner
from toio.cube import ToioCoreCube, IdInformation

LOOP = True

def ctrl_c_handler(_signum, _frame):
    global LOOP
    print("Ctrl_C")
    LOOP = False

signal.signal(signal.SIGINT, ctrl_c_handler)

async def cube_functions():


    device_list = await BLEScanner.scan(1)
    assert len(device_list)
    cube = ToioCoreCube(device_list[0].interface)
    print("dev_list[0] = ", device_list[0].device)
    await cube.connect()    
    print("start")


    while LOOP:
        read_data = await cube.api.id_information.read()
        if read_data is not None:
            if str(read_data) == "Position ID missed":
                read_data = str(read_data)
                #print("lost position")
            else:
                #print("data ari")
                read_data = str(read_data.sensor).split(",")
                read_data[0] = int(read_data[0][27:])
                read_data[1] = read_data[1][3:]
                read_data[1] = int(read_data[1][:-1])
                read_data[2] = read_data[2][7:]
                read_data[2] = int(read_data[2][:-1])
        print(read_data)
        await asyncio.sleep(0.5)

    print("end")
    await cube.disconnect()

asyncio.run(cube_functions())