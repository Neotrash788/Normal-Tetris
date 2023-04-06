import pygame
import main
from datetime import datetime, timedelta
from dicts import *

#============================================================================#

FPS = 60
pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH, SCREEN_HEIGHT = 1920 ,1080
BACKGROUND_SURF = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED | pygame.FULLSCREEN, 0, 0, 1)

BOARD_BACKGROUND = pygame.Surface((1000, 1080))
BOARD_BACKGROUND.fill((0, 25, 50))

preformeing_arr = False
held_current_piece = False

Tiles = pygame.sprite.Group()
Next_queue = pygame.sprite.Group()
Held_display = pygame.sprite.Group()

#============================================================================#

class Debug():
    def __init__(self) -> None:
        # Theese sould lag behind one piece
        self.pieces_placed = main.pices_placed
        self.lines_cleared = main.lines_cleared
        
        self.clear_text = "None"
        self.font = pygame.font.Font(None, 100)

    def get_all_clear_text(self):
        all_clear_text = "ALL CLEAR!" if main.all_clear else "------"
        self.all_clear_text_surf = self.font.render(all_clear_text, True, (200, 200, 200))
    
    def get_new_clear(self):
        if self.pieces_placed != main.pices_placed:

            if self.lines_cleared != main.lines_cleared:
                self.clear_text = clear_type_dict[main.lines_cleared - self.lines_cleared]
                self.lines_cleared = main.lines_cleared

            else: self.clear_text = "None"
            self.pieces_placed = main.pices_placed

        self.clear_text_surf = self.font.render(self.clear_text, True, (200, 200, 200))
    
    def get_combo(self):
        combo_text = f"Combo : {main.combo}"
        self.combo_text_surf = self.font.render(combo_text, True, (200, 200, 200))

    def get_spin_text(self):
        spin_text = spin_type_dict[main.current_shape.spin_type]
        spin_text = f"{spin_text} - Spin!"

        self.spin_text_surf = self.font.render(spin_text, True, (200, 200, 200))
    
    def update(self):
        self.get_combo()
        self.get_new_clear()
        self.get_spin_text()
        self.get_all_clear_text()

        screen.blit(self.clear_text_surf, (0,0))
        screen.blit(self.combo_text_surf, (0,50))
        screen.blit(self.spin_text_surf, (0,100))
        screen.blit(self.all_clear_text_surf, (0, 150))

debug = Debug()
#============================================================================#

