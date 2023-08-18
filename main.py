import random  # for generating random numbers
import sys  # To Exit the game
import pygame
from pygame.locals import *  # Basic Pygame Imports

FPS = 30
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_ASSETS = {}
GAME_SOUNDS = {}
PLAYER = "resources/ASSETS/bird.png"
BACKGROUND = "resources/ASSETS/bg_1.jpg"
PIPE = "resources/ASSETS/pipe.png"


def welcomeScreen():
    # IT WIll Show Welcome Screen TO user to make the game more interactive and interesting
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENHEIGHT - GAME_ASSETS["player"].get_height()) / 2
    messagex = int(SCREENWIDTH - GAME_ASSETS["message"].get_width()) / 2
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0

    # Drawing Rectangle for playbutton
    playbutton = pygame.Rect(108, 222, 68, 65)

    while True:
        for event in pygame.event.get():
            # If user clicks on Cross or presses the Escape button Close the Game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if (
                pygame.mouse.get_pos()[0] > playbutton[0]
                and pygame.mouse.get_pos()[0] < playbutton[0] + playbutton[2]
            ):
                if (
                    pygame.mouse.get_pos()[1] > playbutton[1]
                    and pygame.mouse.get_pos()[1] < playbutton[1] + playbutton[3]
                ):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            if playbutton.collidepoint(
                pygame.mouse.get_pos()
            ):  # checking if mouse is collided with the play button
                if (
                    event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                ):  # checking if mouse has been clicked
                    mainGame()

            else:
                SCREEN.blit(GAME_ASSETS["background"], (0, 0))
                SCREEN.blit(GAME_ASSETS["player"], (playerx, playery))
                SCREEN.blit(GAME_ASSETS["message"], (messagex, messagey))
                SCREEN.blit(GAME_ASSETS["base"], (basex, GROUNDY))
                # Adding INTRO Music
                pygame.mixer.music.load("resources/AUDIO/INTROMUSIC.mp3")
                pygame.mixer.music.play()
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    # ADDING THE BACKGROUND MUSIC
    pygame.mixer.music.stop()
    pygame.mixer.music.load("resources/AUDIO/BGMUSIC.mp3")
    pygame.mixer.music.play()
    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENHEIGHT / 2)
    basex = 0

    # Creating upper and Lower Pipes for the game
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # Upper pipe List
    upperPipes = [
        {"x": SCREENWIDTH + 200, "y": newPipe1[0]["y"]},
        {"x": SCREENWIDTH + 200 + (SCREENWIDTH / 2), "y": newPipe2[0]["y"]},
    ]

    # lists of Lower Pipe
    lowerPipes = [
        {"x": SCREENWIDTH + 200, "y": newPipe1[1]["y"]},
        {"x": SCREENWIDTH + 200 + (SCREENWIDTH / 2), "y": newPipe2[1]["y"]},
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 2
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8  # velocity while flapping
    playerFlapped = False  # It is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS["wing"].play()

        crashTest = isCollide(
            playerx, playery, upperPipes, lowerPipes
        )  # This function will return true if the player is crashed
        if crashTest:
            return

        # check for score
        playerMidPos = playerx + GAME_ASSETS["player"].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe["x"] + GAME_ASSETS["pipe"][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS["point"].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_ASSETS["player"].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe["x"] += pipeVelX
            lowerPipe["x"] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < upperPipes[0]["x"] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]["x"] < -GAME_ASSETS["pipe"][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Lets blit our ASSETS now
        SCREEN.blit(GAME_ASSETS["background"], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_ASSETS["pipe"][0], (upperPipe["x"], upperPipe["y"]))
            SCREEN.blit(GAME_ASSETS["pipe"][1], (lowerPipe["x"], lowerPipe["y"]))

        SCREEN.blit(GAME_ASSETS["base"], (basex, GROUNDY))
        SCREEN.blit(GAME_ASSETS["player"], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_ASSETS["numbers"][digit].get_width()
        Xoffset = (SCREENWIDTH - width) / 2

        for digit in myDigits:
            SCREEN.blit(GAME_ASSETS["numbers"][digit], (Xoffset, SCREENHEIGHT * 0.12))
            Xoffset += GAME_ASSETS["numbers"][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS["hit"].play()
        pygame.mixer.music.stop()
        gameOver()

    for pipe in upperPipes:
        pipeHeight = GAME_ASSETS["pipe"][0].get_height()
        if (
            playery < pipeHeight + pipe["y"]
            and abs(playerx - pipe["x"]) < GAME_ASSETS["pipe"][0].get_width() - 20
        ):
            GAME_SOUNDS["hit"].play()
            print(
                playerx,
                pipe["x"],
            )
            pygame.mixer.music.stop()
            gameOver()

    for pipe in lowerPipes:
        if (playery + GAME_ASSETS["player"].get_height() > pipe["y"]) and abs(
            playerx - pipe["x"]
        ) < GAME_ASSETS["pipe"][0].get_width() - 20:
            GAME_SOUNDS["hit"].play()
            pygame.mixer.music.stop()
            gameOver()

    return False


def getRandomPipe():
    """
    generating positions of the two pipes one upper pipe and other lower pipe
    To blit on the Screen
    """

    pipeHeight = GAME_ASSETS["pipe"][0].get_height()
    offset = SCREENHEIGHT / 4.5
    y2 = offset + random.randrange(
        0, int(SCREENHEIGHT - GAME_ASSETS["base"].get_height() - 1.2 * offset)
    )
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [{"x": pipeX, "y": -y1}, {"x": pipeX, "y": y2}]  # Upper Pipes  # Lower Pipes
    return pipe


def gameOver():
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("Flappy Bird With Sameer")
    GAME_ASSETS["OVER"] = pygame.image.load(
        "resources/ASSETS/gameover.png"
    ).convert_alpha()
    GAME_ASSETS["RETRY"] = pygame.image.load(
        "resources/ASSETS/retry.png"
    ).convert_alpha()
    GAME_ASSETS["HOME"] = pygame.image.load("resources/ASSETS/Home.png").convert_alpha()
    SCREEN.blit(GAME_ASSETS["background"], (0, 0))
    SCREEN.blit(GAME_ASSETS["base"], (0, GROUNDY))
    SCREEN.blit(GAME_ASSETS["OVER"], (0, 0))
    SCREEN.blit(GAME_ASSETS["RETRY"], (30, 220))
    SCREEN.blit(GAME_ASSETS["HOME"], (30, 280))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_SPACE:
                mainGame()

            ### RETRY BUTTON
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if (
                pygame.mouse.get_pos()[0] > 30
                and pygame.mouse.get_pos()[0] < 30 + GAME_ASSETS["RETRY"].get_width()
            ):
                if (
                    pygame.mouse.get_pos()[1] > 220
                    and pygame.mouse.get_pos()[1]
                    < 220 + GAME_ASSETS["RETRY"].get_height()
                ):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mainGame()

            ### HOME BUTTON
            if (
                pygame.mouse.get_pos()[0] > 30
                and pygame.mouse.get_pos()[0] < 30 + GAME_ASSETS["HOME"].get_width()
            ):
                if (
                    pygame.mouse.get_pos()[1] > 280
                    and pygame.mouse.get_pos()[1]
                    < 280 + GAME_ASSETS["HOME"].get_height()
                ):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        welcomeScreen()


### This is the point from Where Our Game is going to be Started ###
if __name__ == "__main__":
    pygame.init()  # Initializing the Modules of Pygame
    FPSCLOCK = pygame.time.Clock()  # for controlling the FPS
    pygame.display.set_caption("Flappy Bird")  # Setting the Caption of The Game

    #### LOADING THE ASSETS ####

    GAME_ASSETS["numbers"] = (
        pygame.image.load("resources/ASSETS/0.png").convert_alpha(),
        pygame.image.load("resources/ASSETS/1.png").convert_alpha(),
        pygame.image.load("resources/ASSETS/2.png").convert_alpha(),
        pygame.image.load("resources/ASSETS/3.png").convert_alpha(),
        pygame.image.load("resources/ASSETS/4.png").convert_alpha(),
        pygame.image.load("resources/ASSETS/5.png").convert_alpha(),
        pygame.image.load("resources/ASSETS/6.png").convert_alpha(),
        pygame.image.load("resources/ASSETS/7.png").convert_alpha(),
        pygame.image.load("resources/ASSETS/8.png").convert_alpha(),
        pygame.image.load("resources/ASSETS/9.png").convert_alpha(),
    )

    GAME_ASSETS["background"] = pygame.image.load(BACKGROUND).convert_alpha()
    GAME_ASSETS["player"] = pygame.image.load(PLAYER).convert_alpha()
    GAME_ASSETS["message"] = pygame.image.load(
        "resources/ASSETS/message.png"
    ).convert_alpha()
    GAME_ASSETS["base"] = pygame.image.load("resources/ASSETS/base.png").convert_alpha()
    GAME_ASSETS["pipe"] = (
        pygame.transform.rotate(
            pygame.image.load(PIPE).convert_alpha(), 180
        ),  #### UPPER PIPES, WE JUST ROTATED THE PIPE BY 180deg
        pygame.image.load(PIPE).convert_alpha(),  #### LOWER PIPES
    )

    # Game Sounds
    GAME_SOUNDS["die"] = pygame.mixer.Sound("resources/AUDIO/die.wav")
    GAME_SOUNDS["hit"] = pygame.mixer.Sound("resources/AUDIO/hit.wav")
    GAME_SOUNDS["point"] = pygame.mixer.Sound("resources/AUDIO/point.wav")
    GAME_SOUNDS["swoosh"] = pygame.mixer.Sound("resources/AUDIO/swoosh.wav")
    GAME_SOUNDS["wing"] = pygame.mixer.Sound("resources/AUDIO/wing.wav")
    while True:
        welcomeScreen()  # Shows a welcomescreen to the user until they starts the game
        mainGame()  # This is our main game funtion
