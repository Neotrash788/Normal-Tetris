import random, time
from dicts import *

#============================================================================#

def check_for_death(new_shape_points):
    # Game over if we can't place a new shape
    vals = [board[pt[1]][pt[0]] for pt in new_shape_points if pt[1] >= 0]
    if not all([i == 0 for i in vals]):
        print("DEATH")
        exit()
    
    return False

def print_board():
   [print(i) for i in board]

def on_board(points):
    for point in points:
        x, y = point
        if x < 0 or x >= BOARD_WIDTH: return False
        if y >= BOARD_HEIGHT: return False
    
    return True

def valid_shape(points):
    if not on_board(points): return False

    # Shape cant intersect any otuher shapes, is allowed to intersect with itself
    vals = [board[pt[1]][pt[0]] for pt in points if pt not in current_shape.points]
    if not all([i == 0 for i in vals]): return False

    return True

def get_random_bag():
    bag = ["i", "t", "z", "s", "o", "j", "l"]
    #bag = ["o", "o", "o", "o", "o", "o", "o"]

    random.shuffle(bag)
    return(bag)

def update_bags():
    # Replace finished bags with new ones
    for i in range(len(bags)): bags[i] = get_random_bag() if bags[i] == [] else bags[i]

def hold():
    global current_shape, held_piece

    # Remove current piece from board
    for pt in current_shape.points: board[pt[1]][pt[0]] = 0
    
    if held_piece == None:
        held_piece = current_shape_id
        gen_next_piece()

    else: held_piece, current_shape = current_shape_id, Shape(held_piece, (4, 2))

def check_for_all_clear():
    if pices_placed == 0: return False
    return all([all([board[y][x] == 0 for x in range(BOARD_WIDTH)]) for y in range(BOARD_HEIGHT)])


def gen_next_piece():
    global next_queue, pos_in_bag, current_shape_id, current_shape, pices_placed

    check_for_lines()
    pos_in_bag += 1
    pices_placed += 1

    # Move to next bag
    if pos_in_bag == 7:
        bags.pop(0)
        bags.append([])

        update_bags()
        pos_in_bag = 0

    # Go to next piece
    current_shape_id = bags[0][pos_in_bag]
    del(current_shape)
    current_shape = Shape(current_shape_id, (4, 2))

    # Look forward to next bag for newt queue if needed
    if pos_in_bag >= 2:
        sect1 = bags[0][pos_in_bag + 1 :]
        sec2 = bags[1][: pos_in_bag - 1]

        next_queue = sect1 + sec2

    else: next_queue = bags[0][pos_in_bag + 1: pos_in_bag + 6]

def steps_to_cords(steps, origin):
   offsets = [offset_dict[i] for i in steps]

   # Get all cords
   points = [origin]
   for offset in offsets: 
       x, y = points[-1]


       ox, oy = offset
       nx, ny = x + ox, y + oy
       points.append((nx, ny))

   # Remove duplicates
   return [i for i in dict.fromkeys(points).keys()]


def tile_filled(pos):
    x, y = pos

    if not on_board([pos]): return True
    if board[y][x] != 0: return True

    return False



def check_for_spin():
    origin = current_shape.origin
    offsets = t_spin_offset_dict[current_shape.orientation]

    corner_offsets = [(1, -1), (1, 1), (-1, 1), (-1, -1)]
    corners = [(origin[0] + offset[0], origin[1] + offset[1]) for offset in corner_offsets]

    main_corners = [(origin[0] + offset[0], origin[1] + offset[1]) for offset in offsets]
    outher_corners = [i for i in corners if i not in main_corners]

    main_corners = [1 for corner in main_corners if tile_filled(corner)]
    outher_corners = [1 for corner in outher_corners if tile_filled(corner)]

    if sum(main_corners) == 2 and sum(outher_corners) >= 1: return 2
    if sum(main_corners) == 1 and sum(outher_corners) >= 2: return 1

    return 0
    

def check_for_lines():
    global clear_type, lines_cleared_last_piece, spin, combo, lines_cleared, all_clear, back_to_back, attack_sent, attack_per_line, attack_per_piece

    # Find all full rows
    lines = []
    for row in range(len(board)):
        if all([i != 0 for i in board[row]]): lines.append(row)
    
    clear_type = len(lines)

    if clear_type != 0:
        combo += 1
        lines_cleared += clear_type
        lines_cleared_last_piece = True

        if current_shape.spin_type == 0 and clear_type != 4: back_to_back = -1
        else: back_to_back += 1
    else:
        combo = -1
        return None

    [board.pop(i) for i in lines[::-1]]
    [board.insert(0, [0 for i in range(BOARD_WIDTH)]) for j in range(len(lines))]

    attack = (current_shape.spin_type, clear_type)
    attack = attack_type_dict[attack]

    attack_sent += attack_dict[attack][combo]

    all_clear = check_for_all_clear()
    if all_clear: attack_sent += 10

    attack_per_line = attack_sent / lines_cleared
    attack_per_piece = attack_sent / pices_placed

#============================================================================#

