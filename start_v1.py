import sys, pygame
import neatV1 

pygame.init()

size = width, height = 1400, 800 #previously width was 800
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
v_rocket = 0 #(m/s)
gravity = 9.81e-2 #(m/s^2)
engineON = False

DEAD_ROCKET = []
GENERATION_COUNT = 10
POPULATION_SIZE = 100
ROCKET_AGENTS = []
TIME_ELAPSED = 0

class Rocket:
    def __init__(self):
        self.rocket = pygame.transform.scale(pygame.image.load("resource/rocket.png"), [rwidth, rlength])
        self.x = (width/2)-self.rocket.get_width()/2
        self.y = 0
        self.rect =  self.rocket.get_rect()
        self.rect.move(width/2,0)
        self.v_rocket = 0
        self.fuel_left = fuel_mass

Algo = neatV1.Neat(POPULATION_SIZE,GENERATION_COUNT)

Algo.init_first_generation()

for i in range(POPULATION_SIZE):
    ROCKET_AGENTS.append(Rocket())


while GENERATION_COUNT:
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run = False

    screen.fill("black")
    TIME_ELAPSED += 1

    for i in range(POPULATION_SIZE):
        if i not in DEAD_ROCKET:
            engineON = Algo.agents[i].getOutput(ROCKET_AGENTS[i].v_rocket,ROCKET_AGENTS[i].rect.y)
            
            if engineON:
                ROCKET_AGENTS[i].v_rocket = ROCKET_AGENTS[i].v_rocket -(v_exhaust * delta_mass)/ROCKET_AGENTS[i].fuel_left + gravity
                ROCKET_AGENTS[i].fuel_left += delta_mass 
            else: 
                ROCKET_AGENTS[i].v_rocket += gravity

            screen.blit(ROCKET_AGENTS[i].rocket, ROCKET_AGENTS[i].rect)
            
            if ROCKET_AGENTS[i].rect.y < height - 30 and ROCKET_AGENTS[i].rect.y > -100 and ROCKET_AGENTS[i].fuel_left > 0:
                ROCKET_AGENTS[i].rect = ROCKET_AGENTS[i].rect.move(0,ROCKET_AGENTS[i].v_rocket)
            
            else:
                DEAD_ROCKET.append(i)
                Algo.agents[i].v_final = ROCKET_AGENTS[i].v_rocket
                Algo.agents[i].fuel_left = ROCKET_AGENTS[i].fuel_left
                Algo.agents[i].distance = 1000 - ROCKET_AGENTS[i].rect.y

    if len(DEAD_ROCKET) == 100:
        print("GENERATION : ", (11 - GENERATION_COUNT))
        GENERATION_COUNT -= 1
        if GENERATION_COUNT == 1:
            Algo.stop_generation(True)
        else:
            Algo.stop_generation()
        DEAD_ROCKET = []
        TIME_ELAPSED = 0
        ROCKET_AGENTS = []
        for i in range(POPULATION_SIZE):
            ROCKET_AGENTS.append(Rocket())

    pygame.time.wait(1)
    pygame.display.flip()
    
pygame.quit()
sys.exit()

