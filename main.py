import pygame
import time
import random
import numpy as np

from meteor import Meteor
from projectiles import Projectile
from ship import Ship
from pupil import Surface_Markers, Connection

pygame.init()

#############
crash_sound = pygame.mixer.Sound("woosh.wav")
#############

display_info = pygame.display.Info()
display_height = int(0.9 * display_info.current_h)
display_width = int((display_height/3) * 4)

black = (0, 0, 0)
white = (255, 255, 255)

red = (200, 0, 0)
green = (0, 200, 0)

bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

cross_hair_color = (255, 0, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Space Explorer')
clock = pygame.time.Clock()

ship_width = int(172 * 1.5)
ship_height = int(151 * 1.5)
shipx = (display_width * 0.45)
shipy = (display_height - ship_height)

pause = False

nb_meteors = 15
surface_markers = Surface_Markers(marker_size=(100, 100))

# def ship():
#     # gameDisplay.blit(shipImg, (x, y))
#     pygame.draw.rect(gameDisplay, ship_color, [shipx, shipy, ship_width, ship_height])

def cross_hair(x, y):
    # gameDisplay.blit(shipImg, (x, y))
    pygame.draw.rect(gameDisplay, cross_hair_color, [x-5, y-5, 10,10])


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def crash():
    ####################################
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()
    ####################################
    largeText = pygame.font.SysFont("comicsansms", 115)
    TextSurf, TextRect = text_objects("Game Over", largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("Play Again", display_width * 0.35, display_height * 0.7, 100, 50, green, bright_green, game_loop)
        button("Quit", display_width * 0.65, display_height * 0.7, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))
    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


def quitgame():
    pygame.quit()
    quit()


def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False


def paused():
    ############
    pygame.mixer.music.pause()
    #############
    largeText = pygame.font.SysFont("comicsansms", 115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("Continue", display_width * 0.35, display_height * 0.7, 100, 50, green, bright_green, unpause)
        button("Quit", display_width * 0.65, display_height * 0.7, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("comicsansms", 115)
        TextSurf, TextRect = text_objects("A bit Racey", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!", display_width * 0.35, display_height * 0.7, 100, 50, green, bright_green, game_loop)
        button("Quit", display_width * 0.65, display_height * 0.7, 100, 50, red, bright_red, quitgame)

        surface_markers.draw(gameDisplay)
        pygame.display.update()
        clock.tick(15)




def game_loop():
    capture = Connection()

    global pause
    ############
    # pygame.mixer.music.load('woosh.wav')
    # pygame.mixer.music.play(-1)
    ############

    meteor_list = pygame.sprite.Group()
    projectile_list = pygame.sprite.Group()

    for i in range(nb_meteors):
        m = Meteor(display_width, display_height)
        meteor_list.add(m)

    ship = Ship(ship_width, ship_height, shipx, shipy)

    gameExit = False

    aimx = display_width // 2
    aimy = 0
    aim = np.array((aimx, aimy))
    aim = aim / np.linalg.norm(aim)

    shot_timer = 0
    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    paused()


        # aimx, aimy = pygame.mouse.get_pos()
        # aim = np.array((aimx, aimy))
        pupil_positions = capture.recent_events()
        if pupil_positions:
            print("Found Pupil")
            aimx, aimy = pupil_positions[-1]
            aimy = 1-aimy
            aimx = aimx * display_width
            aimy = aimy * display_height
            aim = np.array((aimx, aimy))
        else:
            print("No pupil pos")

        shot_timer += 1
        if shot_timer % 20 == 0:
            Projectile(aim - (shipx + ship_width // 2, shipy), shipx, shipy, ship_width, meteor_list, projectile_list, display_width, display_height)
            shot_timer = 0



        gameDisplay.fill(white)

        # Move things
        for projectile in projectile_list:
            projectile.update()

        meteor_list.update()

        # Draw things
        surface_markers.draw(gameDisplay)
        meteor_list.draw(gameDisplay)
        ship.draw(gameDisplay)
        projectile_list.draw(gameDisplay)

        # Remove dead meteors and projectiles
        # projectile_list[:] = [p for p in projectile_list if p.alive]

        cross_hair(aimx, aimy)
        # things_dodged(dodged)

        blocks_hit_list = pygame.sprite.spritecollide(ship, meteor_list, True)
        if blocks_hit_list:
            crash()

        pygame.display.update()
        clock.tick(60)


game_intro()
game_loop()
pygame.quit()
quit()
