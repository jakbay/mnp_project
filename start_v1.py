import sys, pygame, math
import neatV1 

pygame.init()

size = width, height = 1400, 800 #previously width was 800
neatV1.HEIGHT = height
speed = [2, 2]

rlength = 30
rwidth = 10
vmax = 0.1

#init
screen = pygame.display.set_mode(size)

delta_mass = -(30e2) #kg/s
fuel_mass = 1e6
dry_mass = 120000 #kg
rocket_mass = dry_mass + fuel_mass
v_exhaust = -3*3280e-2 #(m/s)
vy_rocket = 0 #(m/s)
gravity = 9.81e-2 #(m/s^2)
engineON = False

DEAD_ROCKET = []
GENERATION_COUNT = 100
neatV1.GENERATION_COUNT = GENERATION_COUNT
generations_left = GENERATION_COUNT
POPULATION_SIZE = 200
ROCKET_AGENTS = []
TIME_ELAPSED = 0

T = v_exhaust * delta_mass

run = True

class Rocket:
    def __init__(self):
        self.rocket = pygame.transform.scale(pygame.image.load("resource/rocket.png").convert_alpha(), [rwidth, rlength])
        self.x = (width/2)-self.rocket.get_width()/2
        self.y = 0
        self.rect = self.rocket.get_rect()
        self.rect.x = self.x
        self.rect.y = 0
        self.vx_rocket = 0
        self.vy_rocket = 0
        self.fuel_left = fuel_mass

Algo = neatV1.Neat(POPULATION_SIZE,GENERATION_COUNT)

Algo.init_first_generation()

ROCKET_AGENTS = [None] * POPULATION_SIZE
for i in range(POPULATION_SIZE):
    ROCKET_AGENTS[i] = Rocket()


while run and generations_left:
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill("black")
    TIME_ELAPSED += 1

    for i in range(POPULATION_SIZE):
        if i not in DEAD_ROCKET:
            engineON = Algo.agents[i].getOutput(ROCKET_AGENTS[i].vy_rocket,ROCKET_AGENTS[i].rect.y)
            
            if engineON and ROCKET_AGENTS[i].fuel_left > abs(delta_mass):
                ROCKET_AGENTS[i].vy_rocket = ROCKET_AGENTS[i].vy_rocket -T/ROCKET_AGENTS[i].fuel_left + gravity
                ROCKET_AGENTS[i].fuel_left += delta_mass
            else: 
                ROCKET_AGENTS[i].vy_rocket += gravity

            screen.blit(ROCKET_AGENTS[i].rocket, ROCKET_AGENTS[i].rect)
            
            if ROCKET_AGENTS[i].rect.y <= height - 30 and ROCKET_AGENTS[i].rect.y >= -100 and ROCKET_AGENTS[i].fuel_left > 0:
                ROCKET_AGENTS[i].rect = ROCKET_AGENTS[i].rect.move(ROCKET_AGENTS[i].vx_rocket,ROCKET_AGENTS[i].vy_rocket)
                Algo.agents[i].y = height - 30 - ROCKET_AGENTS[i].rect.y
                if Algo.agents[i].y < Algo.agents[i].y_min:
                    Algo.agents[i].y_min = Algo.agents[i].y
            
            else:
                DEAD_ROCKET.append(i)
                Algo.agents[i].v_final = math.sqrt((ROCKET_AGENTS[i].vx_rocket)**2 + (ROCKET_AGENTS[i].vy_rocket)**2)
                if (height - 30 - ROCKET_AGENTS[i].rect.y < 0):
                    Algo.agents[i].y = 0
                    Algo.agents[i].distance = 0
                else:
                    Algo.agents[i].y = height - 30 - ROCKET_AGENTS[i].rect.y
                    Algo.agents[i].distance = height - 30 - ROCKET_AGENTS[i].rect.y
                Algo.agents[i].fuel_left = ROCKET_AGENTS[i].fuel_left


    if len(DEAD_ROCKET) == POPULATION_SIZE:
        print("GENERATION : ", (GENERATION_COUNT - generations_left + 1))
        generations_left -= 1
        neatV1.t += 1
        if generations_left == 1:
            Algo.stop_generation(True)
        else:
            Algo.stop_generation()
        DEAD_ROCKET = []
        TIME_ELAPSED = 0
        ROCKET_AGENTS = [None] * POPULATION_SIZE
        for i in range(POPULATION_SIZE):
            ROCKET_AGENTS[i] = Rocket()
    pygame.display.flip()
    
pygame.quit()
sys.exit()

