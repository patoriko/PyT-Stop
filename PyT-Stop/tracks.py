import pygame
from pygame.locals import *
from random import randrange

trackFiles = []
trackTile = ['empty.png', 'start.png', 'vertStraight.png',
             'horiStraight.png', 'turn90.png', 'turn180.png',
             'turn270.png', 'turn360.png', 'checkpointOne.png',
             'checkpointTwo.png']

empty = 0
start = 1
vertStraight = 2
horiStraight = 3
turn90 = 4
turn180 = 5
turn270 = 6
turn360 = 7
check1 = 8
check2 = 9

roverfield = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 4, 3, 5, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 2, 0, 4, 3, 5, 0],
    [0, 0, 1, 0, 2, 0, 2, 0, 2, 0],
    [0, 0, 2, 0, 7, 3, 6, 0, 8, 0],
    [0, 0, 9, 0, 0, 0, 0, 0, 2, 0],
    [0, 0, 2, 0, 0, 0, 0, 0, 2, 0],
    [0, 0, 7, 3, 3, 3, 3, 3, 6, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

roverfieldRot = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]


class Track(pygame.sprite.Sprite):
    def __init__(self, tile_track, y, x, rot):
        pygame.sprite.Sprite.__init__(self)
        self.image = trackFiles[tile_track]
        self.rect = self.image.get_rect()

        if rot != 0:
            self.image = pygame.transform.rotate(self.image, rot * 90)

        self.x = x
        self.y = y

    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y
