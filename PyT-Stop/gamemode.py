import pygame, tracks
from pygame.locals import *
from random import randint
from render import renderImage

pentalty = 180
lapIncrement = 15
halfTile = 500
tileSize = 1000
timerFull = 2500
extraTime = timerFull / 2

# -------------------------------------------- #

class Timer(pygame.sprite.Sprite):
    def finishLap(self):
        self.score += lapIncrement
        self.timeleft += extraTime
        if self.timeleft > timerFull:
            self.timeleft = timerFull

    def generateFinish(self):
        x = randint(0, 9)
        y = randint(0, 9)
        while (tracks.roverfield[y][x] == 5):
            x = randint(0, 9)
            y = randint(0, 9)

        self.x = x * tileSize + halfTile
        self.y = y * tileSize + halfTile
        self.rect.topleft = self.x, self.y

    def reset(self):
        self.timeleft = timerFull
        self.score = 0
        self.generateFinish()

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = renderImage('start.png', False)
        self.rect = self.image.get_rect()
        self.x = 3000
        self.y = 3000
        self.pentalty = pentalty
        self.generateFinish()
        self.rect.topleft = self.x, self.y
        self.score = 0
        self.timeleft = timerFull

    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y
        if (self.pentalty > 0):
            self.pentalty -= 1
        if (self.timeleft > 0):
            self.timeleft -= 1
