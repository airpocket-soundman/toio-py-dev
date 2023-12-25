import asyncio

from toio.scanner import BLEScanner
from toio.cube import ToioCoreCube

async def cube_functions():
    dev_list = await BLEScanner.scan(num=1)
    if len(dev_list) > 0:
        cube = ToioCoreCube(dev_list[0].interface)
        await cube.connect()
        print("Connected")
        print("sleep1")
        await asyncio.sleep(2)
        print("sleep2")
        await asyncio.sleep(2)
        print("sleep2 finished")
        await cube.disconnect()
        print("Disconnected")
    else:
        print("No cubes found")

asyncio.run(cube_functions())