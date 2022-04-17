#Sur le côté avoir une barre qui défile avec la hauteur afficher
#On fait descendre la camera avec la surface on veut un grand truc et on zoom pour faire croire que c'est haut
#Fairematcher distance et vitesse out ça en etant lent pour observer
#On fait défiler l'écran pas la fusée qui reste statique à part quand on est sur les dernier mille metre
#Diagramme des phases en display
import sys, pygame
pygame.init()

size = width, height = 800, 1000
speed = [2, 2]
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
mleft = 50 # marge de gauche
mright = 50 # marge de droite
mbottom = 50 # marge du bas
mtop = 50 # marge du haut

rlength = 30
rwidth = 10
vmax = 0.1

SCALE_T = 10**(-3)

h0 = (height - mbottom) / SCALE_T
h = h0

SCALE_pix = (height - mbottom) / h0

v_rocket = 0.0
gravity = 9.81 * SCALE_T
thrust = 20.0 * SCALE_T

screen = pygame.display.set_mode(size)

rocket = pygame.transform.scale(pygame.image.load("rocket.png"), [rwidth, rlength])
rocket_rect = rocket.get_rect()
rocket_rect = rocket_rect.move((width/2)-rocket.get_width()/2,0)

run = True

font = pygame.font.SysFont("Consolas.ttf", 25)
death = font.render("Vous êtes décédé.", False, red)
deathRect = death.get_rect()
deathRect.x = width / 2
deathRect.y = height / 2
success = font.render("Vous avez atterri.", False, green)
successRect = death.get_rect()
successRect.x = width / 2
successRect.y = height / 2

deltaBoost2 = 0
deltaBoost2_mem = 0
landing = False

def display_label(v_rocket,x,y):
    
    v_RocketText = font.render("Vitesse fusée : " + str(round(v_rocket, 2)) + "m/s", False, white)
    posX = font.render("X : " + str(x), False, white)
    posY = font.render("h : " + str(round(h / 100, 2)) + "m", False, white)
    vRect = v_RocketText.get_rect()
    posXRect = posX.get_rect()
    posYRect = posY.get_rect()

    posXRect.x = 80
    posYRect.x = 80
    vRect.x = 80
    posXRect.y = 50
    posYRect.y = 70
    vRect.y = 90
    
    pygame.draw.line(screen, white, (mleft, mtop), (mleft, height - mbottom))
    pygame.draw.line(screen, white, (mleft, height - mbottom), (width - mright, height - mbottom))

    screen.blit(posX,posXRect)
    screen.blit(posY,posYRect)
    screen.blit(v_RocketText,vRect)
    screen.blit(rocket, rocket_rect)

def delta_boost(h, v, g, t):
    return v**2 - 4 * h * ((t- g) / 2)

while run == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run = False
  
    v_rocket += gravity 

    if(rocket_rect.y < height):
        nbpix = height - mbottom - rlength - h * SCALE_pix - float(rocket_rect.y)
        rocket_rect = rocket_rect.move(0, nbpix)

    x = rocket_rect.x
    h = h - v_rocket

    # On calcule le delta du futur et s'il change de signe, on cherche plus précisément
    # le moment où allumer les boosters.
    deltaBoost2 = delta_boost(h - v_rocket - gravity, v_rocket + gravity, gravity, thrust)
    if not landing and deltaBoost2 >= 0:
        landing = True
        while delta_boost(h, v_rocket, gravity, thrust) < 0:
            v_rocket += gravity * 0.1
            h -= v_rocket * 0.1

    # On fait du PWM jusqu'à atteindre la vitesse maximale
    # d'atterrissage. Cela implique un tâtonnement sur le dernier mètre
    # de la descente.
    if landing:
        if v_rocket > vmax:
            v_rocket -= thrust
        else:
            v_rocket -= gravity
            pygame.time.wait(10)

    screen.fill(black)
    display_label(v_rocket,rocket_rect.x,h)
    
    if h <= 0:
        if v_rocket >= vmax:
            screen.blit(death, deathRect)
        elif v_rocket < vmax:
            screen.blit(success, successRect)
        run = False

    pygame.display.flip()
    if run == False and h <= 0:
        pygame.time.wait(5000)

pygame.quit()
sys.exit()
