#Sur le côté avoir une barre qui défile avec la hauteur afficher
#On fait descendre la camera avec la surface on veut un grand truc et on zoom pour faire croire que c'est haut
#Fairematcher distance et vitesse out ça en etant lent pour observer
#On fait défiler l'écran pas la fusée qui reste statique à part quand on est sur les dernier mille metre
#Diagramme des phases en display
import sys, pygame
pygame.init()

size = width, height = 1700, 900
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

rocket = pygame.image.load("rocket.png")
rocket_rect = rocket.get_rect()

rocket_rect = rocket_rect.move((width/2)-rocket.get_width()/2,0)

v_rocket = 0
v_exhaust = -10e-2
gravity = 9.81*10e-2

def display_label(v_rocket,x,y):
    
    font = pygame.font.SysFont("Consolas.ttf", 25)
    v_RocketText = font.render("Vitesse fusée : " + str(v_rocket), False,(255,255,255))
    posX = font.render("X : " + str(x), False,(255,255,255))
    posY = font.render("Y : " + str(y), False,(255,255,255))
    vRect = v_RocketText.get_rect()
    posXRect = posX.get_rect()
    posYRect = posY.get_rect()

    posXRect.x = 80
    posYRect.x = 80
    vRect.x = 80
    posXRect.y = 50
    posYRect.y = 70
    vRect.y = 90

    screen.blit(posX,posXRect)
    screen.blit(posY,posYRect)
    screen.blit(v_RocketText,vRect)
    screen.blit(rocket, rocket_rect)



while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
  
    v_rocket += gravity 


    if(rocket_rect.y < height):
        rocket_rect = rocket_rect.move(0,v_rocket)
    
    display_label(v_rocket,rocket_rect.x,rocket_rect.y)


    x = rocket_rect.x
    y = rocket_rect.y
    
    screen.fill(black)

    display_label(v_rocket,x,y)
    
    pygame.time.wait(300)
    pygame.display.flip()
