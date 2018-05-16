import pygame
import random
from astar_alghoritm import *

pygame.init()

#Rzeczy konfiguracyjne, w sumie mało ważne
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,255,255)
mix = (255,127,127)
display_width = 900
display_height = 600
FPS = 60
block_size = 30
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Kelner')
pygame.display.update()
gameExit = False
lead_x = display_width/2
lead_y = display_height/2
lead_x_change = 0
lead_y_change = 0
backgroundImg = pygame.image.load('background.png')
clock = pygame.time.Clock()

#Tablica bedaca podstawa calej planszy
myArray=[[0 for j in range(31)] for i in range(21)]
#Przykładowe przeszkody, spróbuję zrobić randomowanie
for x in range (0, 20):
        a = random.randint(0,20)
        b = random.randint(0,20)
        myArray[a][b]=2


star_point = (9,9)
final_point = (14,11)
walls = [(12,9),(12,10),(12,11)]
route = Plan_Route(star_point, final_point, walls)
actions = astar_search(route).reconstruct_path()
print(actions)


#Main game loop
while not gameExit:

#Poruszanie sie manualnie
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                lead_x_change = -block_size
                lead_y_change = 0
            elif event.key == pygame.K_RIGHT:
                lead_x_change = block_size
                lead_y_change = 0
            elif event.key == pygame.K_UP:
                lead_x_change = 0
                lead_y_change = -block_size
            elif event.key == pygame.K_DOWN:
                lead_y_change = block_size
                lead_x_change = 0
            elif event.key == pygame.K_SPACE:
                lead_y_change = 0
                lead_x_change = 0

#Granice mapy
    if lead_x > 900:
        lead_x = 900-block_size
    if lead_x < 0:
        lead_x = 0+block_size
    if lead_y > 600:
        lead_y = 600-block_size
    if lead_y < 0:
        lead_y = 0+block_size
    lead_x += lead_x_change
    lead_y += lead_y_change

#Wyswietlanie, uaktualnianie planszy
    gameDisplay.fill(white)
    for x in range (0, 20):
        for y in range (0, 20):
            if (myArray[x][y]!=0):
                a = x
                b = y
                gameDisplay.fill(red,rect=[a*block_size,b*block_size,block_size,block_size])
            else:
                gameDisplay.blit(backgroundImg, (x*block_size,y*block_size))
#Robot
    pygame.draw.rect(gameDisplay, white, [10*block_size,10*block_size,block_size,block_size])
    pygame.draw.rect(gameDisplay, black, [lead_x,lead_y,block_size,block_size])
#Cel
    gameDisplay.fill(blue,rect=[14*block_size,11*block_size,block_size,block_size])
#Te dwie linijki tutaj odpowiadaja za to ze kelner rusza sie o jeden bloczek a nie smiga jak pojebany
    lead_y_change = 0
    lead_x_change = 0
    pygame.display.update()
    clock.tick(100)

pygame.quit()
quit()
