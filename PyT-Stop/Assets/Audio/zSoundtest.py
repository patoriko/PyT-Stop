import pygame

pygame.mixer.init()
sound = pygame.mixer.Sound("Audio/cruise.wav")

sound.play(loops=-1)
clock = pygame.time.Clock()
t = 0
while t < 10:
    clock.tick(1)
    t = t + 1
