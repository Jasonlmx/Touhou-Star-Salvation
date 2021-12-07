import pygame,sys
import random
import math
import gF
from pygame.sprite import Sprite
import Bullet
import Effect

class slave_circle(pygame.sprite.Sprite):
    def __init__(self):
        super(slave_circle,self).__init__()
        self.surf = pygame.Surface((40,40))
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect()
        self.tx=0.0
        self.ty=0.0
        self.health=200
        self.startFrame=-1
        self.occupy=0
        self.speedx=0
        self.speedy=0
        self.screenRe=0
        self.angle=0
        self.degree=0
        self.degree_step=3
        self.distance=30
        self.maxExistSec=20

    def initialize(self,occupy,degree,degree_step,distance):
        self.degree=degree
        self.degree_step=degree_step
        self.distance=distance
        self.occupy=occupy
        if occupy==2:
            self.screenRe=400

    def countAngle(self,userX,userY):
        dx=self.tx-userX
        dy=self.ty=userY
        if dx!=0:
            t=dy/dx
            deg=math.atan(t)*180/math.pi
        else: 
            if dy>0:
                deg=90
            if dy<0:
                deg=270
        if deg<0:
            deg+=360
        if dy>0 and deg>=180:
            deg=deg-180
        if dy<0 and deg<=180:
            deg=deg+180
        self.angle=deg

    def truePos(self):
        self.rect.centerx=round(self.tx)
        self.rect.centery=round(self.ty)


    def checkValid(self):
        pass

    def checkSec(self,existFrame):
        if existFrame>=self.maxExistSec*60:
            self.kill()
    
    def update(self,screen,frame,bullets,userX,userY):#rewrite required
        if self.startFrame==-1:
            self.startFrame=frame
        existFrame=frame-self.startFrame
        self.degree+=self.degree_step
        self.checkSec(existFrame)
        self.checkValid()
        self.setPosition(userX,userY,existFrame)
        self.drawSlave(screen)

    def setPosition(self,userX,userY,existFrame):
        self.tx=userX+self.distance*math.cos(self.degree/180*math.pi)
        self.ty=userY+self.distance*math.sin(self.degree/180*math.pi)
        self.truePos()

    def drawSlave(self,screen):
        screen.blit(self.surf,self.rect)


   
class slave_linear(pygame.sprite.Sprite):
    def __init__(self):
        super(slave_linear,self).__init__()
        self.surf = pygame.Surface((40,40))
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect()
        self.tx=0.0
        self.ty=0.0
        self.health=200
        self.startFrame=-1
        self.occupy=0
        self.speedx=0
        self.speedy=0
        self.screenRe=0
        self.angle=0
        self.maxExistSec=20
        self.doValidCheck=1
    
    def initial(self,posx,posy,occupy):
        self.tx=posx
        self.ty=posy
        self.fro=occupy
        self.occupy=occupy

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
    
    def countAngle(self):
        if self.speedx!=0:
            t=self.speedy/self.speedx
            deg=math.atan(t)*180/math.pi
        else: 
            if self.speedy>0:
                deg=90
            if self.speedy<0:
                deg=270
        if deg<0:
            deg+=360
        if self.speedy>0 and deg>=180:
            deg=deg-180
        if self.speedy<0 and deg<=180:
            deg=deg+180
        self.angle=deg
    
    def setSpeed(self,angle,speed):
        s=math.sin(math.radians(angle))
        c=math.cos(math.radians(angle))
        self.speedy=s*speed
        self.speedx=c*speed

    def checkValid(self):
        if self.doValidCheck==1:
            if self.rect.top>=600-20:
                self.kill()
            if self.rect.bottom<=0+20:
                self.kill()
            if self.rect.right<=0+30:
                self.kill()
            if self.rect.left>=800-30:
                self.kill()
            if self.rect.right>=400 and self.fro==1:
                self.kill()
            if self.rect.left<=400 and self.fro==2:
                self.kill()
    
    def checkSec(self,existFrame):
        if existFrame>=self.maxExistSec*60:
            self.kill()

    def update(self,screen,frame,bullets,userX,userY):#rewrite required
        if self.startFrame==-1:
            self.startFrame=frame
        existFrame=frame-self.startFrame
        self.movement()
        self.checkValid()
        self.checkSec(existFrame)
        self.drawSlave(screen)
    
    def drawSlave(self,screen):
        screen.blit(self.surf,self.rect)



