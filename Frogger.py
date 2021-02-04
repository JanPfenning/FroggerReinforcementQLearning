import pygame
import random
import threading

pygame.init()
pygame.font.init()
default_font = pygame.font.get_default_font()
font_renderer = pygame.font.Font(default_font, 15)

ORANGE = (255, 140, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 10)

FRAME_W = 520
FRAME_H = 520 #11 posible lines for obstacles

FROG_W = 20
MOVE = FROG_W

screen = pygame.display.set_mode((FRAME_H, FRAME_W))
pygame.display.set_caption("Frogger")

alive = True
running = True
score = 0
stage = 0
current_move = " "

frogpos_x = 0
frogpos_y = 0

clock = pygame.time.Clock()
clock.tick(1)

DRIVE = pygame.USEREVENT+1
pygame.time.set_timer(DRIVE, 100)


def init():
    global frogpos_y, frogpos_x
    frogpos_x = FRAME_W / 2
    frogpos_y = FRAME_H - 2 * FROG_W


def frog_up():
    global frogpos_y
    if frogpos_y-MOVE >= 0:
        frogpos_y -= MOVE


def frog_left():
    global frogpos_x
    if frogpos_x-MOVE >= 0:
        frogpos_x -= MOVE


def frog_right():
    global frogpos_x
    if frogpos_x+MOVE < FRAME_W:
        frogpos_x += MOVE


def frog_down():
    global frogpos_y
    if frogpos_y+MOVE < FRAME_H:
        frogpos_y += MOVE


# lines: [l1,l2,l3,...,]
# line (l1): [v1,v2,v3]
# vehicle (v1): [length, cur_x]
lines = [[] for i in range(11)]
lines[0] = [[2, 0]]
lines[1] = [[2, FRAME_W]]
lines[2] = [[2, 0]]
lines[3] = [[2, FRAME_W]]
lines[4] = [[2, 0]]
lines[5] = [[2, FRAME_W]]
lines[6] = [[2, 0]]
lines[7] = [[2, FRAME_W]]
lines[8] = [[2, 0]]
lines[9] = [[2, FRAME_W]]
lines[10] = [[2, 0]]


def die():
    global alive, FRAME_H, FRAME_W, BLACK, score
    print("died with a score of: "+str(score))
    alive = False
    pygame.time.set_timer(DRIVE, -1)
    #TODO draw endscreen
    font_renderer = pygame.font.Font(default_font, 30)
    label = font_renderer.render("DEFEATED\nSCORE: " + str(score), False, BLACK)
    screen.blit(label, (FRAME_W/2, FRAME_H/2))


def line_to_y(line_number):
    return FRAME_H - (line_number + 1) * 40 - FROG_W


def calculate_vehic():
    global lines, FROG_W, FRAME_W, FRAME_H
    for vehicles in lines:
        obst_count = 0
        ix = lines.index(vehicles)
        for v in vehicles:
            if ix % 2 == 0:
                v[1] += FROG_W
                if v[1] > FRAME_W:
                    vehicles.remove(v)
                else:
                    obst_count += v[0]
            else:
                v[1] -= FROG_W
                if v[1] < 0 - v[0] * FROG_W:
                    vehicles.remove(v)
                else:
                    obst_count += v[0]
        if obst_count < 5:
            r = random.randint(2, 6)
            # coming from left
            if ix % 2 == 0:
                if vehicles[len(vehicles) - 1][1] - vehicles[len(vehicles) - 1][0] * FROG_W > 0:
                    vehicles.append([r, 0])
            # coming from right
            else:
                if vehicles[len(vehicles) - 1][1] + vehicles[len(vehicles) - 1][0] * FROG_W < FRAME_W:
                    vehicles.append([r, FRAME_W])
        if obst_count < 15:
            r = random.randint(0, 5)
            if r == 1:
                r = random.randint(2, 6)
                # coming from left
                if ix % 2 == 0:
                    if vehicles[len(vehicles) - 1][1] - vehicles[len(vehicles) - 1][0] * FROG_W > 0:
                        vehicles.append([r, 0])
                # coming from right
                else:
                    if vehicles[len(vehicles) - 1][1] + vehicles[len(vehicles) - 1][0] * FROG_W < FRAME_W:
                        vehicles.append([r, FRAME_W])


def check_alive():
    global alive, frogpos_x, frogpos_y, lines
    for vehicles in lines:
        ix = lines.index(vehicles)
        for v in vehicles:
            if frogpos_y == line_to_y(ix) and v[1] <= frogpos_x <= v[1] + v[0] * FROG_W:
                die()


def redraw():
    if alive:
        # Redraw
        screen.fill(BLACK)
    else:
        screen.fill(RED)
    # draw score
    label = font_renderer.render("Score: " + str(score), False, WHITE)
    screen.blit(label, (0, 0))
    # draw obstacles
    for vehicles in lines:
        ix = lines.index(vehicles)
        for v in vehicles:
            pygame.draw.rect(screen, YELLOW, [v[1], line_to_y(ix), FROG_W * v[0], FROG_W])
    # draw Frog
    pygame.draw.rect(screen, WHITE, [frogpos_x, frogpos_y, FROG_W, FROG_W])
    pygame.display.flip()


init()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                current_move = "w"
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                current_move = "a"
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                current_move = "s"
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                current_move = "d"
        if event.type == DRIVE:
            if current_move == "w":
                frog_up()
                current_move = ""
            elif current_move == "a":
                frog_left()
                current_move = ""
            elif current_move == "s":
                frog_down()
                current_move = ""
            elif current_move == "d":
                frog_right()
                current_move = ""
            calculate_vehic()
            check_alive()
            redraw()
            if frogpos_y < 40:
                stage += 1
                score += 100
                init()

pygame.quit()
