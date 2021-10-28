import pygame,sys
import random
import math
import gF
from pygame.sprite import Sprite
import global_var
import Effect
import Item

def createItem(tx,ty,items):
    new_item=Item.item()
    new_item.type=7
    new_item.followPlayer=1
    new_item.followSpeed=8
    x_now=tx
    y_now=ty
    if x_now<80:
        x_now=80
    if x_now>640:
        x_now=640
    new_item.initial(x_now,y_now)
    items.add(new_item)

class bulletBarrier(pygame.sprite.Sprite):
    def __init__(self):
        super(bulletBarrier,self).__init__()
        self.surf=pygame.Surface((100,100))
        self.surf.fill((0,255,0))
        self.rect=self.surf.get_rect()
        self.inUse=0
        self.startFrame=-1
        self.image=pygame.image.load('resource/playerMagic.png').convert_alpha()
        self.cvImage=pygame.image.load('resource/playerMagic.png').convert_alpha()
        self.range=200
        self.maxRange=200
        self.tx=0
        self.ty=0
        self.angle=0
    def update(self,frame):
        if self.inUse==1:
            if self.startFrame==-1:
                self.startFrame=frame
            existFrame=frame-self.startFrame
            frm=existFrame
            if frm>=25:
                frm=25
            rng=round(30+frm*(self.maxRange-30)/25)
            self.setRange(rng)
            self.truePos()
            if existFrame>=75:
                self.inUse=0
                self.startFrame=-1

    def setRange(self,range):
        self.surf=pygame.Surface((range,range))
        self.cvImage=pygame.transform.scale(self.image, (range, range))
        self.range=range
        self.rect=self.surf.get_rect()
    def setPos(self,cx,cy):
        self.tx=cx
        self.ty=cy
    def draw(self,screen,frame):
        angle=frame%120*3
        gF.drawRotation(self.cvImage,(self.rect.centerx-self.range//2,self.rect.centery-self.range//2),angle,screen)
        #screen.blit(self.cvImage,(self.rect.centerx-self.range//2,self.rect.centery-self.range//2))
    def truePos(self):
        self.rect.centerx=self.tx
        self.rect.centery=self.ty

class playerGun(pygame.sprite.Sprite):
    def __init__(self):
        super(playerGun,self).__init__()
        self.surf = pygame.Surface((6,15))
        self.surf.fill((255,255,255))
        self.rect=self.surf.get_rect()
        self.tx=0.0
        self.ty=0.0
        self.speedx=0
        self.speedy=0
        self.speed=40
        self.color='green'
        self.hit=60
    def countAngle(self):
        if self.speedx!=0:
            t=self.speedy/self.speedx
            deg=math.atan(t)*180/math.pi
        else: 
            if self.speedy>0:
                deg=90
            elif self.speedy<0:
                deg=270
            else:
                deg=90
        if deg<0:
            deg+=360
        if self.speedy>0 and deg>=180:
            deg=deg-180
        if self.speedy<0 and deg<=180:
            deg=deg+180
        self.angle=deg
    def speedAlter(self,speedx,speedy):
        self.speedx=speedx
        self.speedy=speedy
    
    def selfTarget(self,tx,ty,speed):
        mycx=self.tx
        mycy=self.ty
        dif=math.sqrt(math.pow(tx-mycx,2)+math.pow(ty-mycy,2))
        times=dif/speed
        speedx=(tx-mycx)/times
        speedy=(ty-mycy)/times
        self.speedAlter(speedx,speedy)

    def truePos(self):
        self.rect.centerx=self.tx
        self.rect.centery=self.ty

    def movement(self):
        tick=global_var.get_value('DELTA_T')
        self.tx+=self.speedx*60/1000*tick
        self.ty+=self.speedy*60/1000*tick
        self.truePos()

    def setSpeed(self,angle,speed):
        s=math.sin(math.radians(angle))
        c=math.cos(math.radians(angle))
        self.speedy=s*speed
        self.speedx=c*speed
        self.angle=angle

    def checkVaild(self):
        if self.rect.top>=720-30+10:
            self.kill()
        if self.rect.bottom<=0+30:
            self.kill()
        if self.rect.right<=0+60:
            self.kill()
        if self.rect.left>=660:
            self.kill()


    def update(self,screen):
        self.speedy=-self.speed
        self.movement()
        self.checkVaild()
        self.draw(screen)
        #screen.blit(self.surf,self.rect)

class boomSquare(playerGun):
    def __init__(self):
        super(boomSquare,self).__init__()
        self.angle=0
        self.surf = pygame.Surface((200,200))
        self.surf.fill((255,255,255))
        self.surf.set_alpha(186)
        self.rect=self.surf.get_rect()
        self.lastFrame=0
        self.image=pygame.image.load('resource/boomEffect.png')
        self.image.set_alpha(180)
        self.ifBoss=global_var.get_value('ifBoss')
    def checkValid(self):
        if self.ifBoss:
            if self.lastFrame>=400:
                global_var.set_value('boomStatu',0)
                self.kill()
        else:
            if self.lastFrame>=600:
                global_var.set_value('boomStatu',0)
                self.kill()
            
    def update(self,screen):
        self.lastFrame+=1
        if self.ty>=300:
            if self.ifBoss:
                self.speedy=-1.5
            else:
                self.speedy=-1.0
        else:
            if self.ifBoss:
                self.speedy=-0.7
            else:
                self.speedy=-0.3
        speedx=0
        self.movement()
        self.truePos()
        self.checkValid()
        screen.blit(self.image,(self.rect.centerx-103,self.rect.centery-103))


class straightGun(playerGun):
    def __init__(self):
        super(straightGun,self).__init__()
        self.image=global_var.get_value('playerFire_green')
        self.hit=75
    def draw(self,screen):
        self.countAngle()
        gF.drawRotation(self.image,(self.rect.centerx-24,self.rect.centery-24),-self.angle,screen)


class inclineGun(playerGun):
    def __init__(self):
        super(inclineGun,self).__init__()
        self.angle=0
        self.surf = pygame.Surface((10,10))
        self.surf.fill((255,255,255))
        self.rect=self.surf.get_rect()
        self.image=global_var.get_value('playerFire_blue')
        self.hit=40
    def initial(self,angle,tx,ty,speed):
        self.tx=tx
        self.ty=ty
        self.setSpeed(angle,speed)

    def update(self,screen):
        self.movement()
        self.checkVaild()
        self.draw(screen)
        #screen.blit(self.surf,self.rect)
    
    def draw(self,screen):
        self.countAngle()
        gF.drawRotation(self.image,(self.rect.centerx-24,self.rect.centery-24),-self.angle,screen)

class reimuMainSatsu(playerGun):
    def __init__(self):
        super(reimuMainSatsu,self).__init__()
        self.image=pygame.Surface((96,24)).convert_alpha()
        self.image.fill((0,0,0,0))
        self.image.blit(global_var.get_value('reimu_fire'),(0,0),(0,48,96,24))
    def draw(self,screen):
        self.countAngle()
        gF.drawRotation(self.image,(self.rect.centerx-48,self.rect.centery-12),-self.angle,screen)
        #screen.blit(self.surf,self.rect)

class reimuTargetSatsu(playerGun):
    def __init__(self):
        super(reimuTargetSatsu,self).__init__()
        self.angle=0
        self.surf = pygame.Surface((10,10))
        self.surf.fill((255,255,255))
        self.rect=self.surf.get_rect()
        self.image=pygame.Surface((24,24)).convert_alpha()
        self.image.fill((0,0,0,0))
        self.image.blit(global_var.get_value('reimu_fire'),(0,0),(0,24,24,24))
        #self.image=global_var.get_value('playerFire_blue')
        self.hit=50
        self.lastFrame=0
        self.maxFrame=120
        self.initAngle=0
        self.adjAngle=3
    
    def checkVaild(self):
        if self.rect.top>=720-30+10:
            self.kill()
        if self.rect.bottom<=0+30:
            self.kill()
        if self.rect.right<=0+60-40:
            self.kill()
        if self.rect.left>=660+40:
            self.kill()

    def initial(self,angle,tx,ty,speed):
        self.tx=tx
        self.ty=ty
        self.angle=angle
        self.speed=speed
        self.setSpeed(angle,speed)

    def update(self,screen):
        self.lastFrame+=1
        if self.lastFrame>=self.maxFrame:
            self.kill()
        self.target()
        self.movement()
        self.checkVaild()
        self.draw(screen)
        #screen.blit(self.surf,self.rect)
    
    def target(self):
        pos=global_var.get_value('enemyPos')
        tx=pos[0]
        ty=pos[1]
        self.initAngle=self.angle
        if tx>60 and tx<660 and ty>30 and ty<690:
            self.selfTarget(tx,ty,self.speed)
        self.countAngle()
        if abs(self.initAngle-self.angle)<=self.adjAngle:
            pass
        else:
            da=self.initAngle-self.angle
            if da>0:
                if da>=180:
                    self.setSpeed(self.initAngle+self.adjAngle,self.speed)
                    self.angle=self.initAngle+self.adjAngle
                elif da<180:
                    self.setSpeed(self.initAngle-self.adjAngle,self.speed)
                    self.angle=self.initAngle-self.adjAngle
            else:
                if abs(da)>=180:
                    self.setSpeed(self.initAngle-self.adjAngle,self.speed)
                    self.angle=self.initAngle-self.adjAngle
                elif abs(da)<180:
                    self.setSpeed(self.initAngle+self.adjAngle,self.speed)
                    self.angle=self.initAngle+self.adjAngle
    
    def draw(self,screen):
        self.countAngle()
        gF.drawRotation(self.image,(self.rect.centerx-12,self.rect.centery-12),-self.angle,screen)


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Bullet,self).__init__()
        self.surf = pygame.Surface((5,5))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.tx=0.0
        self.ty=0.0
        self.type=0
        self.speedx=0
        self.speedy=0
        self.startFrame=-1
        self.angle=0
        self.fro=0 #determine where the bullet is from
        self.dx=0
        self.dy=0
        self.distance=10000
        self.graze=1
        self.cancalable=True
    
    def genEffect(self,effects):
        pass

    def initial(self,posx,posy,occupy):
        self.tx=posx
        self.ty=posy
        self.fro=occupy

    def truePos(self):
        self.rect.centerx=self.tx
        self.rect.centery=self.ty
        self.doGraze()
    
    def checkDistance(self):
        px=global_var.get_value('player1x')
        py=global_var.get_value('player1y')
        dx=abs(px-self.tx)
        dy=abs(py-self.ty)
        self.distance=math.sqrt(math.pow(dx,2)+math.pow(dy,2))

    def doGraze(self):
        self.checkDistance()
        w,h=self.surf.get_size()
        if self.graze>0 and ((self.distance-(w+h)/2)<=30):
            self.graze-=1
            if not global_var.get_value('grazing'):
                global_var.get_value('graze_sound').play()
                global_var.set_value('grazing',True)
            grazeNum=global_var.get_value('grazeNum')+1
            global_var.set_value('grazeNum',grazeNum)

    def movement(self):
        tick=global_var.get_value('DELTA_T')
        self.tx+=self.speedx*60/1000*tick
        self.ty+=self.speedy*60/1000*tick
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
        if self.speedy==0 and self.speedx<0:
            deg=180
        self.angle=deg
    
    def setSpeed(self,angle,speed):
        s=math.sin(math.radians(angle))
        c=math.cos(math.radians(angle))
        self.speedy=s*speed
        self.speedx=c*speed
    #def update(self):

    def checkValid(self):
        if self.rect.top>=720-30:
            self.kill()
        if self.rect.bottom<=0+30:
            self.kill()
        if self.rect.right<=0+60:
            self.kill()
        if self.rect.left>=660:
            self.kill()

class small_Bullet(Bullet):
    def __init__(self):
        super(small_Bullet,self).__init__()
        self.type=1
        self.surf = pygame.Surface((8,8))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.image=pygame.image.load('resource/bullet/small_bullet_grey.png')
        self.dx=6
        self.dy=6
    def update(self,screen,bullets,effects):
        self.movement()
        screen.blit(self.image,(self.rect.centerx-6,self.rect.centery-6))
        #screen.blit(self.surf,self.rect)
        self.checkValid()
    def loadColor(self,color):
        self.image=pygame.image.load('resource/bullet/small_bullet_'+color+'.png')

class mid_Bullet(Bullet):
    def __init__(self):
        super(mid_Bullet,self).__init__()
        self.surf = pygame.Surface((15,15))
        self.rect = self.surf.get_rect()
        self.surf.fill((255,255,255))
        self.type=2
        self.image=pygame.image.load('resource/bullet/mid_bullet_grey.png')
        self.dx=12
        self.dy=12

    def update(self,screen,bullets,effects):
        self.movement()
        self.drawBullet(screen)
        #screen.blit(self.surf,self.rect)
        self.checkValid()
    def loadColor(self,color):
        self.image=pygame.image.load('resource/bullet/mid_bullet_'+color+'.png').convert_alpha()
    
    def drawBullet(self,screen):
        screen.blit(self.image,(self.rect.centerx-12,self.rect.centery-12))

class big_Bullet(Bullet):
    def __init__(self):
        super(big_Bullet,self).__init__()
        self.surf = pygame.Surface((40,40))
        self.rect = self.surf.get_rect()
        self.surf.fill((255,255,255))
        self.type=3
        self.image=pygame.image.load('resource/bullet/big_bullet_red.png').convert_alpha()
        #self.image.set_alpha(210)
        self.dx=48
        self.dy=48
    def update(self,screen,bullets,effects):
        self.movement()
        screen.blit(self.image,(self.rect.centerx-48,self.rect.centery-48))
        #screen.blit(self.surf,self.rect)
        self.checkValid()
    def loadColor(self,color):
        self.image=pygame.image.load('resource/bullet/big_bullet_'+color+'.png').convert_alpha()
        #self.image.set_alpha(210)
class big_Bullet_explode(Bullet):
    def __init__(self):
        super(big_Bullet_explode,self).__init__()
        self.surf = pygame.Surface((30,30))
        self.rect = self.surf.get_rect()
        self.surf.fill((255,255,255))
        self.type=3
        self.expValue=1
        self.image=pygame.image.load('resource/bullet/big_bullet_red.png').convert_alpha()
    def update(self,screen,bullets,effects):
        self.movement()
        #screen.blit(self.image,(round(self.rect.centerx-32-5*self.speedx),round(self.rect.centery-32-5*self.speedy)))
        screen.blit(self.image,(self.rect.centerx-48,self.rect.centery-48))
        #screen.blit(self.surf,self.rect)
        self.explode(screen,bullets)
        self.checkValid()
    def loadColor(self,color):
        self.image=pygame.image.load('resource/bullet/big_bullet_'+color+'.png').convert_alpha()
    
    def explode(self,screen,bullets):
        do=0
        if self.fro==1:
            if self.rect.right>=370:
                do=1
        if self.fro==2:
            if self.rect.left<=430:
                do=1
        if self.rect.top<=20 or self.rect.bottom>=580:
            do=1
        if self.rect.left<=30 or self.rect.right>=770:
            do=1

        if do==1 and self.expValue==1:
            for i in range (1,61):
                new_bullet=small_Bullet()
                new_bullet.initial(self.tx,self.ty,self.fro)
                angle=random.random()*360
                speed=random.random()*2+0.1
                new_bullet.setSpeed(angle,speed)
                color=('red','green','purple','grey','blue')
                colorChoose=random.randint(0,4)
                new_bullet.loadColor(color[colorChoose])
                bullets.add(new_bullet)
            self.expValue=0

class star_Bullet(Bullet):
    def __init__(self):
        super(star_Bullet,self).__init__()
        self.surf = pygame.Surface((10,10))
        self.rect = self.surf.get_rect()
        self.surf.fill((255,255,255))
        self.type=4
        self.image=pygame.image.load('resource/bullet/star_bullet_grey.png').convert_alpha()
        self.dAngle=random.randint(0,60)
        self.dx=12
        self.dy=12
        self.lastFrame=0
        #self.cvImage=pygame.image.load('resource/bullet/star_bullet_grey.png')
    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        #screen.blit(self.image,(self.rect.centerx-3,self.rect.centery-3))
        #screen.blit(self.surf,self.rect)
        self.drawBullet(screen)
        self.checkValid()
    def loadColor(self,color):
        self.image=pygame.image.load('resource/bullet/star_bullet_'+color+'.png').convert_alpha()
    def drawBullet(self,screen):
        self.dAngle+=3
        gF.drawRotation(self.image,(self.rect.centerx-12,self.rect.centery-12),self.dAngle,screen)

class scale_Bullet(Bullet):
    def __init__(self):
        super(scale_Bullet,self).__init__()
        self.surf = pygame.Surface((10,10))
        self.rect = self.surf.get_rect()
        self.surf.fill((255,255,255))
        self.type=5
        self.image=pygame.image.load('resource/bullet/scale_bullet_grey.png').convert_alpha()
        self.tempImage=pygame.image.load('resource/bullet/scale_bullet_grey.png').convert_alpha()
        self.lastAngle=0
        #self.cvImage=pygame.image.load('resource/bullet/star_bullet_grey.png')
        self.dx=15
        self.dy=15
    def update(self,screen,bullets,effects):
        self.movement()
        #screen.blit(self.image,(self.rect.centerx-3,self.rect.centery-3))
        #screen.blit(self.surf,self.rect)
        self.drawBullet(screen)
        self.checkValid()
    def loadColor(self,color):
        self.image=pygame.image.load('resource/bullet/scale_bullet_'+color+'.png').convert_alpha()
    def drawBullet(self,screen):
        self.countAngle()
        angle=270-self.angle
        if round(angle)!=round(self.lastAngle):
            self.tempImage=pygame.transform.rotate(self.image, angle)
        #print(str(round(angle))+':'+str(round(self.lastAngle))+'->'+str(round(angle)!=round(self.lastAngle)))
        self.lastAngle=angle
        #w=30
        #h=30
        #pos=gF.returnPosition(w,h,(self.rect.centerx-15,self.rect.centery-15),angle)
        size=w,h=self.tempImage.get_size()
        #print(size)
        screen.blit(self.tempImage,(self.rect.centerx-round(w/2),self.rect.centery-round(h/2)))
        #screen.blit(self.tempImage,pos)
        #gF.drawRotation(self.image,(self.rect.centerx-10,self.rect.centery-10),270-self.angle,screen)

class scale_Bullet_alter1(Bullet):
    def __init__(self):
        super(scale_Bullet_alter1,self).__init__()
        self.surf = pygame.Surface((10,10))
        self.rect = self.surf.get_rect()
        self.surf.fill((255,255,255))
        self.type=5
        self.frame=0
        self.direction=0
        self.rand=random.random()*1.50
        self.image=pygame.image.load('resource/bullet/scale_bullet_grey.png').convert_alpha()
        #self.cvImage=pygame.image.load('resource/bullet/star_bullet_grey.png')
    def checkValid(self):
        if self.frame>=5*60:
            self.kill()
    def update(self,screen,bullets,effects):
        self.frame+=1
        if self.frame==1:
            self.countAngle()
        if self.frame>40 and self.frame<100 and self.frame%2==0:
            self.setSpeed(self.angle+7*self.direction,4)
        if self.frame>100 and self.frame<140 and self.frame%2==0:
            self.setSpeed(self.angle+self.rand,5)
        self.movement()
        #screen.blit(self.image,(self.rect.centerx-3,self.rect.centery-3))
        #screen.blit(self.surf,self.rect)
        self.drawBullet(screen)
        self.checkValid()
    def loadColor(self,color):
        self.image=pygame.image.load('resource/bullet/scale_bullet_'+color+'.png').convert_alpha()
    def drawBullet(self,screen):
        self.countAngle()
        if self.rect.right>=400 and self.fro==2:
            gF.drawRotation(self.image,(self.rect.centerx-15,self.rect.centery-15),270-self.angle,screen)
        if self.rect.left<=400 and self.fro==1:
            gF.drawRotation(self.image,(self.rect.centerx-15,self.rect.centery-15),270-self.angle,screen)

class scale_Bullet_alter2(Bullet):
    def __init__(self):
        super(scale_Bullet_alter2,self).__init__()
        self.surf = pygame.Surface((10,10))
        self.rect = self.surf.get_rect()
        self.surf.fill((255,255,255))
        self.type=5
        self.frame=0
        self.tspeed=0
        self.direction=0
        self.rand=random.random()*0.90
        self.image=pygame.image.load('resource/bullet/scale_bullet_grey.png').convert_alpha()
        #self.cvImage=pygame.image.load('resource/bullet/star_bullet_grey.png')
    def checkValid(self):
        if self.frame>=6*60:
            self.kill()

    def getTspeed(self):
        self.tspeed=math.sqrt(math.pow(self.speedx,2)+math.pow(self.speedy,2))

    def update(self,screen,bullets,effects):
        self.frame+=1
        if self.frame==1:
            self.countAngle()
        if self.frame<=130:
            if self.frame>10 and (self.frame-10)%60<30:
                self.getTspeed()
                self.setSpeed(self.angle+5,self.tspeed)
            else:
                self.getTspeed()
                self.setSpeed(self.angle-4,self.tspeed+0.02)
        elif self.frame<=5*60-45:
            if self.frame>10 and (self.frame-10)%60<30:
                self.getTspeed()
                self.setSpeed(self.angle+9,self.tspeed+0.01)
            else:
                self.getTspeed()
                self.setSpeed(self.angle-6,self.tspeed)

        self.movement()
        #screen.blit(self.image,(self.rect.centerx-3,self.rect.centery-3))
        #screen.blit(self.surf,self.rect)
        self.drawBullet(screen)
        self.checkValid()
    def loadColor(self,color):
        self.image=pygame.image.load('resource/bullet/scale_bullet_'+color+'.png').convert_alpha()
    def drawBullet(self,screen):
        self.countAngle()
        if self.rect.right>=400 and self.fro==2:
            gF.drawRotation(self.image,(self.rect.centerx-15,self.rect.centery-15),270-self.angle,screen)
        if self.rect.left<=400 and self.fro==1:
            gF.drawRotation(self.image,(self.rect.centerx-15,self.rect.centery-15),270-self.angle,screen)

class mid_Bullet_gravity(Bullet):
    def __init__(self):
        super(mid_Bullet_gravity,self).__init__()
        self.surf = pygame.Surface((10,10))
        self.rect = self.surf.get_rect()
        self.surf.fill((255,255,255))
        self.type=2
        self.image=pygame.image.load('resource/bullet/mid_bullet_grey.png').convert_alpha()
        self.gravity=0.1
    def setGravity(self,gravity):
        self.gravity=gravity
    def update(self,screen,bullets,effects):
        self.movement()
        self.speedy+=self.gravity
        screen.blit(self.image,(self.rect.centerx-12,self.rect.centery-12))
        #screen.blit(self.surf,self.rect)
        self.checkValid()
    def loadColor(self,color):
        self.image=pygame.image.load('resource/bullet/mid_bullet_'+color+'.png').convert_alpha()

class orb_Bullet(Bullet):
    def __init__(self):
        super(orb_Bullet,self).__init__()
        self.surf = pygame.Surface((12,12))
        self.rect = self.surf.get_rect()
        self.surf.fill((255,255,255))
        self.type=6
        self.image=pygame.image.load('resource/bullet/orb_bullet_grey.png').convert_alpha()
        self.dx=12
        self.dy=12
        self.lastFrame=0
        self.codeDic=['red','blue','green','purple','pink','jade','yellow']
    def doColorCode(self,code):
        self.image=pygame.image.load('resource/bullet/orb_bullet_'+self.codeDic[code]+'.png')
    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.drawBullet(screen)
        #screen.blit(self.image,(self.rect.centerx-12,self.rect.centery-12))
        #screen.blit(self.surf,self.rect)
        self.checkValid()
    def loadColor(self,color):
        self.image=pygame.image.load('resource/bullet/orb_bullet_'+color+'.png').convert_alpha()
    
    def drawBullet(self,screen):
        screen.blit(self.image,(self.rect.centerx-12,self.rect.centery-12))

class orb_Bullet_gravity(Bullet):
    def __init__(self):
        super(orb_Bullet_gravity,self).__init__()
        self.surf = pygame.Surface((12,12))
        self.rect = self.surf.get_rect()
        self.surf.fill((255,255,255))
        self.type=6
        self.image=pygame.image.load('resource/bullet/orb_bullet_grey.png').convert_alpha()
        self.gravity=0.1
        self.gravMax=999
        self.totalGrav=0
        self.dx=12
        self.dy=12
        self.gravDirection=2
        self.codeDic=['red','blue','green','purple','pink','jade','yellow']
    def doColorCode(self,code):
        self.image=pygame.image.load('resource/bullet/orb_bullet_'+self.codeDic[code]+'.png').convert_alpha()

    def setGravity(self,gravity):
        self.gravity=gravity

    def setGravMax(self,gravMax):
        self.gravMax=gravMax

    def update(self,screen,bullets,effects):
        self.movement()
        if self.totalGrav<self.gravMax:
            if self.gravDirection==2:
                self.speedy+=self.gravity
            elif self.gravDirection==4:
                self.speedy-=self.gravity
            elif self.gravDirection==3:
                self.speedx-=self.gravity
            elif self.gravDirection==1:
                self.speedx+=self.gravity 
            self.totalGrav+=self.gravity
        #if self.ty>300:
            #self.speedx=0
        screen.blit(self.image,(self.rect.centerx-12,self.rect.centery-12))
        #screen.blit(self.surf,self.rect)
        self.checkValid()
    def loadColor(self,color):
        self.image=pygame.image.load('resource/bullet/orb_bullet_'+color+'.png').convert_alpha()
    def drawBullet(self,screen):
        screen.blit(self.image,(self.rect.centerx-12,self.rect.centery-12))

class orb_Bullet_bouncing_leftright(Bullet):
    def __init__(self):
        super(orb_Bullet_bouncing_leftright,self).__init__()
        self.surf = pygame.Surface((8,8))
        self.rect = self.surf.get_rect()
        self.surf.fill((255,255,255))
        self.type=6
        self.bounce=1
        self.image=pygame.image.load('resource/bullet/orb_bullet_grey.png').convert_alpha()
    def update(self,screen,bullets,effects):
        self.movement()
        self.bouncing()
        screen.blit(self.image,(self.rect.centerx-12,self.rect.centery-12))
        #screen.blit(self.surf,self.rect)
        self.checkValid()
    def loadColor(self,color):
        self.image=pygame.image.load('resource/bullet/orb_bullet_'+color+'.png').convert_alpha()
    
    def bouncing(self):
        if self.bounce>0:
            if self.fro==1:
                if self.tx<=30 or self.tx>=370:
                    self.speedx=-self.speedx
                    self.loadColor('red')
                    self.bounce-=1
            if self.fro==2:
                if self.tx<=430 or self.tx>=770:
                    self.speedx=-self.speedx
                    self.loadColor('red')
                    self.bounce-=1
            
class flame_Bullet(Bullet):
    def __init__(self):
        super(flame_Bullet,self).__init__()
        self.surf = pygame.Surface((18,18))
        self.rect = self.surf.get_rect()
        self.surf.fill((255,255,255))
        self.type=7
        self.color='red'
        self.property=0
        self.period=10
        self.count=0
        #self.imageLocate='resource/bullet/flame_bullet_red_1.png'
        #self.image=pygame.image.load('resource/bullet/flame_bullet_red_1.png')
        self.red=[]
        for i in range(1,5):
            red1=pygame.image.load('resource/bullet/flame_bullet_red_'+str(i)+'.png').convert_alpha()
            self.red.append(red1)
        self.blue=[]
        for i in range(1,5):
            blue1=pygame.image.load('resource/bullet/flame_bullet_blue_'+str(i)+'.png').convert_alpha()
            self.blue.append(blue1)
        self.dx=22
        self.dy=22
    def update(self,screen,bullet,effects):
        self.movement()
        self.toggle()
        self.drawBullet(screen)
        #screen.blit(self.surf,self.rect)
        self.checkValid()
    def loadColor(self,color):
        self.color=color
        #self.image=pygame.image.load('resource/bullet/flame_bullet_'+self.color+'_'+str(self.property)+'.png')
    def toggle(self):
        self.count+=1
        if self.count>=self.period:
            self.property+=1
            if self.property>=4:
                self.property=0
            self.count=0
            #self.image=pygame.image.load('resource/bullet/flame_bullet_'+self.color+'_'+str(self.property)+'.png')
    def drawBullet(self,screen):
        self.countAngle()
        if self.color=='red':
            gF.drawRotation(self.red[self.property],(self.rect.centerx-22,self.rect.centery-22),270-self.angle,screen)
        elif self.color=='blue':
            gF.drawRotation(self.blue[self.property],(self.rect.centerx-22,self.rect.centery-22),270-self.angle,screen)
    
class flame_Bullet_alter1(Bullet):
    def __init__(self):
        super(flame_Bullet_alter1,self).__init__()
        self.surf = pygame.Surface((12,12))
        self.rect = self.surf.get_rect()
        self.surf.fill((255,255,255))
        self.type=7
        self.color='red'
        self.property=0
        self.period=10
        self.count=0
        self.frame=0
        self.rand=random.random()*2
        #self.imageLocate='resource/bullet/flame_bullet_red_1.png'
        #self.image=pygame.image.load('resource/bullet/flame_bullet_red_1.png')
        self.red=[]
        for i in range(1,5):
            red1=pygame.image.load('resource/bullet/flame_bullet_red_'+str(i)+'.png').convert_alpha()
            self.red.append(red1)
        self.blue=[]
        for i in range(1,5):
            blue1=pygame.image.load('resource/bullet/flame_bullet_blue_'+str(i)+'.png').convert_alpha()
            self.blue.append(blue1)
    def checkValid(self):
        if self.frame>=4.5*60:
            self.kill()
    def update(self,screen,bullet,effects):
        self.frame+=1
        self.countAngle()
        if self.frame>40 and self.frame<100 and self.frame%2==0:
            self.setSpeed(self.angle+7+self.rand,4)
        self.movement()
        self.toggle()
        self.drawBullet(screen)
        #screen.blit(self.surf,self.rect)
        self.checkValid()
    def loadColor(self,color):
        self.color=color
        #self.image=pygame.image.load('resource/bullet/flame_bullet_'+self.color+'_'+str(self.property)+'.png')
    def toggle(self):
        self.count+=1
        if self.count>=self.period:
            self.property+=1
            if self.property>=4:
                self.property=0
            self.count=0
            #self.image=pygame.image.load('resource/bullet/flame_bullet_'+self.color+'_'+str(self.property)+'.png')
    def drawBullet(self,screen):
        self.countAngle()
        if self.rect.right>=400 and self.fro==2:
            if self.color=='red':
                gF.drawRotation(self.red[self.property],(self.rect.centerx-15,self.rect.centery-15),270-self.angle,screen)
            elif self.color=='blue':
                gF.drawRotation(self.blue[self.property],(self.rect.centerx-15,self.rect.centery-15),270-self.angle,screen)
        if self.rect.left<=400 and self.fro==1:
            if self.color=='red':
                gF.drawRotation(self.red[self.property],(self.rect.centerx-15,self.rect.centery-15),270-self.angle,screen)
            elif self.color=='blue':
                gF.drawRotation(self.blue[self.property],(self.rect.centerx-15,self.rect.centery-15),270-self.angle,screen)
            
class star_Bullet_delaySelfTarget(star_Bullet):
    def __init__(self):
        super(star_Bullet_delaySelfTarget,self).__init__()
        self.delay=90
        self.range=3
        self.waitSec=0
        self.motion=0
        self.playerx=0
        self.playery=0
        self.speed=3
        self.speedx=0
        self.speedy=0
    def setProperty(self,delay,range):
        self.delay=delay
        self.range=range

    def setDelayedTarget(self,playerx,playery,speed):#specific function for delayed bullets
        self.playerx=playerx
        self.playery=playery
        self.speed=speed

    def update(self,screen,bullets,effects):
        self.drawBullet(screen)
        if self.motion==1 and self.waitSec==self.delay:
            if self.fro==1:
                self.selfTarget(global_var.get_value('player1x'),global_var.get_value('player1y'),self.speed)
            else:
                self.selfTarget(global_var.get_value('player2x'),global_var.get_value('player2y'),self.speed)
            self.countAngle()
            self.setSpeed(self.angle+random.random()*self.range*2-self.range,self.speed)
        self.movement()
        self.doDelay()
        #screen.blit(self.surf,self.rect)
        
        self.checkValid()

    def doDelay(self):
        self.waitSec+=1
        if self.waitSec>=self.delay:
            self.motion=1

class laser_Bullet_main(Bullet):
    def __init__(self):
        super(laser_Bullet_main,self).__init__()
        self.ratio=8
        self.surf = pygame.Surface((self.ratio,self.ratio))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.image=pygame.image.load('resource/bullet/small_bullet_grey.png').convert_alpha()
        self.dx=4
        self.dy=4
        self.lastFrame=0
        self.length=20
        self.colorNum=0
    def doColorCode(self,code):
        self.colorNum=code
        self.image=pygame.Surface((16,15))
        self.image=self.image.convert_alpha()
        self.image.fill((0,0,0,0))
        #self.image.set_alpha(256)
        self.image.blit(global_var.get_value('laser_bullet_image'), (0, 0), (64*self.colorNum,0, 16, 15))

    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        new_sub=laser_Bullet_sub(self.length,self.ratio)
        new_sub.initial(self.tx,self.ty,self.fro)
        new_sub.doColorCode(self.colorNum)
        bullets.add(new_sub)
        #screen.blit(self.image,(self.rect.centerx-6,self.rect.centery-6))
        
        #screen.blit(self.surf,self.rect)
        self.draw(screen)
        self.checkValid()
    
    def draw(self,screen):
        screen.blit(self.image,(self.rect.centerx-8,self.rect.centery-8))
    

class laser_Bullet_sub(Bullet):
    def __init__(self,length,ratio):
        super(laser_Bullet_sub,self).__init__()
        self.ratio=ratio
        self.surf = pygame.Surface((self.ratio,self.ratio))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.image=pygame.image.load('resource/bullet/small_bullet_grey.png').convert_alpha()
        self.dx=6
        self.dy=6
        self.length=length
        self.frame=0
        self.speedx=0
        self.speedy=0
        self.colorNum=0
    def doColorCode(self,code):
        self.colorNum=code
        self.image=pygame.Surface((16,15))
        self.image=self.image.convert_alpha()
        self.image.fill((0,0,0,0))
        #self.image.set_alpha(256)
        self.image.blit(global_var.get_value('laser_bullet_image'), (0, 0), (64*self.colorNum,0, 16, 15)) 

    def update(self,screen,bullets,effects):
        self.frame+=1
        self.movement()
        #screen.blit(self.surf,self.rect)
        self.draw(screen)
        self.checkValid()
        if self.frame>=self.length:
            self.kill()
    
    def draw(self,screen):
        screen.blit(self.image,(self.rect.centerx-8,self.rect.centery-8))

class big_star_Bullet(Bullet):
    def __init__(self):
        super(big_star_Bullet,self).__init__()
        self.surf = pygame.Surface((24,24))
        self.rect = self.surf.get_rect()
        self.surf.fill((255,255,255))
        self.type=8
        self.image=pygame.image.load('resource/bullet/star_bullet_grey.png').convert_alpha()
        self.dAngle=random.randint(0,60)
        self.dx=24
        self.dy=24
        self.colorNum=0
        self.image=0
    def doColorCode(self,code):
        self.colorNum=code
        self.image=pygame.Surface((48,48))
        self.image=self.image.convert_alpha()
        #self.image.set_alpha(256)
        self.image.fill((0,0,0,0))
        self.image.blit(global_var.get_value('big_star_bullet_image').convert_alpha(), (0, 0), (48*self.colorNum,0, 48, 48))
    
    def update(self,screen,bullets,effects):
        self.movement()
        #screen.blit(self.image,(self.rect.centerx-3,self.rect.centery-3))
        #screen.blit(self.surf,self.rect)
        self.drawBullet(screen)
        self.checkValid()
    
    def drawBullet(self,screen):
        self.dAngle+=3
        gF.drawRotation(self.image,(self.rect.centerx-24,self.rect.centery-24),self.dAngle,screen)

class circle_Bullet(Bullet):
    def __init__(self):
        super(circle_Bullet,self).__init__()
        self.surf = pygame.Surface((23,23))
        self.rect = self.surf.get_rect()
        self.surf.fill((255,255,255))
        self.type=9
        self.image=pygame.image.load('resource/bullet/small_bullet_grey.png').convert_alpha()
        self.dx=24
        self.dy=24
        self.colorNum=0
    def doColorCode(self,code):
        self.colorNum=code
        self.image=pygame.Surface((48,48))
        #self.image.set_alpha(256)
        self.image=self.image.convert_alpha()
        self.image.fill((0,0,0,0))
        #self.image.set_colorkey((0, 0, 0))
        self.image.blit(global_var.get_value('circle_bullet_image').convert_alpha(), (0, 0), (48*self.colorNum,0, 48, 48))
    
    def update(self,screen,bullets,effects):
        self.movement()
        self.drawBullet(screen)
        #screen.blit(self.surf,self.rect)
        self.checkValid()
    
    def drawBullet(self,screen):
        screen.blit(self.image,(self.rect.centerx-24,self.rect.centery-24))
    
class butterfly_Bullet(Bullet):
    def __init__(self):
        super(butterfly_Bullet,self).__init__()
        self.surf = pygame.Surface((16,16))
        self.rect = self.surf.get_rect()
        self.surf.fill((255,255,255))
        self.type=10
        self.dx=24
        self.dy=24
        self.colorNum=0
        self.lastAngle=-10000
    def doColorCode(self,code):
        self.colorNum=code
        self.image=pygame.Surface((48,48))
        #self.image.set_alpha(256)
        self.image=self.image.convert_alpha()
        self.image.fill((0,0,0,0))
        #self.image.set_colorkey((0, 0, 0))
        self.image.blit(global_var.get_value('butterfly_bullet_image').convert_alpha(), (0, 0), (48*self.colorNum,0, 48, 48))
        self.tempImage=self.image
    def update(self,screen,bullets,effects):
        self.movement()
        #screen.blit(self.image,(self.rect.centerx-3,self.rect.centery-3))
        screen.blit(self.surf,self.rect)
        self.drawBullet(screen)
        self.checkValid()

    def drawBullet(self,screen):
        self.countAngle()
        angle=270-self.angle
        if round(angle)!=round(self.lastAngle):
            self.tempImage=pygame.transform.rotate(self.image, angle)
        #print(str(round(angle))+':'+str(round(self.lastAngle))+'->'+str(round(angle)!=round(self.lastAngle)))
        self.lastAngle=angle
        #w=30
        #h=30
        #pos=gF.returnPosition(w,h,(self.rect.centerx-15,self.rect.centery-15),angle)
        size=w,h=self.tempImage.get_size()
        #print(size)
        screen.blit(self.tempImage,(self.rect.centerx-round(w/2),self.rect.centery-round(h/2)))
        #screen.blit(self.tempImage,pos)
        #gF.drawRotation(self.image,(self.rect.centerx-10,self.rect.centery-10),270-self.angle,screen)

class rice_Bullet(Bullet):
    def __init__(self):
        super(rice_Bullet,self).__init__()
        self.surf = pygame.Surface((8,8))
        self.rect = self.surf.get_rect()
        self.surf.fill((255,255,255))
        self.type=11
        self.dx=12
        self.dy=12
        self.colorNum=0
        self.lastNum=0
        self.lastAngle=-10000
        self.tempImage=0
        self.lastFrame=0
        self.colorDict={'grey':0,'red':1,'lightRed':2,'purple':3,'pink':4,'blue':5,'seaBlue':6,'skyBlue':7,'lightBlue':8,'lakeBlue':8,'darkGreen':9,'green':10,'lightGreen':11,'yellow':12,'lemonYellow':13,'orange':14,'white':15}
    
    def doColorCode(self,code):
        self.colorNum=code
        self.image=pygame.Surface((24,24))
        #self.image.set_alpha(256)
        self.image=self.image.convert_alpha()
        self.image.fill((0,0,0,0))
        #self.image.set_colorkey((0, 0, 0))
        self.image.blit(global_var.get_value('rice_bullet_image').convert_alpha(), (0, 0), (24*self.colorNum,0, 24, 24))
        if self.tempImage==0:
            self.tempImage=self.image
    def loadColor(self,color):
        self.doColorCode(self.colorDict[color])

    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        #screen.blit(self.image,(self.rect.centerx-3,self.rect.centery-3))
        screen.blit(self.surf,self.rect)
        self.drawBullet(screen)
        self.checkValid()

    def drawBullet(self,screen):
        self.countAngle()
        angle=270-self.angle
        if round(angle)!=round(self.lastAngle) or self.lastFrame==1 or self.lastNum!=self.colorNum:
            self.tempImage=pygame.transform.rotate(self.image, angle)
        self.lastNum=self.colorNum
        #print(str(round(angle))+':'+str(round(self.lastAngle))+'->'+str(round(angle)!=round(self.lastAngle)))
        self.lastAngle=angle
        #w=30
        #h=30
        #pos=gF.returnPosition(w,h,(self.rect.centerx-15,self.rect.centery-15),angle)
        size=w,h=self.tempImage.get_size()
        #print(size)
        screen.blit(self.tempImage,(self.rect.centerx-round(w/2),self.rect.centery-round(h/2)))
        #screen.blit(self.tempImage,pos)
        #gF.drawRotation(self.image,(self.rect.centerx-10,self.rect.centery-10),270-self.angle,screen)

class satsu_Bullet(rice_Bullet):
    def __init__(self):
        super(satsu_Bullet,self).__init__()
        self.surf = pygame.Surface((7,7))
        self.rect = self.surf.get_rect()
        self.surf.fill((255,255,255))
        self.type=12
    
    def doColorCode(self,code):
        self.colorNum=code
        self.image=pygame.Surface((24,24))
        #self.image.set_alpha(256)
        self.image=self.image.convert_alpha()
        self.image.fill((0,0,0,0))
        #self.image.set_colorkey((0, 0, 0))
        self.image.blit(global_var.get_value('satsu_bullet_image').convert_alpha(), (0, 0), (24*self.colorNum,0, 24, 24))
        self.tempImage=self.image
class bact_Bullet(rice_Bullet):
    def __init__(self):
        super(bact_Bullet,self).__init__()
        self.surf = pygame.Surface((8,8))
        self.rect = self.surf.get_rect()
        self.surf.fill((255,255,255))
        self.type=13
    
    def doColorCode(self,code):
        self.colorNum=code
        self.image=pygame.Surface((24,24))
        #self.image.set_alpha(256)
        self.image=self.image.convert_alpha()
        self.image.fill((0,0,0,0))
        #self.image.set_colorkey((0, 0, 0))
        self.image.blit(global_var.get_value('bact_bullet_image').convert_alpha(), (0, 0), (24*self.colorNum,0, 24, 24))
        self.tempImage=self.image
#bullets modified for lightness level
class star_Bullet_Part4_Hex(star_Bullet):
    def __init__(self):
        super(star_Bullet_Part4_Hex,self).__init__()
        self.displayDelay=9
        self.lastFrame=0
        self.direction=1
        self.rotationAngle=0.3
        self.speed=4
        self.dAngle=random.randint(0,60)
    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.moving_strategy()
        if self.lastFrame>=self.displayDelay:
            self.drawBullet(screen)
        self.checkValid()
    
    def moving_strategy(self):
        self.countAngle()
        self.setSpeed(self.angle+self.direction*self.rotationAngle,self.speed)
    
class orb_Bullet_Part6_delay(orb_Bullet):
    def __init__(self):
        super(orb_Bullet_Part6_delay,self).__init__()
        self.displayDelay=2
        self.changeAngle=0
        self.speed=1
        self.changeSpeed=6
        self.changeFrame=30
        self.lastFrame=0
    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.moving_strategy()
        if self.lastFrame>=self.displayDelay:
            self.drawBullet(screen)
        self.checkValid()
    
    def moving_strategy(self):
        self.countAngle()
        if self.lastFrame==self.displayDelay:
            self.setSpeed(self.angle+self.changeAngle,self.speed)
        if self.lastFrame==self.changeFrame:
            self.setSpeed(self.angle+self.changeAngle,self.changeSpeed)
    
class orb_Bullet_Part7_delay(orb_Bullet):
    def __init__(self):
        super(orb_Bullet_Part7_delay,self).__init__()
        self.displayDelay=2
        self.changeAngle=0
        self.speed=1
        self.changeSpeed=5.8
        self.changeFrame=60
        self.lastFrame=0
    
    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.moving_strategy()
        if self.lastFrame>=self.displayDelay:
            self.drawBullet(screen)
        self.checkValid()

    def moving_strategy(self):
        self.countAngle()
        if self.lastFrame==self.displayDelay:
            self.setSpeed(self.angle+self.changeAngle,self.speed)
        if self.lastFrame==self.changeFrame:
            self.setSpeed(self.angle+self.changeAngle,self.changeSpeed)
    
class mid_Bullet_Part8_acc(mid_Bullet):
    def __init__(self):
        super(mid_Bullet_Part8_acc,self).__init__()
        self.speedLimit=6.0
        self.acceleration=0.1
        self.speedNow=1
        self.lastFrame=0
        self.delayAcc=30

    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.countAngle()
        if self.lastFrame<=self.delayAcc:
            self.speedNow+=0.005
            self.setSpeed(self.angle,self.speedNow)
        elif self.speedNow<=self.speedLimit:
            self.speedNow+=self.acceleration
            self.setSpeed(self.angle,self.speedNow)
        self.drawBullet(screen)
        self.checkValid()

class orb_Bullet_bouncing_limit(orb_Bullet):
    def __init__(self,limit):
        super(orb_Bullet_bouncing_limit,self).__init__()
        self.bounceMax=1
        self.limit=limit
        self.lastFrame=0
    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.bouncing()
        self.drawBullet(screen)
        self.doLimit()
        #screen.blit(self.image,(self.rect.centerx-12,self.rect.centery-12))
        #screen.blit(self.surf,self.rect)
        self.checkValid()
    def bouncing(self):
        if self.bounceMax>0:
            if self.tx<=60 or self.tx>=660:
                self.speedx=-self.speedx
                self.bounceMax-=1
    
    def doLimit(self):
        if self.lastFrame>=self.limit:
            self.kill()

class big_star_Bullet_comet(big_star_Bullet):
    def __init__(self,subSpeed,limit):
        super(big_star_Bullet_comet,self).__init__()
        self.tailLimit=limit
        self.lastFrame=0
        self.bounceMax=20
        self.subSpeed=subSpeed
    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.bouncing()
        self.fire(bullets)
        #screen.blit(self.image,(self.rect.centerx-3,self.rect.centery-3))
        #screen.blit(self.surf,self.rect)
        self.drawBullet(screen)
        self.checkValid()

    def fire(self,bullets):
        self.countAngle()
        if self.lastFrame%3==0:
            for i in range(-1,2):
                if i!=0:
                    new_bullet=orb_Bullet_bouncing_limit(self.tailLimit)
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.setSpeed(self.angle+i*90,self.subSpeed)
                    new_bullet.loadColor('purple')
                    bullets.add(new_bullet)
    
    def bouncing(self):
        if self.bounceMax>0:
            if self.tx<=60 or self.tx>=660:
                self.speedx=-self.speedx
                self.bounceMax-=1

class laser_Bullet_immune(laser_Bullet_main):
    def __init__(self,immuneFrame):
        super(laser_Bullet_immune,self).__init__()
        self.immuneFrame=immuneFrame
        self.length=14

    def checkValid(self):
        if self.lastFrame>=self.immuneFrame:
            if self.rect.top>=720-30:
                self.kill()
            if self.rect.bottom<=0+30:
                self.kill()
            if self.rect.right<=0+60:
                self.kill()
            if self.rect.left>=660:
                self.kill()

class star_Bullet_immune(star_Bullet):
    def __init__(self,immuneFrame):
        super(star_Bullet_immune,self).__init__()
        self.immuneFrame=immuneFrame
    
    def checkValid(self):
        if self.lastFrame>=self.immuneFrame:
            if self.rect.top>=720-30:
                self.kill()
            if self.rect.bottom<=0+30:
                self.kill()
            if self.rect.right<=0+60:
                self.kill()
            if self.rect.left>=660:
                self.kill()

class star_Bullet_fountain(big_star_Bullet):
    def __init__(self):
        super(star_Bullet_fountain,self).__init__()
        self.touchFrame=0
        self.lastFrame=0
        self.touched=False
        self.touch_direction=0
        self.randomAngle=random.random()*360
        self.eruptRandomAngle=16

    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.detect()
        if self.touched:
            self.touchFrame+=1
        self.movement()
        if not self.touched and self.lastFrame%20==0:
            global_var.get_value('kira_sound').play()
        self.fire(bullets,effects)
        #screen.blit(self.image,(self.rect.centerx-3,self.rect.centery-3))
        #screen.blit(self.surf,self.rect)
        self.drawBullet(screen)
        self.checkValid()

    def fire(self,bullets,effects):
        if self.touched and self.touchFrame==1:
            new_laser=laser_Bullet_main()
            new_laser.length=60
            new_laser.initial(self.tx,self.ty,1)
            new_laser.doColorCode(0)
            laserSpeed=12
            if self.touch_direction==1:
                new_laser.setSpeed(180,laserSpeed)
            elif self.touch_direction==2:
                new_laser.setSpeed(270,laserSpeed)
            elif self.touch_direction==3:
                new_laser.setSpeed(0,laserSpeed)
            elif self.touch_direction==4:
                new_laser.setSpeed(90,laserSpeed)
            bullets.add(new_laser)
            new_effect=Effect.bulletCreate(7)
            new_effect.initial(self.tx,self.ty,84,48,60)
            effects.add(new_effect)
            global_var.get_value('laser_sound').play()
        if self.touched and self.touchFrame%8==0 and self.touchFrame<=90:
            new_bullet=orb_Bullet_gravity()
            new_bullet.setGravity(0.05)
            new_bullet.initial(self.tx,self.ty,1)
            randomValue=-(self.eruptRandomAngle/2)+random.random()*self.eruptRandomAngle
            randomSpeed=random.random()*4+6
            if self.touch_direction==1:
                new_bullet.setSpeed(180+randomValue,randomSpeed)
                new_bullet.setGravity(0.055)
                new_bullet.gravDirection=1
            elif self.touch_direction==2:
                new_bullet.setSpeed(270+randomValue,randomSpeed)
                new_bullet.gravDirection=2
            elif self.touch_direction==3:
                new_bullet.setSpeed(0+randomValue,randomSpeed)
                new_bullet.setGravity(0.055)
                new_bullet.gravDirection=3
            elif self.touch_direction==4:
                new_bullet.setSpeed(90+randomValue,randomSpeed)
                new_bullet.gravDirection=4
            #new_bullet.loadColor('blue')
            new_bullet.doColorCode(random.randint(0,6))
            bullets.add(new_bullet)
        if self.touched and self.touchFrame%90==0 and self.touchFrame!=0:
            new_effect=Effect.bulletCreate(3)
            new_effect.initial(self.tx,self.ty,84,32,25)
            effects.add(new_effect)
            self.randomAngle=random.random()*360
            for i in range(0,18):
                new_bullet=star_Bullet()
                new_bullet.initial(self.tx,self.ty,1)
                new_bullet.setSpeed(self.randomAngle+i*(360/18),2.5)
                new_bullet.loadColor('blue')
                bullets.add(new_bullet)
            global_var.get_value('enemyGun_sound2').play()
        if self.touchFrame>=270:
            self.kill()


    def detect(self):
        if self.ty>=690:
            self.touched=True
            self.touch_direction=2
        elif self.ty<=30:
            self.touched=True
            self.touch_direction=4
        elif self.tx<=60:
            self.touched=True
            self.touch_direction=3
        elif self.tx>=660:
            self.touched=True
            self.touch_direction=1
        if self.touched:
            self.speedx=0
            self.speedy=0

class orb_Bullet_distance(orb_Bullet):
    def __init__(self):
        super(orb_Bullet_distance,self).__init__()
        self.distance=1000
        self.tempImage=0

    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.checkDistance()
        self.drawBullet(screen)
        #screen.blit(self.image,(self.rect.centerx-12,self.rect.centery-12))
        #screen.blit(self.surf,self.rect)
        self.checkValid()
    
    def checkDistance(self):
        px=global_var.get_value('player1x')
        py=global_var.get_value('player1y')
        dx=abs(px-self.tx)
        dy=abs(py-self.ty)
        self.distance=math.sqrt(math.pow(dx,2)+math.pow(dy,2))
    
    def drawBullet(self,screen):
        if self.lastFrame<=5:
            screen.blit(self.image,(self.rect.centerx-12,self.rect.centery-12))
        elif self.lastFrame<=30:
            self.tempImage=self.image
            alpha=256-round((self.lastFrame-5)*10.24)
            self.tempImage.set_alpha(alpha)
            screen.blit(self.tempImage,(self.rect.centerx-12,self.rect.centery-12))
        else:
            self.tempImage=self.image
            alpha=round(-1/200*self.distance**2+256)
            if alpha>=256:
                alpha=256
            if alpha<=0:
                alpha=0
            self.tempImage.set_alpha(alpha)
            screen.blit(self.tempImage,(self.rect.centerx-12,self.rect.centery-12))
    
class big_star_Bullet_distance(big_star_Bullet):
    def __init__(self):
        super(big_star_Bullet_distance,self).__init__()
        self.distance=1000
        self.tempImage=0
        self.lastFrame=0
    def checkDistance(self):
        px=global_var.get_value('player1x')
        py=global_var.get_value('player1y')
        dx=abs(px-self.tx)
        dy=abs(py-self.ty)
        self.distance=math.sqrt(math.pow(dx,2)+math.pow(dy,2))

    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.checkDistance()
        #screen.blit(self.image,(self.rect.centerx-3,self.rect.centery-3))
        #screen.blit(self.surf,self.rect)
        self.drawBullet(screen)
        self.checkValid()
    
    def drawBullet(self,screen):
        self.dAngle+=3
        if self.lastFrame<=5:
            gF.drawRotation(self.image,(self.rect.centerx-24,self.rect.centery-24),self.dAngle,screen)
        else:
            self.tempImage=self.image
            alpha=round((103/75)*self.distance-(56/3))
            if alpha>=256:
                alpha=256
            if alpha<=50:
                alpha=50
            self.tempImage.set_alpha(alpha)
            gF.drawRotation(self.tempImage,(self.rect.centerx-24,self.rect.centery-24),self.dAngle,screen)
        
class orb_Bullet_star_pattern_main(orb_Bullet):
    def __init__(self,multiple,speed,eventNum):
        super(orb_Bullet_star_pattern_main,self).__init__()
        self.multiple=multiple
        self.interval=4
        self.speed=speed
        self.length=self.multiple*self.speed
        self.n=round(self.length*0.5258)
        self.lastFrame=0
        self.turnCount=0
        self.splitAngle=0
        self.eventNum=eventNum
        self.direction=random.randint(0,1)
        if self.direction==0:
            self.direction=-1
        self.moveAngle=self.splitAngle+(30+random.random()*30)*self.direction
        self.resetAngle=self.moveAngle
        self.transColor='lakeBlue'
        self.trackColor='blue'
        self.cancalable=False
    def update(self,screen,bullets,effects):
        for i in range(2):
            self.lastFrame+=1
            self.moveStratege()
            self.movement()
            self.fire(bullets,effects)
            self.sound()
            self.drawBullet(screen)
            #screen.blit(self.image,(self.rect.centerx-12,self.rect.centery-12))
            #screen.blit(self.surf,self.rect)
            self.checkValid()
            
    
    def moveStratege(self):
        if self.lastFrame==2:
            self.countAngle()
            self.setSpeed(self.angle+162,self.speed)
        elif (self.lastFrame-2)%self.multiple==0 and self.turnCount<=4:
            self.countAngle()
            self.setSpeed(self.angle+144,self.speed)
            self.resetAngle+=144
            self.moveAngle=self.resetAngle
            self.turnCount+=1
        if self.turnCount>=5:#涩沙沙到此一游
            self.kill()

    def sound(self):
        if self.lastFrame%6==0:
            global_var.get_value('enemyGun_sound1').stop()
            global_var.get_value('enemyGun_sound1').play()
    
    def fire(self,bullets,effects):
        if self.lastFrame%self.interval==0:
            
            if self.trackColor=='orange':
                new_effect=Effect.bulletCreate(6)
            else:
                new_effect=Effect.bulletCreate(1)
            new_effect.initial(self.tx,self.ty,64,24,self.interval*2)
            effects.add(new_effect)

            new_bullet=orb_Bullet_split_5(self.splitAngle,self.eventNum,self.moveAngle)
            new_bullet.initial(self.tx,self.ty,1)
            new_bullet.setSpeed(0,0)
            new_bullet.loadColor(self.trackColor)
            new_bullet.transColor=self.transColor
            bullets.add(new_bullet)
            self.moveAngle-=17
        
        
class orb_Bullet_split_5(orb_Bullet):
    def __init__(self,splitAngle,eventNum,moveAngle):
        super(orb_Bullet_split_5,self).__init__()
        self.splitAngle=splitAngle
        self.lastFrame=0
        self.splitFrame=200
        self.eventNum=eventNum
        self.doEvent=True
        self.moveAngle=moveAngle
        self.transColor='lakeBlue'
    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.drawBullet(screen)
        self.split(bullets)
        #screen.blit(self.image,(self.rect.centerx-12,self.rect.centery-12))
        #screen.blit(self.surf,self.rect)
        self.checkValid()
    
    def split(self,bullets):
        if global_var.get_value('bossEvent_'+str(self.eventNum)):
            for i in range(0,5):
                new_bullet=orb_Bullet_split_sub(50,50,self.moveAngle)
                new_bullet.initial(self.tx,self.ty,1)
                new_bullet.setSpeed(self.splitAngle+i*(360/5),4)
                new_bullet.loadColor(self.transColor)
                bullets.add(new_bullet)
            #global_var.set_value('bossEvent_'+str(self.eventNum),False)
            self.kill()

class orb_Bullet_split_sub(orb_Bullet):
    def __init__(self,moveFrame,stayFrame,moveAngle):
        super(orb_Bullet_split_sub,self).__init__()
        self.moveFrame=moveFrame
        self.stayFrame=stayFrame
        self.moveAngle=moveAngle
        self.speed=1.8

    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.checkFrame()
        self.movement()
        self.drawBullet(screen)
        #self.split()
        #screen.blit(self.image,(self.rect.centerx-12,self.rect.centery-12))
        #screen.blit(self.surf,self.rect)
        self.checkValid()
    
    def checkFrame(self):
        if self.lastFrame==self.moveFrame:
            self.setSpeed(0,0)
        if self.lastFrame==(self.stayFrame+self.moveFrame):
            self.setSpeed(self.moveAngle,self.speed)
        
class orb_Bullet_bouncing_5(orb_Bullet):
    def __init__(self):
        super(orb_Bullet_bouncing_5,self).__init__()
        self.bounceMax=1
        self.lastFrame=0
    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.bouncing()
        self.drawBullet(screen)
        #screen.blit(self.image,(self.rect.centerx-12,self.rect.centery-12))
        #screen.blit(self.surf,self.rect)
        self.checkValid()
    def bouncing(self):
        if self.bounceMax>0:
            if self.tx<=60 or self.tx>=660:
                self.speedx=-self.speedx
                self.bounceMax-=1
                self.loadColor('blue')
                if not global_var.get_value('kiraing'):
                    global_var.get_value('kira_sound').stop()
                    global_var.get_value('kira_sound').play()
                    global_var.set_value('kiraing',True)
            elif self.ty<=30:
                self.speedy=-self.speedy
                self.bounceMax-=1
                self.loadColor('blue')
                if not global_var.get_value('kiraing'):
                    global_var.get_value('kira_sound').stop()
                    global_var.get_value('kira_sound').play()
                    global_var.set_value('kiraing',True)

class big_Bullet_tracing_test(big_Bullet):
    def __init__(self):
        super(big_Bullet_tracing_test,self).__init__()
        self.preFrame=40
        self.stayFrame=60
        self.lastFrame=0
        self.transSpeed=4
        self.transFrame=100
    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.motionStrat()
        self.movement()
        self.fire(bullets,effects)
        self.drawBullet(screen)
        #screen.blit(self.image,(self.rect.centerx-12,self.rect.centery-12))
        #screen.blit(self.surf,self.rect)
        self.checkValid()
    
    def drawBullet(self,screen):
        if self.lastFrame<=self.preFrame+self.stayFrame:
            screen.blit(self.image,(self.rect.centerx-48,self.rect.centery-48))
        else:
            alpha=210-(210-60)/self.transFrame*(self.lastFrame-self.preFrame-self.stayFrame)
            self.image.set_alpha(alpha)
            screen.blit(self.image,(self.rect.centerx-48,self.rect.centery-48))
    def motionStrat(self):
        if self.lastFrame==self.preFrame:
            self.speedx=0
            self.speedy=0
        
        if self.lastFrame==self.preFrame+self.stayFrame:
            px=global_var.get_value('player1x')
            py=global_var.get_value('player1y')
            self.selfTarget(px,py,self.transSpeed)
        
        if self.lastFrame>=self.preFrame+self.stayFrame+self.transFrame:
            self.kill()
    
    def fire(self,bullets,effects):
        if self.lastFrame<self.preFrame:
            self.countAngle()
            intervalAngle=30
            adjust=0
            speedAdjust=0
            if self.lastFrame%8==0:
                new_effect=Effect.bulletCreate(0)
                new_effect.initial(self.tx,self.ty,64,32,8)
                effects.add(new_effect)
                if not global_var.get_value('enemyFiring1'):
                    global_var.get_value('enemyGun_sound1').stop()
                    global_var.get_value('enemyGun_sound1').play()
                    global_var.set_value('enemyFiring1',True)
                if self.speedx<0:
                    adjust+=3
                else:
                    adjust-=3
                speedAdjust-=0.2
                for i in range(0,6):
                    new_bullet=small_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.setSpeed(self.angle-180-2.5*intervalAngle+i*intervalAngle+adjust,4+speedAdjust)
                    new_bullet.loadColor('blue')
                    bullets.add(new_bullet)
        
        if self.lastFrame>=self.preFrame and self.lastFrame<self.preFrame+self.stayFrame:
            if (self.lastFrame-self.preFrame)%25==0:
                new_effect=Effect.bulletCreate(3)
                new_effect.initial(self.tx,self.ty,84,32,25)
                effects.add(new_effect)
                if not global_var.get_value('enemyFiring2'):
                    global_var.get_value('enemyGun_sound2').stop()
                    global_var.get_value('enemyGun_sound2').play()
                    global_var.set_value('enemyFiring2',True)
                new_bullet=star_Bullet()
                new_bullet.initial(self.tx,self.ty,1)
                px=global_var.get_value('player1x')
                py=global_var.get_value('player1y')
                new_bullet.selfTarget(px,py,5)
                new_bullet.countAngle()
                new_bullet.loadColor('blue')
                angle=new_bullet.angle
                bullets.add(new_bullet)
                for i in range(1,10):
                    new_bullet=star_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.setSpeed(angle-i*(360/10),5)
                    new_bullet.loadColor('blue')
                    bullets.add(new_bullet)
        
        if self.lastFrame>=self.preFrame+self.stayFrame-40:
            if (self.lastFrame-self.preFrame+self.stayFrame)%4==0:
                new_effect=Effect.bulletCreate(5)
                new_effect.initial(self.tx,self.ty,84,32,4)
                effects.add(new_effect)
                if not global_var.get_value('enemyFiring1'):
                    global_var.get_value('enemyGun_sound1').stop()
                    global_var.get_value('enemyGun_sound1').play()
                    global_var.set_value('enemyFiring1',True)
                angle=random.random()*360
                speed=0.1
                for i in range(0,1):
                    new_bullet=orb_bullet_delay()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.setSpeed(angle-i*(360/3),speed)
                    new_bullet.startSpeed=speed
                    new_bullet.loadColor('green')
                    bullets.add(new_bullet)

class orb_bullet_delay(orb_Bullet):
    def __init__(self):
        super(orb_bullet_delay,self).__init__()
        self.retainFrame=70
        self.startSpeed=0.1
        self.endSpeed=4.5
        self.accFrame=120
    
    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.motionStrat()
        self.drawBullet(screen)
        #screen.blit(self.image,(self.rect.centerx-12,self.rect.centery-12))
        #screen.blit(self.surf,self.rect)
        self.checkValid()

    def motionStrat(self):
        if self.lastFrame<=self.retainFrame:
            if self.lastFrame==self.retainFrame:
                if not global_var.get_value('kiraing'):
                    global_var.get_value('kira_sound').stop()
                    global_var.get_value('kira_sound').play()
                    global_var.set_value('kiraing',True)
        elif self.lastFrame-self.retainFrame<=self.accFrame:
            self.countAngle()
            speed=self.startSpeed+(self.lastFrame-self.retainFrame)*(self.endSpeed-self.startSpeed)/self.accFrame
            self.setSpeed(self.angle,speed)
        
class laser_bullet_decline(laser_Bullet_sub):
    def __init__(self,length,ratio):
        super(laser_bullet_decline,self).__init__(length,ratio)
        self.length=length
        self.ratio=ratio
    def draw(self,screen):
        width=round((1-self.frame/self.length)*13)+3
        image=pygame.transform.scale(self.image,(width,width))
        screen.blit(image,(self.rect.centerx-round(width/2),self.rect.centery-round(width/2)))
        #screen.blit(self.surf,self.rect)
    
class mid_bullet_delay(mid_Bullet):
    def __init__(self):
        super(mid_bullet_delay,self).__init__()
        self.delay=40
        self.lastFrame=0
        self.speed=5
    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.motionStrat()
        self.drawBullet(screen)
        #screen.blit(self.surf,self.rect)
        self.checkValid()
    
    def setDelay(self,delay,speed):
        self.delay=delay
        self.speed=speed
    
    def motionStrat(self):
        if self.lastFrame==self.delay:
            if not global_var.get_value('kiraing'):
                    global_var.get_value('kira_sound').play()
                    global_var.set_value('kiraing',True)
            self.countAngle()
            self.setSpeed(self.angle,self.speed)

class star_bullet_side_selfTarget(star_Bullet):
    def __init__(self):
        super(star_bullet_side_selfTarget,self).__init__()
        self.speed=0
        self.bounce=1
        self.toggle=0
    def setSpeed(self,angle,speed):
        s=math.sin(math.radians(angle))
        c=math.cos(math.radians(angle))
        self.speedy=s*speed
        self.speedx=c*speed
        self.speed=speed

    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.motion_strategy(effects)
        self.drawBullet(screen)
        self.checkValid()
    
    def checkValid(self):
        if self.rect.top>=720-20:
            self.kill()
        if self.rect.bottom<=0+20:
            self.kill()
        if self.rect.right<=0+50:
            self.kill()
        if self.rect.left>=670:
            self.kill()

    def motion_strategy(self,effects):
        bound=False
        if self.tx<=60 or self.tx>=660 or self.ty<=30:
            bound=True
        if self.bounce>=1 and bound and self.ty<=500:
            if self.toggle%2==1:
                self.loadColor('lakeBlue')
            else:
                self.loadColor('orange')
            new_effect=Effect.bulletCreate(4)
            new_effect.initial(self.tx,self.ty,84,48,5)
            effects.add(new_effect)
            global_var.get_value('kira_sound').stop()
            global_var.get_value('kira_sound').play()
            self.bounce=0
            px=global_var.get_value('player1x')
            py=global_var.get_value('player1y')
            self.selfTarget(px,py,self.speed)

class big_star_Bullet_slave(big_star_Bullet):
    def __init__(self,tAngle):
        super(big_star_Bullet_slave,self).__init__()
        self.tAngle=tAngle
        self.speed=4
        self.maxFrame=round(360/abs(tAngle))
        self.lastFrame=0
        self.fireCount=0
        self.cancalable=False
        self.toggle=0
    def setSpeed(self,angle,speed):
        s=math.sin(math.radians(angle))
        c=math.cos(math.radians(angle))
        self.speedy=s*speed
        self.speedx=c*speed
        self.speed=speed

    def update(self,screen,bullets,effects):
        for i in range(0,2):
            self.lastFrame+=1
            self.fire(bullets,effects)
            self.movement()
            self.motion_strategy(effects)
            #screen.blit(self.image,(self.rect.centerx-3,self.rect.centery-3))
            #screen.blit(self.surf,self.rect)
            self.drawBullet(screen)
            self.checkValid()
    
    def motion_strategy(self,effects):
        self.countAngle()
        self.setSpeed(self.angle+self.tAngle,self.speed)

    def checkValid(self):
        if self.lastFrame>=self.maxFrame:
            self.kill()
        
    def fire(self,bullets,effects):
        if self.lastFrame%3==0:
            self.countAngle()
            if not global_var.get_value('enemyFiring2'):
                global_var.get_value('enemyGun_sound2').stop()
                global_var.get_value('enemyGun_sound2').play()
                global_var.set_value('enemyFiring2',True)
            
            if self.toggle%2==0:
                new_effect=Effect.bulletCreate(4)
            else:
                new_effect=Effect.bulletCreate(6)
            new_effect.initial(self.tx,self.ty,84,32,8)
            effects.add(new_effect)

            self.fireCount+=1
            if self.tAngle<0:
                self.directAdj=-1
            else:
                self.directAdj=1
            new_bullet=rice_Bullet_delay(delay=90)
            new_bullet.initial(self.tx,self.ty,1)
            new_bullet.toggle=self.toggle
            if self.toggle%2==0:
                new_bullet.loadColor('blue')
            else:
                new_bullet.loadColor('orange')
            new_bullet.setSpeed(self.angle+(100+self.fireCount*3)*self.directAdj,0.001)
            new_bullet.speed=4-(self.fireCount-1)*0.05
            bullets.add(new_bullet)

class star_Bullet_delay(star_Bullet):
    def __init__(self,delay=40):
        super(star_Bullet_delay,self).__init__()
        self.delay=delay
        self.speed=4
        self.angle=0

    def doDelay(self,effects):
        if self.lastFrame==self.delay:
            if not global_var.get_value('kiraing'):
                global_var.get_value('kira_sound').stop()
                global_var.get_value('kira_sound').play()
                global_var.set_value('kiraing',True)
            new_effect=Effect.bulletCreate(4)
            new_effect.initial(self.tx,self.ty,84,32,6)
            effects.add(new_effect)
            self.countAngle()
            self.setSpeed(self.angle,self.speed)
    
    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.doDelay(effects)
        #screen.blit(self.image,(self.rect.centerx-3,self.rect.centery-3))
        #screen.blit(self.surf,self.rect)
        self.drawBullet(screen)
        self.checkValid()
    
class rice_Bullet_delay(satsu_Bullet):
    def __init__(self,delay=40):
        super(rice_Bullet_delay,self).__init__()
        self.delay=delay
        self.speed=4
        self.n_speed=0
        self.angle=0
        self.lastFrame=0
        self.accFrame=30
        self.toggle=0
    def doDelay(self,effects):
        if self.lastFrame==self.delay:
            if not global_var.get_value('kiraing'):
                global_var.get_value('kira_sound').stop()
                global_var.get_value('kira_sound').play()
                global_var.set_value('kiraing',True)
            if self.toggle%2==0:
                code=6
            else:
                code=4
            new_effect=Effect.bulletCreate(code)
            new_effect.initial(self.tx,self.ty,84,32,6)
            effects.add(new_effect)
            self.countAngle()
            #self.setSpeed(self.angle,self.speed)
            if self.toggle%2==0:
                self.loadColor('orange')
            else:
                self.loadColor('blue')

    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.doDelay(effects)
        self.accelerate()
        #screen.blit(self.image,(self.rect.centerx-3,self.rect.centery-3))
        
        self.drawBullet(screen)
        #screen.blit(self.surf,self.rect)
        self.checkValid()
    
    def accelerate(self):
        if self.lastFrame>=self.delay and self.lastFrame<self.delay+self.accFrame:
            self.n_speed+=(self.speed/self.accFrame)
            self.setSpeed(self.angle,self.n_speed)
