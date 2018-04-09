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

import collections
import math
import cocos
import random
import sys
from cocos import tiles, actions, layer, collision_model as cm
from cocos.director import director
from cocos.actions import MoveTo
import pyglet
from pyglet.window import key

##global
speeed = 100
collision_manager = cm.CollisionManagerBruteForce() #menager kolizji
orlenColl = cm.CollisionManagerBruteForce() #menager kolizji dla stacji paliw
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

class DriveKelner(actions.Driver):
    def step(self, dt):
        global inAction, startAction, doTask, cAdres, isPack, cel, ruch, packAdres, isPicked

        if(not inAction):
            plik = open('NLP.out')
            try:
                tekst = plik.read()
            finally:
                plik.close()
            pl = eval(tekst)
            
            
##            if(len(pl) == 2):
##              zadanie2 = pl[1]
##              rozkaz2 = zadanie2[0]
            zadanie = pl[0]
            rozkaz = zadanie[0]
            if(rozkaz == 'ODBIERZ' or rozkaz == 'ZAWIEĹą'):
              adres = zadanie[2]
            if(rozkaz == 'JEDĹą'):
              adres = zadanie[1]
##            if(len(pl) == 2):
##              if(rozkaz2 == 'ODBIERZ' or rozkaz2 == 'ZAWIEĹą'):
##                adres2 = zadanie2[2]
##              if(rozkaz2 == 'JEDĹą'):
##                adres2 = zadanie2[1]
            inAction=True
            startAction=True
            
        if(not isPack):
          packAdres = cAdres
          while(packAdres == cAdres):
            packAdres = random.choice(list(paczki))
          paczki[packAdres].opacity = 255
          cel = packAdres
          while(cel == packAdres or cel == cAdres):
            cel = random.choice(list(paczki))
          print("musze odebrac zamowienie z " + packAdres + " i dostarczyc na " + cel)
          print("musze odebrac zamowienie z " + packAdres + " i dostarczyc na " + cel)
          isPack = True
          isPicked = False
        
        if(startAction):
            startAction = False
            if(rozkaz == 'ODBIERZ' or rozkaz == 'JEDĹą'):
                ruch = MoveTo(self.target.position,0)
                for i in shortest_path(G, cAdres, adres.lower()):
                  ruch += MoveTo(miejsca[i], 2)
                self.target.do(ruch)
            if(rozkaz == 'ZATANKUJ'):
                ruch = MoveTo(self.target.position,0)
                for i in shortest_path(G, cAdres, 'wojtyniaka'):
                  ruch += MoveTo(miejsca[i], 2)
                self.target.do(ruch)
            if(rozkaz == 'ZAWIEĹą'):
                ruch = MoveTo(self.target.position,0)
                for i in shortest_path(G, cAdres, adres.lower()):
                  ruch += MoveTo(miejsca[i], 2)
                self.target.do(ruch)
            if(rozkaz == 'ODPOCZNIJ'):
                print('Odpoczywam')
            if(rozkaz == 'PRZERWA'):
                ruch = MoveTo(self.target.position,0)
                for i in shortest_path(G, cAdres, 'start'):
                  ruch += MoveTo(miejsca[i], 2)
                self.target.do(ruch)

        if(inAction):
            #print(packAdres + ' ' + cel + ' ' +cAdres + ' ' + str(isPicked) + str(isPack)) 
            if(self.target.position == miejsca['mickiewicza']):
                paczki['mickiewicza'].opacity = 0
                inAction = False
                cAdres = 'mickiewicza'
                if(packAdres == 'mickiweicza'):
                  isPicked = True
                if(cel == 'mickiewicza' and isPicked):
                  isPack = False
                if(packAdres == 'mickiweicza'):
                  isPicked = True
            if(self.target.position == miejsca['orlicza']):
                paczki['orlicza'].opacity = 0
                inAction = False
                cAdres = 'orlicza'
                if(packAdres == 'orlicza'):
                  isPicked = True
                if(cel == 'orlicza' and isPicked):
                  isPack = False
                if(packAdres == 'orlicza'):
                  isPicked = True
            if(self.target.position == miejsca['kuchnia']):
                paczki['kuchnia'].opacity = 0
                inAction = False
                cAdres = 'kuchnia'
                if(packAdres == 'kuchnia'):
                  isPicked = True
                if(cel == 'kuchnia' and isPicked):
                  isPack = False
                if(packAdres == 'kuchnia'):
                  isPicked = True
            if(self.target.position == miejsca['kopernika']):
                paczki['kopernika'].opacity = 0
                inAction = False
                cAdres = 'kopernika'
                if(packAdres == 'kopernika'):
                  isPicked = True
                if(cel == 'kopernika' and isPicked):
                  isPack = False
                if(packAdres == 'kopernika'):
                  isPicked = True
            if(self.target.position == miejsca['borsuka']):
                paczki['borsuka'].opacity = 0
                inAction = False
                cAdres = 'borsuka'
                if(packAdres == 'borsuka'):
                  isPicked = True
                if(cel == 'borsuka' and isPicked):
                  isPack = False
                if(packAdres == 'borsuka'):
                  isPicked = True
            if(self.target.position == miejsca['wojtyniaka']):
                inAction = False
                cAdres = 'wojtyniaka'
            if(cAdres == cel):
              isPicked = True
  
            
            # handle input and move the car

        super(DriveKelner, self).step(dt)
        scroller.set_focus(self.target.x, self.target.y)


