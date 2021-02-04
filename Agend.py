import numpy as np
import env
import random
import time


def calc_state(lines, frogpos_x, frogpos_y):
    ret = ""
    from_left = env.y_to_line(frogpos_y) % 2 == 0 or env.y_to_line(frogpos_y+env.FROG_W) % 2 == 0
    up_blocked = not env.check_alive(frogpos_x, frogpos_y - env.MOVE, lines)
    left_blocked = not env.check_alive(frogpos_x - env.MOVE, frogpos_y, lines) or frogpos_x - env.MOVE < 0 and from_left
    right_blocked = not env.check_alive(frogpos_x + env.MOVE, frogpos_y, lines) or frogpos_x + env.MOVE > env.FRAME_W and not from_left
    #down_blocked = env.check_alive(frogpos_x, frogpos_y + env.MOVE, lines) or frogpos_y + env.MOVE > env.FRAME_H
    ne_blocked = not env.check_alive(frogpos_x + env.MOVE, frogpos_y - env.MOVE, lines) or frogpos_x + env.MOVE > env.FRAME_W and from_left
    nw_blocked = not env.check_alive(frogpos_x - env.MOVE, frogpos_y - env.MOVE, lines) or frogpos_x - env.MOVE < 0 and not from_left
    #se_blocked = env.check_alive(frogpos_x + env.MOVE, frogpos_y + env.MOVE, lines) or frogpos_x + env.MOVE > env.FRAME_W
    #sw_blocked = env.check_alive(frogpos_x - env.MOVE, frogpos_y + env.MOVE, lines) or frogpos_x - env.MOVE < 0
    nee_blocked = not env.check_alive(frogpos_x + 2*env.MOVE, frogpos_y - env.MOVE, lines) or frogpos_x + 2*env.MOVE > env.FRAME_W
    nww_blocked = not env.check_alive(frogpos_x - 2*env.MOVE, frogpos_y - env.MOVE, lines) or frogpos_x - 2*env.MOVE < 0
    #see_blocked = env.check_alive(frogpos_x + 2*env.MOVE, frogpos_y + env.MOVE, lines) or frogpos_x + 2*env.MOVE > env.FRAME_W
    #sww_blocked = env.check_alive(frogpos_x - 2*env.MOVE, frogpos_y + env.MOVE, lines) or frogpos_x - 2*env.MOVE < 0
    right_third = frogpos_x >= (2/3)*env.FRAME_W
    left_third = frogpos_x <= env.FRAME_W/3
    if from_left:
        ret += "1"
    else:
        ret += "0"
    if up_blocked:
        ret += "1"
    else:
        ret += "0"
    if ne_blocked:
        ret += "1"
    else:
        ret += "0"
    if right_blocked:
        ret += "1"
    else:
        ret += "0"
    #if se_blocked:
    #    ret += "1"
    #else:
    #    ret += "0"
    #if down_blocked:
    #    ret += "1"
    #else:
    #    ret += "0"
    #if sw_blocked:
    #    ret += "1"
    #else:
    #    ret += "0"
    if left_blocked:
        ret += "1"
    else:
        ret += "0"
    if nw_blocked:
        ret += "1"
    else:
        ret += "0"
    if nww_blocked:
        ret += "1"
    else:
        ret += "0"
    if nee_blocked:
        ret += "1"
    else:
        ret += "0"
    #if sww_blocked:
    #    ret += "1"
    #else:
    #    ret += "0"
    #if see_blocked:
    #    ret += "1"
    #else:
    #    ret += "0"
    if left_third:
        ret += "1"
    else:
        ret += "0"
    if right_third:
        ret += "1"
    else:
        ret += "0"
    return int(ret, base=2)


def translate(act):
    if act == 0:
        return "w"
    if act == 1:
        return "a"
    if act == 2:
        return "s"
    if act == 3:
        return "d"
    if act == 4:
        return ""
    if act == "w":
        return 0
    if act == "a":
        return 1
    if act == "s":
        return 2
    if act == "d":
        return 3
    if act == "":
        return 4


#q_table = np.zeros((np.power(2, 10), 5))
q_table = np.loadtxt(open("q_table_less_info.csv", "rb"), delimiter=",", skiprows=0)
num_days = 10000
min_steps_per_day = 1000
max_steps_per_day = 100000
learning_rate = 0.1
discount_rate = 0.99
max_exploration_rate = 0.001#1
min_exploration_rate = 0.0001
exploration_rate = max_exploration_rate
exploration_decay_rate = 1#0.001

# keep track of score to see improvement
score_per_day = []

for day in range(num_days):
    print("Day: " + str(day))
    alive, screen, frogpos_x, frogpos_y, lines, score, stage, running, pygame = env.init_day()
    state = calc_state(lines, frogpos_x, frogpos_y)
    old_score = score
    #print(exploration_rate)
    step = 0
    interrupt = False
    while not interrupt:
        step += 1
        if alive:
            #print("Step: " + str(step))
            #print("left" if frogpos_x <= env.FRAME_W/3 else "right" if frogpos_x >= 2*env.FRAME_W/3 else "center")
            #print(state)
            exploration_rate_threshold = random.uniform(0, 1)
            if exploration_rate_threshold > exploration_rate:
                #if env.check_alive(frogpos_x, frogpos_y - env.MOVE, lines) and \
                #    (env.check_alive(frogpos_x + env.MOVE, frogpos_y - env.MOVE, lines) or frogpos_x + env.MOVE > env.FRAME_W) \
                #    and (env.check_alive(frogpos_x - env.MOVE, frogpos_y - env.MOVE, lines) or frogpos_x - env.MOVE < 0):
                #    action = "w"
                #else:
                #    action = ""
                # exploit
                action = np.argmax(q_table[state, :]) #return column index of biggest values in row (smallest index for several maxima)
                action = translate(action)
            else:
                # explore
                action = translate(random.randint(0, 5))
            alive, screen, frogpos_x, frogpos_y, lines, score, stage, running, pygame = \
                env.day(alive, screen, frogpos_x, frogpos_y, lines, score, stage, running, pygame, action)

            new_state = calc_state(lines, frogpos_x, frogpos_y)
            reward = score - old_score

            if not alive and not exploration_rate_threshold > exploration_rate:
                print("Died cause random")
            elif not alive and not q_table[state].all == 0:
                print(q_table[state])
                print("Died cause intentional: "+str(action)+" at state: "+str(state))

            #print(reward)
            q_table[state, translate(action)] = q_table[state, translate(action)] * (1 - learning_rate) + \
                learning_rate * (reward + discount_rate * np.max(q_table[new_state, :]))

            state = new_state
            old_score = score
        else:
            break
        x = random.randint(min_steps_per_day*min_steps_per_day, max_steps_per_day*max_steps_per_day)
        if step*step > x:
            interrupt = True

    exploration_rate = min_exploration_rate + \
        (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate * day)
    #print(score)
    score_per_day.append(score)
    np.savetxt("q_table_less_info.csv", q_table, delimiter=",")


print(q_table)
print(score_per_day)
