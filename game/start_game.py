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

screen = pygame.display.set_mode(size)

rocket = pygame.transform.scale(pygame.image.load("rocket.png"), [rwidth, rlength])
rocket_rect = rocket.get_rect()
rocket_rect = rocket_rect.move((width/2)-rocket.get_width()/2,0)

v_rocket = 0
v_exhaust = -10e-3
thrust = 200 * 10e-3
gravity = 9.81*10e-3

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

def display_label(v_rocket,x,y):
    
    v_RocketText = font.render("Vitesse fusée : " + str(v_rocket), False, white)
    posX = font.render("X : " + str(x), False, white)
    posY = font.render("Y : " + str(y), False, white)
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

while run == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run = False
  
    v_rocket += gravity 


    if(rocket_rect.y < height):
        rocket_rect = rocket_rect.move(0,v_rocket)
    
    display_label(v_rocket,rocket_rect.x,rocket_rect.y)


    x = rocket_rect.x
    y = rocket_rect.y
    
    h = height - mbottom - y - rlength

    deltaBoost2 = v_rocket**2 - 4 * h * ((thrust - gravity) / 2)
    print(deltaBoost2)

    if deltaBoost2 >= -25:
        v_rocket -= thrust

    screen.fill(black)

    display_label(v_rocket,x,y)
    
    if y >= height - mbottom - rlength:
        if v_rocket >= vmax:
            screen.blit(death, deathRect)
        elif v_rocket < vmax:
            screen.blit(success, successRect)
        
        run = False
            
    
    pygame.time.wait(10)
    pygame.display.flip()
    
    if run == False:
        pygame.time.wait(1000)

pygame.quit()
sys.exit()
