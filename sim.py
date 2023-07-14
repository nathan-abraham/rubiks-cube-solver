from ursina import *
from cube import Cube
from solver import solve_cube

class Simulation(Ursina):
    cube_colors = [
        color.blue,  # right
        color.green,  # left
        color.white,  # top
        color.yellow,  # bottom
        color.orange,  # back
        color.red,  # front
    ]

    faces = ("R", "L", "U", "D", "F", "B")
    faces_to_normal = {
        "R": Vec3(1,0,0),
        "L": Vec3(-1,0,0),
        "U": Vec3(0,1,0),
        "D": Vec3(0,-1,0),
        "F": Vec3(0,0,-1),
        "B": Vec3(0,0,1),
    }


    def __init__(self):
        super().__init__()
        self.internal_cube = Cube(3)
        self.controller = Entity(model='cube', scale=3, collider='box', visible=False)
        self.reverse_dir = False

        self.controller.input = self.controller_input
        self.rotation_helper = Entity()
        self.win_text_entity = Text(y=.35, text='', color=color.green, origin=(0,0), scale=3)

        self.generate_cube()

        self.randomize_button = Button(text='randomize', color=color.azure, position=(.7,-.1), on_click=self.randomize)
        self.randomize_button.fit_to_text()

        self.solve_beginners_button = Button(text='solve (beginner\'s)', color=color.azure, position=(.7,-.2), on_click=self.solve_beginners)
        self.solve_beginners_button.fit_to_text()

        self.solve_button = Button(text='solve (kociemba)', color=color.azure, position=(.7,-.3), on_click=self.solve)
        self.solve_button.fit_to_text()

        self.reset_button = Button(text='reset', color=color.azure, position=(.7,-.4), on_click=self.reset)
        self.reset_button.fit_to_text()

        window.color = color._16
        EditorCamera()

    def generate_cube(self):
        # make a model with a separate color on each face
        self.combine_parent = Entity(enabled=False)
        for i in range(3):
            dir = Vec3(0, 0, 0)
            dir[i] = 1

            e = Entity(parent=self.combine_parent, model='plane', origin_y=-.5, texture='white_cube', color=self.cube_colors[i*2])
            e.look_at(dir, 'up')

            e_flipped = Entity(parent=self.combine_parent, model='plane', origin_y=-.5, texture='white_cube', color=self.cube_colors[(i*2)+1])
            e_flipped.look_at(-dir, 'up')

        self.combine_parent.combine()

        # place 3x3x3 cubes
        self.cubes = []
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    e = Entity(model=copy(self.combine_parent.model), position=Vec3(x,y,z) - (Vec3(3,3,3)/3), texture='white_cube')
                    self.cubes.append(e)

    def controller_input(self, key):
        if held_keys["shift"]:
            self.reverse_dir = True
        else:
            self.reverse_dir = False

        dir = -1 if self.reverse_dir else 1
        modifier = "'" if self.reverse_dir else ""

        if key == 'r':
            self.rotate_side(Vec3(1,0,0), dir)
            self.internal_cube.move("R" + modifier)
        elif key == 'u':
            self.rotate_side(Vec3(0,1,0), dir)
            self.internal_cube.move("U" + modifier)
        elif key == 'b':
            self.rotate_side(Vec3(0,0,1), dir)
            self.internal_cube.move("B" + modifier)
        elif key == 'l':
            self.rotate_side(Vec3(-1,0,0), dir)
            self.internal_cube.move("L" + modifier)
        elif key == 'd':
            self.rotate_side(Vec3(0,-1,0), dir)
            self.internal_cube.move("D" + modifier)
        elif key == 'f':
            self.rotate_side(Vec3(0,0,-1), dir)
            self.internal_cube.move("F" + modifier)


    def rotate_side(self, normal, direction=1, speed=1):
        if normal == Vec3(1,0,0):
            [setattr(e, 'world_parent', self.rotation_helper) for e in self.cubes if e.x > 0]
            self.rotation_helper.animate('rotation_x', 90 * direction, duration=.2*speed, curve=curve.linear)
        elif normal == Vec3(-1,0,0):
            [setattr(e, 'world_parent', self.rotation_helper) for e in self.cubes if e.x < 0]
            self.rotation_helper.animate('rotation_x', -90 * direction, duration=.2*speed, curve=curve.linear)

        elif normal == Vec3(0,1,0):
            [setattr(e, 'world_parent', self.rotation_helper) for e in self.cubes if e.y > 0]
            self.rotation_helper.animate('rotation_y', 90 * direction, duration=.2*speed, curve=curve.linear)
        elif normal == Vec3(0,-1,0):
            [setattr(e, 'world_parent', self.rotation_helper) for e in self.cubes if e.y < 0]
            self.rotation_helper.animate('rotation_y', -90 * direction, duration=.2*speed, curve=curve.linear)

        elif normal == Vec3(0,0,1):
            [setattr(e, 'world_parent', self.rotation_helper) for e in self.cubes if e.z > 0]
            self.rotation_helper.animate('rotation_z', -90 * direction, duration=.2*speed, curve=curve.linear)
        elif normal == Vec3(0,0,-1):
            [setattr(e, 'world_parent', self.rotation_helper) for e in self.cubes if e.z < 0]
            self.rotation_helper.animate('rotation_z', 90 * direction, duration=.2*speed, curve=curve.linear)


        invoke(self.reset_rotation_helper, delay=.3*speed)

        if speed:
            self.controller.ignore_input = True
            invoke(setattr, self.controller, 'ignore_input', False, delay=.24*speed)

    def reset_rotation_helper(self):
        [setattr(e, 'world_parent', scene) for e in self.cubes]
        self.rotation_helper.rotation = (0,0,0)


    def check_for_win(self):
        if self.internal_cube.check_solved():
            print("SOLVED")
            self.win_text_entity.text = 'SOLVED!'
            self.win_text_entity.appear()
        else:
            self.win_text_entity.text = ''

    def randomize(self):
        for _ in range(40):
            face = random.choice(self.faces)
            dir = random.choice((-1,1))
            self.rotate_side(normal=self.faces_to_normal[face], direction=dir, speed=0)
            self.internal_cube.move(face + ("'" if dir == -1 else ""))

    def reset(self):
        for e in self.cubes:
            destroy(e)
        self.cubes.clear()

        for x in range(3):
            for y in range(3):
                for z in range(3):
                    e = Entity(model=copy(self.combine_parent.model), position=Vec3(x,y,z) - (Vec3(3,3,3)/3), texture='white_cube')
                    self.cubes.append(e)

        for e in self.cubes:
            e.rotation = (0,0,0)

        self.internal_cube = Cube(3)
        self.win_text_entity.text = ''
        self.reset_rotation_helper()

    def perform_move(self, move: str, move_speed: int, change_internal_cube: bool = True):
        # print("move:", move)
        if move[-1] == "'":
            self.rotate_side(self.faces_to_normal[move[:-1]], -1, speed=move_speed)
        else:
            self.rotate_side(self.faces_to_normal[move], 1, speed=move_speed)
        if change_internal_cube:
            self.internal_cube.move(move)

    def perform_moves(self, move_list: list[str], index: int, move_speed: int, change_internal_cube: bool = True):
        if index >= len(move_list):
            invoke(self.check_for_win, delay=.25*move_speed)
            return

        move = move_list[index]
        self.perform_move(move, move_speed, change_internal_cube=change_internal_cube)

        invoke(self.perform_moves, move_list, index+1, move_speed, change_internal_cube=False, delay=.5*move_speed)

    def solve(self):
        import kociemba
        moves = kociemba.solve(self.internal_cube.to_string_notation()).split(" ")
        # break up moves with a 2 at the end into two moves
        move_list = []
        for move in moves:
            if move[-1] == "2":
                move_list.append(move[:-1])
                move_list.append(move[:-1])
            else:
                move_list.append(move)

        self.perform_moves(move_list, 0, 0, change_internal_cube=True)

    def solve_beginners(self):
        moves = solve_cube(self.internal_cube)
        # break up moves with a 2 at the end into two moves
        move_list = []
        for move in moves:
            if move[-1] == "2":
                move_list.append(move[:-1])
                move_list.append(move[:-1])
            else:
                move_list.append(move)

        self.perform_moves(move_list, 0, 0, change_internal_cube=False)

if __name__ == "__main__":
    app = Simulation()
    app.run()
