from cube import Cube, Piece
from data import str_sort

c = Cube(3)
correct_pos_map = {str_sort(p.orientation): p.pos for p in c.pieces}
correct_orientation_map = {str_sort(p.orientation): p.orientation for p in c.pieces}

def solve_cube(internal_cube: Cube) -> list[str]:
    return solve_white_cross(internal_cube) + solve_first_layer(internal_cube) + solve_second_layer(internal_cube)

def solve_white_cross(internal_cube: Cube) -> list[str]:
    move_list = []

    while True:
        unsolved_white_edges = [piece for piece in internal_cube.pieces if "w" in piece.orientation and piece.type == "e" and (piece.pos != correct_pos_map[str_sort(piece.orientation)] or piece.orientation != correct_orientation_map[str_sort(piece.orientation)])]
        unsolved_white_edges.sort(key=lambda piece: str_sort(piece.orientation))
        if len(unsolved_white_edges) == 0:
            break

        piece = unsolved_white_edges[0]
        if piece.pos[2] == -1:
            piece = unsolved_white_edges[0]
            # twist the bottom layer until the white piece is directly below where it needs to go on the top layer
            other_color = [color for color in piece.orientation if color != "w" and color != "0"][0]
            while other_color not in internal_cube.get_piece((piece.pos[0], piece.pos[1], 0)).orientation:
                move_list.append("D")
                internal_cube.move("D")

            # move it to the top layer
            front_center_piece = internal_cube.get_piece((piece.pos[0], piece.pos[1], 0))
            front_face_color = [color for color in front_center_piece.orientation if color != "0"][0]

            # if white is on the bottom of the piece
            if piece.orientation[5] == "w":
                converted_algorithm = convert_algorithm("F F", front_face_color, "w")
            else:
                converted_algorithm = convert_algorithm("D R F' R'", front_face_color, "w")
            move_list.extend(converted_algorithm)
            for move in converted_algorithm:
                internal_cube.move(move)
        elif piece.pos[2] == 0:
            # move it to the bottom layer
            if piece.pos[0] == 1 and piece.pos[1] == 1:
                algorithm = "B' D' B"
            elif piece.pos[0] == 1 and piece.pos[1] == -1:
                algorithm = "R' D' R"
            elif piece.pos[0] == -1 and piece.pos[1] == -1:
                algorithm = "L D L'"
            else:
                algorithm = "B D B'"
            move_list.extend(algorithm.split(" "))
            for move in algorithm.split(" "):
                internal_cube.move(move)
            
        elif piece.pos[2] == 1:
            # move it to the bottom layer
            if piece.pos[0] == 1 and piece.pos[1] == 0:
                algorithm = "R R"
            elif piece.pos[0] == 0 and piece.pos[1] == -1:
                algorithm = "F F"
            elif piece.pos[0] == -1 and piece.pos[1] == 0:
                algorithm = "L L"
            else:
                algorithm = "B B"
            move_list.extend(algorithm.split(" "))
            for move in algorithm.split(" "):
                internal_cube.move(move)
            
    return move_list

