## William's Snake Game

import pygame
import time
import random

pygame.init()

##Global variables
# Colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)
bground = (204, 204, 0)

# Display vars.
display_width = 800
display_height = 600

# Variables
gameDisplay = pygame.display.set_mode((display_width, display_height))  ##resolution, note that this is a tuple.
pygame.display.set_caption("Shnake")  # Title at the top of the screen

icon = pygame.image.load('logoapple32x32.png')  # Loads the icon for the top left
pygame.display.set_icon(icon)  # Sets the icon for the top left

snakeHeadImg = pygame.image.load("snakeHead.png")  # Loads the image for the snake head
appleImg = pygame.image.load("apple20x20.png")  # Loads the image for the apple

appleThickness = 20  # Defines how thick apple will be. Note to self: This is changable
clock = pygame.time.Clock()  # Starts clocking the game, used later for FPS
blockSize = 20  # Defines how big the snake will be. Changing this will mess up collision detection.
FPS = 15  # Frames per second. Called at the bottom of script

smallfont = pygame.font.SysFont("arial", 25)  ## format: ("font", fontsize)
medfont = pygame.font.SysFont("arial", 40)  ##
largefont = pygame.font.SysFont("arial", 80)  ##

direction = "right"  # Starting direction of snake, used in main gameLoop


##

def pauseGame():
    gameisPaused = True
    message_to_screen("Paused",
                          black,
                          -100,
                          size="large")
    message_to_screen("Press ESC to continue or Q to quit.",
                          black,
                          25,
                          size="small")
    pygame.display.update()
    while gameisPaused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameisPaused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        clock.tick(5)


def text_objects(text, color, size):  # Function to render text
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace=0, size="medium"):  # Function to blit (draw) text to surface
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)


##

def score(score):
    text = smallfont.render("Score: " + str(score), True, black)
    gameDisplay.blit(text, [0, 0])


def randAppleGen():  # Function to generate random apples
    randAppleX = round(
        random.randrange(0, display_width - appleThickness))  # /10.0)*10.0 ##Create another rand X value for new apple
    randAppleY = round(
        random.randrange(0, display_height - appleThickness))  # /10.0)*10.0 ##Create another rand Y value for new apple
    return randAppleX, randAppleY


def gameIntro():  # Function for game menu.
    intro = True

    while intro:  # Event handling during menu
        for eachEvent in pygame.event.get():
            if eachEvent.type == pygame.QUIT:
                pygame.quit()
                quit()

            if eachEvent.type == pygame.KEYDOWN:
                if eachEvent.key == pygame.K_c:
                    gameLoop()
                if eachEvent.key == pygame.K_q:
                    pygame.quit()
                    quit()

        # Text displayed in menu
        gameDisplay.fill(white)
        message_to_screen("Welcome to Slither",
                          green,
                          -90,
                          "large")

        message_to_screen("The more apples you eat, the longer you are",
                          black,
                          100)

        message_to_screen("The objective of the game is to eat red apples",
                          black,
                          0,
                          "small")

        message_to_screen("If you run into yourself, or the edges, you die!",
                          black,
                          30,
                          "small")
        message_to_screen("Press C to play or Q to quit.",
                          black,
                          180)

        pygame.display.update()
        clock.tick(500)


def snake(blockSize, snakeList):  # Function to draw snake

    if direction == "right":
        head = pygame.transform.rotate(snakeHeadImg,
                                       270)  # In gameLoop, right,left,up,down are used to change direction of snakeHead
    elif direction == "left":
        head = pygame.transform.rotate(snakeHeadImg, 90)
    elif direction == "up":
        head = snakeHeadImg
    elif direction == "down":
        head = pygame.transform.rotate(snakeHeadImg, 180)

    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))  ##???
    for XandY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, green,
                         [XandY[0], XandY[1], blockSize, blockSize])  ##width height, width height, drawing


##Main Game Loop

def gameLoop():
    global direction  ## Make direction a global var. Important

    # Local variables
    gameExit = False
    gameOver = False

    lead_x = display_width / 2
    lead_y = display_height / 2

    lead_x_change = 10
    lead_y_change = 0

    snakeList = []
    snakeLength = 3
    scoreCount = 0



    randAppleX, randAppleY = randAppleGen()  # Generate apples. Calls randAppleGen()

    # Main Game Loop ##eventHandler
    while not gameExit:
        if gameOver == True:
            message_to_screen("Game over",
                              red,
                              -50,
                              size="large")

            message_to_screen("Press C to play again or Q to quit",
                              black,
                              50,
                              size="medium")
        snakeHead = []  # Creates list snakeHead
        snakeHead.append(lead_x)  # Appends snakeHead x value to list
        snakeHead.append(lead_y)  # Appends snakeHead y value to list
        snakeList.append(snakeHead)  # Appends coordinates of snakeHead x,y to list
        while gameOver == True:  # Handles game over


            pygame.display.update()

            for event in pygame.event.get():  # eventHandler for loss screen
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        direction = "right"
                        gameLoop()

        for event in pygame.event.get():  # eventHandler for keyboard events during game
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != "right":  # Each of these handles either arrow keys or WASD key events.
                    lead_x_change = -blockSize
                    lead_y_change = 0
                    direction = "left"
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != "left":
                    lead_x_change = blockSize
                    lead_y_change = 0
                    direction = "right"
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != "down":
                    lead_y_change = -blockSize
                    lead_x_change = 0
                    direction = "up"
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != "up":
                    lead_y_change = blockSize
                    lead_x_change = 0
                    direction = "down"
                elif event.key == pygame.K_ESCAPE:
                    pauseGame()

        # Checks if user has hit screen boundaries.

        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:  # If user hits display boundaries
            gameOver = True  # They lose

        lead_x += lead_x_change  # Ensures continous movement of the snake
        lead_y += lead_y_change

        # Drawing

        gameDisplay.fill(bground)  # Fills the display background with predefined bground colour (defined at the top)

        gameDisplay.blit(appleImg,
                         (randAppleX, randAppleY))  ##Draws the apple using the appleImg, at random coordinates.





        if len(
                snakeList) > snakeLength:  # If the length of the list of snake body coordinates is greater than the length
            del snakeList[0]  # Delete the oldest value in the list (as the snake is constantly moving)

        for eachSegment in snakeList[:-1]:  # For each coordinate in snakeList
            if eachSegment == snakeHead:  # If the segment touches the snakeHead
                ##                gameDisplay.fill(bground)
                ##                snake(blockSize, snakeList)
                ##
                ##                pygame.display.update
                time.sleep(0.3)
                gameOver = True  # Game over

        snake(blockSize, snakeList)  ##Creates snake using function snake

        score(scoreCount)  # Displays score (it minuses 3 because the snake starts at 3)

        pygame.display.update()  ##Updates to screen


        ## COLLISION DETECTION

        if lead_x + blockSize > randAppleX and lead_x < randAppleX + appleThickness:
            if lead_y + blockSize > randAppleY and lead_y < randAppleY + appleThickness:
                randAppleX, randAppleY = randAppleGen()
                scoreCount += 1
                snakeLength += 3

        clock.tick(FPS)
    pygame.quit()
    quit()

    ##update screen


##
gameIntro()
gameLoop()
##Code goes above.
