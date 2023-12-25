import sys

from toio.simple import SimpleCube


def test():
    start_pos_x =30
    start_pos_y =30
    start_degree = 0
    targets = ((30, -30, -90), (90, -30, -90), (90, 30, -90), (30, 30, -90))

    with SimpleCube() as cube:
        cube.move_to(speed=30, x = start_pos_x, y = start_pos_y)
        cube.set_orientation(speed = 30, degree = start_degree)
        for target in targets:
            target_pos_x, target_pos_y , rotate = target
            print(f"move to ({target_pos_x}, {target_pos_y})")
            success = cube.move_to(speed=30, x=target_pos_x, y=target_pos_y)
            print(f"arrival: {success}")
            cube.turn(speed = 20, degree = rotate)
            if not success:
                print("Position ID missed")
                break
            cube.sleep(0.5)


if __name__ == "__main__":
    sys.exit(test())