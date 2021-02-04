import pygame
import random

ORANGE = (255, 140, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 10)

FRAME_W = 520
FRAME_H = 520  # 11 posible lines for obstacles

FROG_W = 20
MOVE = FROG_W

STAGE_REWARD = 1000
W_REWARD = 50
STANDING_PUNISH = 20
DEATH_PUNISH = 10000

TICK = pygame.USEREVENT+1
TICK_DELAY = 80

def init_day():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((FRAME_H, FRAME_W))
    pygame.display.set_caption("Frogger")

    alive = True
    running = True
    score = 0
    stage = 0

    frogpos_x, frogpos_y = frog_to_bottom()

    clock = pygame.time.Clock()
    clock.tick(1)

    pygame.time.set_timer(TICK, TICK_DELAY)

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

    return alive, screen, frogpos_x, frogpos_y, lines, score, stage, running, pygame

def die(screen, score):
    print("died with a score of: "+str(score))
    alive = False
    pygame.time.set_timer(TICK, -1)
    #TODO draw endscreen
    default_font = pygame.font.get_default_font()
    font_renderer = pygame.font.Font(default_font, 30)
    score -= DEATH_PUNISH
    label = font_renderer.render("DEFEATED\nSCORE: " + str(score), False, BLACK)
    screen.blit(label, (FRAME_W/2, FRAME_H/2))


def calculate_vehic(lines):
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
                if len(vehicles)<1:
                    vehicles.append([r, 0])
                elif vehicles[len(vehicles) - 1][1] - vehicles[len(vehicles) - 1][0] * FROG_W > 0:
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
    return lines


def check_alive(frogpos_x, frogpos_y, lines):
    for vehicles in lines:
        ix = lines.index(vehicles)
        for v in vehicles:
            if frogpos_y == line_to_y(ix) and v[1] <= frogpos_x <= v[1] + v[0] * FROG_W:
                return False
    return True


def redraw(alive, screen, frogpos_x, frogpos_y, lines, score):
    if alive:
        screen.fill(BLACK)
    else:
        screen.fill(RED)
    # draw score
    default_font = pygame.font.get_default_font()
    font_renderer = pygame.font.Font(default_font, 30)
    label = font_renderer.render("Score: " + str(score), False, WHITE)
    screen.blit(label, (0, 0))
    # draw obstacles
    for vehicles in lines:
        ix = lines.index(vehicles)
        for v in vehicles:
            pygame.draw.rect(screen, YELLOW, [v[1], line_to_y(ix), FROG_W * v[0], FROG_W])
    # draw Frog
    try:
        pygame.draw.rect(screen, WHITE, [frogpos_x, frogpos_y, FROG_W, FROG_W])
        pygame.display.flip()
    except TypeError as e:
        print(screen)
        print(WHITE)
        print(frogpos_x)
        print(frogpos_y)
        print(FROG_W)


def line_to_y(line_number):
    return FRAME_H - (line_number + 1) * 40 - FROG_W


def y_to_line(y_pos):
    return -0.025*y_pos+0.025*FRAME_H-0.025*FROG_W

def frog_to_bottom():
    return FRAME_W / 2, FRAME_H - 2 * FROG_W


def frog_up(frogpos_y):
    if frogpos_y-MOVE >= 0:
        return frogpos_y - MOVE
    else: return frogpos_y


def frog_left(frogpos_x):
    if frogpos_x-MOVE >= 0:
        return frogpos_x - MOVE
    else: return frogpos_x


def frog_right(frogpos_x):
    if frogpos_x+MOVE < FRAME_W:
        return frogpos_x + MOVE
    else: return frogpos_x


def frog_down(frogpos_y):
    if frogpos_y+MOVE < FRAME_H:
        return frogpos_y + MOVE
    else: return frogpos_y


def day(alive, screen, frogpos_x, frogpos_y, lines, score, stage, running, pygame, current_move):
    ticked = False
    while not ticked:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == TICK:
                ticked = True
                if current_move == "w":
                    score += W_REWARD
                    frogpos_y = frog_up(frogpos_y)
                elif current_move == "a":
                    score -= STANDING_PUNISH
                    frogpos_x = frog_left(frogpos_x)
                elif current_move == "s":
                    score -= (STANDING_PUNISH+W_REWARD)
                    frogpos_y = frog_down(frogpos_y)
                elif current_move == "d":
                    score -= STANDING_PUNISH
                    frogpos_x = frog_right(frogpos_x)
                elif current_move == "":
                    score -= STANDING_PUNISH
                calculate_vehic(lines)
                redraw(alive, screen, frogpos_x, frogpos_y, lines, score)
                if frogpos_y < 40:
                    stage += 1
                    score += STAGE_REWARD
                    frogpos_x, frogpos_y = frog_to_bottom()
                alive = check_alive(frogpos_x, frogpos_y, lines)
                if not alive:
                    score -= DEATH_PUNISH
                    pygame.quit()
                    return False, None, frogpos_x, frogpos_y, lines, score, stage, False, None
                return alive, screen, frogpos_x, frogpos_y, lines, score, stage, running, pygame