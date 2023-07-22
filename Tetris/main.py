import time
import math
import pygame
import random

from dicts import *
from datetime import datetime

def read_file(file = "board.board"):
    with open(file, "r") as f:
        board = f.read().split("\n")
        return [[int(j) for j in i.split(" ")] for i in board]

def write_file(board, file = "board.board"):
    board_str = "\n".join([" ".join([str(j) for j in i]) for i in board])
    with open(file, "w") as f:
        f.write(board_str)

def setup():
    bag = Bag()
    board = Board_class(read_file())
    current_shape = Shape(bag.bag[0])

    update_board()
    held_piece = Held_piece()
    next_queue = Next_queue()

    apm = 0
    b2b = -1
    combo = 0

    total_lines = 0
    total_atack = 0
    total_pieces = 0
    current_frame = 1

    min_fps = 1000
    preforming_arr = True

    

    # Lord forgive me for what im about to do
    globals().update(locals())

def id_to_cords(id, origin):
    steps = shape_step_dict[id]
    return steps_to_cords(steps, origin)

def steps_to_cords(steps, origin):
    offsets = [step_offset_dict[i] for i in steps]
    pos_ls = [origin]
    
    for offset in offsets:
        x, y = pos_ls[-1]
        ox, oy = offset
        nx, ny = x + ox, y + oy

        pos_ls.append((nx, ny))
    
    return list(dict.fromkeys(pos_ls))

def update_board():
    board.remove_previous_shape_pos()
    board.stamp_current_shape()

def new_shape():
    global current_shape
    
    bag.update()
    current_shape = Shape(bag.bag[0])

    update_board()

def check_for_spin():
    # 1, 2 = mini, full spin
    origin = current_shape.pos_ls[0]
    corner_offsets = [(1, 1), (-1, 1), (-1, -1), (1, -1)]

    corners = [(origin[0] + offset[0], origin[1] + offset[1]) for offset in corner_offsets]
    corners = [i for i in corners if not board.empty_tile(i)]
    
    if len(corners) < 3: return 0

    main_offsets = main_corner_dict[current_shape.current_rotation] 
    main_cornerss = [(origin[0] + offset[0], origin[1] + offset[1]) for offset in main_offsets]


    if all([i in corners for i in main_cornerss]):return 2
    return 1

def print_board():
    [print(i) for i in board.board]

def hold():
    global current_shape

    current_shape.prev_pos_ls = current_shape.pos_ls
    board.remove_previous_shape_pos()

    if held_piece.id == 0:
        held_piece.id = current_shape.id
        new_shape()
        return None

    held_piece.id, current_shape = current_shape.id, Shape(held_piece.id)

def handle_atack(lines, spin):
    global b2b, total_atack

    atack_type = lines
    if spin == 1: atack_type += 4
    if spin == 2: atack_type += 6

    if atack_type >= 4: b2b += 1
    else: b2b = -1

    stationary_text_displays[4].set_text(f"B2B X{b2b}", (0, 0, 0))
    stationary_text_displays[4].active = True if b2b > 0 else False    


    atack = atack_dict[atack_type][combo]
    if b2b >0: atack += math.floor(math.sqrt(b2b))

    if all([all(i == 0 for i in board.board[j]) for j in range(2, 23)]):
        atack += 10
        moveing_text_displays[3].frame = 0
        moveing_text_displays[3].active = True
        moveing_text_displays[3].set_text("ALL CLEAR", (200, 200, 200))


    # b2b in tetrio is only like this untill 25
    # But in a real game going past 25 is highly unlikely
    total_atack += atack

