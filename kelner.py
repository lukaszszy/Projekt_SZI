import pygame
from astar_alghoritm import *
import tensorflow as tf
import random
import sys
import os

pygame.init()

#Rzeczy konfiguracyjne
red = (255,0,0)
block_size = 30
clock = pygame.time.Clock()
size = 10
display = size*block_size
gameDisplay = pygame.display.set_mode((display, display))

kelner_position_x = 0 
kelner_position_y = 0 
goal_x = 0 #położenie na mapie celu w osi x
goal_y = 0 ##położenie na mapie celu w osi y
j = -1
wc_x = 0	#położenie na mapie wc w osi x
wc_y = 9    #położenie na mapie wc w osi y
wc = {(wc_x, wc_y)}
kuchnia_x = 9
kuchnia_y = 0
solution = None
solution_len = 0
kelner_x = 0
kelner_y = 0
key = ['E', 'S', 'W', 'N']
kuchnia = {kuchnia_x, kuchnia_y}
tree = {(0,2),(0,4),(9,3),(9,5)}
klient = {(8, 2), (8, 5), (8, 8), (5, 2), (5, 5), (5, 8), (2, 2), (2, 5), (2, 8)} #położenie klientów na mapie
wallsSet = klient | wc | kuchnia


#myArray=[[0 for j in range(31)] for i in range(21)]

#Przykładowe przeszkody, spróbuję zrobić randomowanie
#for x in range (0, 20):
#        a = random.randint(0,20)
#        b = random.randint(0,20)
#        myArray[a][b]=2

class Walls:
    def __init__(self, klient, wc, kuchnia, tree):
        self.klient = klient
        self.wc = wc
        self.kuchnia = kuchnia
        self.tree = tree
        self.wallsAll = klient | wc | kuchnia | tree 

walls = Walls(klient, wc, kuchnia, tree)



kelnerImg = pygame.image.load('images/kelner.png')
rotation = 0 #startowy obrót kelnera
transform = pygame.transform.rotate(kelnerImg, rotation)

wcImg = pygame.image.load("images/wc.png")
kuchniaImg = pygame.image.load("images/kitchen.png")
treeImg = pygame.image.load("images/tree.png")
klientImg = pygame.image.load("images/table.png")

# PROJEKT INDYWIDUALNY

#Wyłączenie błędów kompilacji tensorflow
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

# Podajemy ścieżkę do obrazu, który chcemy sklasyfikować.
image_path = r"C:\Users\Amu\Downloads\Projekt_SZI-20180614T141815Z-001\Projekt_SZI\materialy_do_klasyfikatora\10.jpeg"
#image_path = sys.argv[1]

# Pobieramy dane z obrazu.
image_data = tf.gfile.FastGFile(image_path, 'rb').read()

# Pobieramy etykiety z pliku do tablicy 
label_lines = [line.rstrip() for line 
    in tf.gfile.GFile("tf_files/retrained_labels.txt")]
				   
# Odczytujemy graf, który wcześniej został wytrenowany
with tf.gfile.FastGFile("tf_files/retrained_graph.pb", 'rb') as f:
 
    # Inicjalizujemy graf.
    graph_def = tf.GraphDef()

    # Parsujemy dane do zmiennej
    graph_def.ParseFromString(f.read())

    # Iportujemy zserializowany bufor protokolu do utworzonego grafu.
    # Wyodrębniamy oiekty jako tf.Tensor
    _ = tf.import_graph_def(graph_def, name='')	
    
with tf.Session() as sess:

    # Uzywamy wytrenowanego modelu do klasyfikacji. 
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

    # Zwracamy wartości predykacyjne do tablicy.
    predictions = sess.run(softmax_tensor,{'DecodeJpeg/contents:0': image_data})
	
    # Sortujemy wartości według najwyższej zgodności.
    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
    print(label_lines[top_k[0]])

	# Wyswietlenie wyników.

    #for node_id in top_k:
    #    human_string = label_lines[node_id]
    #    score = predictions[0][node_id]
    #    print('%s (score = %.5f)' % (human_string, score))    
	
running = True
while (running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            goal_x = int(pos[0]/ block_size)
            goal_y = int(pos[1]/ block_size)
            kelner_position_x = (kelner_x/block_size)
            kelner_position_y = (kelner_y / block_size)
            if (goal_x, goal_y) not in wallsSet:
                j = 0
                solution = None
                route = PlanRoute((kelner_position_x, kelner_position_y, key[0]), (goal_x, goal_y), walls, size)
                if (astar_search(route) != None):
                    solution = astar_search(route).solution()
                    solution_len = solution.__len__()
                    print(solution)

    if j>=0 and j < solution_len and (solution != None):
        x = solution[j]
        if x == 'SkretPrawo':
            rotation = rotation - 90
            transform = pygame.transform.rotate(kelnerImg, rotation)
            key = key[1:] + [key[0]]
        if x == 'SkretLewo':
            rotation = rotation + 90
            transform = pygame.transform.rotate(kelnerImg, rotation)
            key = [key[3]] + key[:3]
        if x == 'Prosto':
            y = key[0]
            if y == 'N':
                kelner_y -= block_size
            if y == 'S':
                kelner_y += block_size
            if y == 'W':
                kelner_x -= block_size
            if y == 'E':
                kelner_x += block_size
        j = j + 1
    """Poruszanie się przyciskami klawiatury"""
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: 
	    kelner_y -= block_size
    if pressed[pygame.K_DOWN]: 
	    kelner_y += block_size
    if pressed[pygame.K_LEFT]: 
	    kelner_x -= block_size
    if pressed[pygame.K_RIGHT]: 
	    kelner_x += block_size

    """Kolor tla"""
    gameDisplay.fill((179, 149, 149))

    """Siatka tla"""
    for i in range(0, display, 30): 
        vertical_line = pygame.Surface((1, display), pygame.SRCALPHA)
        vertical_line.fill((149, 96, 96, 30))
        gameDisplay.blit(vertical_line, (i - 1, 0))
        horizontal_line = pygame.Surface((display, 1), pygame.SRCALPHA)
        horizontal_line.fill((149, 96, 96, 30))
        gameDisplay.blit(horizontal_line, (0, i - 1))

    """Rysowanie klientow"""
    for x in klient: 
        #pygame.draw.rect(gameDisplay, (255, 255, 255), pygame.Rect(x[0] * block_size, x[1] * block_size, block_size, block_size))
        gameDisplay.blit(klientImg, (x[0]*block_size, x[1]*block_size))
    for y in tree: 
        gameDisplay.blit(treeImg, (y[0]*block_size, y[1]*block_size))
#for x in range (0, 20):
#       for y in range (0, 20):
#            if (myArray[x][y]!=0):
#                a = x
#                b = y
#                gameDisplay.fill(red,rect=[a*block_size,b*block_size,block_size,block_size])

    gameDisplay.blit(wcImg, (wc_x*block_size, wc_y*block_size))
    gameDisplay.blit(kuchniaImg, (kuchnia_x*block_size, kuchnia_y*block_size))
    gameDisplay.blit(transform, (kelner_x, kelner_y)) 
  
    pygame.display.flip()
    clock.tick(10)
