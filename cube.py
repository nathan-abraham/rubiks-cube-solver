from itertools import combinations
import numpy as np
from data import move_maps, generate_rotation_matrix
from random import choice

class Piece:
    def __init__(self, type: str, orientation: str, pos: tuple[int]):
        self.type = type
        # top, front, right, back, left, bottom
        self.orientation = orientation
        self.pos = pos

    def move(self, move_type: str):
        rotation_matrix = generate_rotation_matrix(move_type)
        vec = np.array(self.pos)
        self.pos = tuple(np.dot(rotation_matrix, vec))
        move_map = move_maps[move_type]

        new_orientation = [*self.orientation]
        for i, x in enumerate(self.orientation):
            new_orientation[move_map[i]] = x
        self.orientation = "".join(new_orientation)

    def __repr__(self):
        return f"{self.type}, {self.orientation}, {self.pos}"

class Cube:
    colors = ["r", "b", "o", "g", "w", "y"]
    opposites = {
        "r": "o",
        "b": "g",
        "o": "r",
        "g": "b",
        "w": "y",
        "y": "w"
    }
    top_face_locs = [(-1, 1, 1), (0, 1, 1), (1, 1, 1), (-1, 0, 1), (0, 0, 1), (1, 0, 1), (-1, -1, 1), (0, -1, 1), (1, -1, 1)]
    front_face_locs = [(-1, -1, 1), (0, -1, 1), (1, -1, 1), (-1, -1, 0), (0, -1, 0), (1, -1, 0), (-1, -1, -1), (0, -1, -1), (1, -1, -1)]
    right_face_locs = [(1, -1, 1), (1, 0, 1), (1, 1, 1), (1, -1, 0), (1, 0, 0), (1, 1, 0), (1, -1, -1), (1, 0, -1), (1, 1, -1)]
    back_face_locs = [(1, 1, 1), (0, 1, 1), (-1, 1, 1), (1, 1, 0), (0, 1, 0), (-1, 1, 0), (1, 1, -1), (0, 1, -1), (-1, 1, -1)]
    left_face_locs = [(-1, 1, 1), (-1, 0, 1), (-1, -1, 1), (-1, 1, 0), (-1, 0, 0), (-1, -1, 0), (-1, 1, -1), (-1, 0, -1), (-1, -1, -1)]
    bottom_face_locs = [(-1, -1, -1), (0, -1, -1), (1, -1, -1), (-1, 0, -1), (0, 0, -1), (1, 0, -1), (-1, 1, -1), (0, 1, -1), (1, 1, -1)]

    """
    Initialize cube with white on top and red at the front
    Corners number starting at top left of white face and go clockwise
    Edges start at top and go clockwise
    """
    def __init__(self, n: int):
        self.dimension = n
        top_layer = [
            Piece("c", "w00og0", (-1, 1, 1)), Piece("e", "w00o00", (0, 1, 1)), Piece("c", "w0bo00", (1, 1, 1)),
            Piece("e", "w000g0", (-1, 0, 1)), Piece("t", "w00000", (0, 0, 1)), Piece("e", "w0b000", (1, 0, 1)),
            Piece("c", "wr00g0", (-1, -1, 1)), Piece("e", "wr0000", (0, -1, 1)), Piece("c", "wrb000", (1, -1, 1))
        ]
        middle_layer = [
            Piece("e", "000og0", (-1, 1, 0)), Piece("t", "000o00", (0, 1, 0)), Piece("e", "00bo00", (1, 1, 0)),
            Piece("t", "0000g0", (-1, 0, 0)), Piece("x", "w00000", (0, 0, 1)), Piece("t", "00b000", (1, 0, 0)),
            Piece("e", "0r00g0", (-1, -1, 0)), Piece("t", "0r0000", (0, -1, 0)), Piece("e", "0rb000", (1, -1, 0)),
        ]
        bottom_layer = [
            Piece("c", "000ogy", (-1, 1, -1)), Piece("e", "000o0y", (0, 1, -1)), Piece("c", "00bo0y", (1, 1, -1)),
            Piece("e", "0000gy", (-1, 0, -1)), Piece("t", "00000y", (0, 0, -1)), Piece("e", "00b00y", (1, 0, -1)),
            Piece("c", "0r00gy", (-1, -1, -1)), Piece("e", "0r000y", (0, -1, -1)), Piece("c", "0rb00y", (1, -1, -1)),
        ]
        self.pieces = [*top_layer, *middle_layer, *bottom_layer]

    def get_piece(self, target_pos: tuple[int]) -> Piece:
        for piece in self.pieces:
            if piece.pos == target_pos:
                return piece
        return None

    def get(self, target_pos: tuple[int], idx: int) -> str:
        return self.get_piece(target_pos).orientation[idx]

    def _move(self, move_type: str):
        for piece in self.pieces:
            if move_type in ["R", "R'"]:
                if piece.pos[0] == 1:
                    piece.move(move_type)
            elif move_type in ["L", "L'"]:
                if piece.pos[0] == -1:
                    piece.move(move_type)
            elif move_type in ["U", "U'"]:
                if piece.pos[2] == 1:
                    piece.move(move_type)
            elif move_type in ["D", "D'"]:
                if piece.pos[2] == -1:
                    piece.move(move_type)
            elif move_type in ["F", "F'"]:
                if piece.pos[1] == -1:
                    piece.move(move_type)
            elif move_type in ["B", "B'"]:
                if piece.pos[1] == 1:
                    piece.move(move_type)
            else:
                raise Exception("Invalid move type")

    def move(self, move_type: str):
        if move_type[-1] == "2":
            self._move(move_type[:-1])
            self._move(move_type[:-1])
        else:
            self._move(move_type)

    def get_face(self, face: str) -> list[str]:
        if face == "top":
            return [self.get(loc, 0) for loc in self.top_face_locs]
        elif face == "front":
            return [self.get(loc, 1) for loc in self.front_face_locs]
        elif face == "right":
            return [self.get(loc, 2) for loc in self.right_face_locs]
        elif face == "back":
            return [self.get(loc, 3) for loc in self.back_face_locs]
        elif face == "left":
            return [self.get(loc, 4) for loc in self.left_face_locs]
        elif face == "bottom":
            return [self.get(loc, 5) for loc in self.bottom_face_locs]
        else:
            raise Exception("Invalid face")

    def get_layer(self, layer: str) -> list[Piece]:
        if layer == "top":
            return [piece for piece in self.pieces if piece.pos[2] == 1]
        elif layer == "middle":
            return [piece for piece in self.pieces if piece.pos[2] == 0]
        elif layer == "bottom":
            return [piece for piece in self.pieces if piece.pos[2] == -1]

    def check_solved(self) -> bool:
        for face in ["top", "front", "right", "back", "left", "bottom"]:
            colors = self.get_face(face)
            if len(set(colors)) != 1:
                return False
        return True

    def to_string_notation(self) -> str:
        string_notation = ""
        color_map = {
            "w": "U",
            "y": "D",
            "r": "F",
            "o": "B",
            "g": "L",
            "b": "R"
        }
        for face in ["top", "right", "front", "bottom", "left", "back"]:
            colors = self.get_face(face)
            for color in colors:
                string_notation += color_map[color]
        return string_notation

    def scramble(self):
        for _ in range(20):
            move_type = choice(["R", "L", "U", "D", "F", "B"])
            direction = choice(["", "'"])
            self.move(move_type + direction)


    def print_cube(self):
        print("Top Face")
        for i, c in enumerate(self.get_face("top")):
            print(c, end=" ")
            if i % 3 == 2:
                print()

        print("Front Face")
        for i, c in enumerate(self.get_face("front")):
            print(c, end=" ")
            if i % 3 == 2:
                print()

        print("Right Face")
        for i, c in enumerate(self.get_face("right")):
            print(c, end=" ")
            if i % 3 == 2:
                print()
        
        print("Back Face")
        for i, c in enumerate(self.get_face("back")):
            print(c, end=" ")
            if i % 3 == 2:
                print()
        
        print("Left Face")
        for i, c in enumerate(self.get_face("left")):
            print(c, end=" ")
            if i % 3 == 2:
                print()

        print("Bottom Face")
        for i, c in enumerate(self.get_face("bottom")):
            print(c, end=" ")
            if i % 3 == 2:
                print()
        

if __name__ == "__main__":
    c = Cube(3)
    print(c.to_string_notation())

    # do flower pattern
    c.move("R")
    c.move("L'")
    c.move("F")
    c.move("B'")
    c.move("U")
    c.move("D'")
    c.move("R")
    c.move("L'")
 
    c.print_cube()
    print(c.check_solved())

    # reverse flower pattern
    c.move("L")
    c.move("R'")
    c.move("D")
    c.move("U'")
    c.move("B")
    c.move("F'")
    c.move("L")
    c.move("R'")

    c.print_cube()
    print(c.check_solved())

    c.move("R'2")
    c.print_cube()
    print(c.check_solved())