def handle_line_clears(spin):
    global combo, total_lines

    lines = []
    for row in range(23):
        if 0 not in board.board[row]: lines.append(row)

    if len(lines) == 0:
        combo = -1
        return None
    


    clear_type = clear_type_dict[len(lines)]
    total_lines += len(lines)

    moveing_text_displays[0].frame = 0
    moveing_text_displays[0].active = True
    moveing_text_displays[0].set_text(clear_type, (0, 0, 0))

    combo += 1
    moveing_text_displays[2].frame = 0
    if combo > 0: moveing_text_displays[2].active = True
    moveing_text_displays[2].set_text(f"X{combo} Combo", (0, 0, 0))


    board.remove_previous_shape_pos()


        

    for row in lines[::-1]:
        board.board.pop(row)
    
    for i in range(len(lines)):
        board.board.insert(0, [0 for i in range(10)])

    board.tile_surf_dirty.fill((0, 0, 0))
    
    for row in range(23):
        for col in range(10):
            id = board.board[row][col]
            if id == 0: continue

            surf = pygame.Surface((45, 45))
            surf.fill(col_dict[id])

            board.tile_surf_dirty.blit(surf, (col * 45, row * 45))
    
    update_board()
    handle_atack(len(lines), spin)

    '''
    Instead of stamping evrey tile, paste the lines which wernt cleared
    max_line = max(lines)
    min_line = min(lines)
    line_diff = max_line - min_line

    # There is a gap between cleared lines
    middle = max_line - min_line + 1 != len(lines)
    board.remove_previous_shape_pos()

    a1 = (0, 45)
    a2 = (0, 0, 450, min_line * 45)

    surf = pygame.Surface((450, 45))
    #board.tile_surf_dirty.blit(surf, (0, 1035 - 45))

    board.tile_surf_dirty.blit(board.tile_surf_dirty, a1, a2)
    update_board()

    #screen.blit(board.tile_surf_dirty, (250 + 450 + 45 + 45, 25))
    #pygame.display.update()

    #time.sleep(10)
    #exit()
    '''        

def handle_movement():
    global preforming_arr

    # Vert
    if key_time_dict[pygame.K_DOWN] == 1:
        current_shape.move_untill_ground()
        update_board()

    # Horz
    if key_time_dict[pygame.K_LEFT] != -1: key_time_dict[pygame.K_LEFT] += 1
    if key_time_dict[pygame.K_RIGHT] != -1: key_time_dict[pygame.K_RIGHT] += 1

    if key_time_dict[pygame.K_LEFT] != -1 and key_time_dict[pygame.K_RIGHT] != -1: return None
    if key_time_dict[pygame.K_LEFT] == -1 and key_time_dict[pygame.K_RIGHT] == -1: preforming_arr = False

    if not preforming_arr:
        if key_time_dict[pygame.K_LEFT] >= senceitivity_dict["DAS"]:
            preforming_arr = True
            key_time_dict[pygame.K_LEFT] -= senceitivity_dict["ARR"]

        if key_time_dict[pygame.K_RIGHT] >= senceitivity_dict["DAS"]:
            preforming_arr = True
            key_time_dict[pygame.K_RIGHT] -= senceitivity_dict["ARR"]
        
        return None

    if key_time_dict[pygame.K_LEFT] >= senceitivity_dict["ARR"]:
        current_shape.move(-1, 0)
        update_board()
        key_time_dict[pygame.K_LEFT] -= senceitivity_dict["ARR"]
        
    if key_time_dict[pygame.K_RIGHT] >= senceitivity_dict["ARR"]:
        current_shape.move(1, 0)
        update_board()
        key_time_dict[pygame.K_RIGHT] -= senceitivity_dict["ARR"]

def place_current_shape():
    spin = current_shape.spin
    update_board()
    new_shape()
    update_board()
    handle_line_clears(spin)


class Board_class():
    def __init__(self, board) -> None:
        super().__init__()
        # 500, 1000
        self.board = board

        # ==================== Background ==================== #

        self.background_surf = pygame.Surface((450, 900), pygame.SRCALPHA)
        self.background_surf.fill((0, 0, 0, 150))

        # Main border
        # Top / Bottom
        pygame.draw.line(self.background_surf, (255, 255, 255), (0, 0), (450, 0), 3)
        pygame.draw.line(self.background_surf, (255, 255, 255), (450, 0), (450, 900), 3)

        # Left / Right
        pygame.draw.line(self.background_surf, (255, 255, 255), (0, 0), (0, 900), 3)
        pygame.draw.line(self.background_surf, (255, 255, 255), (0, 900), (450, 900), 3)

        # Horz
        for y in range(23):
            pygame.draw.line(self.background_surf, (50, 50, 50), (0, y * 45), (450, y * 45))

        # Vert
        for x in range(10):
            pygame.draw.line(self.background_surf, (50, 50, 50), (x * 45, 0), (x * 45, 900))

        # ==================== Main Tiles ==================== #
        self.tile_surf_dirty = pygame.Surface((450, 1035))

        self.tile_surf_clean = pygame.Surface((450, 1035))
        self.tile_surf_clean.set_colorkey((0, 0, 0))

        
    def empty_tile(self, pos):
        if pos[1] < 0: return True

        if not self.on_board(pos): return False
        if self.board[pos[1]][pos[0]] != 0: return False

        return True
    
    def on_board(self, pos):
        if pos[0] < 0 or pos[0] >= 10: return False
        if pos[1] < 0 or pos[1] >= 23: return False

        return True

    def stamp_current_shape(self):
        # Put shape on processing board
        for pos in current_shape.pos_ls:
            if pos[1] < 0: continue
            self.board[pos[1]][pos[0]] = current_shape.id

        # Put shape on dirty board
        surf = pygame.Surface((45, 45), pygame.SRCALPHA)
        surf.fill(col_dict[current_shape.id])
        #surf.fill((255, 255, 255, 255))

        for pos in current_shape.pos_ls:
            self.tile_surf_dirty.blit(surf, (pos[0] * 45, pos[1] * 45))

    
    def remove_previous_shape_pos(self):
        # Remove shape from processing board
        for pos in current_shape.prev_pos_ls:
            if pos[1] < 0: continue
            self.board[pos[1]][pos[0]] = 0

        # Remove shape from dirty board
        surf = pygame.Surface((45, 45))
        surf.fill((0, 0, 0))

        for pos in current_shape.prev_pos_ls:
            self.tile_surf_dirty.blit(surf, (pos[0] * 45, pos[1] * 45))
    
    def render(self):
        screen.blit(self.background_surf, (250, 160))

        # Clean dirty board and print
        self.tile_surf_clean.blit(self.tile_surf_dirty, (0, 0))
        screen.blit(self.tile_surf_clean, (250, 25))

        self.draw_shadow()
    
    def draw_shadow(self):
        surf = pygame.Surface((45, 45))
        surf.fill((100, 100, 100))

        for pos in current_shape.get_shadow_cords():
            if pos in current_shape.pos_ls: continue
            screen.blit(surf, (250 + pos[0] * 45,25 + pos[1] * 45))

