import pygame, sys
import player
import tracks
import camera
import gamemode
import engine as e
from pygame.locals import *
from render import renderImage

# -------------------------------------------- #

def loadVideoSettings():
    global scale
    f = open('settings.txt','r')
    dat = f.read()
    scale = int(dat[0])
    f.close()
    return dat[1]
def saveVideoSettings():
    global fullscreen, scale
    f = open('settings.txt','w')
    f.write(str(scale) + fullscreen)
    f.close()

# -------------------------------------------- #

mainClock = pygame.time.Clock()

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(64)
pygame.display.set_caption('PyT Stop')

iconImg = pygame.image.load('Assets\icon.png')
pygame.display.set_icon(iconImg)

global displayDimensions, scale, fullscreen
displayDimensions = [356,200]
fullscreen = loadVideoSettings()
global screen
if fullscreen == 'n':
    screen = pygame.display.set_mode((displayDimensions[0] * scale, displayDimensions[1] * scale),0,32)
else:
    screen = pygame.display.set_mode((displayDimensions[0] * scale, displayDimensions[1] * scale),pygame.FULLSCREEN)
display = pygame.Surface(displayDimensions)

pygame.mouse.set_visible(True)

# -------------------------------------------- #

global font
pressStart = pygame.font.Font('Assets\Fonts\pressStart.ttf', 45)

global framerate
framerate = 75


def text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


click = False

centreWidth = -1
centreHeight = -1

# -------------------------------------------- #

