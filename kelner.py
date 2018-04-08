import pygame
 
pygame.init()
 
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,255,255)
mix = (255,127,127)
 
display_width = 800
display_height = 600
 
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Kelner')
 
pygame.display.update()
 
gameExit = False
lead_x = display_width/2
lead_y = display_height/2
lead_x_change = 0
lead_y_change = 0
 
clock = pygame.time.Clock()
 
while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                lead_x_change = -2
                lead_y_change = 0
            elif event.key == pygame.K_RIGHT:
                lead_x_change = 2
                lead_y_change = 0
            elif event.key == pygame.K_UP:
                lead_x_change = 0
                lead_y_change = -2
            elif event.key == pygame.K_DOWN:
                lead_y_change = 2
                lead_x_change = 0
            elif event.key == pygame.K_SPACE:
                lead_y_change = 0
                lead_x_change = 0
 
    if lead_x > 750:
        lead_x = 750
    if lead_x < 50:
        lead_x = 50
    if lead_y > 550:
        lead_y = 550
    if lead_y < 50:
        lead_y = 50
    lead_x += lead_x_change
    lead_y += lead_y_change
           
    gameDisplay.fill(white)
    pygame.draw.rect(gameDisplay, black, [lead_x,lead_y,30,30])
    gameDisplay.fill(red,rect=[200,200,50,50])
    gameDisplay.fill(red,rect=[400,200,50,50])
    gameDisplay.fill(blue,rect=[200,350,50,50])
    gameDisplay.fill(blue,rect=[400,350,50,50])
    gameDisplay.fill(blue,rect=[600,400,50,50])
    gameDisplay.fill(blue,rect=[100,500,50,50])
    gameDisplay.fill(mix,rect=[100,300,50,50])
    gameDisplay.fill(mix,rect=[30,40,50,50])
    gameDisplay.fill(mix,rect=[730,550,50,50])
 
 
    pygame.display.update()
 
    clock.tick(100)
   
pygame.quit()
quit()