class Shape():
    def __init__(self, id) -> None:
        self.id = id
        self.spin = 0
        self.current_rotation = 'u'
        self.steps = shape_step_dict[id]
        
        origin = (4, 1) if id != 1 else (4, 2)
        self.pos_ls = id_to_cords(id, origin)
        self.prev_pos_ls = id_to_cords(id, origin)

    def move_untill_ground(self):
        prev_pos_ls = self.pos_ls

        while self.move(0, 1):
            pass
        
        # This is one movement so keep prev pos the same
        self.prev_pos_ls = prev_pos_ls
    
    def get_shadow_cords(self):
        prev = self.prev_pos_ls
        current = self.pos_ls

        self.move_untill_ground()
        shadow = self.pos_ls

        self.pos_ls = current
        self.prev_pos_ls = prev

        return shadow

    def move(self, x, y):
        # Check if it can move
        
        pos_ls = [(pt[0] + x, pt[1] + y) for pt in self.pos_ls]
        if not all([board.empty_tile(pt) for pt in pos_ls if pt not in self.pos_ls]): return False

        # Move Successfull
        self.prev_pos_ls = self.pos_ls
        self.pos_ls = pos_ls
        return True
    
    def rotate(self, dir):
        pos_ls = self.srs(dir)
        if pos_ls == None: return None

        if dir == "cw": self.current_rotation = rotate_cw_dict[self.current_rotation]
        if dir == "ccw": self.current_rotation = rotate_ccw_dict[self.current_rotation]
        if dir == "180": self.current_rotation = rotate_cw_dict[rotate_cw_dict[self.current_rotation]]

        self.prev_pos_ls = self.pos_ls
        self.pos_ls = pos_ls

        update_board()
        if self.id == shape_id_dict["t"]: self.spin = check_for_spin()
        else: self.spin = 0

        if self.spin != 0:
            moveing_text_displays[1].frame = 0
            moveing_text_displays[1].active = True
            moveing_text_displays[1].set_text(spin_type_dict[self.spin], (col_dict[3]))
    
    def srs(self, dir):
        for i in range(5):
            # Get the offset
            if self.id == 1:
                if dir == "cw": offset = kick_i_cw_dict[self.current_rotation][i] 
                elif dir == "ccw": offset = kick_i_ccw_dict[self.current_rotation][i]
                else: offset = kick_i_180_dict[self.current_rotation][i]

            else:
                if dir == "cw": offset = kick_cw_dict[self.current_rotation][i]
                elif dir == "ccw": offset = kick_ccw_dict[self.current_rotation][i]
                else: offset = kick_180_dict[self.current_rotation][i]

            # Get the new shape
            if dir == "cw": steps = [rotate_cw_dict[j] for j in self.steps]
            elif dir == "ccw": steps = [rotate_ccw_dict[j] for j in self.steps]
            else: steps = [rotate_cw_dict[rotate_cw_dict[j]] for j in self.steps]
            
            origin = self.pos_ls[0]
            origin = (origin[0] + offset[0], origin[1] + offset[1])

            pos_ls = steps_to_cords(steps, origin)
            test_ls = [i for i in pos_ls if i not in self.pos_ls]

            if not all(board.empty_tile(j) for j in test_ls): continue

            self.steps = steps

            return pos_ls
        
        return None

