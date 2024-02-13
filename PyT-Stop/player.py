import pygame, math, tracks
from pygame.locals import *
from random import randint
from render import renderImage

centreX = -1
centreY = -1


def rotCentre(image, rect, angle):
    rotImage = pygame.transform.rotate(image, angle)
    rotRect = rotImage.get_rect(center=rect.center)
    return rotImage, rotRect


def findspawn():
    x = randint(2, 3)
    y = randint(2, 3)
    while(tracks.roverfield[y][x] == 5):
        x = randint(2, 3)
        y = randint(2, 3)
    return x * 1000 + centreX, y * 1000 + centreY


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = renderImage('cars/formula.png')
        self.rect = self.image.get_rect()
        self.image_orig = self.image
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        centreX = int(pygame.display.Info().current_w / 2)
        centreY = int(pygame.display.Info().current_h / 2)
        self.x = centreX
        self.y = centreY
        self.rect.topleft = self.x, self.y
        self.x, self.y = findspawn()
        self.dir = 0
        self.speed = 0.0
        self.maxspeed = 20.25
        self.minSpeed = -1.95
        self.acceleration = 0.095
        self.brakeForce = 0.45
        self.idleSpeed = 0.05
        self.steering = 2.25

    def reset(self):
        self.x = int(pygame.display.Info().current_w / 2)
        self.y = int(pygame.display.Info().current_h / 2)
        self.speed = 0.0
        self.dir = 0
        self.image, self.rect = rotCentre(
            self.image_orig, self.rect, self.dir)
        self.rect.topleft = self.x, self.y
        self.x, self.y = findspawn()

    def impact(self):
        if self.speed > 0:
            self.speed = self.minSpeed

    def idle(self):
        if self.speed > 0:
            self.speed -= self.idleSpeed
        if self.speed < 0:
            self.speed += self.idleSpeed

    def accelerate(self):
        if self.speed < self.maxspeed:
            self.speed = self.speed + self.acceleration

    def brake(self):
        if self.speed > self.minSpeed:
            self.speed = self.speed - self.brakeForce

    def steerLeft(self):
        self.dir = self.dir+self.steering
        if self.dir > 360:
            self.dir = 0
        self.image, self.rect = rotCentre(
            self.image_orig, self.rect, self.dir)

    def steerRight(self):
        self.dir = self.dir-self.steering
        if self.dir < 0:
            self.dir = 360
        self.image, self.rect = rotCentre(
            self.image_orig, self.rect, self.dir)

    def update(self, last_x, last_y):
        self.x = self.x + self.speed * math.cos(math.radians(270-self.dir))
        self.y = self.y + self.speed * math.sin(math.radians(270-self.dir))
