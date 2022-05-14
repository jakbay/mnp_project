import sys, pygame, math
import random
import gc
import neatV1
import numpy as np
import pandas as pd

size = width, height = 350, 800 #previously width was 800
neatV1.HEIGHT = height
speed = [2, 2]

rlength = 30
rwidth = 10
vmax = 0.1

screen = 0

black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0

mleft = 50 # marge de gauche
mright = 50 # marge de droite
mbottom = 50 # marge du bas
mtop = 50 # marge du haut

YTOP = mtop
YBOTTOM = height - mbottom - rlength

SCALE_T = 10**(-2)
h0 = 2.5 * (height + mtop - mbottom)
SCALE_pix = (height - mbottom) / h0

delta_mass = -(3000) #kg/s
fuel_mass = 1e5
dry_mass = 120000 #kg
rocket_mass = dry_mass + fuel_mass
v_exhaust = -3*3280 * SCALE_T #(m/s)
vy_rocket = 0 #(m/s)
gravity = 9.8 * SCALE_T #(m/s^2)
engineON = False

DEAD_ROCKET = []
GENERATION_COUNT = 50
neatV1.GENERATION_COUNT = GENERATION_COUNT
generations_left = GENERATION_COUNT
POPULATION_SIZE = 200
ROCKET_AGENTS = []
TIME_ELAPSED = 0
CAMPER_REMOVAL = 1000 / SCALE_T

DT_DATA_RECORDING = 1
MAX_MEM_SIZE = round(CAMPER_REMOVAL * 1.1)
current_data = np.empty((POPULATION_SIZE, 4, MAX_MEM_SIZE), dtype=object)
recorded_data = np.empty((GENERATION_COUNT, 4, MAX_MEM_SIZE), dtype=object)

T = (v_exhaust * delta_mass)
fourchette_min = 0

class Rocket:
    def __init__(self, dh0):
        self.rocket = pygame.transform.scale(pygame.image.load("resource/rocket.png").convert_alpha(), [rwidth, rlength])
        self.x = (width/2)-self.rocket.get_width()/2
        global fourchette_min
        if dh0:
            fourchette_min = round((h0/((0.5 * GENERATION_COUNT)))*(1/(2-(GENERATION_COUNT-generations_left)/GENERATION_COUNT)))
        else:
            fourchette_min = 0
        self.y = h0 - random.randint(0, fourchette_min)
        self.y_last = self.y
        self.rect = self.rocket.get_rect()
        self.rect.x = self.x
        self.rect.y = height - self.y * SCALE_pix
        self.vx_rocket = 0
        self.vy_rocket = 0
        self.fuel_left = fuel_mass
        self.camper = 0
        self.remove = False