def mainMenu():
    while True:

        screen.fill((243, 243, 243))
        pygame.display.set_caption("PyT Stop - Menu")
        text("PyT Stop", pressStart, (0, 0, 0), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        buttonGame = pygame.Rect(100, 175, 225, 60)
        buttonControls = pygame.Rect(100, 275, 225, 60)
        buttonCredits = pygame.Rect(100, 375, 225, 60)
        buttonQuit = pygame.Rect(100, 475, 225, 60)

        if buttonGame.collidepoint((mx, my)):
            if click:
                game()
        if buttonControls.collidepoint((mx, my)):
            if click:
                controls()
        if buttonCredits.collidepoint((mx, my)):
            if click:
                credits()
        if buttonQuit.collidepoint((mx, my)):
            if click:
                quit()

        pygame.draw.rect(screen, (191, 10, 48), buttonGame)
        text('PLAY', pygame.font.Font('Assets\Fonts\pressStart.ttf', 35), (0, 0, 0), screen, 145, 190)
        pygame.draw.rect(screen, (191, 10, 48), buttonControls)
        text('CONTROLS', pygame.font.Font('Assets\Fonts\pressStart.ttf', 25), (0, 0, 0), screen, 110, 293)
        pygame.draw.rect(screen, (191, 10, 48), buttonCredits)
        text('CREDITS', pygame.font.Font('Assets\Fonts\pressStart.ttf', 30), (0, 0, 0), screen, 110, 393)
        pygame.draw.rect(screen, (191, 10, 48), buttonQuit)
        text('QUIT', pygame.font.Font('Assets\Fonts\pressStart.ttf', 35), (0, 0, 0), screen, 145, 490)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(framerate)


centreWidth = int(pygame.display.Info().current_w / 2)
centreHeight = int(pygame.display.Info().current_h / 2)

background = pygame.Surface(screen.get_size())
background = background.convert_alpha()
background.fill((26, 26, 26))

# -------------------------------------------- #

def game():
    running = True
    pygame.display.set_caption("PyT Stop")
    font = pygame.font.Font('Assets\Fonts\pressStart.ttf', 24)
    car = player.Player()
    cam = camera.camera()
    timer = gamemode.Timer()
    tracksSprite = pygame.sprite.Group()
    playerSprite = pygame.sprite.Group()
    timerSprite = pygame.sprite.Group()

    for tile_num in range(0, len(tracks.trackTile)):
        tracks.trackFiles.append(renderImage(
            tracks.trackTile[tile_num], False))
    for x in range(0, 10):
        for y in range(0, 10):
            tracksSprite.add(
                tracks.Track(tracks.roverfield[x][y], x * 1000, y * 1000, tracks.roverfieldRot[x][y]))

    timerSprite.add(timer)
    playerSprite.add(car)

    cam.set_pos(car.x, car.y)

    while running:

        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if (keys[K_r]):
                    car.reset()
                    timer.reset()
                if (keys[K_ESCAPE]):
                    pygame.quit()
                    sys.exit(0)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                break

        keys = pygame.key.get_pressed()
        if (timer.timeleft > 0):
            if keys[K_a]:
                car.steerLeft()
            if keys[K_d]:
                car.steerRight()
            if keys[K_w]:
                car.accelerate()
            else:
                car.idle()
            if keys[K_s]:
                car.brake()

        cam.set_pos(car.x, car.y)

        textFPS = font.render(
            'FPS: ' + str(int(mainClock.get_fps())), 1, (224, 16, 16))
        textposFPS = textFPS.get_rect(centery=25, centerx=90)

        textTimer = font.render('Timer: ' + str(int((timer.timeleft / 60)/60)) +
                                ': ' + str(int((timer.timeleft / 60) % 60)), 1, (224, 16, 16))
        textposTimer = textFPS.get_rect(centery=75, centerx=95)

        textSpeed = font.render('Speed: ' + str(int((car.speed / 60)/60)) +
                                ': ' + str(int((car.speed / 60) % 60)), 1, (224, 16, 16))
        textposSpeed = textFPS.get_rect(centery=125, centerx=95)

        screen.blit(background, (0, 0))

        tracksSprite.update(cam.x, cam.y)
        tracksSprite.draw(screen)
        playerSprite.update(cam.x, cam.y)
        playerSprite.draw(screen)
        timerSprite.update(cam.x, cam.y)
        timerSprite.draw(screen)

        if (timer.timeleft == 0):
            car.speed = 0
            textTimer = font.render(
                'Final Time: ' + str(timer.score), 1, (224, 16, 16))
            textposTimer = textFPS.get_rect(
                centery=centreHeight / 2, centerx=centreWidth / 2)

        screen.blit(textFPS, textposFPS)
        screen.blit(textTimer, textposTimer)
        screen.blit(textSpeed, textposSpeed)
        pygame.display.flip()

        if pygame.sprite.spritecollide(car, timerSprite, True):
            timer.finishLap()
            timer.generateFinish()
            timerSprite.add(timer)

        mainClock.tick(framerate)

# -------------------------------------------- #

def controls():
    running = True
    while running:
        screen.fill((243, 243, 243))

        mx, my = pygame.mouse.get_pos()

        banner = pygame.Rect(0, 0, 1280, 120)

        pygame.display.set_caption("PyT Stop - Controls")
        pygame.draw.rect(screen, (191, 10, 48), banner)
        text("PyT Stop Controls", pygame.font.Font('Assets\Fonts\pressStart.ttf', 45),
             (0, 0, 0), screen, 70, 25)

        x = -50
        y = 100

        imageControls = renderImage('controls.jpg')

        def controlsImage(x, y):
            screen.blit(imageControls, (x, y))

        controlsImage(x, y)

        buttonBack = pygame.Rect(50, 620, 225, 60)

        if buttonBack.collidepoint((mx, my)):
            if click:
                mainMenu()

        pygame.draw.rect(screen, (191, 10, 48), buttonBack)
        text('BACK', pygame.font.Font('Assets\Fonts\pressStart.ttf', 35),
             (0, 0, 0), screen, 65, 635)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(framerate)

# -------------------------------------------- #

def credits():
    running = True
    while running:
        screen.fill((243, 243, 243))

        mx, my = pygame.mouse.get_pos()

        buttonBack = pygame.Rect(50, 620, 225, 60)

        if buttonBack.collidepoint((mx, my)):
            if click:
                mainMenu()

        pygame.display.set_caption("PyT Stop - Credits")
        pygame.draw.rect(screen, (191, 10, 48), buttonBack)
        text('BACK', pygame.font.Font('Assets\Fonts\pressStart.ttf', 35),
             (0, 0, 0), screen, 65, 635)

        text('Credits', pygame.font.Font(
            'Assets\Fonts\pressStart.ttf', 32), (0, 0, 0), screen, 20, 20)
        text('Code By', pygame.font.Font(
            'Assets\Fonts\pressStart.ttf', 32), (191, 10, 48), screen, 115, 135)
        text('Patrick Taylor', pygame.font.Font(
            'Assets\Fonts\pressStart.ttf', 22), (10, 10, 10), screen, 140, 190)
        text('Sound By', pygame.font.Font(
            'Assets\Fonts\pressStart.ttf', 32), (191, 10, 48), screen, 115, 285)
        text('Patrick Taylor', pygame.font.Font(
            'Assets\Fonts\pressStart.ttf', 22), (10, 10, 10), screen, 140, 340)
        text('Font', pygame.font.Font(
            'Assets\Fonts\pressStart.ttf', 28), (191, 10, 48), screen, 655, 135)
        text('Press Start 2P', pygame.font.Font(
            'Assets\Fonts\pressStart.ttf', 18), (10, 10, 10), screen, 670, 190)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(framerate)

# -------------------------------------------- #

def quit():
    running = True
    while running:
        pygame.quit()
        sys.exit()

# -------------------------------------------- #

mainMenu()