def solve_first_layer(internal_cube: Cube) -> list[str]:
    move_list = []

    while True:
        unsolved_white_corners = [piece for piece in internal_cube.pieces if "w" in piece.orientation and piece.type == "c" and (piece.pos != correct_pos_map[str_sort(piece.orientation)] or piece.orientation != correct_orientation_map[str_sort(piece.orientation)])]
        unsolved_white_corners.sort(key=lambda piece: str_sort(piece.orientation))
        if len(unsolved_white_corners) == 0:
            break
        piece = unsolved_white_corners[0]
        if piece.pos[2] == -1:
            if piece.orientation[5] != "w":
                # twist the bottom layer until the white piece is directly below where it needs to go on the top layer
                correct_pos = correct_pos_map[str_sort(piece.orientation)]
                while piece.pos[0] != correct_pos[0] or piece.pos[1] != correct_pos[1]:
                    move_list.append("D")
                    internal_cube.move("D")

                first_center_piece = internal_cube.get_piece((piece.pos[0], 0, 0))
                second_center_piece = internal_cube.get_piece((0, piece.pos[1], 0))

                first_outward_dir = [i for i in range(6) if first_center_piece.orientation[i] != "0"][0]
                second_outward_dir = [i for i in range(6) if second_center_piece.orientation[i] != "0"][0]
                first_color = first_center_piece.orientation[first_outward_dir]
                second_color = second_center_piece.orientation[second_outward_dir]
                if piece.orientation[first_outward_dir] == first_color:
                    if is_right_of(first_center_piece, second_center_piece):
                        converted_algorithm = convert_algorithm("L D L'", first_color, "w")
                    else:
                        converted_algorithm = convert_algorithm("R' D' R", first_color, "w")
                else:
                    if is_right_of(first_center_piece, second_center_piece):
                        converted_algorithm = convert_algorithm("R' D' R", second_color, "w")
                    else:
                        converted_algorithm = convert_algorithm("L D L'", second_color, "w")
                for move in converted_algorithm:
                    internal_cube.move(move)
                move_list.extend(converted_algorithm)
            else:
                # twist the bottom layer until the white piece is directly below where it needs to go on the top layer
                correct_pos = correct_pos_map[str_sort(piece.orientation)]
                while piece.pos[0] != correct_pos[0] or piece.pos[1] != correct_pos[1]:
                    move_list.append("D")
                    internal_cube.move("D")

                first_center_piece = internal_cube.get_piece((piece.pos[0], 0, 0))
                second_center_piece = internal_cube.get_piece((0, piece.pos[1], 0))

                first_outward_dir = [i for i in range(6) if first_center_piece.orientation[i] != "0"][0]
                second_outward_dir = [i for i in range(6) if second_center_piece.orientation[i] != "0"][0]
                first_color = first_center_piece.orientation[first_outward_dir]
                second_color = second_center_piece.orientation[second_outward_dir]

                if is_right_of(first_center_piece, second_center_piece):
                    converted_algorithm = convert_algorithm("R' D R", second_color, "w")
                else:
                    converted_algorithm = convert_algorithm("R' D R", first_color, "w")
                for move in converted_algorithm:
                    internal_cube.move(move)
                move_list.extend(converted_algorithm)
        else:
            first_center_piece = internal_cube.get_piece((piece.pos[0], 0, 0))
            second_center_piece = internal_cube.get_piece((0, piece.pos[1], 0))

            first_outward_dir = [i for i in range(6) if first_center_piece.orientation[i] != "0"][0]
            second_outward_dir = [i for i in range(6) if second_center_piece.orientation[i] != "0"][0]
            first_color = first_center_piece.orientation[first_outward_dir]
            second_color = second_center_piece.orientation[second_outward_dir]

            if is_right_of(first_center_piece, second_center_piece):
                converted_algorithm = convert_algorithm("R' D R", second_color, "w")
            else:
                converted_algorithm = convert_algorithm("R' D R", first_color, "w")
            for move in converted_algorithm:
                internal_cube.move(move)
            move_list.extend(converted_algorithm)

    return move_list

def solve_second_layer(internal_cube: Cube) -> list[str]:
    move_list = []

    while True:
        target_edges = [piece for piece in internal_cube.pieces if (piece.pos[2] == 0 or piece.pos[2] == -1) and piece.type == "e" and "y" not in piece.orientation and (piece.pos != correct_pos_map[str_sort(piece.orientation)] or piece.orientation != correct_orientation_map[str_sort(piece.orientation)])]
        target_edges.sort(key=lambda piece: str_sort(piece.orientation))
        if len(target_edges) == 0:
            break
        piece = target_edges[0]

        if piece.pos[2] == -1:
            # get the color that is not facing down
            other_color = [color for i, color in enumerate(piece.orientation) if color != "0" and i != 5][0]
            # twist the bottom layer until the center piece with the other color is directly below the edge piece
            while other_color not in internal_cube.get_piece((piece.pos[0], piece.pos[1], 0)).orientation:
                move_list.append("D")
                internal_cube.move("D")
            
            # get the current center piece
            current_center_piece = internal_cube.get_piece((piece.pos[0], piece.pos[1], 0))
            current_color = [color for color in current_center_piece.orientation if color != "0"][0]

            # get the center piece on both the faces left and right of the current face
            first_center_piece = internal_cube.get_piece((*rotate_ccw(piece.pos[:2]), 0))
            second_center_piece = internal_cube.get_piece((*rotate_cw(piece.pos[:2]), 0))
            first_color = [color for color in first_center_piece.orientation if color != "0"][0]
            second_color = [color for color in second_center_piece.orientation if color != "0"][0]

            converted_algorithm = None
            if piece.orientation[5] == first_color:
                if is_right_of(first_center_piece, current_center_piece):
                    converted_algorithm = convert_algorithm("U' L' U L U F U' F'", current_color, "y")
                else:
                    converted_algorithm = convert_algorithm("U R U' R' U' F' U F", current_color, "y")
            elif piece.orientation[5] == second_color:
                if is_right_of(second_center_piece, current_center_piece):
                    converted_algorithm = convert_algorithm("U' L' U L U F U' F'", current_color, "y")
                else:
                    converted_algorithm = convert_algorithm("U R U' R' U' F' U F", current_color, "y")
            for move in converted_algorithm:
                internal_cube.move(move)
            move_list.extend(converted_algorithm)
        else:
            first_center_piece = internal_cube.get_piece((piece.pos[0], 0, 0))
            second_center_piece = internal_cube.get_piece((0, piece.pos[1], 0))
            first_color = [color for color in first_center_piece.orientation if color != "0"][0]
            second_color = [color for color in second_center_piece.orientation if color != "0"][0]
            if is_right_of(first_center_piece, second_center_piece):
                converted_algorithm = convert_algorithm("U R U' R' U' F' U F", first_color, "y")
            else:
                converted_algorithm = convert_algorithm("U' L' U L U F U' F'", first_color, "y")
            for move in converted_algorithm:
                internal_cube.move(move)
            move_list.extend(converted_algorithm)

    return move_list

