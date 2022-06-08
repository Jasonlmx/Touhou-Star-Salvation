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
        self.surf.set_alpha(256)
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
            self.x_adj=int(math.sin(self.frame*math.pi/180)*10)
        screen.blit(self.surf,(int(self.tx+self.x_adj)-128,int(self.ty)-128))
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

class bossCardPattern(background):
    def __init__(self):
        super(bossCardPattern,self).__init__()
        self.image=global_var.get_value('bossCardPatternPic')
        self.surf=self.image[0]
        self.rect = self.surf.get_rect()
        self.index=0
        self.speedy=-1.3

    def checkValid(self):
        if self.rect.bottom<=30:
            self.ty+=384*3
    
    def inStage(self):
        ifIn=False
        if self.rect.top<=690 or self.rect.bottom>=30:
            ifIn=True
        return ifIn

    def update(self,screen):
        self.frame+=1
        self.movement()
        if self.frame%12==0:
            self.index+=1
        self.index=self.index%60
        self.surf=self.image[self.index]
        if self.inStage():
            screen.blit(self.surf,(int(self.tx)-192,int(self.ty)-192))
        self.checkValid()
    
class duelLevelBackObj(background):
    def __init__(self):
        super(duelLevelBackObj,self).__init__()
        self.surf = global_var.get_value('duelLevelBack')
    
    def checkValid(self):
        if self.ty>=690+140:
            self.ty-=280*4

    def update(self,screen):
        self.frame+=1
        self.movement()
        if self.ty<30-140 or self.ty>690+140:
            pass
        else:
            screen.blit(self.surf,(round(self.tx-140),round(self.ty-140)))
        self.checkValid()
    