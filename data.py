from math import sin, cos, radians
import numpy as np

# 0 represents top of cube, 1 represents front of the cube, 2 represents right,
# 3 represents back, 4 represents left, 5 represents bottom

# R is a clockwise rotation of the right face, L is a clockwise rotation of the left face,
# U is a clockwise rotation of the top face, D is a clockwise rotation of the bottom face,
# F is a clockwise rotation of the front face, B is a clockwise rotation of the back face
# X' is a counter-clockwise rotation of face X

move_maps = {
    "R": {
        0: 3,
        1: 0,
        2: 2,
        3: 5,
        4: 4,
        5: 1
    },
    "R'": {
        0: 1,
        1: 5,
        2: 2,
        3: 0,
        4: 4,
        5: 3
    },
    "L": {
        0: 1,
        1: 5,
        2: 2,
        3: 0,
        4: 4,
        5: 3
    }, 
    "L'": {
        0: 3,
        1: 0,
        2: 2,
        3: 5,
        4: 4,
        5: 1
    },
    "U": {
        0: 0,
        1: 4,
        2: 1,
        3: 2,
        4: 3,
        5: 5
    },
    "U'": {
        0: 0,
        1: 2,
        2: 3,
        3: 4,
        4: 1,
        5: 5
    },
    "D": {
        0: 0,
        1: 2,
        2: 3,
        3: 4,
        4: 1,
        5: 5
    },
    "D'": {
        0: 0,
        1: 4,
        2: 1,
        3: 2,
        4: 3,
        5: 5
    },
    "F": {
        0: 2,
        1: 1,
        2: 5,
        3: 3,
        4: 0,
        5: 4
    },
    "F'": {
        0: 4,
        1: 1,
        2: 0,
        3: 3,
        4: 5,
        5: 2
    },
    "B": {
        0: 4,
        1: 1,
        2: 0,
        3: 3,
        4: 5,
        5: 2
    },
    "B'": {
        0: 2,
        1: 1,
        2: 5,
        3: 3,
        4: 0,
        5: 4
    }
}

def generate_rotation_matrix(move_type: str):
    move_to_angle_axis = {
        "R": (-90, "x"),
        "R'": (90, "x"),
        "L": (90, "x"),
        "L'": (-90, "x"),
        "U": (-90, "z"),
        "U'": (90, "z"),
        "D": (90, "z"),
        "D'": (-90, "z"),
        "F": (90, "y"),
        "F'": (-90, "y"),
        "B": (-90, "y"),
        "B'": (90, "y")
    }

    if move_type not in move_to_angle_axis:
        raise ValueError("Invalid move type")
    angle_axis = move_to_angle_axis[move_type]
    angle = radians(angle_axis[0])
    axis = angle_axis[1]

    cos_angle = int(cos(angle))
    sin_angle = int(sin(angle))

    if axis == "x":
        return np.array([[1, 0, 0], [0, cos_angle, -sin_angle], [0, sin_angle, cos_angle]])
    elif axis == "y":
        return np.array([[cos_angle, 0, sin_angle], [0, 1, 0], [-sin_angle, 0, cos_angle]])
    elif axis == "z":
        return np.array([[cos_angle, -sin_angle, 0], [sin_angle, cos_angle, 0], [0, 0, 1]])

def str_sort(s: str) -> str:
    return "".join(sorted(s))

# create a map of a piece's orientation to its correct position
# the key is the piece's orientation, and the value is the piece's correct position

correct_pos_map = {
    str_sort("w00og0"): (-1, 1, 1),
    str_sort("w00o00"): (0, 1, 1),
    str_sort("w00ob0"): (1, 1, 1),
    str_sort("w000g0"): (-1, 0, 1),
    str_sort("w00000"): (0, 0, 1),
    str_sort("w0b000"): (1, 0, 1),
    str_sort("wr00g0"): (-1, -1, 1),
    str_sort("wr0000"): (0, -1, 1),
    str_sort("wrb000"): (1, -1, 1),
}

correct_orientation_map = {
    str_sort("w00og0"): "w00og0",
    str_sort("w00o00"): "w00o00",
    str_sort("w00ob0"): "w00ob0",
    str_sort("w000g0"): "w000g0",
    str_sort("w00000"): "w00000",
    str_sort("w0b000"): "w0b000",
    str_sort("wr00g0"): "wr00g0",
    str_sort("wr0000"): "wr0000",
    str_sort("wrb000"): "wrb000",
}
