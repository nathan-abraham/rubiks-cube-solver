from cube import Cube, Piece
from data import str_sort

c = Cube(3)
correct_pos_map = {str_sort(p.orientation): p.pos for p in c.pieces}
correct_orientation_map = {str_sort(p.orientation): p.orientation for p in c.pieces}

def solve_cube(internal_cube: Cube) -> list[str]:
    raw_algorithm = solve_white_cross(internal_cube) + solve_first_layer(internal_cube) + solve_second_layer(internal_cube) + solve_yellow_cross(internal_cube) + solve_yellow_edges(internal_cube) + solve_yellow_corner_position(internal_cube) + solve_yellow_corner_orientation(internal_cube)
    return optimize_algorithm(raw_algorithm)

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

    # assert that the white cross is solved
    if not all([piece.pos == correct_pos_map[str_sort(piece.orientation)] and piece.orientation == correct_orientation_map[str_sort(piece.orientation)] for piece in internal_cube.pieces if "w" in piece.orientation and piece.type == "e"]):
        raise Exception("White cross not solved")
            
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

    # assert that the first layer is solved
    if not all([piece.pos == correct_pos_map[str_sort(piece.orientation)] and piece.orientation == correct_orientation_map[str_sort(piece.orientation)] for piece in internal_cube.pieces if "w" in piece.orientation]):
        raise Exception("First layer is not solved")

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

    # assert that the second layer is solved
    if not all([piece.pos == correct_pos_map[str_sort(piece.orientation)] and piece.orientation == correct_orientation_map[str_sort(piece.orientation)] for piece in internal_cube.pieces if "y" not in piece.orientation]):
        raise Exception("Second layer is not solved")

    return move_list

def solve_yellow_cross(internal_cube: Cube) -> list[str]:
    move_list = []
    algorithm = None
    
    # get all yellow edges
    top_edge = internal_cube.get_piece((0, 1, -1))
    right_edge = internal_cube.get_piece((-1, 0, -1))
    bottom_edge = internal_cube.get_piece((0, -1, -1))
    left_edge = internal_cube.get_piece((1, 0, -1))
    # get number of yellow edges facing down
    num_facing_down = sum([1 for edge in [top_edge, right_edge, bottom_edge, left_edge] if edge.orientation[5] == "y"])

    # yellow dot on top
    if num_facing_down == 0:
        algorithm = "F R U R' U' R U R' U' F' U' F R U R' U' F'"
    # yellow line or L on top
    elif num_facing_down == 2:
        # line cases
        if top_edge.orientation[5] == "y" and bottom_edge.orientation[5] == "y":
            algorithm = "U F R U R' U' F'"
        elif left_edge.orientation[5] == "y" and right_edge.orientation[5] == "y":
            algorithm = "F R U R' U' F'"
        # L cases
        elif top_edge.orientation[5] == "y" and left_edge.orientation[5] == "y":
            algorithm = "F R U R' U' R U R' U' F'"
        elif top_edge.orientation[5] == "y" and right_edge.orientation[5] == "y":
            algorithm = "U' F R U R' U' R U R' U' F'"
        elif bottom_edge.orientation[5] == "y" and right_edge.orientation[5] == "y":
            algorithm = "U U F R U R' U' F' F R U R' U' F'"
        elif bottom_edge.orientation[5] == "y" and left_edge.orientation[5] == "y":
            algorithm = "U F R U R' U' R U R' U' F'"

    if algorithm:
        converted_algorithm = convert_algorithm(algorithm, "r", "y")
        for move in converted_algorithm:
            internal_cube.move(move)
        move_list.extend(converted_algorithm)

    # assert that the yellow cross is solved
    f2l = [piece for piece in internal_cube.pieces if piece.pos[2] != -1]
    bottom_layer_edges = [piece for piece in internal_cube.pieces if piece.pos[2] == -1 and piece.type == "e"]
    if not all([piece.pos == correct_pos_map[str_sort(piece.orientation)] and piece.orientation == correct_orientation_map[str_sort(piece.orientation)] for piece in f2l] and [piece.orientation[5] == "y" for piece in bottom_layer_edges]):
        raise Exception("Yellow cross is not solved")

    return move_list