class Held_tile(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()
        self.x, self.y = pos

        self.image = pygame.Surface((44, 44))
        self.image.fill((100, 100, 100))

        rect_x = pos[0] * 45 + 505
        rect_y = pos[1] * 45 + 22
        self.rect = self.image.get_rect(topleft = (rect_x, rect_y))

    def update(self) -> None:
        shape = main.held_piece

        # If there is no held piece return none
        if shape == None:
            self.image.fill(col_dict[0])
            return None

        id = 0
        offset = -1 if shape == "i" else 0
        # Get cords + cols on held display for shape
        cords = main.steps_to_cords(main.shape_dict[shape], (2 + offset, 1))
        if (self.x, self.y) in cords: id = main.shape_id_dict[shape]
        
        # If hold is disabled make it grey
        if held_current_piece and id != 0: id = 8
        self.image.fill(col_dict[id])
      
class Next_queue_tile(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()
        self.x, self.y = pos

        self.image = pygame.Surface((44, 44))
        self.image.fill((100, 100, 100))

        rect_x = pos[0] * 45 + 1235
        rect_y = pos[1] * 45 + 22
        self.rect = self.image.get_rect(topleft = (rect_x, rect_y))
    
    def update(self):
        pos_in_queue = self.y // 3
        shape = main.next_queue[pos_in_queue]

        self.image.fill((100, 100, 100))
        col = col_dict[main.shape_id_dict[shape]]

        oy = 3 * pos_in_queue
        ox = 0 if shape != "o" else -1

        cords = main.steps_to_cords(main.shape_dict[shape], (1 + ox, 1 + oy))
        if (self.x, self.y) in cords: id = self.image.fill(col)

class Board_tile(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()
        self.x, self.y = pos

        self.image = pygame.Surface((44, 44))
        self.image.fill((100, 100, 100))

        rect_x = pos[0] * 45 + 735
        rect_y = pos[1] * 45 + 22
        self.rect = self.image.get_rect(topleft = (rect_x, rect_y))
    
    def update(self) -> None:
        id = main.board[self.y][self.x]
        self.image.fill(col_dict[id])
        if (self.x, self.y) in shadow_points and id == 0: self.image.fill((col_dict[8]))

# Board
for row in range(23):
    for col in range(10):
        Tiles.add(Board_tile((col, row)))

# Held
for row in range(4):
    for col in range(2):
        Held_display.add(Held_tile((row, col)))

# Next
for row in range(4):
    for col in range(14):
        Next_queue.add(Next_queue_tile((row, col)))

#============================================================================#

def handle_lattral_movement(keys):
    global preformeing_arr
    movement = False

    held_time = key_time_dict[pygame.K_RIGHT] + key_time_dict[pygame.K_LEFT]
    if keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]: return None
    
    if preformeing_arr and held_time >= senceitivity_dict["ARR"]: movement = True
    elif not preformeing_arr and held_time >= senceitivity_dict["DAS"]: preformeing_arr = True

    if not movement: return None
    if keys[pygame.K_LEFT]: key_time_dict[pygame.K_LEFT] -= senceitivity_dict["ARR"]
    if keys[pygame.K_RIGHT]: key_time_dict[pygame.K_RIGHT] -= senceitivity_dict["ARR"]

    if keys[pygame.K_LEFT]: main.current_shape.move_left()
    if keys[pygame.K_RIGHT]: main.current_shape.move_right()

def handle_verticle_movement(keys):
    if not keys[pygame.K_DOWN]: return None
    if senceitivity_dict["SDF"] == -1: main.current_shape.move_untill_ground()
    if not key_time_dict[pygame.K_DOWN] >= senceitivity_dict["SDF"]: return None

    main.current_shape.move_down()
    key_time_dict[pygame.K_DOWN] -= senceitivity_dict["SDF"]

def handle_movement() -> None:
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]: key_time_dict[pygame.K_RIGHT] += 1
    if keys[pygame.K_LEFT]: key_time_dict[pygame.K_LEFT] += 1
    if keys[pygame.K_DOWN]: key_time_dict[pygame.K_DOWN] += 1
    
    handle_lattral_movement(keys)
    handle_verticle_movement(keys)

#============================================================================#

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
            
            if event.key == pygame.K_RIGHT:
                key_time_dict[pygame.K_RIGHT] = 0
            
            if event.key == pygame.K_LEFT:
                key_time_dict[pygame.K_LEFT] = 0
            
            if event.key == pygame.K_DOWN:
                key_time_dict[pygame.K_DOWN] = 0

            if event.key == pygame.K_0:
                frame = 0
                

        # Key Down
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RIGHT:
                preformeing_arr = False
                key_time_dict[pygame.K_RIGHT] = 0

                main.current_shape.move_right()
            
            if event.key == pygame.K_LEFT:
                preformeing_arr = False
                key_time_dict[pygame.K_LEFT] = 0

                main.current_shape.move_left()

            if event.key == pygame.K_UP:
                main.current_shape.rotate_cw()
            
            if event.key == pygame.K_z:
                main.current_shape.rotate_ccw()
            
            if event.key == pygame.K_a:
                main.current_shape.rotate_180()
            
            if event.key == pygame.K_c:
                if not held_current_piece:
                    main.hold()
                    held_current_piece = True
            
            if event.key == pygame.K_r:
                main.setup()
                debug.__init__()
            
            if event.key == pygame.K_DOWN:
                key_time_dict[pygame.K_DOWN] = 0
    
            if event.key == pygame.K_SPACE:
                held_current_piece = False
                main.current_shape.hard_drop()

    handle_movement() 

    #Render + Update
    main.update_game()
    
    main.current_shape.draw_on_board()
    shadow_points = main.current_shape.get_shadow()

    [i.update() for i in Tiles.sprites()]
    [i.update() for i in Next_queue.sprites()]
    [i.update() for i in Held_display.sprites()]
    
    screen.blit(BACKGROUND_SURF, (0, 0))
    screen.blit(BOARD_BACKGROUND, (460, 0))

    Tiles.draw(screen)
    Next_queue.draw(screen)
    Held_display.draw(screen)
    
    debug.update()
    

    pygame.display.update()

    frame_end = datetime.now()
    frame_time = frame_end - frame_start
    fps = 1 / frame_time.total_seconds()
    #print(fps)

    clock.tick(FPS)