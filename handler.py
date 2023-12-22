import asyncio

from toio.scanner import BLEScanner
from toio.cube import ToioCoreCube, IdInformation, ButtonInformation

async def cube_functions():
    def notification_handler(payload: bytearray):
        id_info = ButtonInformation(payload)
        print(str(id_info))

    dev_list = await BLEScanner.scan(1)
    assert len(dev_list)
    cube = ToioCoreCube(dev_list[0].interface)
    await cube.connect()
    print("start")
    await cube.api.button.register_notification_handler(notification_handler)
    await asyncio.sleep(10)
    await cube.api.button.unregister_notification_handler(
        notification_handler
    )
    print("end")
    await cube.disconnect()

asyncio.run(cube_functions())