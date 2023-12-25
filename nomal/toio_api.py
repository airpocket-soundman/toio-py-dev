import asyncio
from toio.cube import ToioCoreCube
from toio.cube.api.base_class import CubeCharacteristic


cube = ToioCoreCube(None)
for key, value in vars(cube.api).items():
    if isinstance(value, CubeCharacteristic):
        print(f"{key:20s}: <interface class>")
    else:
        print(f"{key:20s}: {value}")