class Hagrid_slave_typeCircle(slave_circle):
    def __init__ (self):
        super(Hagrid_slave_typeCircle,self).__init__()
        self.maxExistSec=4
    
    def update(self,screen,frame,bullets,userX,userY):
        if self.startFrame==-1:
            self.startFrame=frame
        existFrame=frame-self.startFrame
        self.degree+=self.degree_step
        self.checkSec(existFrame)
        self.checkValid()
        self.setPosition(userX,userY,existFrame)
        #self.drawSlave(screen)
        self.countAngle(userX,userY)
        self.attack(existFrame,bullets)
    
    def attack(self,existFrame,bullets):
        if existFrame%6==0:
            for i in range(1,5):
                new_bullet=Bullet.scale_Bullet()
                new_bullet.initial(self.rect.centerx,self.rect.centery,self.occupy)
                new_bullet.setSpeed(self.degree+(i-1)*90,3)
                new_bullet.loadColor('green')
                bullets.add(new_bullet)

class Hagrid_slave_typeLinear(slave_linear):
    def __init__ (self):
        super(Hagrid_slave_typeLinear,self).__init__()
        self.maxExistSec=10
        self.doValidCheck=1
        self.time=0
        self.playerx=0
        self.playery=0
    def setPlayer(self,x,y):
        self.playerx=x
        self.playery=y

    def update(self,screen,frame,bullets,userX,userY):#rewrited
        if self.startFrame==-1:
            self.startFrame=frame
        existFrame=frame-self.startFrame
        self.movement()
        self.actionControl()
        self.checkValid()
        self.checkSec(existFrame)
        self.drawSlave(screen)
        self.attack(existFrame,bullets)

    def actionControl(self):
        self.countAngle()
        if self.time%2==0:
            self.setSpeed(self.angle+0.5,3)
        else:
            self.setSpeed(self.angle-0.5,3)
    
    def attack(self,existFrame,bullets):
        if existFrame%14==0:
            new_bullet=Bullet.star_Bullet_delaySelfTarget()
            new_bullet.initial(self.rect.centerx,self.rect.centery,self.occupy)
            new_bullet.setProperty(150,1.5)
            new_bullet.setDelayedTarget(self.playerx,self.playery,1.5)
            new_bullet.loadColor('blue')
            bullets.add(new_bullet)
    
    
class bulletCancelLasting(pygame.sprite.Sprite):
    def __init__ (self):
        super(bulletCancelLasting,self).__init__()
        self.tx=0
        self.ty=0
        self.maxFrame=12
        self.maxRadius=900
        self.lastFrame=0
        self.doBonus=False
    def initial(self,tx,ty,maxFrame=12,maxRadius=900,doBonus=False,harsh=False):
        self.tx=tx
        self.ty=ty
        self.maxFrame=maxFrame
        self.maxRadius=maxRadius
        self.doBonus=doBonus
        self.harsh=harsh

    def checkValid(self):
        if self.lastFrame>=self.maxFrame:
            self.kill()
    def getDistance(self,bx,by):
        dx=self.tx-bx
        dy=self.ty-by
        dist=math.sqrt(dx**2+dy**2)
        return dist

    def cancelBullet(self,bullets,effects,items,radius):
        for bullet in bullets:
            if self.getDistance(bullet.tx,bullet.ty)<radius:
                if (bullet.cancalable or self.harsh) and bullet.type!=15:
                    new_effect=Effect.bulletVanish()
                    exception=(5,7,10,11,12,13,15,16)
                    if not bullet.type in exception:
                        new_effect.initial(bullet.image,bullet.rect.centerx,bullet.rect.centery,bullet.dx,bullet.dy)
                    elif bullet.type==5:
                        new_effect.initial(bullet.tempImage,bullet.rect.centerx,bullet.rect.centery,bullet.dx,bullet.dy)
                    elif bullet.type==7:
                        if bullet.color=='red':
                            new_effect.initial(bullet.red[0],bullet.rect.centerx,bullet.rect.centery,bullet.dx,bullet.dy)
                        else:
                            new_effect.initial(bullet.blue[0],bullet.rect.centerx,bullet.rect.centery,bullet.dx,bullet.dy)
                    elif bullet.type==10 or bullet.type==11 or bullet.type==12 or bullet.type==13:
                        new_effect.initial(bullet.tempImage,bullet.rect.centerx,bullet.rect.centery,bullet.dx,bullet.dy)

                    effects.add(new_effect)
                    if self.doBonus and bullet.type!=15:
                        Bullet.createItem(bullet.tx,bullet.ty,items)
                    bullet.kill()

    def update(self,screen,frame,bullets,effects,items):
        self.lastFrame+=1
        radius=self.maxRadius*(self.lastFrame/self.maxFrame)
        self.cancelBullet(bullets,effects,items,radius)
        self.checkValid()