def main_loop(dh0=False):
    Algo = neatV1.Neat(POPULATION_SIZE,GENERATION_COUNT)

    Algo.init_first_generation()

    ROCKET_AGENTS = [None] * POPULATION_SIZE
    for i in range(POPULATION_SIZE):
        ROCKET_AGENTS[i] = Rocket(dh0)

    run = True
    global generations_left
    global TIME_ELAPSED
    global DEAD_ROCKET
    global current_data
    global recorded_data
    while run and generations_left:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill("black")
        TIME_ELAPSED += 1
        for i in range(POPULATION_SIZE):
            if i not in DEAD_ROCKET:
                if TIME_ELAPSED % DT_DATA_RECORDING == 0:
                    idx = int(TIME_ELAPSED/DT_DATA_RECORDING) - 1
                    current_data[i][0][idx] = Algo.agents[i].id
                    current_data[i][1][idx] = ROCKET_AGENTS[i].y
                    current_data[i][2][idx] = ROCKET_AGENTS[i].vy_rocket
                    current_data[i][3][idx] = ROCKET_AGENTS[i].fuel_left
                engineON = Algo.agents[i].getOutput(ROCKET_AGENTS[i].vy_rocket,ROCKET_AGENTS[i].y)

                if ROCKET_AGENTS[i].y == ROCKET_AGENTS[i].y_last:
                    ROCKET_AGENTS[i].camper += 1
                else:
                    ROCKET_AGENTS[i].y_last = ROCKET_AGENTS[i].y
                    ROCKET_AGENTS[i].camper = 0
                if ROCKET_AGENTS[i].camper >= CAMPER_REMOVAL:
                    ROCKET_AGENTS[i].remove = True
                if (engineON and ROCKET_AGENTS[i].fuel_left > abs(delta_mass)) or TIME_ELAPSED >= CAMPER_REMOVAL or ROCKET_AGENTS[i].remove:
                    if TIME_ELAPSED >= CAMPER_REMOVAL:
                        print("Terminating current generation.")
                    ROCKET_AGENTS[i].vy_rocket = ROCKET_AGENTS[i].vy_rocket -T/ROCKET_AGENTS[i].fuel_left + gravity
                    ROCKET_AGENTS[i].fuel_left += delta_mass * SCALE_T
                else:
                    ROCKET_AGENTS[i].vy_rocket += gravity

                screen.blit(ROCKET_AGENTS[i].rocket, ROCKET_AGENTS[i].rect)
                pygame.draw.line(screen, white, (mleft, mtop), (mleft, height - mbottom))
                pygame.draw.line(screen, white, (mleft, height - mbottom), (width - mright, height - mbottom))

                if ROCKET_AGENTS[i].rect.y <= YBOTTOM and ROCKET_AGENTS[i].rect.y >= 0 and ROCKET_AGENTS[i].fuel_left > 0:
                    ROCKET_AGENTS[i].rect = ROCKET_AGENTS[i].rect.move(ROCKET_AGENTS[i].vx_rocket,ROCKET_AGENTS[i].vy_rocket * SCALE_pix)
                    Algo.agents[i].y =(YBOTTOM - ROCKET_AGENTS[i].rect.y + rlength) / SCALE_pix
                    ROCKET_AGENTS[i].y = Algo.agents[i].y
                    if Algo.agents[i].y < Algo.agents[i].y_min:
                        Algo.agents[i].y_min = Algo.agents[i].y

                else:
                    DEAD_ROCKET.append(i)
                    Algo.agents[i].v_final = math.sqrt((ROCKET_AGENTS[i].vx_rocket)**2 + (ROCKET_AGENTS[i].vy_rocket)**2)
                    if (YBOTTOM - ROCKET_AGENTS[i].rect.y < 0):
                        Algo.agents[i].y = 0
                        Algo.agents[i].distance = 0
                    else:
                        Algo.agents[i].y = YBOTTOM - ROCKET_AGENTS[i].rect.y
                        Algo.agents[i].distance = YBOTTOM - ROCKET_AGENTS[i].rect.y - rlength
                    Algo.agents[i].fuel_left = ROCKET_AGENTS[i].fuel_left

        if len(DEAD_ROCKET) == POPULATION_SIZE:
            print("GENERATION : ", (GENERATION_COUNT - generations_left + 1))
            generations_left -= 1
            neatV1.t += 1
            bestID = Algo.stop_generation(generations_left == 1)
            for i in range(POPULATION_SIZE):
                if current_data[i][0][0] == bestID:
                    for j in range(MAX_MEM_SIZE):
                        if current_data[i][0][j] == None:
                            break
                        recorded_data[GENERATION_COUNT - generations_left - 1][0][j] = current_data[i][0][j]
                        recorded_data[GENERATION_COUNT - generations_left - 1][1][j] = current_data[i][1][j]
                        recorded_data[GENERATION_COUNT - generations_left - 1][2][j] = current_data[i][2][j]
                        recorded_data[GENERATION_COUNT - generations_left - 1][3][j] = current_data[i][3][j]
                    break
            current_data = np.empty((POPULATION_SIZE, 4, MAX_MEM_SIZE), dtype=object)
            Algo.clear_fitness_arr()
            DEAD_ROCKET = []
            TIME_ELAPSED = 0
            ROCKET_AGENTS = [None] * POPULATION_SIZE
            for i in range(POPULATION_SIZE):
                ROCKET_AGENTS[i] = Rocket(dh0)
            print("Conditions initiales : hmax =", h0, "hmin =", h0 - fourchette_min)
        pygame.display.flip()

pygame.init()
screen = pygame.display.set_mode(size)
main_loop()

for i in range(GENERATION_COUNT):
    data = recorded_data[i][:]
    df = pd.DataFrame({'id': data[0], 'h': data[1], 'v': data[2], 'fuel': data[3]})
    df = df[df['id'].notna()]
    df = df[df['h'].notna()]
    df = df[df['v'].notna()]
    df = df[df['fuel'].notna()]
    df.to_csv("data/generation"+str(i)+".csv")
pygame.quit()
gc.collect()
globals().clear()