class Held_piece():
    def __init__(self) -> None:
        self.id = 0

    def render(self):
        if self.id == 0: return None

        surf = pygame.Surface((45, 45))
        surf.fill(col_dict[self.id])

        origin = (-1, 0) if self.id == 1 else (0, 0)

        for pos in id_to_cords(self.id, origin):
            x, y = pos[0] * 45, pos[1] * 45
            screen.blit(surf, (115 + x, 160 + y))

class Next_queue():
    def __init__(self) -> None:
        self.render()
    
    def render(self):
        shapes = bag.bag[1:6]
        shapes = [id_to_cords(i, (0, 0)) for i in shapes]
        surf = pygame.Surface((45, 45))
        
        for shape in range(5):
            surf.fill(col_dict[bag.bag[shape + 1]])
            pos_ls = shapes[shape]
            y_offset = 160 + 150 * shape

            x_offset = -45 if bag.bag[shape + 1] == 2 else 0
            for pos in pos_ls:
                screen.blit(surf, (790 + pos[0] * 45 + x_offset, y_offset + pos[1] * 45))

class Bag():
    def __init__(self) -> None:
        self.bag = [i for i in range(14)]  
        [self.update() for i in range(14)]

    def update(self):
        self.bag.pop(0)
        if len(self.bag) != 7: return None

        shapes = [i for i in range(1, 8)]
        random.shuffle(shapes)
        
        [self.bag.append(i) for i in shapes]

class Moveing_text():
    def __init__(self, pos, align, size = 30) -> None:
        self.pos = pos
        self.align = align
        self.active = False

        self.frame = 0
        self.size = size
        self.font = pygame.font.Font(None, self.size)

    def update_text(self, spaceing):
        self.chars[0][1].topleft = (0, 0)
        #else: self.chars[0][1].topright = (0, 0)
        #if self.align == "r": self.chars = self.chars[::-1]

        for char in range(1, len(self.text)):
            pos = self.chars[char - 1][1].topright
            pos = (pos[0] + spaceing, pos[1])
            self.chars[char][1].topleft = pos

        width = abs(self.chars[-1][1].right - self.chars[0][1].left)
        self.image = pygame.Surface((width, self.size), pygame.SRCALPHA)
        
        for char in self.chars:
            self.image.blit(char[0], char[1])
        
        if self.align == "l": self.rect = self.image.get_rect(topleft = self.pos)
        elif self.align == "r": self.rect = self.image.get_rect(topright = self.pos)
        else: self.rect = self.image.get_rect(center = self.pos)

    def set_text(self, text, col):
        self.text = text
        self.chars = []

        for char in text:
            surf = self.font.render(char, True, col)
            rect = surf.get_rect()
            self.chars.append((surf, rect))

        self.update_text(0)

    def render(self):
        screen.blit(self.image, self.rect)
        
class Stationary_text():
    def __init__(self, title, pos, align) -> None:
        self.pos = pos
        self.active = True

        self.align = align
        self.font = pygame.font.Font(None, 40)
        self.title_surf = self.font.render(title, True, (0, 0, 0))

        self.font = pygame.font.Font(None, 30)
        self.set_text("", (0, 0, 0))

    
    def set_text(self, text, col):
        self.value_surf = self.font.render(text, True, col)

        width = max(self.title_surf.get_width(), self.value_surf.get_width())
        self.image = pygame.Surface((width, 60), pygame.SRCALPHA)
                
        if self.align == "l": self.title_rect = self.title_surf.get_rect(topleft = (0, 0))
        else: self.title_rect = self.title_surf.get_rect(topright = (width, 0))

        if self.align == "l": self.value_rect = self.value_surf.get_rect(topleft = (0, 30))
        else: self.value_rect = self.value_surf.get_rect(topright = (width, 30))

        if self.align == "l": self.rect = self.image.get_rect(topleft = self.pos)
        else: self.rect = self.image.get_rect(topright = self.pos)

        self.image.blit(self.title_surf, self.title_rect)
        self.image.blit(self.value_surf, self.value_rect)

    def render(self):
        screen.blit(self.image, self.rect)

