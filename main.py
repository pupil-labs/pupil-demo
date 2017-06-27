import pygame
import time
import random
import numpy as np

pygame.init()

#############
crash_sound = pygame.mixer.Sound("woosh.wav")
#############

display_info = pygame.display.Info()
display_width = display_info.current_w // 2
display_height = display_info.current_h

black = (0, 0, 0)
white = (255, 255, 255)

red = (200, 0, 0)
green = (0, 200, 0)

bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

block_color = (53, 115, 255)
projectile_color = (0, 255, 255)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Space Explorer')
clock = pygame.time.Clock()

ship_width = 100
ship_height= 100
shipx = (display_width * 0.45)
shipy = (display_height - ship_height)
shipImg = pygame.image.load('racecar.png')
shipImg = pygame.transform.scale(shipImg, (ship_width, ship_height))
gameIcon = shipImg.copy() #pygame.image.load('racecar.jpg')

pygame.display.set_icon(gameIcon)

pause = False

nb_meteors = 10

def things_dodged(count):
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render("Dodged: " + str(count), True, black)
    gameDisplay.blit(text, (0, 0))


def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])


def ship():
    # gameDisplay.blit(shipImg, (x, y))
    pygame.draw.rect(gameDisplay, block_color, [shipx, shipy, ship_width, ship_height])


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

        pygame.display.update()
        clock.tick(15)


class Meteor:
    def __init__(self):
        self.width = 100
        self.height = 100
        self.reset()

    def reset(self):
        self.x = random.randrange(0, display_width - self.width)
        self.y = -self.height
        self.speed = random.randrange(5, 10) * 10
        self.direction = np.array((random.randrange(7), 10))
        self.direction = self.direction / np.linalg.norm(self.direction)

    def move(self):
        # Reset if no longer in bounds
        if self.y > display_height or self.x > display_width or self.x + self.width < 0:
            self.reset()

        self.x += self.speed * self.direction[0]
        self.y += self.speed * self.direction[1]

    def draw(self):
        pygame.draw.rect(gameDisplay, block_color, [int(self.x), int(self.y), self.width, self.height])


class Projectile:
    def __init__(self, direction, meteors):
        self.x = (display_width * 0.45)
        self.y = (display_height * 0.8)
        self.speed = 7
        self.meteors = meteors
        self.alive = True
        self.length = 30
        self.direction = direction / np.linalg.norm(direction)

    def move(self):
        # Reset if no longer in bounds
        if self.y > display_height or self.x > display_width or self.x < 0:
            self.alive = False

        self.x += self.speed * self.direction[0]
        self.y += self.speed * self.direction[1]

        for meteor in self.meteors:
            if self.y < meteor.y + meteor.height:
                if self.x > meteor.x and self.x < meteor.x + meteor.width or self.x + car_width > meteor.x and self.x + car_width < meteor.x + meteor.width:
                    meteor.reset()
                    self.alive = False

    def draw(self):
        pygame.draw.line(gameDisplay, projectile_color, [int(self.x), int(self.y)], [int(self.x + self.direction[0] * self.length), int(self.y + self.direction[1] * self.length)], 5)

def game_loop():
    global pause
    ############
    # pygame.mixer.music.load('woosh.wav')
    # pygame.mixer.music.play(-1)
    ############

    x_change = 0
    # shipx = (display_width * 0.45)
    # shipy = (display_height * 0.8)

    meteors = [Meteor() for i in range(nb_meteors)]
    projectiles = []

    dodged = 0

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_p:
                    pause = True
                    paused()
                if event.key == pygame.K_UP:
                    projectiles.append(Projectile((1,-1), meteors))

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0


        gameDisplay.fill(white)

        for projectile in projectiles:
            projectile.move()
            projectile.draw()

        for meteor in meteors:
            meteor.move()
            meteor.draw()

        # Remove dead projectiles
        tmp = []
        for projectile in projectiles:
            if projectile.alive:
                tmp.append(projectile)
        projectiles = tmp

        ship()
        things_dodged(dodged)

        for meteor in meteors:
            if shipy < meteor.y + meteor.height:
                if shipx < meteor.x and shipx + ship_width > meteor.x or shipx < meteor.x + meteor.width and shipx + ship_width > meteor.x + meteor.width:
                    crash()

        pygame.display.update()
        clock.tick(60)


game_intro()
game_loop()
pygame.quit()
quit()