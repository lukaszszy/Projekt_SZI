import pygame
from astar_alghoritm import *
import tensorflow as tf
import random
import sys
import os
import re
from data import *
from id3 import Id3Estimator, export_graphviz
import numpy as np
import random

pygame.init()


#PROJEKT INDYWIDUALNY ZW
#nazwy cech
feature_names = ["kwasne",
                 "gorzkie",
                 "szybkie",
                 "pitne","slodkie","lekkostrawne","na wynos","kaloryczne","zdrowe","ekskluzywne","tanie","smaczne"]
				 
#przypadki testowe z wartościami cech:
X = np.array([

[0,0,0,4,8,8,10,0,2,6,2,"tak"],
[0,0,5,10,7,7,10,0,0,5,1,"tak"],
[4,0,1,8,8,6,10,0,1,8,4,"tak"],
[5,0,6,5,8,8,10,1,0,5,0,"tak"],
[3,1,2,5,8,5,9,9,1,8,4,"tak"],
[5,0,6,6,8,5,10,0,1,4,4,"tak"],
[2,0,2,5,5,8,10,8,0,5,5,"tak"],
[5,3,1,9,9,9,9,1,1,9,4,"tak"],
[6,0,0,3,8,7,10,5,0,6,2,"tak"],
[6,0,3,4,5,4,10,7,0,6,7,"tak"],
[0,0,1,4,7,9,0,0,7,2,1,"tak"],
[0,7,0,5,9,5,0,0,9,5,0,"tak"],
[0,2,4,8,8,5,1,0,10,1,1,"tak"],
[0,5,8,7,8,4,0,5,0,7,0,"tak"],
[1,8,5,5,6,5,8,0,10,4,2,"tak"],
[0,3,2,6,7,7,0,0,10,0,0,"tak"],
[0,5,5,9,9,4,0,0,10,1,1,"przepyszne"],
[1,9,9,9,4,4,1,1,1,9,1,"przepyszne"],
[0,0,5,2,8,5,0,0,5,5,0,"przepyszne"],
[0,0,3,3,7,4,0,0,8,1,5,"przepyszne"],
[10,5,7,7,9,7,0,0,8,1,4,"przepyszne"],
[10,7,7,10,10,10,0,0,9,0,0,"przepyszne"],
[10,0,10,10,8,8,0,0,10,8,8,"przepyszne"],
[10,10,10,10,10,9,0,0,9,0,7,"przepyszne"],
[10,4,10,10,7,8,0,0,10,2,4,"przepyszne"],
[10,10,10,10,10,10,0,0,6,0,3,"przepyszne"],
[10,8,5,10,9,10,0,0,9,0,9,"przepyszne"],
[10,9,9,9,9,9,1,1,9,1,4,"przepyszne"],
[10,4,5,8,8,9,0,0,8,0,8,"przepyszne"],
[10,4,8,8,9,8,0,0,9,0,4,"przepyszne"],
[0,0,0,3,8,7,7,10,1,7,0,"przepyszne"],
[0,0,0,1,4,4,10,10,0,5,0,"domowej roboty"],
[0,0,0,2,2,4,5,10,2,9,1,"domowej roboty"],
[0,0,3,3,6,4,10,10,0,7,0,"domowej roboty"],
[1,1,5,3,4,5,9,9,1,7,4,"domowej roboty"],
[0,0,1,3,3,3,10,10,0,3,3,"domowej roboty"],
[0,0,2,2,3,1,10,10,0,7,7,"domowej roboty"],
[1,1,1,1,1,1,9,9,1,9,1,"domowej roboty"],
[0,0,0,2,4,2,10,10,0,5,0,"domowej roboty"],
[0,0,3,2,3,3,10,10,0,6,3,"domowej roboty"],
[10,5,0,9,7,7,0,0,4,1,0,"domowej roboty"],
[10,7,0,9,9,9,10,0,7,0,0,"domowej roboty"],
[10,0,2,8,3,6,0,0,4,8,0,"domowej roboty"],
[10,0,5,8,9,6,0,0,6,0,0,"domowej roboty"],
[7,3,2,7,7,7,0,0,4,1,1,"domowej roboty"],
[10,8,1,10,10,8,0,0,7,0,0,"domowej roboty"],
[10,8,5,7,5,9,0,0,5,0,0,"domowej roboty"],
[10,9,1,9,9,9,1,1,9,1,1,"domowej roboty"],
[10,5,0,8,8,8,0,0,0,0,2,"domowej roboty"],
[10,3,4,8,8,8,0,0,9,0,0,"domowej roboty"],
[10,5,9,8,6,8,10,0,3,3,1,"domowej roboty"],
[10,7,10,9,9,10,10,0,7,0,3,"domowej roboty"],
[10,7,9,8,8,9,10,0,6,5,5,"domowej roboty"],
[10,10,10,10,10,10,10,0,8,0,0,"domowej roboty"],
[10,2,10,10,7,7,9,0,10,1,2,"domowej roboty"],
[10,8,8,8,10,8,10,0,5,0,0,"domowej roboty"],
[10,8,5,7,5,9,0,0,8,1,5,"domowej roboty"],
[10,9,9,9,3,9,9,1,9,1,3,"domowej roboty"],
[10,5,10,10,9,8,10,0,8,0,2,"domowej roboty"],
[10,2,10,5,7,7,10,0,3,0,0,"domowej roboty"],
[0,0,4,4,8,4,5,8,1,7,0,"domowej roboty"],
[0,0,0,7,7,7,8,9,0,4,0,"przecietnie"],
[0,0,0,7,7,3,9,10,0,8,3,"przecietnie"],
[0,0,0,5,9,7,7,10,0,5,0,"przecietnie"],
[1,1,3,8,6,8,6,9,1,6,4,"przecietnie"],
[0,0,2,4,5,4,10,10,0,2,0,"przecietnie"],
[0,0,2,5,5,3,5,10,0,8,8,"przecietnie"],
[1,1,1,9,9,4,1,1,1,9,1,"przecietnie"],
[0,0,0,7,7,4,5,5,0,5,0,"przecietnie"],
[0,0,2,3,4,3,10,10,0,6,0,"przecietnie"],
[10,5,3,8,10,5,0,0,7,1,1,"przecietnie"],
[10,7,0,9,10,8,0,0,8,0,0,"przecietnie"],
[10,0,3,8,8,8,0,0,8,8,3,"przecietnie"],
[10,10,5,10,10,6,0,0,6,0,0,"przecietnie"],
[8,1,5,8,8,7,0,0,5,1,1,"przecietnie"],
[10,6,5,10,10,8,0,0,8,0,0,"przecietnie"],
[10,0,5,9,8,10,0,0,10,0,0,"przecietnie"],
[10,9,1,9,9,9,1,1,9,1,1,"przecietnie"],
[10,5,5,8,8,7,0,0,10,0,3,"przecietnie"],
[10,1,2,10,9,9,0,0,9,0,0,"przecietnie"],
[0,0,1,3,5,3,9,10,2,5,4,"przecietnie"],
[0,0,0,1,5,3,10,10,0,7,0,"przecietnie"],
[0,0,0,4,3,3,8,10,2,8,1,"przecietnie"],
[0,0,2,5,6,4,10,10,0,7,0,"przecietnie"],
[1,1,5,3,6,4,9,9,1,10,4,"przecietnie"],
[0,0,1,4,4,3,10,10,0,2,2,"przecietnie"],
[0,0,5,3,5,0,10,10,0,6,6,"przecietnie"],
[1,1,1,1,3,1,9,9,1,9,1,"przecietnie"],
[0,0,0,2,3,6,5,10,0,5,0,"przecietnie"],
[0,0,2,2,2,2,10,10,0,6,2,"przecietnie"],
[0,0,0,5,5,2,8,8,2,7,2,"przecietnie"],
[0,0,0,3,5,4,9,9,0,6,2,"tak"],
[0,0,1,2,2,2,6,10,1,8,1,"tak"],
[0,5,5,3,6,4,8,8,0,0,0,"tak"],
[1,1,4,2,5,4,9,9,1,7,3,"tak"],
[0,0,2,5,5,5,10,10,0,0,2,"tak"],
[0,0,5,8,9,0,10,10,0,5,5,"tak"],
[1,4,4,9,4,3,9,1,1,9,1,"tak"],
[0,0,0,2,3,3,5,5,0,5,0,"tak"],
[0,0,2,2,2,2,8,10,0,6,1,"tak"],
[0,0,0,4,2,2,2,9,1,7,1,"tak"],
[0,0,0,3,5,3,9,9,0,5,2,"tak"],
[0,0,0,5,5,5,7,8,0,8,2,"tak"],
[0,8,0,2,4,3,5,10,0,5,0,"tak"],
[1,1,4,2,5,4,9,9,1,6,3,"tak"],
[0,0,2,5,5,6,10,10,1,3,2,"tak"],
[0,0,5,5,5,0,10,10,0,5,5,"tak"],
[1,1,1,9,3,1,9,9,1,9,1,"tak"],
[0,0,0,2,3,1,5,5,0,5,2,"tak"],
[0,0,2,4,4,2,5,10,0,5,1,"tak"],
[0,0,9,0,4,0,10,0,1,8,2,"tak"],
[0,0,10,10,9,5,10,0,0,4,5,"tak"],
[0,3,10,8,5,4,10,1,1,8,3,"tak"],
[0,8,10,10,8,8,10,0,8,0,8,"tak"],
[1,1,10,5,7,5,9,0,1,5,3,"tak"],
[0,4,10,10,9,8,10,0,3,2,2,"tak"],
[0,0,5,5,5,5,10,10,0,5,5,"tak"],
[1,9,9,9,9,9,9,1,1,9,9,"tak"],
[0,0,10,8,3,5,10,0,0,5,2,"tak"],
[0,0,10,5,5,3,0,1,0,3,5,"tak"],
[0,10,5,5,3,3,0,0,10,1,0,"tak"],
[0,10,8,10,7,5,0,0,10,0,0,"tak"],
[0,10,9,10,4,3,0,0,10,2,7,"tak"],
[0,10,10,10,8,6,0,0,10,0,0,"tak"],
[1,10,10,3,6,6,6,0,10,2,2,"tak"],
[0,10,10,10,8,7,0,0,10,0,0,"tak"],
[0,10,10,5,5,2,0,0,10,0,0,"tak"],
[1,9,9,9,3,9,1,1,9,1,1,"tak"],
[0,10,5,2,4,4,0,0,10,0,0,"tak"],
[0,10,10,2,2,2,10,0,10,0,0,"tak"],
[0,0,1,5,9,5,8,8,1,7,2,"tak"],
[3,0,0,10,9,7,8,9,0,2,0,"tak"],
[4,0,1,3,7,5,8,5,1,9,4,"tak"],
[5,0,5,8,8,6,5,5,0,5,0,"tak"],
[3,1,3,3,7,7,9,9,1,5,4,"tak"],
[5,0,2,8,8,5,10,10,0,4,1,"tak"],
[5,0,5,2,5,5,10,10,0,5,5,"tak"],
[1,1,1,9,9,9,9,1,1,9,1,"tak"],
[6,0,0,3,3,4,5,5,0,5,1,"tak"],
[8,0,2,2,4,6,1,10,0,8,2,"tak"],
[0,0,10,5,5,3,8,7,3,5,4,"tak"],
[1,0,10,10,7,7,10,0,0,6,4,"tak"],
[4,2,9,8,6,5,5,1,2,9,5,"tak"],
[5,6,8,8,8,6,8,10,5,0,5,"tak"],
[3,1,10,3,6,5,9,6,1,5,4,"tak"],
[5,5,8,7,6,6,10,0,2,3,4,"tak"],
[5,0,10,5,5,5,10,10,0,5,5,"tak"],
[1,9,9,9,9,9,9,1,1,9,1,"tak"],
[6,0,10,5,5,6,10,0,5,5,2,"tak"],
[6,0,10,4,4,6,0,2,0,4,5,"tak"]])
y = np.array(
["chlodnik",
"chlodnik",
"chlodnik",
"chlodnik",
"chlodnik",
"chlodnik",
"chlodnik",
"chlodnik",
"chlodnik",
"chlodnik",
"chlodnik",
"chlodnik",
"chlodnik",
"chlodnik",
"chlodnik",
"ciasto czekoladowe",
"ciasto czekoladowe",
"ciasto czekoladowe",
"ciasto czekoladowe",
"ciasto czekoladowe",
"ciasto czekoladowe",
"ciasto czekoladowe",
"ciasto czekoladowe",
"ciasto czekoladowe",
"ciasto czekoladowe",
"ciasto czekoladowe",
"ciasto czekoladowe",
"ciasto czekoladowe",
"ciasto czekoladowe",
"ciasto czekoladowe",
"frytki",
"frytki",
"frytki",
"frytki",
"frytki",
"frytki",
"frytki",
"frytki",
"frytki",
"frytki",
"frytki",
"frytki",
"frytki",
"frytki",
"frytki",
"krokiety z miesem",
"krokiety z miesem",
"krokiety z miesem",
"krokiety z miesem",
"krokiety z miesem",
"krokiety z miesem",
"krokiety z miesem",
"krokiety z miesem",
"krokiety z miesem",
"krokiety z miesem",
"krokiety z miesem",
"krokiety z miesem",
"krokiety z miesem",
"krokiety z miesem",
"krokiety z miesem",
"lody truskawkowe",
"lody truskawkowe",
"lody truskawkowe",
"lody truskawkowe",
"lody truskawkowe",
"lody truskawkowe",
"lody truskawkowe",
"lody truskawkowe",
"lody truskawkowe",
"lody truskawkowe",
"lody truskawkowe",
"lody truskawkowe",
"lody truskawkowe",
"lody truskawkowe",
"lody truskawkowe",
"ryz",
"ryz",
"ryz",
"ryz",
"ryz",
"ryz",
"ryz",
"ryz",
"ryz",
"ryz",
"ryz",
"ryz",
"ryz",
"ryz",
"ryz",
"sok pomaranczowy",
"sok pomaranczowy",
"sok pomaranczowy",
"sok pomaranczowy",
"sok pomaranczowy",
"sok pomaranczowy",
"sok pomaranczowy",
"sok pomaranczowy",
"sok pomaranczowy",
"sok pomaranczowy",
"sok pomaranczowy",
"sok pomaranczowy",
"sok pomaranczowy",
"sok pomaranczowy",
"sok pomaranczowy",
"spaghetti po bolonsku",
"spaghetti po bolonsku",
"spaghetti po bolonsku",
"spaghetti po bolonsku",
"spaghetti po bolonsku",
"spaghetti po bolonsku",
"spaghetti po bolonsku",
"spaghetti po bolonsku",
"spaghetti po bolonsku",
"spaghetti po bolonsku",
"spaghetti po bolonsku",
"spaghetti po bolonsku",
"spaghetti po bolonsku",
"spaghetti po bolonsku",
"spaghetti po bolonsku",
"wino czerwone",
"wino czerwone",
"wino czerwone",
"wino czerwone",
"wino czerwone",
"wino czerwone",
"wino czerwone",
"wino czerwone",
"wino czerwone",
"wino czerwone",
"wino czerwone",
"wino czerwone",
"wino czerwone",
"wino czerwone",
"wino czerwone",
"zupa pomidorowa",
"zupa pomidorowa",
"zupa pomidorowa",
"zupa pomidorowa",
"zupa pomidorowa",
"zupa pomidorowa",
"zupa pomidorowa",
"zupa pomidorowa",
"zupa pomidorowa",
"zupa pomidorowa",
"zupa pomidorowa",
"zupa pomidorowa",
"zupa pomidorowa",
"zupa pomidorowa",
"zupa pomidorowa",
])
# tworzenie drzewa decyzyjnego
clf = Id3Estimator()
# fit - synonim do "find patterns in data"
clf.fit(X, y, check_input=True)