class Shape():
    def __init__(self, shape, origin) -> None:
        self.spin = False
        self.spin_type = 0

        self.shape = shape
        self.origin = origin
        self.frames_on_ground = 0

        self.orientation = "u"
        self.steps = shape_dict[shape]
        self.points = steps_to_cords(self.steps, self.origin)

        # Check evrey new piece
        check_for_death(self.points)

    def valid_rotation(self, direction, origin):
        if direction == "cw":  steps = [rotate_cw_dict[step] for step in self.steps]
        if direction == "ccw": steps = [rotate_ccw_dict[step] for step in self.steps]
        if direction == "180": steps = [rotate_cw_dict[step2] for step2 in [rotate_cw_dict[step] for step in self.steps]]

        cords = steps_to_cords(steps, origin)
        return valid_shape(cords)
    
    def get_srs_offset(self, direction):
        if self.shape == "o": return None

        if direction == "cw": offsets = kick_cw_dict[self.orientation]
        if direction == "ccw": offsets = kick_ccw_dict[self.orientation]

        if self.shape == "i" and direction == "cw": offsets = kick_i_cw_dict[self.orientation]
        if self.shape == "i" and direction == "ccw": offsets = kick_i_ccw_dict[self.orientation]

        # Try tests in order
        for current_offset in offsets:
            ox, oy = current_offset
            origin = (self.origin[0] + ox, self.origin[1] + oy)

            if self.valid_rotation(direction, origin):
                # If the piece is spun or not + return offset
                self.spin = True if current_offset != (0, 0) else False
                return current_offset

        
        # No offset means cant rotate
        return None

    def rotate_cw(self):
        offset = self.get_srs_offset("cw")
        if offset == None: return None

        # Srs offset
        ox, oy = offset
        self.orientation = rotate_cw_dict[self.orientation]
        self.origin = (self.origin[0] + ox, self.origin[1] + oy)

        # Update
        self.steps = [rotate_cw_dict[step] for step in self.steps]

        self.update_points()
        self.spin_type = check_for_spin() if current_shape.shape == "t" else 0

    def rotate_ccw(self):
        offset = self.get_srs_offset("ccw")
        if offset == None: return None

        # Srs offset
        ox, oy = offset
        self.orientation = rotate_ccw_dict[self.orientation]
        self.origin = (self.origin[0] + ox, self.origin[1] + oy)

        # Update
        self.steps = [rotate_ccw_dict[step] for step in self.steps]

        self.update_points()
        self.spin_type = check_for_spin() if current_shape.shape == "t" else 0

    def rotate_180(self):
        if not self.valid_rotation("180", self.origin): return None

        self.orientation = rotate_cw_dict[rotate_cw_dict[self.orientation]]
        self.steps = [rotate_cw_dict[step] for step in self.steps]
        self.steps = [rotate_cw_dict[step] for step in self.steps]

        self.update_points()
        self.spin_type = check_for_spin() if current_shape.shape == "t" else 0
        
    def draw_on_board(self):
        # Only called in gui as it is visuals
        for pos in self.points:
            x, y = pos
            if y < 0: continue
            board[y][x] = shape_id_dict[self.shape]

    def update_points(self):
        # Remove previous positions from board (if any)
        for point in self.points:
            x, y = point
            if y < 0: continue
            board[y][x] = 0
        
        self.points = steps_to_cords(self.steps, self.origin)
    
    def check_for_ground(self):
        # Check if piece can move down
        origin = (self.origin[0], self.origin[1] + 1)   
        new_points = steps_to_cords(self.steps, origin)

        return not valid_shape(new_points)

    def apply_grav(self):
        self.origin = (self.origin[0], self.origin[1] + 1)
        self.update_points()
    
    def move_down(self):
        if self.check_for_ground(): return None
        self.origin = (self.origin[0], self.origin[1] + 1)
        self.update_points()


    def move_left(self):
        # Check if this is a valid move
        if not valid_shape([(pt[0] - 1, pt[1]) for pt in self.points]): return None

        # Move
        self.origin = (self.origin[0] - 1, self.origin[1])
        self.update_points()

    def move_right(self):
        # Check for valid move
        if not valid_shape([(pt[0] + 1, pt[1]) for pt in self.points]): return None

        # Move
        self.origin = (self.origin[0] + 1, self.origin[1])
        self.update_points()
    
    def move_untill_ground(self):
        while not self.check_for_ground():
            self.origin = self.origin = (self.origin[0], self.origin[1] + 1)
            self.update_points()
    
    def hard_drop(self):
        self.move_untill_ground()
        self.draw_on_board()
        gen_next_piece()
    
    def get_shadow(self):
        # This function is called in gui only as it is asthetic
        origin = (self.origin[0], self.origin[1])

        while valid_shape(steps_to_cords(self.steps, (origin[0], origin[1] + 1))):
            origin = (origin[0], origin[1] + 1)
        
        return steps_to_cords(self.steps, origin)

#============================================================================#

def setup():
    global spin, combo,\
    bags, pos_in_bag,\
    BOARD_WIDTH, BOARD_HEIGHT, board,\
    clear_type, lines_cleared_last_piece,\
    held_piece, next_queue, current_shape, current_shape_id,\
    lines_cleared, pices_placed, all_clear, back_to_back, attack_sent, attack_per_line,\
    attack_per_piece
    

    BOARD_WIDTH, BOARD_HEIGHT = 10, 23
    board = [[0 for col in range(BOARD_WIDTH)] for row in range(BOARD_HEIGHT)]

    bags = [[], []]
    update_bags()

    pos_in_bag = 0
    held_piece = None

    next_queue = bags[0][1:6]
    current_shape_id = bags[0][0]
    current_shape = Shape(current_shape_id, (4, 2))

    spin = False
    clear_type = 0
    lines_cleared_last_piece = False

    combo = -1
    pices_placed = 0
    lines_cleared = 0

    all_clear = False
    attack_sent = 0
    back_to_back = -1

    attack_per_piece = 0
    attack_per_line = 0

#============================================================================#

def update_game():
    global clear_type
    current_shape.check_for_ground()

setup()
