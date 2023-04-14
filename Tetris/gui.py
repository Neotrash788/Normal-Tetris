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
        self.text_clear_type = "None"
        self.display_clear = False
        self.frame = -1
        self.display_spin = False

    def get_text(self):
        if main.all_clear: self.all_clear = True

        self.text_combo = f"{main.combo} Combo"
        self.display_combo = True if main.combo >= 1 else False

        self.text_back_to_back = f"B2B x{main.back_to_back}"
        self.display_back_to_back = True if main.back_to_back >= 1 else False

        self.text_attack_sent = f"{main.attack_sent}"
        self.text_lines_cleared = f"{main.lines_cleared}"

        spin_text = spin_type_dict[main.current_shape.spin_type]
        self.display_spin = False if spin_text == None else True
        self.text_spin = f"{spin_text}"

        atack_per_line = round(main.attack_per_line, 2)
        self.text_atack_per_line = f"{atack_per_line}"

        atack_per_piece = round(main.attack_per_piece, 2)
        self.text_atack_per_piece = f"{atack_per_piece}"

    def render_text(self):
        # Atack / Line
        # ========================================================================= #
        font = pygame.font.Font("UbuntuMono-Bold.ttf", 35)

        title_surf = font.render("Efficiency", True, (120, 104, 0))
        title_rect = title_surf.get_rect(midtop = (90, 0))

        value_surf = font.render(self.text_atack_per_line, True, (120, 104, 0))
        value_rect = value_surf.get_rect(midtop = (90, 50))

        unit_surf = font.render("Atk / Line", True, (120, 104, 0))
        unit_rect = title_surf.get_rect(midtop = (90, 105))

        box = pygame.Surface((180, 60))
        box = box.get_rect(topleft = (0, 40))

        self.surf_atack_per_line = pygame.Surface((180, 135), pygame.SRCALPHA)
        self.rect_atack_per_line = self.surf_atack_per_line.get_rect(midtop = (595, 120))
        
        self.surf_atack_per_line.blit(title_surf, title_rect)
        self.surf_atack_per_line.blit(value_surf, value_rect)
        self.surf_atack_per_line.blit(unit_surf, unit_rect)

        pygame.draw.rect(self.surf_atack_per_line, (200, 200, 200), box, 5)

        # Atack / Piece
        # ========================================================================= #
        title_surf = font.render("Efficiency", True, (120, 104, 0))
        title_rect = title_surf.get_rect(midtop = (90, 0))

        value_surf = font.render(self.text_atack_per_piece, True, (120, 104, 0))
        value_rect = value_surf.get_rect(midtop = (90, 50))

        font = pygame.font.Font("UbuntuMono-Bold.ttf", 32)

        unit_surf = font.render("Atk / Piece", True, (120, 104, 0))
        unit_rect = title_surf.get_rect(midtop = (90, 105))

        font = pygame.font.Font("UbuntuMono-Bold.ttf", 35)

        box = pygame.Surface((180, 60))
        box = box.get_rect(topleft = (0, 40))

        self.surf_atack_per_piece = pygame.Surface((180, 135), pygame.SRCALPHA)
        self.rect_atack_per_piece = self.surf_atack_per_piece.get_rect(midtop = (595, 285))
        
        self.surf_atack_per_piece.blit(title_surf, title_rect)
        self.surf_atack_per_piece.blit(value_surf, value_rect)
        self.surf_atack_per_piece.blit(unit_surf, unit_rect)

        pygame.draw.rect(self.surf_atack_per_piece, (200, 200, 200), box, 5)
        
        # B2B
        # ========================================================================= #
        font = pygame.font.Font("UbuntuMono-Bold.ttf", 30)

        title_surf = font.render("Back To Back", True, (120, 104, 0))
        title_rect = title_surf.get_rect(midtop = (90, 0))

        font = pygame.font.Font("UbuntuMono-Bold.ttf", 35)

        value_surf = font.render(self.text_back_to_back, True, (120, 104, 0))
        value_rect = value_surf.get_rect(midtop = (90, 45))

        box = pygame.Surface((180, 60))
        box = box.get_rect(topleft = (0, 35))

        self.surf_back_to_back = pygame.Surface((180, 100), pygame.SRCALPHA)
        self.rect_back_to_back = self.surf_atack_per_piece.get_rect(midtop = (595, 445))

        self.surf_back_to_back.blit(title_surf, title_rect)
        self.surf_back_to_back.blit(value_surf, value_rect)

        pygame.draw.rect(self.surf_back_to_back, (200, 200, 200), box, 5)

        # Lines Cleared (This Piece)
        # ========================================================================= #
        font = pygame.font.Font("UbuntuMono-Bold.ttf", 35 + (self.frame // 2))

        pos = (595, 575) if self.display_back_to_back else (595, 450)

        self.surf_clear_type = font.render(self.text_clear_type, True, (120, 104, 0))
        self.rect_clear_type = self.surf_clear_type.get_rect(center = pos)

        self.surf_clear_type.set_alpha(240 - (self.frame * 4))

        if self.display_clear: self.frame += 1
        if self.frame >= 60: self.display_clear = False

        # Spin Text
        # ========================================================================= #
        font = pygame.font.Font("UbuntuMono-Bold.ttf", 30)

        shape_id = shape_id_dict[main.current_shape.shape]

        pos = (595, 575) if self.display_back_to_back else (595, 450)
        #pos = (595, 540) if self.display_back_to_back else (595, 440)

        self.surf_spin = font.render(self.text_spin, True, (col_dict[shape_id]))
        self.rect_spin = self.surf_spin.get_rect(center = pos)

        # The next 2 could be done useing seprate classes 
        # But its only 2 objects so its not worth it and could be confused with the above ones

        # Atack
        # ========================================================================= #
        font = pygame.font.Font("UbuntuMono-Bold.ttf", 35)

        title_surf = font.render("Atack Sent", True, (150, 60, 60))
        title_rect = title_surf.get_rect(midtop = (90, 0))

        box_surf = font.render("[        ]", True, (150, 60, 60))
        box_rect = box_surf.get_rect(midtop = (90, 40))

        value_surf = font.render(self.text_attack_sent, True, (150, 60, 60))
        value_rect = value_surf.get_rect(midtop = (90, 40))

        self.surf_atack = pygame.Surface((180, 80), pygame.SRCALPHA)
        self.rect_atack = self.surf_atack_per_line.get_rect(midtop = (1325, 660))

        self.surf_atack.blit(box_surf, box_rect)
        self.surf_atack.blit(title_surf, title_rect)
        self.surf_atack.blit(value_surf, value_rect)

        # Total Lines Cleard
        # ========================================================================= #
        
        title_surf = font.render("Lines", True, (150, 60, 60))
        title_rect = title_surf.get_rect(midtop = (90, 0))

        box_surf = font.render("[        ]", True, (150, 60, 60))
        box_rect = box_surf.get_rect(midtop = (90, 40))

        value_surf = font.render(self.text_lines_cleared, True, (150, 60, 60))
        value_rect = value_surf.get_rect(midtop = (90, 40))

        self.surf_lines_cleard = pygame.Surface((180, 80), pygame.SRCALPHA)
        self.rect_lines_cleard = self.surf_lines_cleard.get_rect(midtop = (1325, 760))

        self.surf_lines_cleard.blit(box_surf, box_rect)
        self.surf_lines_cleard.blit(title_surf, title_rect)
        self.surf_lines_cleard.blit(value_surf, value_rect)

        # Combo
        # ========================================================================= #

        box_surf = font.render("[        ]", True, (150, 60, 60))
        box_rect = box_surf.get_rect(midtop = (90, 0))

        value_surf = font.render(self.text_combo, True, (150, 60, 60))
        value_rect = value_surf.get_rect(midtop = (90, 0))

        self.surf_combo = pygame.Surface((180, 40), pygame.SRCALPHA)
        self.rect_combo = self.surf_combo.get_rect(midtop = (1325, 875))

        self.surf_combo.blit(box_surf, box_rect)
        self.surf_combo.blit(value_surf, value_rect)
        # ========================================================================= #



    def get_new_clear(self):
        # Calculateed useing the diffrance in total lines cleard
        if self.pieces_placed != main.pices_placed:

            if self.lines_cleared != main.lines_cleared:
                self.display_clear = True
                self.frame = 0
                self.text_clear_type = clear_type_dict[main.lines_cleared - self.lines_cleared]
                self.lines_cleared = main.lines_cleared

            #else: self.display_clear = False
            self.pieces_placed = main.pices_placed
    
    def update(self):
        self.get_text()
        self.render_text()
        self.get_new_clear()

        screen.blit(self.surf_atack_per_line, self.rect_atack_per_line)
        screen.blit(self.surf_atack_per_piece, self.rect_atack_per_piece)
        screen.blit(self.surf_atack, self.rect_atack)
        screen.blit(self.surf_lines_cleard, self.rect_lines_cleard)


        if self.display_combo: screen.blit(self.surf_combo, self.rect_combo)
        if self.display_spin: screen.blit(self.surf_spin, self.rect_spin)
        if self.display_back_to_back: screen.blit(self.surf_back_to_back, self.rect_back_to_back)
        if self.display_clear: screen.blit(self.surf_clear_type, self.rect_clear_type)


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