export_graphviz(clf.tree_, "test.dot", feature_names)



#Rzeczy konfiguracyjne
red = (255,0,0)
block_size = 30
clock = pygame.time.Clock()
size = 20
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
klient = {(19,2), 
(0,19), 
(15,17), 
(19,2), 
(2,0), 
(3,0), 
(0,4), 
(0,5), 
(19,19), 
(18,10), 
(0,18), 
(0,7), 
(19,19), 
(14,18), 
(18,0), 
(18,17)} #położenie klientów na mapie

wallsSet = klient | wc | kuchnia | tree


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

zamowienia = []
dostarczanie_zamowienia = False

running = True
while (running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            dostarczanie_zamowienia = False
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
#                    print(solution)
        else:
            dostarczanie_zamowienia = True
            kelner_position_x = (kelner_x/block_size)
            kelner_position_y = (kelner_y / block_size)

            if (goal_x, goal_y) not in wallsSet:
                j = 0
                solution = None
                route = PlanRoute((kelner_position_x, kelner_position_y, key[0]), (goal_x, goal_y), walls, size)
                if (astar_search(route) != None):
                    solution = astar_search(route).solution()
                    solution_len = solution.__len__()
 #                   print(solution)

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

        # Pojawienie się kelnera w kuchni
        if j == solution_len and(goal_x == kuchnia_x and goal_y == kuchnia_y):
            if len(zamowienia) > 0:
                for z in zamowienia: print (z[1], end=' ')
                tekst = input('\nPodaj produkt z kuchni: ')
                # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
                # PROJEKT INDYWIDUALNY
                #Wyłączenie błędów kompilacji tensorflow
                os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
                # Podajemy ścieżkę do obrazu, który chcemy sklasyfikować.
                #image_path = r"D:\SZI\materialy_do_klasyfikatora\10.jpeg"
                image_path = r"C:\\\\Users\\\\Amu\\\\Downloads\\\\A_Sztuczna_inteligencja\\\\materialy_do_klasyfikatora\\\\"
                image_path += tekst
                image_path += r".jpeg"
                #image_path = sys.argv[1]
                # Pobieramy dane z obrazu.
                image_data = tf.gfile.FastGFile(image_path, 'rb').read()
                # Pobieramy etykiety z pliku do tablicy 
                label_lines = [line.rstrip() for line in tf.gfile.GFile("tf_files/retrained_labels.txt")]	   
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
                    # Wyswietlenie wyników.
                    #for node_id in top_k:
                    #    human_string = label_lines[node_id]
                    #    score = predictions[0][node_id]
                    #    print('%s (score = %.5f)' % (human_string, score)) 
                # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
                produkt = label_lines[top_k[0]]
                znaleziono = False
                while not znaleziono:
                    for item in zamowienia:
                        if produkt in item:
                            stolik_x = item[0][0]
                            stolik_y = item[0][1]
                            stolik = (stolik_x, stolik_y)
                            znaleziono = True
                            zamowienia.remove((stolik,produkt))
                            # Podejscie z daniem do stolika
                            goal_x = stolik_x
                            goal_y = stolik_y
                            dostarczanie_zamowienia = True
                            print ("Zanoszę do stolika " + produkt)
                    znaleziono = True
            else:
                print ("Brak produktów do wydania.")    

        else:
            if j == solution_len and(goal_x != kuchnia_x and goal_y != kuchnia_y) and dostarczanie_zamowienia == False:						        
                print('Jaki chcesz produkt? "kwasne", "gorzkie","szybkie","pitne","slodkie","lekkostrawne","na wynos","kaloryczne","zdrowe","ekskluzywne","tanie","smaczne. Wybierz dwie cechy')
                produkt1 = input('Podaj jaki: ')
                produkt2 = input('Podaj jaki: ')

                dod = []
                for i in range(0,149):
                    dod = X[i]
                    if(dod[4] == '10' and produkt1 == 'slodkie'):
                        danie = (clf.predict(X)[i]) #wyswietla jedena decyzje z tablicy X
                        print('Kelner: Czy odpowiada Panu danie: ' + danie)
                        print('Tak')
                        break
				   
                stolik = (goal_x,goal_y)
#                danie = input('Podaj produkt: ')
                zamowienia.append((stolik,danie))

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