def solve_yellow_edges(internal_cube: Cube) -> list[str]:
    move_list = []

    for _ in range(4):
        internal_cube.move("D")
        move_list.append("D")

        # get all yellow edges
        top_edge = internal_cube.get_piece((0, 1, -1))
        right_edge = internal_cube.get_piece((-1, 0, -1))
        bottom_edge = internal_cube.get_piece((0, -1, -1))
        left_edge = internal_cube.get_piece((1, 0, -1))

        is_correct = { "top": False, "right": False, "bottom": False, "left": False }
        if correct_pos_map[str_sort(top_edge.orientation)] == top_edge.pos:
            is_correct["top"] = True
        if correct_pos_map[str_sort(right_edge.orientation)] == right_edge.pos:
            is_correct["right"] = True
        if correct_pos_map[str_sort(bottom_edge.orientation)] == bottom_edge.pos:
            is_correct["bottom"] = True
        if correct_pos_map[str_sort(left_edge.orientation)] == left_edge.pos:
            is_correct["left"] = True

        num_correct = sum([1 for correct in is_correct if is_correct[correct]])
        # if number of correct is 4, then we are done
        if num_correct == 4:
            return move_list
        # if number of correct is 2, then we must position the cube so that those are on the top and right
        elif num_correct == 2:
            if is_correct["top"] and is_correct["right"]:
                # do nothing
                pass
            elif is_correct["right"] and is_correct["bottom"]:
                internal_cube.move("D'")
                move_list.append("D'")
            elif is_correct["bottom"] and is_correct["left"]:
                internal_cube.move("D2")
                move_list.append("D")
                move_list.append("D")
            elif is_correct["left"] and is_correct["top"]:
                internal_cube.move("D")
                move_list.append("D")
            else:
                if is_correct["top"] and is_correct["bottom"]:
                    algorithm = "R U R' U R U U R' U'"
                    converted_algorithm = convert_algorithm(algorithm, "r", "y")
                    for move in converted_algorithm:
                        internal_cube.move(move)
                    move_list.extend(converted_algorithm)
                elif is_correct["right"] and is_correct["left"]:
                    algorithm = "R U R' U R U U R' U'"
                    converted_algorithm = convert_algorithm(algorithm, "r", "y")
                    for move in converted_algorithm:
                        internal_cube.move(move)
                    move_list.extend(converted_algorithm)
            # perform algorithm
            algorithm = "R U R' U R U U R'"
            converted_algorithm = convert_algorithm(algorithm, "r", "y")
            for move in converted_algorithm:
                internal_cube.move(move)
            move_list.extend(converted_algorithm)

            # get all yellow edges
            top_edge = internal_cube.get_piece((0, 1, -1))
            right_edge = internal_cube.get_piece((-1, 0, -1))
            bottom_edge = internal_cube.get_piece((0, -1, -1))
            left_edge = internal_cube.get_piece((1, 0, -1))

            # twist the bottom layer until they are all correct (if one is correct, then they all are)
            num_loops = 0
            continue_flag = False
            while not (correct_pos_map[str_sort(top_edge.orientation)] == top_edge.pos and correct_pos_map[str_sort(right_edge.orientation)] == right_edge.pos and correct_pos_map[str_sort(bottom_edge.orientation)] == bottom_edge.pos and correct_pos_map[str_sort(left_edge.orientation)] == left_edge.pos):
                if num_loops > 4:
                    continue_flag = True
                    break

                internal_cube.move("D'")
                move_list.append("D'")
                num_loops += 1
            if continue_flag:
                continue
            break
        else:
            # raise Exception("Invalid cube state")
            pass

    f2l = [piece for piece in internal_cube.pieces if piece.pos[2] != -1]
    bottom_layer_edges = [piece for piece in internal_cube.pieces if piece.pos[2] == -1 and piece.type == "e"]

    if not all([piece.pos == correct_pos_map[str_sort(piece.orientation)] and piece.orientation == correct_orientation_map[str_sort(piece.orientation)] for piece in f2l + bottom_layer_edges]):
        raise Exception("Yellow edges not in correct position")

    return move_list

