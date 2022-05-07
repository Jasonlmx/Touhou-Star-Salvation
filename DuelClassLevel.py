import pygame,sys
import random
import math
from pygame.locals import *
from pygame.sprite import Group
import gF 
import Bullet
import DADcharacter
import Slave
import global_var
import Effect
import gameRule

class testEnemy(DADcharacter.enemy):
    def __init__(self):
        super(testEnemy,self).__init__()



def stageController(screen,frame,enemys,bullets,slaves,items,effects,backgrounds,bosses,player):
    if frame%50==0:
        new_enemy=testEnemy()
        new_enemy.initialize(random.random()*600+60,random.random()*660+30,0,-1)
        enemys.add(new_enemy)