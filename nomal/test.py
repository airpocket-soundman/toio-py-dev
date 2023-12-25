import asyncio
from toio import *

async def cube_functions():
    dev_list = await BLEScanner.scan(num=10, sort="rssi", timeout = 5)
    print("dev_list = ", dev_list)
    
    try:
        assert len(dev_list)
        cube = ToioCoreCube(dev_list[0].interface)
        await cube.connect()
        await cube.disconnect()
        print("dev_list[0] = ", dev_list[0].interface)
        for n, ble_dev in enumerate(dev_list):
            print(f"\ncube:{n}")
            print(ble_dev)

    except AssertionError:
        print("no toio!")
        pass

    

asyncio.run(cube_functions())