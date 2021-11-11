import pygame,sys
import random
import math
from pygame.locals import *
from pygame.sprite import Group
import gF 
import global_var

class item(pygame.sprite.Sprite):
    def __init__(self):
        super(item,self).__init__()
        self.surf = pygame.Surface((20,20))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.tx=0.0
        self.ty=0.0
        self.type=0
        self.speedx=0
        self.speedy=-3
        self.distance=1000
        self.lastFrame=0
        self.rotationAngle=0
        self.image=0
        self.alias=0
        self.followPlayer=0
        self.followSpeed=7
        self.direction=4
        self.rotatedImage=0
    def initial(self,posx,posy):
        self.tx=posx
        self.ty=posy
        image=pygame.Surface((24,24))
        image=image.convert_alpha()
        #image.set_alpha(256)
        image.fill((0,0,0,0))
        #image.set_colorkey((0, 0, 0))
        image.blit(global_var.get_value('itemImage'), (0, 0), (24*self.type,0, 24,24))
        if self.type==7:
            image.set_alpha(150)
        alias=pygame.Surface((24,24))
        alias=alias.convert_alpha()
        alias.fill((0,0,0,0))
        alias.blit(global_var.get_value('itemImage'), (0, 0), (24*(self.type+8),0, 24,24))
        self.image=image
        self.alias=alias

    def truePos(self):
        self.rect.centerx=self.tx
        self.rect.centery=self.ty
    
    def movement(self):
        self.tx+=self.speedx
        self.ty+=self.speedy
        self.truePos()
    
    def speedAlter(self,speedx,speedy):
        self.speedx=speedx
        self.speedy=speedy
    
    def selfTarget(self,playercx,playercy,speed):
        mycx=self.tx
        mycy=self.ty
        dif=math.sqrt(math.pow(playercx-mycx,2)+math.pow(playercy-mycy,2))
        times=dif/speed
        speedx=(playercx-mycx)/times
        speedy=(playercy-mycy)/times
        self.speedAlter(speedx,speedy)

    def checkValid(self,player):
        if self.rect.top>=720-30:
            self.kill()
        if self.rect.right<=0+60:
            self.kill()
        if self.rect.left>=660:
            self.kill()
        if self.distance<=10:
            self.doBonus(player)
            self.kill()
    
    def countDistance(self):
        px=global_var.get_value('player1x')
        py=global_var.get_value('player1y')
        dx=abs(px-self.tx)
        dy=abs(py-self.ty)
        self.distance=math.sqrt(math.pow(dx,2)+math.pow(dy,2))

    def update(self,screen,player):
        self.lastFrame+=1
        if self.lastFrame<=60:
            if self.followPlayer!=1 or self.lastFrame<=30:
                self.speedy+=0.10
        self.movement()
        self.countDistance()
        if self.type!=7:
            if self.followPlayer==1 and self.lastFrame>=30:
                px=global_var.get_value('player1x')
                py=global_var.get_value('player1y')
                self.selfTarget(px,py,self.followSpeed)
                self.followSpeed+=0.1
        elif self.followPlayer==1 and self.lastFrame>=20:
            px=global_var.get_value('player1x')
            py=global_var.get_value('player1y')
            self.selfTarget(px,py,self.followSpeed)
            self.followSpeed+=0.12
        #screen.blit(self.image,(self.rect.centerx-6,self.rect.centery-6))
        #screen.blit(self.surf,self.rect)
        self.draw(screen)
        self.checkValid(player)
    
    def doBonus(self,player):
        if self.type==0:
            if player.power<400:
                player.power+=2
        if self.type==1:
            player.score+=10000
        if self.type==2:
            player.score+=150000
        if self.type==3:
            if player.power<=300:
                player.power+=100
            else:
                player.power=400
        if self.type==4:
            player.score+=20000
        if self.type==5:
            player.power=400
        if self.type==6:
            player.life+=1
            global_var.get_value('life_get').play()
        if self.type==7:
            player.score+=100
        
        if not global_var.get_value('item_getting'):
            if self.type!=6:
                global_var.get_value('item_get').play()
                global_var.set_value('item_getting',True)

    def draw(self,screen):
        if self.ty<=18:
            screen.blit(self.alias,(self.rect.centerx-12,30))
        else:
            if self.type!=7:
                if self.lastFrame<=27:
                    if self.lastFrame%3==0:
                        self.rotationAngle-=45
                    gF.drawRotation(self.image,(self.rect.centerx-12,self.rect.centery-12),self.rotationAngle,screen)
                else:
                    screen.blit(self.image,(self.rect.centerx-12,self.rect.centery-12))
            else:
                screen.blit(self.image,(self.rect.centerx-12,self.rect.centery-12))