def main():
    global keyboard, scroller
    from cocos.director import director
    director.init(width=800, height=600, autoscale=False, resizable=True)
    global inAction, startAction, doTask, isPack, cel, ruch, isPicked, packAdres
    isPiscked = False
    isPack = False
    inAction = False
    doTask = True
    startAction = False
    packAdres = ''

    scroller = layer.ScrollingManager()
    test_layer = tiles.load('mapaSZI.tmx')['Warstwa Kafelków 1']
    obj = tiles.load('mapaSZI.tmx')['GameObjects']
    poi = tiles.load('mapaSZI.tmx')['Points']
    scroller.add(test_layer)
#0=start, 1=up, 2=bottom 3=bottom1,
#0=wojtyniaka, 1=mickiewicza, 2=kopernika, 3=orlicza, 4= kuchnia, 5=borsuka
    kelner_layer = layer.ScrollableLayer()
    kelner = cocos.sprite.Sprite('kelner.png')
    kelner_layer.add(kelner)


    global miejsca
    global paczki
    miejsca = {}
    paczki = {}
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

    wojX = obj.objects[0].x
    wojY = obj.objects[0].y
    miejsca['wojtyniaka'] = (wojX, wojY)

    micX = obj.objects[1].x
    micY = obj.objects[1].y
    miejsca['mickiewicza'] = (micX, micY)

    kopX = obj.objects[2].x
    kopY = obj.objects[2].y
    miejsca['kopernika'] = (kopX, kopY)

    orlX = obj.objects[3].x
    orlY = obj.objects[3].y
    miejsca['orlicza'] = (orlX, orlY)

    kuchX = obj.objects[4].x
    kuchY = obj.objects[4].y
    miejsca['kuchnia'] = (kuchX, kuchY)

    borX = obj.objects[5].x
    borY = obj.objects[5].y
    miejsca['borsuka'] = (borX, borY)

    paczki['mickiewicza'] = cocos.sprite.Sprite('menu.png')
    paczki['orlicza'] = cocos.sprite.Sprite('menu.png')
    paczki['kuchnia'] = cocos.sprite.Sprite('menu.png')
    paczki['kopernika'] = cocos.sprite.Sprite('menu.png')
    paczki['borsuka'] = cocos.sprite.Sprite('menu.png')
    paczki['mickiewicza'].position = miejsca['mickiewicza']
    paczki['orlicza'].position = miejsca['orlicza']
    paczki['kuchnia'].position = miejsca['kuchnia']
    paczki['kopernika'].position = miejsca['kopernika']
    paczki['borsuka'].position = miejsca['borsuka']
    kelner_layer.add(paczki['mickiewicza'])
    kelner_layer.add(paczki['orlicza'])
    kelner_layer.add(paczki['kuchnia'])
    kelner_layer.add(paczki['kopernika'])
    kelner_layer.add(paczki['borsuka'])
    paczki['mickiewicza'].opacity = 0
    paczki['orlicza'].opacity = 0
    paczki['kuchnia'].opacity = 0
    paczki['kopernika'].opacity = 0
    paczki['borsuka'].opacity = 0
    
    global G
    G = Graf()
    G.add_vertex('start')
    G.add_vertex('mickiewicza')
    G.add_vertex('up')
    G.add_vertex('borsuka')
    G.add_vertex('bottom1')
    G.add_vertex('wojtyniaka')
    G.add_vertex('kuchnia')
    G.add_vertex('orlicza')
    G.add_vertex('bottom')
    G.add_vertex('kopernika')

    G.add_edge('start', 'mickiewicza', 9)
    G.add_edge('mickiewicza', 'up', 2)
    G.add_edge('up', 'borsuka', 2)
    G.add_edge('borsuka', 'bottom1', 4)
    G.add_edge('bottom1', 'wojtyniaka', 1)
    G.add_edge('bottom1', 'kuchnia', 3)
    G.add_edge('kuchnia', 'orlicza', 5)
    G.add_edge('orlicza', 'bottom', 3)
    G.add_edge('bottom', 'kopernika', 3)
    G.add_edge('kopernika', 'start', 3)

    G.add_edge('mickiewicza', 'start', 9)
    G.add_edge('up', 'mickiewicza', 2)
    G.add_edge('borsuka', 'up', 2)
    G.add_edge('bottom1', 'borsuka', 4)
    G.add_edge('wojtyniaka', 'bottom1', 1)
    G.add_edge('kuchnia', 'bottom1', 3)
    G.add_edge('orlicza', 'kuchnia', 5)
    G.add_edge('bottom', 'orlicza', 3)
    G.add_edge('kopernika', 'bottom', 3)
    G.add_edge('start', 'kopernika', 3)

    print(shortest_path(G, 'mickiewicza', 'kuchnia'))
    print( paczki[random.choice(list(paczki))].position )

    short = shortest_path(G, 'mickiewicza', 'kuchnia')

    kelner.position = miejsca['start']
    kelner.rotation = 90
    
	
    global cAdres
    cAdres = 'start'
    kelner.do(DriveKelner())
    scroller.add(kelner_layer)
    main_scene = cocos.scene.Scene(scroller)
    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    def on_key_press(key, modifier):#obsluga klawiatury
        if key == pyglet.window.key.Z:
            if scroller.scale == 0.25:
                scroller.do(actions.ScaleTo(1, 0.5))
            else:
                scroller.do(actions.ScaleTo(.25, 0.5))
        elif key == pyglet.window.key.D:
            test_layer.set_debug(True)
        elif key == pyglet.window.key.RIGHT:
            kelner.rotation = 90
            kelner.speed = speeed
        elif key == pyglet.window.key.LEFT:
            kelner.rotation = -90
            kelner.speed = speeed
        elif key == pyglet.window.key.UP:
            kelner.rotation = 0
            kelner.speed = speeed
        elif key == pyglet.window.key.DOWN:
            kelner.rotation = 180
            kelner.speed = speeed
        elif key == pyglet.window.key.SPACE:
            kelner.speed = 0

    director.window.push_handlers(on_key_press)

    director.run(main_scene)

if __name__ == "__main__":
  main()