def solve_yellow_corner_position(internal_cube: Cube) -> list[str]:
    move_list = []

    # get all yellow corners, order is top left (r as front and y as top) and goes clockwise
    corners = [internal_cube.get_piece((1, 1, -1)), internal_cube.get_piece((-1, 1, -1)), internal_cube.get_piece((-1, -1, -1)), internal_cube.get_piece((1, -1, -1))]
    # get number of yellow corners in correct position
    is_correct = [corner.pos == correct_pos_map[str_sort(corner.orientation)] for corner in corners]
    num_correct = sum([1 for correct in is_correct if correct])
    if num_correct == 4:
        return move_list
    elif num_correct == 0 or num_correct == 1:
        # while number of correct is not 4
        num_loops = 0
        while num_correct != 4:
            if num_loops > 8:
                raise Exception("Invalid cube state")

            algorithm = "U R U' L' U R' U' L"
            if is_correct[0]:
                converted_algorithm = convert_algorithm(algorithm, "o", "y")
            elif is_correct[1]:
                converted_algorithm = convert_algorithm(algorithm, "g", "y")
            elif is_correct[2]:
                converted_algorithm = convert_algorithm(algorithm, "r", "y")
            else:
                converted_algorithm = convert_algorithm(algorithm, "b", "y")
            for move in converted_algorithm:
                internal_cube.move(move)
            move_list.extend(converted_algorithm)

            corners = [internal_cube.get_piece((1, 1, -1)), internal_cube.get_piece((-1, 1, -1)), internal_cube.get_piece((-1, -1, -1)), internal_cube.get_piece((1, -1, -1))]
            is_correct = [corner.pos == correct_pos_map[str_sort(corner.orientation)] for corner in corners]
            num_correct = sum([1 for correct in is_correct if correct])

            num_loops += 1
    else:
        raise Exception("Invalid cube state")

    # assert that the yellow corners are in the correct position
    if not all([piece.pos == correct_pos_map[str_sort(piece.orientation)] for piece in internal_cube.pieces if piece.type == "c" and "y" in piece.orientation]):
        raise Exception("Yellow corners not in correct position")

    return move_list

def solve_yellow_corner_orientation(internal_cube: Cube) -> list[str]:
    move_list = []
    outer_num_loops = 0
    while not all([piece.orientation[5] == "y" for piece in internal_cube.pieces if piece.type == "c" and "y" in piece.orientation]):
        if outer_num_loops > 4:
            raise Exception("Invalid cube state")
        anchor_piece = internal_cube.get_piece((-1, -1, -1))
        # if the anchor piece is not in the right orientation, then we need to correct it
        inner_num_loops = 0
        while anchor_piece.orientation[5] != "y":
            if inner_num_loops > 6:
                raise Exception("Invalid cube state")
            algorithm = "R' D' R D"
            converted_algorithm = convert_algorithm(algorithm, "r", "y")
            for move in converted_algorithm:
                internal_cube.move(move)
            move_list.extend(converted_algorithm)
            inner_num_loops += 1
        internal_cube.move("D'")
        move_list.append("D'")
        outer_num_loops += 1

    num_loops = 0
    while not is_solved(internal_cube):
        if num_loops > 4:
            raise Exception("Invalid cube state")
        internal_cube.move("D'")
        move_list.append("D'")
        num_loops += 1

    if not is_solved(internal_cube):
        raise Exception("Cube not solved after yellow corner orientation")

    return move_list

def optimize_algorithm(algorithm: list[str]) -> list[str]:
    # three subsequent moves in the same direction can be replaced with a single move in the opposite direction

    first_iteration = []
    i = 0
    while i < len(algorithm):
        if i < len(algorithm) - 2 and algorithm[i] == algorithm[i + 1] == algorithm[i + 2]:
            if "'" in algorithm[i]:
                first_iteration.append(algorithm[i][:-1])
            else:
                first_iteration.append(algorithm[i] + "'")
            i += 3
        else:
            first_iteration.append(algorithm[i])
            i += 1

    # a move followed by its inverse can be removed
    second_iteration = [] 
    i = 0
    while i < len(first_iteration):
        if i < len(first_iteration) - 1 and first_iteration[i] == inverse(first_iteration[i + 1]):
            i += 2
        else:
            second_iteration.append(first_iteration[i])
            i += 1

    print("Reduced algorithm from", len(algorithm), "moves to", len(second_iteration), "moves")

    return second_iteration

def inverse(move: str) -> str:
    if "'" in move:
        return move[:-1]
    else:
        return move + "'"

def is_solved(internal_cube: Cube):
    for piece in internal_cube.pieces:
        if piece.pos != correct_pos_map[str_sort(piece.orientation)] or piece.orientation != correct_orientation_map[str_sort(piece.orientation)]:
            return False
    return True

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

    # moves = solve_cube(c)

    # red center should be right of green center
    # print(is_right_of(c.get_piece((0,-1,0)), c.get_piece((-1,0,0))))

    # test against 100 random scrambles
    # for _ in range(100):
    #     c.scramble(num_moves=100)
    #     try:
    #         moves = solve_cube(c) 
    #     except Exception as e:
    #         raise e