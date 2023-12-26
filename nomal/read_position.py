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
                print("lost position")
            else:
                print(read_data)



                
    print("end")
    await cube.disconnect()

asyncio.run(cube_functions())