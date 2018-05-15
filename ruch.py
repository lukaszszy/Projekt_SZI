#!/usr/bin python3
# -*- coding: utf-8 -*-
#from __future__ import division, print_function, unicode_literals

# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

##import sys
##import os
##import time
##
##testinfo = "s, q"
##tags = "tiles, Driver"

##pyglet.resource.path.append(pyglet.resource.get_script_home())
##pyglet.resource.reindex()

# testinfo = "s, q"
# tags = "tiles, Driver"

##from __future__ import division, print_function, unicode_literals


from collections import defaultdict
import math
import random
import sys
import bisect

import collections
import math
import cocos
import random
import sys
import agents
import math, random, sys, time, bisect, string
from cocos import tiles, actions, layer, collision_model as cm
from cocos.director import director
from cocos.actions import MoveTo
import pyglet
from pyglet.window import key

##global
speeed = 100
collision_manager = cm.CollisionManagerBruteForce() #menager kolizji
orlenColl = cm.CollisionManagerBruteForce() #menager kolizji
x = 0
##/global

class Graf:

  def __init__(self):
      self.wiechrzcholki = set()

      self.krawedzie = collections.defaultdict(list)
      self.wagi = {}

  def add_vertex(self, value):
    self.wiechrzcholki.add(value)

  def add_edge(self, od_wierzcholka, do_wierzcholka, dystans):
    if od_wierzcholka == do_wierzcholka: pass  # bez cykli
    self.krawedzie[od_wierzcholka].append(do_wierzcholka)
    self.wagi[(od_wierzcholka, do_wierzcholka)] = dystans

def dijkstra(graf, start):
  S = set()

  delta = dict.fromkeys(list(graf.wiechrzcholki), math.inf)
  poprzednik = dict.fromkeys(list(graf.wiechrzcholki), None)

  delta[start] = 0


  while S != graf.wiechrzcholki:
    v = min((set(delta.keys()) - S), key=delta.get)
    for sasiad in set(graf.krawedzie[v]) - S:
      nowa_sciezka = delta[v] + graf.wagi[v,sasiad]

      if nowa_sciezka < delta[sasiad]:
        delta[sasiad] = nowa_sciezka

        poprzednik[sasiad] = v
    S.add(v)

  return (delta, poprzednik)

def shortest_path(graf, start, end):

  delta, poprzednik = dijkstra(graf, start)

  sciezka = []
  wierzcholek = end

  while wierzcholek is not None and wierzcholek is not start:
    sciezka.append(wierzcholek)
    wierzcholek = poprzednik[wierzcholek]

  sciezka.reverse()
  return sciezka

global inAction, startAction, doTask, G, miejsca, paczki


def main():
    global keyboard, scroller
    from cocos.director import director
    director.init(width=800, height=600, autoscale=False, resizable=True)
    global startAction, doTask, isPack, cel, ruch, isPicked, packAdres

    scroller = layer.ScrollingManager()
    test_layer = tiles.load('mapaSZI.tmx')['Warstwa Kafelków 1']
    obj = tiles.load('mapa.tmx')['GameObjects']
    poi = tiles.load('mapa.tmx')['Points']
    scroller.add(test_layer)
#0=start, 1=up, 2=bottom 3=bottom1,
#0=wojtyniaka, 1=mickiewicza, 2=kopernika, 3=orlicza, 4= kuchnia, 5=borsuka
    kelner_layer = layer.ScrollableLayer()
    kelner = cocos.sprite.Sprite('kelner.png')
    kelner_layer.add(kelner)



    miejsca = {}
    startX = poi.objects[0].x
    startY = poi.objects[0].y
    miejsca['start'] = (startX, startY)

    upX = poi.objects[1].x
    upY = poi.objects[1].y
    miejsca['up'] = (upX, upY)

    bottomX = poi.objects[2].x
    bottomY = poi.objects[2].y
    miejsca['bottom'] = (bottomX, bottomY)

    bottom1X = poi.objects[3].x
    bottom1Y = poi.objects[3].y
    miejsca['bottom1'] = (bottom1X, bottom1Y)

    stacjaX = obj.objects[0].x
    stacjaY = obj.objects[0].y
    miejsca['stacja'] = (stacjaX, stacjaY)

    micX = obj.objects[1].x
    micY = obj.objects[1].y
    miejsca['mickiewicza'] = (micX, micY)

    kopX = obj.objects[2].x
    kopY = obj.objects[2].y
    miejsca['kopernika'] = (kopX, kopY)

    orlX = obj.objects[3].x
    orlY = obj.objects[3].y
    miejsca['orlicza'] = (orlX, orlY)

    pasX = obj.objects[4].x
    pasY = obj.objects[4].y
    miejsca['pascala'] = (pasX, pasY)

    borX = obj.objects[5].x
    borY = obj.objects[5].y
    miejsca['borsuka'] = (borX, borY)

    G = Graf()
    G.add_vertex('start')
    G.add_vertex('mickiewicza')
    G.add_vertex('up')
    G.add_vertex('borsuka')
    G.add_vertex('bottom1')
    G.add_vertex('stacja')
    G.add_vertex('pascala')
    G.add_vertex('orlicza')
    G.add_vertex('bottom')
    G.add_vertex('kopernika')
    G.add_edge('start', 'mickiewicza', 9)
    G.add_edge('mickiewicza', 'up', 2)
    G.add_edge('up', 'borsuka', 2)
    G.add_edge('borsuka', 'bottom1', 4)
    G.add_edge('bottom1', 'stacja', 1)
    G.add_edge('bottom1', 'pascala', 3)
    G.add_edge('pascala', 'orlicza', 5)
    G.add_edge('orlicza', 'bottom', 3)
    G.add_edge('bottom', 'kopernika', 3)
    G.add_edge('kopernika', 'start', 3)


    G.add_edge('mickiewicza', 'start', 9)
    G.add_edge('up', 'mickiewicza', 2)
    G.add_edge('borsuka', 'up', 2)
    G.add_edge('bottom1', 'borsuka', 4)
    G.add_edge('stacja', 'bottom1', 1)
    G.add_edge('pascala', 'bottom1', 3)
    G.add_edge('orlicza', 'pascala', 5)
    G.add_edge('bottom', 'orlicza', 3)
    G.add_edge('kopernika', 'bottom', 3)
    G.add_edge('start', 'kopernika', 3)

    print(shortest_path(G, 'mickiewicza', 'pascala'))

    short = shortest_path(G, 'mickiewicza', 'pascala')

    kelner.position = miejsca['start']
    kelner.rotation = 90


    ruch = MoveTo(miejsca['start'],0)
    for i in short:
        ruch += MoveTo(miejsca[i], 2)
        kelner.do(ruch)


    scroller.add(kelner_layer)
    main_scene = cocos.scene.Scene(scroller)

    director.run(main_scene)

if __name__ == "__main__":
  main()
