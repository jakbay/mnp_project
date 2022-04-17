#Sur le côté avoir une barre qui défile avec la hauteur afficher
#On fait descendre la camera avec la surface on veut un grand truc et on zoom pour faire croire que c'est haut
#Fairematcher distance et vitesse out ça en etant lent pour observer
#On fait défiler l'écran pas la fusée qui reste statique à part quand on est sur les dernier mille metre
#Diagramme des phases en display
import sys, pygame
pygame.init()

size = width, height = 800, 1000
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

h0 = 1 * (height - mbottom) / SCALE_T # n * 10k m
h = h0
vcontrol = 0

SCALE_pix = (height - mbottom) / h0

v_rocket = 0.0
gravity = 9.81 * SCALE_T

m0 = 750e3
ve = (20 * m0 / 435.0 * (gravity / SCALE_T)) * SCALE_T # 435 = ISP du mélange LOX - LH2 (wikipedia)
u = (20.0 * m0 / ve)
t = 0

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
    
def thrust(t):
    return ((u * ve) / (m0 - u * t)) * SCALE_T

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
    
    # On set une vitesse maximale en fonction
    # de l'altitude. A tweaker jusqu'à trouver
    # la combinaison optimale.
    # TODO: Voir si on peut trouver une fonction
    # de l'altitude plutôt que ce if else dégueu ?!
    vcontrol = h / 5000
    if h >= 10000 and h < 50000:
        vcontrol = 15.0
    elif h >= 2000 and h < 10000:
        vcontrol = 8.0
    elif h >= 500 and h < 2000:
        vcontrol = 1
    elif h >= 100 and h < 500:
        vcontrol = 0.2
    elif h < 100:
        vcontrol = 0.1

    if v_rocket > vcontrol:
        v_rocket -= thrust(t)
        t += SCALE_T
    elif v_rocket < vcontrol + gravity:
        pass
    else:
        v_rocket -= gravity
        t += SCALE_T

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