def render_text():
    for display in moveing_text_displays:
        if display.active:
            frame = display.frame
            display.update_text(frame // 3)
            display.image.set_alpha(255 - (frame * 6))

            display.render()
            display.frame += 1

            if display.frame >= 60: display.active = False
    
    for display in stationary_text_displays:
        if display.active:
            display.render()

if __name__ == "__main__":
    FPS = 60
    pygame.init()
    clock = pygame.time.Clock()

    SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED | pygame.FULLSCREEN)

    SCREEN_BACKGROUND = pygame.image.load("background.png").convert()
    SCREEN_BACKGROUND = pygame.transform.scale(SCREEN_BACKGROUND, (1920, 1080))
    SCREEN_BACKGROUND.set_alpha(100)

    '''
    #Generate an empty board
    BOARD_WIDTH, BOARD_HEIGHT = 10, 20
    board = [[0 for x in range(BOARD_WIDTH)] for y in range(BOARD_HEIGHT)]
    '''

    bag = Bag()
    board = Board_class(read_file())
    current_shape = Shape(bag.bag[0])
    update_board()

    apm = 0
    b2b = -1
    combo = -1
    
    total_lines = 0
    total_atack = 0
    total_pieces = 0
    current_frame = 1

    # Board starts at (250, 25)
    moveing_text_displays = [
        Moveing_text((245, 400), "r"), # Line Clear
        Moveing_text((245, 375), "r"), # Spin Type
        Moveing_text((245, 425), "r"), # Combo
        Moveing_text((475, 600), "m", 100)
    ]

    stationary_text_displays = [
        Stationary_text("ATTACK", (245, 630), "r"),
        Stationary_text("SPEED", (245, 705), ("r")),

        Stationary_text("Effecincey", (245, 535), "r"),
        Stationary_text("", (245, 555), "r"),

        Stationary_text("Back to Back", (245, 460), "r"),
    ]

    stationary_text_displays[4].active = False

    #TEST_TEXT.set_text("THIS IS A TEST!", (255, 255, 255))

    held_piece = Held_piece()
    next_queue = Next_queue()
    preforming_arr = True
    min_fps = 1000

    
                                           
    while True:
        frame_start = datetime.now()

        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Key up
            if event.type == pygame.KEYUP:
                # Quit
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                
                if event.key == pygame.K_LEFT:
                    key_time_dict[pygame.K_LEFT] = -1

                if event.key == pygame.K_RIGHT:
                    key_time_dict[pygame.K_RIGHT] = -1
                
                if event.key == pygame.K_DOWN:
                    key_time_dict[pygame.K_DOWN] = -1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_shape.move_untill_ground()
                    place_current_shape()
                    
                    total_pieces += 1

                if event.key == pygame.K_RIGHT:
                    current_shape.move(1, 0)
                    update_board()
                    key_time_dict[pygame.K_RIGHT] = 1

                if event.key == pygame.K_LEFT:
                    current_shape.move(-1, 0)
                    update_board()
                    key_time_dict[pygame.K_LEFT] = 1

                if event.key == pygame.K_DOWN:
                    key_time_dict[pygame.K_DOWN] = 1

                if event.key == pygame.K_UP:
                    current_shape.rotate("cw")
                
                if event.key == pygame.K_z:
                    current_shape.rotate("ccw")

                if event.key == pygame.K_a:
                    current_shape.rotate("180")
                
                if event.key == pygame.K_c:
                    hold()
                    update_board()

                if event.key == pygame.K_r:
                    setup()
                    
        handle_movement()
        screen.blit(SCREEN_BACKGROUND, (0, 0))
        board.render()
        held_piece.render()
        next_queue.render()

        line_efficiency = round(total_atack / total_lines, 2) if total_lines != 0 else 0
        stationary_text_displays[3].set_text(f"{line_efficiency}/Line", (0, 75, 75))

        piece_effecincey = round(total_atack / total_pieces, 2) if total_pieces != 0 else 0
        stationary_text_displays[2].set_text(f"{piece_effecincey}/Piece", (0, 75, 75))

        pps = round(total_pieces / (current_frame / 60), 2)
        stationary_text_displays[1].set_text(f"{total_pieces}, {pps}/Sec", (0, 0, 0))
        

        apm = round(total_atack / (current_frame / 3600), 2)
        stationary_text_displays[0].set_text(f"{total_atack}, {apm}/M", (0, 0, 0))

        render_text()


        frame_end = datetime.now()
        frame_time = frame_end - frame_start
        frame_time = frame_time.microseconds / 10 ** 6
        fps = 1 / frame_time
        if fps < min_fps: min_fps = fps

        #print(fps)

        pygame.display.update()

        current_frame += 1
        clock.tick(FPS)

