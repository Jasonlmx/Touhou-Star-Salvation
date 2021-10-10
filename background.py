import pygame,sys
import random
import math
from pygame.locals import *
from pygame.sprite import Group
import global_var

class background(pygame.sprite.Sprite):
    def __init__(self):
        super(background,self).__init__()
        self.surf = global_var.get_value('lake_bg')
        self.surf.set_alpha(200)
        self.surf.convert()
        self.rect = self.surf.get_rect()
        self.tx=0.0
        self.ty=0.0
        self.type=0
        self.speedx=0
        self.speedy=1.0
        self.x_adj=0
        self.frame=0
        self.cardBg=False
    def checkValid(self):
        if self.rect.top>=720:
            self.ty-=1024
    
    def initial(self,posx,posy):
        self.tx=posx
        self.ty=posy
    
    def speedAlter(self,speedx,speedy):
        self.speedx=speedx
        self.speedy=speedy
    
    def truePos(self):
        self.rect.centerx=self.tx
        self.rect.centery=self.ty
    
    def movement(self):
        self.tx+=self.speedx
        self.ty+=self.speedy
        self.truePos()
    
    def update(self,screen):
        self.frame+=1
        self.movement()
        if self.cardBg:
            self.x_adj=0
        else:
            self.x_adj=round(math.sin(self.frame*math.pi/180)*10)
        screen.blit(self.surf,(round(self.tx+self.x_adj)-128,round(self.ty)-128))
        self.checkValid()

class lake_bg(background):
    def __init__(self):
        super(lake_bg,self).__init__()

class cloud_bg(background):
    def __init__(self):
        super(cloud_bg,self).__init__()
        self.surf = global_var.get_value('cloud_bg')
        self.surf.set_alpha(200)
        self.speedy=2.0