def rotate_ccw(vec: tuple[int, int]) -> tuple[int, int]:
    return (-vec[1], vec[0])

def rotate_cw(vec: tuple[int, int]) -> tuple[int, int]:
    return (vec[1], -vec[0])

def is_right_of(piece1: Piece, piece2: Piece) -> bool:
    # is piece1 to the right of piece2 (counter-clockwise)
    # if we can rotate piece2 x and y coordinates 90 degrees counter-clockwise and get piece1, then piece1 is to the right of piece2
    if rotate_ccw((piece2.pos[0], piece2.pos[1])) == (piece1.pos[0], piece1.pos[1]):
        return True

def convert_algorithm(algorithm: str, front_face_color: str, top_face_color: str) -> list[str]:
    move_map = None

    # if red is front and white is top, then the algorithm is already in the correct orientation
    if front_face_color == "r" and top_face_color == "w":
        return algorithm.split(" ")
    # if blue is front and white is top, then the algorithm needs to be rotated 90 degrees counter-clockwise about the z axis
    elif front_face_color == "b" and top_face_color == "w":
        move_map = fill_move_map({
            "F": "R",
            "R": "B",
            "B": "L",
            "L": "F",
            "U": "U",
            "D": "D"
        })
    # if orange is front and white is top, then the algorithm needs to be rotated 180 degrees about the z axis
    elif front_face_color == "o" and top_face_color == "w":
        move_map = fill_move_map({
            "F": "B",
            "R": "L",
            "B": "F",
            "L": "R",
            "U": "U",
            "D": "D"
        })
    # if green is front and white is top, then the algorithm needs to be rotated 90 degrees clockwise about the z axis
    elif front_face_color == "g" and top_face_color == "w":
        move_map = fill_move_map({
            "F": "L",
            "R": "F",
            "B": "R",
            "L": "B",
            "U": "U",
            "D": "D"
        })
    # conditions for yellow being the top face
    elif front_face_color == "r" and top_face_color == "y":
        move_map = fill_move_map({
            "F": "F",
            "R": "L",
            "B": "B",
            "L": "R",
            "U": "D",
            "D": "U"
        })
    elif front_face_color == "b" and top_face_color == "y":
        move_map = fill_move_map({
            "F": "R",
            "R": "F",
            "B": "L",
            "L": "B",
            "U": "D",
            "D": "U"
        })
    elif front_face_color == "o" and top_face_color == "y":
        move_map = fill_move_map({
            "F": "B",
            "R": "R",
            "B": "F",
            "L": "L",
            "U": "D",
            "D": "U"
        })
    elif front_face_color == "g" and top_face_color == "y":
        move_map = fill_move_map({
            "F": "L",
            "R": "B",
            "B": "R",
            "L": "F",
            "U": "D",
            "D": "U"
        })
    if move_map:
        return [move_map[move] for move in algorithm.split(" ")]
    else:
        raise Exception("Invalid front and top face colors")

def fill_move_map(move_map: dict[str, str]) -> dict[str, str]:
    # for each move in the move map, fill in the inverse move
    new_move_map = move_map.copy()
    for move in move_map:
        new_move_map[move + "'"] = move_map[move] + "'"
    return new_move_map

if __name__ == "__main__":
    c = Cube(3)
    c.scramble() 

    moves = solve_cube(c)
    # red center should be right of green center
    print(is_right_of(c.get_piece((0,-1,0)), c.get_piece((-1,0,0))))