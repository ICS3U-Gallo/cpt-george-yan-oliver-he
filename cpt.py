# cpt
import pygame
from random import randint

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

Bird_images = [pygame.image.load("images/bluebird-downflap.png"),
               pygame.image.load("images/bluebird-midflap.png"),
               pygame.image.load("images/bluebird-upflap.png")]

pygame.init()

size = 700, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Flappy Bird in Python by @KartikKannapur")

done = False
clock = pygame.time.Clock()


class Bird:
    def __init__(self):
        x = 350
        y = 250

        self.image = pygame.transform.scale(Bird_images[0], [35, 35])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.last_update = 0
        self.curr_frame = 0
        self.y_speed = 0
        self.gravity = 0.25

    def fly(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.y_speed = -2

        self.rect.y += self.y_speed
        self.y_speed += self.gravity


    def animate(self):
        if pygame.time.get_ticks() - self.last_update > 200:
            self.curr_frame += 1
            self.image = pygame.transform.scale(Bird_images[self.curr_frame % len(Bird_images)], (35,35))
            self.last_update = pygame.time.get_ticks()

    def update(self):
        self.animate()
        self.fly()

        screen.blit(self.image, self.rect)


bird = Bird()


def gameover():
    font = pygame.font.SysFont(None, 55)
    text = font.render("Game Over! Try Again", True, red)
    screen.blit(text, [150, 250])


def obstacle(xloc, yloc, xsize, ysize):
    pygame.draw.rect(screen, green, [xloc, yloc, xsize, ysize])
    pygame.draw.rect(screen, green, [xloc, int(yloc + ysize + space), xsize, ysize + 500])


def Score(score):
    font = pygame.font.SysFont(None, 55)
    text = font.render("Score: " + str(score), True, white)
    screen.blit(text, [0, 0])

x = 350
y = 250


x_speed = 0
y_speed = 0
height = 480
xlocation = 700
ylocation = 0
xsize = 70
ysize = randint(0, 350)

space = 150
obspeed = 2
score = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            y_speed = -10

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_UP:
            y_speed = 5

    Bird.update(bird)

    pygame.display.update()

    screen.fill(black)
    obstacle(xlocation, ylocation, xsize, ysize)
    Score(score)


    y += y_speed
    xlocation -= obspeed

    if y > height:
        gameover()
        y_speed = 0
        obspeed = 0

    if x + 20 > xlocation and y - 20 < ysize and x - 15 < xsize + xlocation:
        gameover()
        y_speed = 0
        obspeed = 0

    if x + 20 > xlocation and y + 20 < ysize and x - 15 < xsize + xlocation:
        gameover()
        y_speed = 0
        obspeed = 0

    if xlocation < -80:
        xlocation = 700
        ysize = randint(0, 350)

    if x > xlocation and x < xlocation + 3:
        score = score + 1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
