import asyncio
from toio.scanner import BLEScanner
from toio.cube import ToioCoreCube

async def cube_functions():
    device_list = await BLEScanner.scan(1)
    assert len(device_list)
    cube = ToioCoreCube(device_list[0].interface)
    print("dev_list[0] = ", device_list[0].device)
    await cube.connect()
    print("start")
    for n in range(20):

        print(f"\n ---{str(n):5s}---")
        read_data = await cube.api.battery.read()        
        if read_data is not None:
            print("battery  : ", read_data)

        read_data = await cube.api.button.read()
        if read_data is not None:
            print("button   : ", read_data)

        read_data = await cube.api.id_information.read()
        if read_data is not None:
            print("id info  : ", read_data)
        else:
            print("id info  : no id information.")

        read_data = await cube.api.sensor.read()
        if read_data is not None:
            print("sensor   : ", read_data)

    print("end")
    await cube.disconnect()

asyncio.run(cube_functions())