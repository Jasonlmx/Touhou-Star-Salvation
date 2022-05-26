from imp import new_module
from pickle import FALSE
from xxlimited import new
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

def sendFireSound(num):
    index=str(num)
    boolSign='enemyFiring'+index
    soundIndex='enemyGun_sound'+index
    if not global_var.get_value(boolSign):
        global_var.get_value(soundIndex).stop()
        global_var.get_value(soundIndex).play()
        global_var.set_value(boolSign,True)

def sendKiraSound():
    if not global_var.get_value('kiraing'):
        global_var.get_value('kira_sound').stop()
        global_var.get_value('kira_sound').play()
        global_var.set_value('kiraing',True)

#  bullet zone

class part2_acc_bullet(Bullet.orb_bullet_lgtnsp6_stay_accelerate):
    def __init__(self):
        super(part2_acc_bullet,self).__init__()
    
    def motionStrate(self):
        if self.lastFrame==self.accStart:
            sendKiraSound()
        if self.lastFrame>=self.accStart and self.lastFrame<self.accStart+self.accFrame:
            acc=(self.endSpeed-self.initialSpeed)/self.accFrame
            self.speedNow+=acc
            self.setSpeed(self.angle,self.speedNow)

class part3_acc_bullet(Bullet.rice_bullet_lgtnsp6_stay_accelerate):
    def __init__(self):
        super(part3_acc_bullet,self).__init__()

    def motionStrate(self):
        if self.lastFrame==self.accStart:
            sendKiraSound()
        if self.lastFrame>=self.accStart and self.lastFrame<self.accStart+self.accFrame:
            acc=(self.endSpeed-self.initialSpeed)/self.accFrame
            self.speedNow+=acc
            self.setSpeed(self.angle,self.speedNow)

class part4_gravity_bullet(Bullet.rice_Bullet):
    def __init__(self):
        super(part4_gravity_bullet,self).__init__()
        self.maxSpeed=4
        self.gravePerSec=+0.04
        self.makeNoise=True

    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.motionStrate()
        #screen.blit(self.image,(self.rect.centerx-3,self.rect.centery-3))
        #screen.blit(self.surf,self.rect)
        if self.lastFrame<=self.createMax and self.ifDrawCreate:
            self.drawCreateImg(screen)
        else:
            self.drawBullet(screen)
        self.checkValid()

    def speedCalc(self):
        speed=math.sqrt(self.speedx**2+self.speedy**2)
        return speed
    
    def checkValid(self):
        if self.rect.top>=720-30+self.validAccuracy[1]:
            self.kill()
        if self.rect.right<=0+60-self.validAccuracy[3]:
            self.kill()
        if self.rect.left>=620+self.validAccuracy[2]:
            self.kill()

    def motionStrate(self):
        if self.speedCalc()<=self.maxSpeed or self.speedy<0:
            self.speedy+=self.gravePerSec
        elif self.makeNoise:
            self.makeNoise=False
            sendKiraSound()

class part4_gravity_bullet2(Bullet.orb_Bullet):
    def __init__(self):
        super(part4_gravity_bullet2,self).__init__()
        self.maxSpeed=4
        self.gravePerSec=+0.04
        self.makeNoise=True
    
    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.motionStrate()
        #screen.blit(self.image,(self.rect.centerx-3,self.rect.centery-3))
        #screen.blit(self.surf,self.rect)
        if self.lastFrame<=self.createMax and self.ifDrawCreate:
            self.drawCreateImg(screen)
        else:
            self.drawBullet(screen)
        self.checkValid()

    def speedCalc(self):
        speed=math.sqrt(self.speedx**2+self.speedy**2)
        return speed
    
    def checkValid(self):
        if self.rect.top>=720-30+self.validAccuracy[1]:
            self.kill()
        if self.rect.right<=0+60-self.validAccuracy[3]:
            self.kill()
        if self.rect.left>=620+self.validAccuracy[2]:
            self.kill()

    def motionStrate(self):
        if self.speedCalc()<=self.maxSpeed or self.speedy<0:
            self.speedy+=self.gravePerSec
        elif self.makeNoise:
            self.makeNoise=False
            sendKiraSound()

class midpath_spell1_wind_bullet(Bullet.sharp_Bullet):
    def __init__(self):
        super(midpath_spell1_wind_bullet,self).__init__()
        self.angleIncPerFrame=-1.9
        self.angleIncChange=+0.02
        self.initialSpeed=4
        self.judgeBool=True
    def setSpeed(self,angle,speed):
        s=math.sin(math.radians(angle))
        c=math.cos(math.radians(angle))
        self.speedy=s*speed
        self.speedx=c*speed
        #self.initialSpeed=speed

    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.motionStrate()
        if self.lastFrame<=self.createMax and self.ifDrawCreate:
            self.drawCreateImg(screen)
        else:
            self.drawBullet(screen)
        self.checkValid()

    def motionStrate(self):
        self.countAngle()
        if self.judgeBool:
            if self.angleIncPerFrame<0:
                self.angleIncPerFrame+=self.angleIncChange
            else:
                self.angleIncPerFrame=0     
        else:
            if self.angleIncPerFrame>0:
                self.angleIncPerFrame+=self.angleIncChange
            else:
                self.angleIncPerFrame=0   
        angle=self.angle+self.angleIncPerFrame
        self.setSpeed(angle,self.speed)
        
class midpath_spell2_rain_bullet(Bullet.rice_Bullet):
    def __init__(self):
        super(midpath_spell2_rain_bullet,self).__init__()
        self.maxSpeed=4
        self.gravePerSec=+0.03
        self.makeNoise=True
        self.startFrame=0
        

    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        if self.lastFrame>self.startFrame:
            self.motionStrate()
        #screen.blit(self.image,(self.rect.centerx-3,self.rect.centery-3))
        #screen.blit(self.surf,self.rect)
        if self.lastFrame<=self.createMax and self.ifDrawCreate:
            self.drawCreateImg(screen)
        else:
            self.drawBullet(screen)
        self.checkValid()

    def speedCalc(self):
        speed=math.sqrt(self.speedx**2+self.speedy**2)
        return speed
    
    def checkValid(self):
        if self.rect.top>=720-30+self.validAccuracy[1]:
            self.kill()
        if self.rect.right<=0+60-self.validAccuracy[3]:
            self.kill()
        if self.rect.left>=620+self.validAccuracy[2]:
            self.kill()

    def motionStrate(self):
        if self.speedCalc()<=self.maxSpeed or self.speedy<0:
            self.speedy+=self.gravePerSec
        elif self.makeNoise:
            self.makeNoise=False
            sendKiraSound()

class midpath_spell2_laser_bullet_main(Bullet.laser_Bullet_main):
    def __init__(self,ratio=8,leng=20,speed=5):
            super(midpath_spell2_laser_bullet_main,self).__init__()
            self.ratio=ratio
            self.surf = pygame.Surface((self.ratio,self.ratio))
            self.surf.fill((255,255,255))
            self.rect = self.surf.get_rect()
            self.speed=speed
            self.length=leng
            self.angleChangePerFrame=-4.5
            self.angleChangeInc=0.05
            self.initialSpeed=speed
            self.maxFrame=100
            self.adj=0
    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.motionStrate()
        self.countAngle()
        new_sub=Bullet.laser_Bullet_sub(self.length,self.ratio)
        new_sub.ifExtraJudgePoint=True
        new_sub.angle=self.angle
        new_sub.speed=self.speed
        new_sub.initial(self.tx,self.ty,self.fro)
        new_sub.doColorCode(self.colorNum)
        bullets.add(new_sub)
        self.checkValid()
    
    def motionStrate(self):
        self.countAngle()
        if self.adj==0:
            if self.angleChangePerFrame<=2:
                angle=self.angle+self.angleChangePerFrame
                self.angleChangePerFrame+=self.angleChangeInc
                self.speed+=0.12
                self.setSpeed(angle,self.speed)
        elif self.adj==1:
            if self.angleChangePerFrame<=2:
                angle=self.angle-self.angleChangePerFrame
                self.angleChangePerFrame+=self.angleChangeInc
                self.speed+=0.12
                self.setSpeed(angle,self.speed)

    def checkValid(self):
        if self.lastFrame>=self.maxFrame:
            self.kill()

class midpath_spell3_small_snow_bullet(Bullet.small_Bullet):
    def __init__(self):
        super(midpath_spell3_small_snow_bullet,self).__init__()
        self.signalReciever=False
        self.ifChanged=False
        self.initialSpeed=0
    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.signalRecieve() 
        self.motionStrate(bullets)
        if self.lastFrame<=self.createMax and self.ifDrawCreate:
            self.drawCreateImg(screen)
        else:
            self.drawBullet(screen)
        #screen.blit(self.surf,self.rect)
        self.checkValid()
    
    def motionStrate(self,bullets):
        if self.signalReciever and not self.ifChanged:
            self.countAngle()
            angle=random.random()*360
            new_bullet=midpath_spell3_small_snow_bullet_acc()
            new_bullet.initial(self.tx,self.ty,0)
            new_bullet.setAccSpeed(angle,0.001,self.initialSpeed-1.2,60,90)
            new_bullet.setSpeed(angle,0.001)
            new_bullet.loadColor('lightBlue')
            bullets.add(new_bullet)
            self.kill()

    def signalRecieve(self):
        self.signalReciever=global_var.get_value('midPathSpell3Signal')

class midpath_spell3_small_snow_bullet_acc(Bullet.small_bullet_lgtnsp6_stay_accelerate):
    def __init__(self):
        super(midpath_spell3_small_snow_bullet_acc,self).__init__()

class midpath_spell3_mid_snow_bullet(Bullet.mid_Bullet):
    def __init__(self):
        super(midpath_spell3_mid_snow_bullet,self).__init__()
        self.ifChanged=False
        self.signalReciever=False
        self.warnLineProcessSign=False
        self.warnLineFrame=0
        self.maxIncFrame=70
    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.signalRecieve() 
        self.warnRecieve()
        self.motionStrate(bullets)
        self.drawWarnCircle(screen)
        if self.lastFrame<=self.createMax and self.ifDrawCreate:
            self.drawCreateImg(screen)
        else:
            self.drawBullet(screen)
        #screen.blit(self.surf,self.rect)
        self.checkValid()
    
    def drawWarnCircle(self,screen):
        if self.warnLineProcessSign and self.warnLineFrame<=self.maxIncFrame:
            radius=round(23*(self.warnLineFrame/self.maxIncFrame)+1)
        else:
            radius=24
        if self.warnLineProcessSign:
            pygame.draw.circle(screen,(255,255,255),(round(self.tx),round(self.ty)),radius,1)

    def motionStrate(self,bullets):
        if self.signalReciever and not self.ifChanged:
            radius=12
            initialAngle=random.random()*360
            for i in range(6):
                new_bullet=part3_acc_bullet()
                nx=self.tx+radius*math.cos((initialAngle+i*(360/6))*math.pi/180)
                ny=self.ty+radius*math.sin((initialAngle+i*(360/6))*math.pi/180)
                new_bullet.initial(nx,ny,0)
                new_bullet.setAccSpeed(initialAngle+i*(360/6),0.001,2.5,60,90)
                new_bullet.doColorCode(8)
                new_bullet.setSpeed(initialAngle+i*(360/6),0.001)
                bullets.add(new_bullet)
            self.kill()
    def warnRecieve(self):
        self.warnLineFrame=global_var.get_value('midPathSpell3WarnFrame')
        self.warnLineProcessSign=global_var.get_value('midPathSpell3Warn')

    def signalRecieve(self):
        self.signalReciever=global_var.get_value('midPathSpell3Signal')

class part6_base_laserBullet(midpath_spell2_laser_bullet_main):
    def __init__(self,ratio=8,leng=20,speed=5):
        super(part6_base_laserBullet,self).__init__()
        self.ratio=ratio
        self.surf = pygame.Surface((self.ratio,self.ratio))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()            
        self.speed=speed
        self.length=leng
    def motionStrate(self):
        pass

class part6_rice_to_laserBullet_bullet(Bullet.rice_Bullet):
    def __init__(self):
        super(part6_rice_to_laserBullet_bullet,self).__init__()
        self.transFrame=90

    def update(self, screen, bullets, effects):
        self.lastFrame+=1
        self.movement()
        self.trans(bullets)
        if self.lastFrame<=self.createMax and self.ifDrawCreate:
            self.drawCreateImg(screen)
        else:
            self.drawBullet(screen)
        self.checkValid()
    
    def trans(self,bullets):
        if self.lastFrame==self.transFrame:
            new_bullet=part6_base_laserBullet(6,20,12)
            new_bullet.initial(self.tx,self.ty,0)
            self.countAngle()
            new_bullet.setSpeed(self.angle,12)
            new_bullet.doColorCode(3)
            bullets.add(new_bullet)
            self.kill()

#  enemy zone


class testEnemy(DADcharacter.enemy):
    def __init__(self):
        super(testEnemy,self).__init__()

class part1_enemy(DADcharacter.spirit):
    def __init__(self):
        super(part1_enemy,self).__init__()
        self.actionNum=0
        self.angleList=[270,220,320]
        self.frameList=[]
        self.speed=2.4
        self.speedQuit=4
        self.staySec=2.5
        self.health=500
        self.fireFrame=random.randint(0,40)

    def ai_move(self):
        if self.lastFrame<=1.5*60:
            self.setSpeed(90,self.speed)
        elif self.lastFrame<=2*60:
            speedNow=self.speed/30*(120-self.lastFrame)
            self.setSpeed(90,speedNow)
        elif self.lastFrame<=(2+self.staySec)*60:
            pass
        elif self.lastFrame<=(2+self.staySec+0.5)*60:
            speedNow=self.speedQuit/30*(30-((2+self.staySec+0.5)*60-self.lastFrame))
            self.setSpeed(self.angleList[self.actionNum],speedNow)
        elif self.lastFrame>=(2+self.staySec+0.5+1)*60:
            self.kill()

    def fire(self, frame, bullets, effects):
        self.fireFrame+=1
        if self.rect.centery>=17:
            if self.lastFrame<=1.5*60:
                if self.fireFrame%40==0:
                    sendFireSound(3)
                    for i in range(0,5):
                        new_bullet=Bullet.rice_Bullet()
                        new_bullet.initial(self.tx,self.ty,0)
                        new_bullet.loadColor('green')
                        new_bullet.setSpeed(50+20*i,4)
                        bullets.add(new_bullet)
            elif self.lastFrame<=(2+self.staySec)*60:
                if self.fireFrame%80==0:
                    sendFireSound(3)
                    new_bullet=Bullet.orb_Bullet()
                    new_bullet.initial(self.tx,self.ty,0)
                    new_bullet.loadColor('lightGreen')
                    px=global_var.get_value('player1x')
                    py=global_var.get_value('player1y')
                    new_bullet.selfTarget(px,py,3.2)
                    bullets.add(new_bullet)
            else:
                if self.fireFrame%40==0:
                    self.randomAngle=random.random()*360
                    sendFireSound(3)
                    for i in range(16):
                        new_bullet=Bullet.kunai_Bullet()
                        new_bullet.initial(self.tx,self.ty,0)
                        new_bullet.loadColor('green')
                        px=global_var.get_value('player1x')
                        py=global_var.get_value('player1y')
                        new_bullet.setSpeed(self.randomAngle+(360/16*i),4)
                        bullets.add(new_bullet)

class part2_enemy(DADcharacter.yinyangyu):
    def __init__(self):
        super(part2_enemy,self).__init__()
        self.InitAngle=90
        self.speed=3
        self.amplifyAngle=random.random()*20+10
        self.health=1000
        self.fireFrame=random.randint(0,120)
        self.randomAngle=random.random()*360
    def ai_move(self):
        self.angle=self.amplifyAngle*math.sin(self.lastFrame*3/180*math.pi)+self.InitAngle
        self.setSpeed(self.angle,self.speed)
        if self.rect.top>=710:
            self.kill()
    
    def fire(self, frame, bullets, effects):
        self.fireFrame+=1
        if self.fireFrame%120<=16:
            if self.fireFrame%8==0:
                sendFireSound(3)
                new_bullet=Bullet.orb_Bullet()
                new_bullet.initial(self.tx,self.ty,0)
                px=global_var.get_value('player1x')
                py=global_var.get_value('player1y')
                new_bullet.selfTarget(px,py,4)
                new_bullet.loadColor('red')
                bullets.add(new_bullet)
    
    def doKill(self, effects, items, bullets):
        global_var.get_value('enemyDead_sound').play()
        new_effect=Effect.enemyDead()
        new_effect.initial(self.deadImage,self.rect.centerx,self.rect.centery)
        effects.add(new_effect)
        self.dropItem(items)
        for i in range(12):
            new_bullet=part2_acc_bullet()
            new_bullet.initial(self.tx,self.ty,0)
            new_bullet.setSpeed(self.randomAngle+i*(360/12),0.6)
            new_bullet.setAccSpeed(self.randomAngle+i*(360/12),0.6,2.3,60,40)
            new_bullet.loadColor('green')
            bullets.add(new_bullet)
            if False:
                new_bullet=part2_acc_bullet()
                new_bullet.initial(self.tx,self.ty,0)
                new_bullet.setSpeed(self.randomAngle+i*(360/12),1.2)
                new_bullet.setAccSpeed(self.randomAngle+i*(360/12),1.2,2.8,60,40)
                new_bullet.loadColor('green')
                bullets.add(new_bullet)
        self.kill()
    
    def dropItem(self,items):
        self.createItem(items,0,3)
        self.createItem(items,1,5)

class part3_enemy_main(DADcharacter.butterfly):
    def __init__(self):
        super(part3_enemy_main,self).__init__()
        self.health=7000
        self.actionNum=0
        self.inFrame=30
        self.decendFrame=20
        self.accFrame=20
        self.stayFrame=480
        self.angleList=(0,180)
        self.inSpeed=4.5
        self.decendSpeed=self.inSpeed
        self.accSpeed=0
        self.fireAngle=random.random()*360
        self.bulletSpeed=1.8
        self.speedMultipler=0
        self.fireCount=0
        self.fireFrame=0
        self.sign=1
        self.firetime=0
        self.colorList=(10,6)

    def ai_move(self):
        if self.lastFrame==1:
            self.setSpeed(self.angleList[self.actionNum],self.inSpeed)
        if self.lastFrame>=self.inFrame and self.lastFrame<self.inFrame+self.decendFrame:
            self.decendSpeed-=self.inSpeed/self.decendFrame
            self.setSpeed(self.angleList[self.actionNum],self.decendSpeed)
        if self.lastFrame==self.inFrame+self.decendFrame:
            self.setSpeed(90,0.01)
        if self.lastFrame>=self.inFrame+self.decendFrame+self.stayFrame and self.lastFrame<self.inFrame+self.decendFrame+self.stayFrame+self.accFrame:
            self.accSpeed+=self.inSpeed/self.accFrame
            self.setSpeed(self.angleList[self.actionNum]-180,self.accSpeed)
        if self.lastFrame>=self.inFrame+self.decendFrame+self.stayFrame+self.accFrame+self.inFrame+20:
            self.kill()

    def fire(self, frame, bullets, effects):
        if self.lastFrame>=self.inFrame+self.decendFrame and self.lastFrame<=self.inFrame+self.decendFrame+self.stayFrame:
            
            if self.fireFrame%100<=18:
                if self.fireFrame%100==0:
                    self.fireAngle=random.random()*360
                    self.speedMultipler=0
                    self.bulletSpeed=1.4
                    self.fireCount+=1
                    self.firetime=0
                    if self.fireCount%2==0:
                        self.sign=-1
                    else:
                        self.sign=1

                if self.fireFrame%100%3==0:
                    sendFireSound(3)
                    for i in range(0,5):
                        for j in range(0,5):
                            new_bullet=part3_acc_bullet()
                            new_bullet.initial(self.tx,self.ty,0)
                            new_bullet.setSpeed(self.fireAngle+i*(360/5),1+j*0.3)
                            new_bullet.setAccSpeed(self.fireAngle+i*(360/5),1+j*0.3,self.bulletSpeed+j*(0.3+self.speedMultipler),20,40)
                            #new_bullet.setSpeed(self.fireAngle+i*(360/6),self.bulletSpeed+j*(0.3+self.speedMultipler))
                            new_bullet.doColorCode(self.colorList[self.actionNum])
                            bullets.add(new_bullet)
                    self.fireAngle+=360/5/7*self.sign
                    self.speedMultipler+=0.12
                    self.bulletSpeed+=0.6
                    self.firetime+=1
            self.fireFrame+=1
    
    def dropItem(self,items):
        self.createItem(items,0,4)
        self.createItem(items,1,6)
                    
class part3_enemy_spirite(DADcharacter.spirit):
    def __init__(self):
        super(part3_enemy_spirite,self).__init__()
        self.health=1000
        self.actionNum=0
        self.amplifyAngle=15+random.random()*10
        self.initAngle=270
        self.randomSinFrame=random.randint(0,180)
        self.speed=2.7
        self.speedNow=self.speed
        self.upFrame=180+random.randint(0,40)
        self.decendFrame=20
        self.quitSpeed=4
        self.quitAcc=20
        self.stayFrame=0
        self.stayFrameMax=240
        self.angleList=[180,0,315,235]

        self.fireFrame=random.randint(0,80)
        self.quitFire=(1,-1)
        self.BulletColorDict=('green','blue')
        self.BulletColorDict2=(10,5)
    def ai_move(self):
        if self.lastFrame<=self.upFrame:
            self.randomSinFrame+=1
            if self.lastFrame%90==0:
                self.amplifyAngle+=3
            self.angle=self.amplifyAngle*math.sin(self.randomSinFrame*2/180*math.pi)+self.initAngle
            self.setSpeed(self.angle,self.speed)
        elif self.lastFrame<=self.upFrame+self.decendFrame:
            self.speedNow-=self.speed/self.decendFrame
            self.setSpeed(self.angle,self.speedNow)
        elif self.stayFrameMax>=self.stayFrame:
            self.stayFrame+=1
            if self.stayFrame==1:
                self.setSpeed(self.angleList[self.actionNum],0.05)
        elif self.speedNow<=self.quitSpeed:
            self.speedNow+=self.quitSpeed/self.quitAcc
            self.setSpeed(self.angleList[self.actionNum+2],self.speedNow)
        if self.rect.bottom<=25 or self.rect.left>=625 or self.rect.right<=55:
            self.kill()

    def fire(self, frame, bullets, effects):
        self.fireFrame+=1
        if self.lastFrame<=self.upFrame:
            if self.fireFrame%80>=75:
                sendFireSound(3)
                angle=255+random.random()*50
                new_bullet=part3_acc_bullet()
                new_bullet.initial(self.tx,self.ty,0)
                new_bullet.setSpeed(angle,0.2)
                new_bullet.setAccSpeed(angle,0.2,4+random.random(),30,10+(self.fireFrame%80-75)*3)
                new_bullet.doColorCode(self.BulletColorDict2[self.actionNum])
                bullets.add(new_bullet)
        elif self.stayFrameMax>=self.stayFrame:
            if self.stayFrame<=150:
                if self.fireFrame%70==0:
                    sendFireSound(2)
                    new_bullet=Bullet.scale_Bullet()
                    new_bullet.initial(self.tx,self.ty,0)
                    px=global_var.get_value('player1x')
                    py=global_var.get_value('player1y')
                    new_bullet.selfTarget(px,py,5)
                    new_bullet.countAngle()
                    angle=new_bullet.angle
                    #new_bullet.loadColor('green')
                    #bullets.add(new_bullet)
                    for i in (-1,0,1):
                        for j in range(3):
                            new_bullet=Bullet.scale_Bullet()
                            new_bullet.initial(self.tx,self.ty,0)
                            new_bullet.setSpeed(angle+i*45,4+0.8*j)
                            new_bullet.loadColor(self.BulletColorDict[self.actionNum])
                            bullets.add(new_bullet)
            else:
                if self.fireFrame%40==0:
                    angle=random.random()*360
                    for i in range(10):
                        new_bullet=Bullet.small_Bullet()
                        new_bullet.initial(self.tx,self.ty,0)
                        new_bullet.setSpeed(angle+i*(360/10),3)
                        new_bullet.loadColor('white')
                        bullets.add(new_bullet)
        else:
            if self.fireFrame%30==0:
                sendFireSound(2)
                angleAdj=random.random()*10-5
                for i in range(5):
                    new_bullet=Bullet.orb_Bullet()
                    new_bullet.initial(self.tx,self.ty,0)
                    new_bullet.setSpeed(90+i*(90/5)*self.quitFire[self.actionNum]+angleAdj,5)
                    new_bullet.loadColor(self.BulletColorDict[self.actionNum])
                    bullets.add(new_bullet)

class part4_enemy_kedama(DADcharacter.kedama):
    def __init__(self):
        super(part4_enemy_kedama,self).__init__()
        self.health=500
        self.actionNum=0
        self.startAngleAdjList=(25,-25)
        self.angleAdj=0.35
        self.angleNow=0
        self.adjPerFrame=(-self.angleAdj,self.angleAdj)
        self.angleList=(0,180)
        self.speed=4
        self.fireFrame=random.randint(0,50)

    def ai_move(self):
        if self.lastFrame==1:
            self.setSpeed(self.angleList[self.actionNum]+self.startAngleAdjList[self.actionNum],self.speed)
            self.angleNow=self.angleList[self.actionNum]+self.startAngleAdjList[self.actionNum]
        else:
            self.angleNow+=self.adjPerFrame[self.actionNum]
            self.setSpeed(self.angleNow,self.speed)
        if self.rect.left>=620 or self.rect.right<=60:
            self.kill()
    
    def fire(self, frame, bullets, effects):
        self.fireFrame+=1
        if self.fireFrame%50==0:
            sendFireSound(3)
            adjAngle=random.random()*20+260
            for i in (-1,0,1):
                new_bullet=part4_gravity_bullet()
                new_bullet.initial(self.tx,self.ty,0)
                new_bullet.setSpeed(adjAngle+i*25,3)
                new_bullet.doColorCode(8)
                bullets.add(new_bullet)
    
    def dropItem(self,items):
        self.createItem(items,0,1)
        self.createItem(items,1,3)
    
    def doKill(self, effects, items, bullets):
        global_var.get_value('enemyDead_sound').play()
        new_effect=Effect.enemyDead()
        new_effect.initial(self.deadImage,self.rect.centerx,self.rect.centery)
        effects.add(new_effect)
        angle=random.random()*50+245
        for i in (-1.5,-0.5,0.5,1.5):
            new_bullet=part4_gravity_bullet2()
            new_bullet.initial(self.tx,self.ty,0)
            new_bullet.setSpeed(angle+i*18,4)
            new_bullet.loadColor('blue')
            new_bullet.gravePerSec=0.08
            bullets.add(new_bullet)

        self.dropItem(items)
        self.kill()

class support_enemy_yinyangyu(DADcharacter.yinyangyu):
    def __init__(self):
        super(support_enemy_yinyangyu,self).__init__()
        self.fireInterval=60
        self.fireFrame=random.randint(0,self.fireInterval)
        self.colorNum=0
        self.health=1200
    def ai_move(self):
        if self.rect.left>=620 or self.rect.right<=60:
            self.kill()

    def fire(self, frame, bullets, effects):
        self.fireFrame+=1
        if self.fireFrame%self.fireInterval==0:
            sendFireSound(1)
            '''new_bullet=Bullet.small_Bullet()
            new_bullet.initial(self.tx,self.ty,0)
            px=global_var.get_value('player1x')
            py=global_var.get_value('player1y')
            new_bullet.selfTarget(px,py,3)
            new_bullet.countAngle()
            angle=new_bullet.angle
            rndAdj=random.random()*10-5'''
            angle=random.random()*360
            for i in range(10):
                for j in range(2):
                    new_bullet=part3_acc_bullet()
                    new_bullet.initial(self.tx,self.ty,0)
                    new_bullet.setSpeed(angle+i*36,0.5+0.5*j)
                    new_bullet.setAccSpeed(angle+i*36,0.5+0.5*j,3.5+2*j,50,60)
                    new_bullet.loadColor('red')
                    bullets.add(new_bullet)
    
    def dropItem(self, items):
        self.createItem(items,0,1)
        self.createItem(items,1,2)


class part5_enemy_kedama(DADcharacter.kedama):
    def __init__(self):
        super(part5_enemy_kedama,self).__init__()
        self.actionNum=0
        self.turnSign=[1,-1,1,-1]
        self.turnFrame=70
        self.changeFrame=40
        self.angleNow=90
        self.angleList=[90,90,270,270]
        self.initialSpeed=4.2
        self.health=600
        self.fireInterval=8
        self.fireFrame=random.randint(0,self.fireInterval)
    def ai_move(self):
        if self.lastFrame==1:
            self.angleNow=self.angleList[self.actionNum]
            self.setSpeed(self.angleNow,self.initialSpeed)
            
        if self.lastFrame>=self.turnFrame and self.lastFrame<self.changeFrame+self.turnFrame:
            self.angleNow+=90/self.changeFrame*self.turnSign[self.actionNum]
            self.setSpeed(self.angleNow,self.initialSpeed)
        if self.rect.left>=620 or self.rect.right<=60 or self.rect.top>=690 or self.rect.bottom<=30:
            self.kill()
    
    def fire(self, frame, bullets, effects):
        self.fireFrame+=1
        if self.fireFrame%self.fireInterval==0:
            sendFireSound(2)
            angle=random.random()*360
            new_bullet=part2_acc_bullet()
            new_bullet.initial(self.tx,self.ty,0)
            new_bullet.setSpeed(angle,0.2)
            new_bullet.setAccSpeed(angle,0.2,4,60,50)
            #new_bullet.doColorCode(random.randint(0,6))
            new_bullet.loadColor('green')
            bullets.add(new_bullet)

    def dropItem(self, items):
        self.createItem(items,0,2)
        self.createItem(items,1,3)

class part6_winged_butterfly(DADcharacter.butterfly):
    def __init__(self):
        super(part6_winged_butterfly,self).__init__()
        self.actionNum=0

        self.inFrame=70
        self.decFrame=20
        self.stayFrame=7*60
        self.incFrame=20
        self.outFrame=70
        self.initialSpeed=2.0
        self.speedNow=self.initialSpeed
        self.fireInterval=2
        self.fireFrame=0
        self.health=5000
        self.ifFire=False
        self.fireAngle=0
    def ai_move(self):
        self.ifFire=False
        if self.lastFrame==1:
            self.setSpeed(90,self.initialSpeed)
        elif self.lastFrame>self.inFrame and self.lastFrame<=self.inFrame+self.decFrame:
            self.speedNow-=self.initialSpeed/self.decFrame
            self.setSpeed(90,self.speedNow)
        elif self.lastFrame<=self.inFrame+self.decFrame+self.stayFrame and self.lastFrame>self.inFrame+self.decFrame:
            self.ifFire=True
        elif self.lastFrame<=self.inFrame+self.decFrame+self.stayFrame+self.incFrame and self.lastFrame>self.inFrame+self.decFrame+self.stayFrame:
            self.speedNow+=self.initialSpeed/self.incFrame
            self.setSpeed(270,self.speedNow)
        elif self.lastFrame>=self.inFrame+self.decFrame+self.stayFrame+self.incFrame+self.outFrame:
            self.kill()
    
    def fire(self, frame, bullets, effects):
        if self.ifFire:
            self.fireFrame+=1
            if self.fireFrame==1:
                new_bullet=Bullet.small_Bullet()
                new_bullet.initial(self.tx,self.ty,0)
                px=global_var.get_value('player1x')
                py=global_var.get_value('player1y')
                new_bullet.selfTarget(px,py,3)
                new_bullet.countAngle()
                #self.fireAngle=new_bullet.angle
                if self.actionNum==0:
                    self.fireAngle=90-30+random.random()*20
                elif self.actionNum==1:
                    self.fireAngle=90+30-random.random()*20

            if self.fireFrame%self.fireInterval==0:
                sendFireSound(2)
                angle=self.fireAngle
                angleAdj=80*math.sin(self.lastFrame*3/180*math.pi)+90
                for i in (-1,1):
                    for j in range(3):
                        fireAngle=angle+i*angleAdj
                        new_bullet=Bullet.sharp_Bullet()
                        radius=30
                        rx=self.tx+radius*math.cos(fireAngle/180*math.pi)
                        ry=self.ty+radius*math.sin(fireAngle/180*math.pi)
                        new_bullet.initial(rx,ry,0)
                        new_bullet.setSpeed(fireAngle,7.5+1.3*j)
                        new_bullet.doColorCode(4)
                        bullets.add(new_bullet)

class part6_side_enemy(DADcharacter.spirit):
    def __init__(self):
        super(part6_side_enemy,self).__init__()
        self.colorNum=4
        self.actionNum=0
        self.inFrame=50+random.randint(0,30)
        self.decFrame=20
        self.stayFrame=70
        self.incFrame=20
        self.outFrame=60
        self.initialSpeed=2.5
        self.outSpeed=5
        self.speedNow=self.initialSpeed
        self.initialAngle=90+20+random.random()*10
        self.fireInterval=60
        self.fireFrame=random.randint(0,self.fireInterval)
        self.ifFire=False
    def ai_move(self):
        self.ifFire=False
        if self.lastFrame==1:
            #self.initialAngle=90+20+random.random()*10
            self.setSpeed(self.initialAngle,self.speedNow)
        elif self.lastFrame>self.inFrame and self.lastFrame<=self.inFrame+self.decFrame:
            self.speedNow-=self.initialSpeed/self.decFrame
            self.setSpeed(self.initialAngle,self.speedNow)
        elif self.lastFrame>self.inFrame+self.decFrame and self.lastFrame<=self.inFrame+self.decFrame+self.stayFrame:
            self.ifFire=True
        elif self.lastFrame>self.inFrame+self.decFrame+self.stayFrame and self.lastFrame<=self.inFrame+self.decFrame+self.stayFrame+self.incFrame:
            self.speedNow+=self.outSpeed/self.incFrame
            px=global_var.get_value('player1x')
            py=global_var.get_value('player1y')
            self.selfTarget(px,py,self.speedNow)
        if self.rect.left>=620 or self.rect.right<=60 or self.rect.top>=690 or self.rect.bottom<=30:
            self.kill()
    
    def fire(self, frame, bullets, effects):
        if self.ifFire:
            self.fireFrame+=1
            if self.fireFrame%self.fireInterval==0:
                sendFireSound(2)
                new_bullet=part6_rice_to_laserBullet_bullet()
                new_bullet.initial(self.tx,self.ty,0)
                px=global_var.get_value('player1x')
                py=global_var.get_value('player1y')
                new_bullet.selfTarget(px,py,1.7)
                new_bullet.doColorCode(3)
                new_bullet.countAngle()
                angle=new_bullet.angle
                bullets.add(new_bullet)
                for i in (-2,-1,1,2):
                    new_bullet=part3_acc_bullet()
                    new_bullet.initial(self.tx,self.ty,0)
                    new_bullet.setSpeed(angle+i*30,1.7)
                    new_bullet.setAccSpeed(angle+i*30,1.7,5,30,90)
                    new_bullet.doColorCode(3)
                    bullets.add(new_bullet)


class part6_side_enemy_2(part6_side_enemy):
    def __init__(self):
        super(part6_side_enemy_2,self).__init__()
        self.fireInterval=30
        self.fireFrame=random.randint(0,self.fireInterval)
        self.initialAngle=90-20-random.random()*10
    def fire(self, frame, bullets, effects):
        if self.ifFire:
            self.fireFrame+=1
            if self.fireFrame%self.fireInterval==0:
                angle=random.random()*360
                sendFireSound(2)
                for i in range(12):
                    new_bullet=part3_acc_bullet()
                    new_bullet.initial(self.tx,self.ty,0)
                    new_bullet.setSpeed(angle+i*(360/12),1.7)
                    new_bullet.setAccSpeed(angle+i*(360/12),1.7,5,40,50)
                    new_bullet.doColorCode(10)
                    bullets.add(new_bullet)
    
class part7_enemy_spirit(DADcharacter.spirit):
    def __init__(self):
        super(part7_enemy_spirit,self).__init__()
        self.actionNum=0
        self.initialAngleList=[0,180,0,180]
        self.health=800
        self.fireInterval=60
        self.fireFrame=random.randint(0,self.fireInterval)
    def ai_move(self):
        if self.lastFrame==1:
            self.setSpeed(self.initialAngleList[self.actionNum],2.3)
        if self.rect.left>=620 or self.rect.right<=60 or self.rect.top>=690 or self.rect.bottom<=30:
            self.kill()
    
    def fire(self, frame, bullets, effects):
        self.fireFrame+=1
        if self.fireFrame%self.fireInterval==0:
            sendFireSound(3)
            new_bullet=Bullet.small_Bullet()
            new_bullet.initial(self.tx,self.ty,0)
            px=global_var.get_value('player1x')
            py=global_var.get_value('player1y')
            new_bullet.selfTarget(px,py,3)
            new_bullet.countAngle()
            angle=new_bullet.angle
            for i in (-1,0,1):
                new_bullet=Bullet.small_Bullet()
                new_bullet.initial(self.tx,self.ty,0)
                new_bullet.setSpeed(angle+i*2,2.4)
                new_bullet.loadColor('green')
                bullets.add(new_bullet)
#  boss zone

class sanaeMidpath(DADcharacter.Boss):
    def __init__(self):
        super(sanaeMidpath,self).__init__()

        #effect zone
        self.image=global_var.get_value('sanaeSpriteMap')
        self.lightEffect=global_var.get_value('orinLightEffect')
        self.reset=True
        self.idlePart=0
        self.idleFrame=0
        #self.movingFrame=0#  comtaminated
        self.motionFrame=0
        self.movingPart=0
        self.attackingFrame=0
        self.attackingPart=0
        self.decendingFrameMove=0
        self.decendingFrameAttack=0
        self.idleInterval=6
        self.movingInterval=5
        self.attackingInterval=6
        self.attackAnimeSign=False # adjustable 
        self.lightEffectRotationAngle=0
        self.lightEffectRotationPerFrame=3
        self.movingLeft=False
        self.displayAdj=0
        self.alreadyMoved=False
        self.attackLightEffectSign=False # adjustable, only considerable when attackAnimeSign is True
        self.existDrawFrame=0
        self.midPathStayFrame=0
        #spell zone
        self.maxSpell=4
        self.bulletAdj=(-18,-65)
        self.randomAngle=0
    def draw(self,screen):
        self.existDrawFrame+=1
        amplify=4
        self.displayAdj=amplify*math.sin(self.existDrawFrame*4/180*math.pi)
        dpy=self.ty+self.displayAdj
        #print(self.speedx)
        if abs(self.speedx)>=0.1 or abs(self.speedy)>=0.1:
            self.alreadyMoved=True
            self.motionFrame+=1
            self.attackingFrame=0
            self.attackingPart=0
            self.decendingFrameMove=0
            self.decendingFrameAttack=0
            if self.motionFrame>=self.movingInterval:
                self.movingPart+=1
                self.motionFrame=0
            if self.movingPart>3:
                self.movingPart=3
            if self.speedx<0:
                temp=pygame.transform.flip(self.image[1][self.movingPart],True,False)
                self.movingLeft=True
            else:
                temp=self.image[1][self.movingPart]
                self.movingLeft=False
            pos=(round(self.tx-48),round(dpy-48))
            screen.blit(temp,pos)
        elif self.attackAnimeSign and not self.alreadyMoved:
            self.attackingFrame+=1
            self.decendingFrameMove=0
            self.decendingFrameAttack=0
            if self.attackingFrame>=self.attackingInterval:
                self.attackingPart+=1
                self.attackingFrame=0
            if self.attackingPart>2:
                self.attackingPart=2
            pos=(round(self.tx-48),round(dpy-72))
            screen.blit(self.image[2][self.attackingPart],pos)

            if self.attackLightEffectSign and self.attackingPart==2:
                self.lightEffectRotationAngle+=self.lightEffectRotationPerFrame
                if self.lightEffectRotationAngle>=360:
                    self.lightEffectRotationAngle=self.lightEffectRotationAngle%360
                antiAngle=360-self.lightEffectRotationAngle
                pygame.draw.circle(screen,(120,120,200),(round(self.tx-18),round(self.ty-65)),22,4)
                gF.drawRotation(self.lightEffect,(round(self.tx-18-32),round(self.ty-65-32)),self.lightEffectRotationAngle,screen)
                gF.drawRotation(self.lightEffect,(round(self.tx-18-32),round(self.ty-65-32)),antiAngle,screen)
                
        else:
            #print(self.movingPart)
            if self.movingPart>0:
                self.decendingFrameMove+=1
                if self.decendingFrameMove>=self.movingInterval:
                    self.movingPart-=1
                    self.decendingFrameMove=0
                if self.movingPart==0:
                    self.alreadyMoved=False
                if self.movingLeft:
                    temp=pygame.transform.flip(self.image[1][self.movingPart],True,False)
                else:
                    temp=self.image[1][self.movingPart]

                pos=(round(self.tx-48),round(dpy-48))
                screen.blit(temp,pos)
            elif self.attackingPart>0:
                self.decendingFrameAttack+=1
                if self.decendingFrameAttack>=self.attackingInterval:
                    self.attackingPart-=1
                    self.decendingFrameAttack=0
                pos=(round(self.tx-48),round(dpy-72))
                screen.blit(self.image[2][self.attackingPart],pos)
            else:
                #print('is idle')
                self.idleFrame+=1
                if self.idleFrame>=self.idleInterval:
                    self.idlePart+=1
                    self.idleFrame=0
                if self.idlePart>3:
                    self.idlePart=0
                pos=(round(self.tx-48),round(dpy-48))
                #print(pos)
                screen.blit(self.image[0][self.idlePart],pos)
            
    def attack(self, frame, items, effects, bullets, backgrounds, enemys, slaves, player):
        if self.cardNum==0: 
            self.noneSpell_0(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
        if self.cardNum==1:
            if not self.ifSpell:
                self.noneSpell_1(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
            else:
                self.spell_1(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
        if self.cardNum==2:
            if not self.ifSpell:
                self.noneSpell_2(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
            else:
                self.spell_2(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
        if self.cardNum==3:
            if not self.ifSpell:
                self.noneSpell_3(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
            else:
                self.spell_3(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
        if self.cardNum==4:
            self.midPathStayFrame+=1
            if self.midPathStayFrame==100:
                self.gotoPosition(340,-200,60)
            if self.midPathStayFrame==160:
                global_var.set_value('DuelClassLevel_ifMidpath',True)
                global_var.set_value('DeulClassLevel_midpathFrame',frame)
                self.kill()

    def noneSpell_0(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        self.maxHealth=20000
        self.health=20000
        self.reset=True
        self.frameLimit=1200
    
    def spell_1(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            self.maxHealth=39000
            self.health=self.maxHealth
            self.gotoPosition(340,200,30)
            self.randomAngle=random.random()*360
            self.frameLimit=3600
            self.frameLimitMax=self.frameLimit
            self.startFrame=120
            self.attackAnimeSign=True
            self.attackLightEffectSign=True
            self.angleIncPerSec=0

            # spell zone
            self.cardBonus=10000000
            self.spellName='Wind Sign[Hogsmade Hurricane]'
            self.chSpellName=u'御风「霍格莫德飓风」'
            global_var.get_value('spell_sound').play()
            player.spellBonus=True
            # send spell effect
            new_effect=Effect.sanaeFaceSpell()
            effects.add(new_effect)
            self.doSpellCardAttack(effects)

        self.cardBonus-=self.framePunishment
        speed=2*self.lastFrame/self.frameLimitMax+8
        amp=1.3*self.lastFrame/self.frameLimitMax+1
        inSpellFrame=self.lastFrame-self.startFrame
        if self.lastFrame>=self.startFrame:
            if True:
                if inSpellFrame%2==0:
                    sendFireSound(2)
                    if inSpellFrame%360<180:
                        #self.angleIncPerSec=1*math.sin(inSpellFrame*2*math.pi/180)-1.3
                        
                        boolSign=True
                    else:
                        #self.angleIncPerSec=-(1*math.sin(inSpellFrame*2*math.pi/180)-1.3)
                        #self.angleIncChange=-self.angleIncPerSec/90
                        boolSign=False
                    self.angleIncPerSec=amp*math.cos((inSpellFrame+90)*math.pi/180)
                    self.angleIncChange=-self.angleIncPerSec/100
                    for i in range(0,6):
                        new_bullet=midpath_spell1_wind_bullet()
                        new_bullet.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                        new_bullet.doColorCode(10)
                        new_bullet.setSpeed(self.randomAngle+i*(360/6),speed)
                        new_bullet.speed=speed
                        new_bullet.angleIncPerFrame=self.angleIncPerSec
                        new_bullet.angleIncChange=self.angleIncChange
                        new_bullet.judgeBool=boolSign
                        bullets.add(new_bullet)
                    self.randomAngle-=1*math.cos((inSpellFrame+90)*math.pi/180)
                if inSpellFrame%10==0:
                    if boolSign:
                        self.randomAngle+=20+2*random.random()
                    else:
                        self.randomAngle-=20+2*random.random()
            if inSpellFrame%90==0:
                angle=random.random()*360
                sendFireSound(1)
                sendKiraSound()
                for i in range(30):
                    new_bullet=Bullet.orb_Bullet()
                    new_bullet.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                    new_bullet.setSpeed(angle+i*(360/30),2.4)
                    new_bullet.loadColor('lightGreen')
                    #new_bullet.doColorCode(0)
                    bullets.add(new_bullet)

        if self.health<=0 or self.frameLimit<=0:
            self.cancalAllBullet(bullets,items,effects,True)
            self.reset=True
            self.ifSpell=True
            self.cardNum+=1
            self.health=20000
            if self.frameLimit>0:
                self.createItem(items,0,5)
                self.createItem(items,1,20)
                ifBonus=player.spellBonus
            else:
                ifBonus=False
            self.drawResult(effects,self.cardBonus,ifBonus)
            if ifBonus:
                player.score+=self.cardBonus
                global_var.get_value('bonus_sound').play()
            global_var.get_value('spell_end').play()
            self.attackLightEffectSign=False
            self.attackAnimeSign=False
    
    def spell_2(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            self.maxHealth=50000
            self.health=self.maxHealth
            self.gotoPosition(340,200,30)
            self.randomAngle=random.random()*360
            self.frameLimit=3600
            self.frameLimitMax=self.frameLimit
            self.startFrame=120
            self.attackAnimeSign=False
            self.attackLightEffectSign=False
            self.fireCount=0

            # spell zone
            self.cardBonus=10000000
            self.spellName='Sudden Rain[Thunder Storm]'
            self.chSpellName=u'骤雨「雷暴操纵术」'
            global_var.get_value('spell_sound').play()
            player.spellBonus=True
            self.bulletSenderAngle=0
            self.bulletSenderAngleInc=62
            self.senderRadius=20
            # send spell effect
            new_effect=Effect.sanaeFaceSpell()
            effects.add(new_effect)
            self.doSpellCardAttack(effects)
        
        self.cardBonus-=self.framePunishment
        inSpellFrame=self.lastFrame-self.startFrame

        if self.lastFrame>=self.startFrame:
            '''self.attackAnimeSign=True
            self.attackLightEffectSign=True'''
            xPos=340+280*math.sin(inSpellFrame*4/180*math.pi)
            if inSpellFrame%2==0:
                sendFireSound(2)
                self.bulletSenderAngle+=self.bulletSenderAngleInc+random.random()*30
                for i in range(2):
                    individualAngle=self.bulletSenderAngle+i*(360/2)
                    nx=xPos+self.senderRadius*math.cos(individualAngle*math.pi/180)
                    ny=30+self.senderRadius*math.sin(individualAngle*math.pi/180)
                    sendAngle=individualAngle-140
                    new_bullet=midpath_spell2_rain_bullet()
                    new_bullet.initial(nx,ny,0)
                    new_bullet.setSpeed(sendAngle,2)
                    new_bullet.doColorCode(6)
                    new_bullet.maxSpeed=7
                    bullets.add(new_bullet)
            '''if inSpellFrame%15==0:
                angle=88+random.random()*4
                for i in range(3):
                    new_bullet=Bullet.sharp_Bullet()
                    new_bullet.initial(xPos,30,0)
                    new_bullet.setSpeed(angle,5.5+1*i)
                    new_bullet.doColorCode(2)
                    bullets.add(new_bullet)'''
            if inSpellFrame>=140:
                if inSpellFrame%140==0:
                    new_effect=Effect.bulletCreate(6)
                    new_effect.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],92,48,30)
                    effects.add(new_effect)

                    global_var.get_value('laser_sound').stop()
                    global_var.get_value('laser_sound').play()
                    self.fireCount+=1
                    adj=(1,-1)
                    decision=self.fireCount%2
                    self.randomAngle=(random.random()*20+120)*adj[decision]+90
                    for i in range(9):
                        new_bullet=midpath_spell2_laser_bullet_main(4,30,7)
                        new_bullet.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                        new_bullet.doColorCode(13)
                        new_bullet.adj=decision
                        new_bullet.setSpeed(self.randomAngle+i*40,7)
                        bullets.add(new_bullet)
            
            if inSpellFrame%140==110:
                self.attackAnimeSign=True
                self.attackLightEffectSign=True
            if inSpellFrame%140==30:
                self.attackAnimeSign=False
                self.attackLightEffectSign=False

            if inSpellFrame%280==190:
                self.gotoPosition(player.cx+random.random()*60-30,random.random()*40+180,60)

        if self.health<=0 or self.frameLimit<=0:
            self.cancalAllBullet(bullets,items,effects,True)
            self.reset=True
            self.ifSpell=True
            self.cardNum+=1
            self.health=20000
            if self.frameLimit>0:
                self.createItem(items,0,5)
                self.createItem(items,1,20)
                ifBonus=player.spellBonus
            else:
                ifBonus=False
            self.drawResult(effects,self.cardBonus,ifBonus)
            if ifBonus:
                player.score+=self.cardBonus
                global_var.get_value('bonus_sound').play()
            global_var.get_value('spell_end').play()
            self.attackLightEffectSign=False
            self.attackAnimeSign=False


    def spell_3(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            self.maxHealth=50000
            self.health=self.maxHealth
            self.gotoPosition(340,200,30)
            self.randomAngle=random.random()*360
            self.frameLimit=3600
            self.frameLimitMax=self.frameLimit
            self.startFrame=120
            self.warnFrame=0
            self.attackAnimeSign=False
            self.attackLightEffectSign=False
            global_var.set_value('midPathSpell3Signal',False)
            
            # spell zone
            self.cardBonus=10000000
            self.spellName='Blizzard[Icy Snow]'
            self.chSpellName=u'暴雪「凝冰之雪」'
            global_var.get_value('spell_sound').play()
            player.spellBonus=True
            self.snow_interval=2

            # send spell effect
            new_effect=Effect.sanaeFaceSpell()
            effects.add(new_effect)
            self.doSpellCardAttack(effects)
        
        self.cardBonus-=self.framePunishment
        inSpellFrame=self.lastFrame-self.startFrame


        
        hailAndSnow_ratio=7
        freeze_interval=360
        if self.lastFrame>=self.startFrame:
            sendKiraSound()
            if inSpellFrame%self.snow_interval==0:
                hailSign=random.randint(0,hailAndSnow_ratio)
                pos=(random.random()*560+60,25)
                angle=random.random()*8+86
                speed=3.5+random.random()
                if hailSign==0:
                    new_bullet=midpath_spell3_mid_snow_bullet()
                    new_bullet.initial(pos[0],pos[1],0)
                    new_bullet.setSpeed(angle,speed-1)
                    new_bullet.loadColor('white')
                    bullets.add(new_bullet)
                else:
                    new_bullet=midpath_spell3_small_snow_bullet()
                    new_bullet.initialSpeed=speed
                    new_bullet.initial(pos[0],pos[1],0)
                    new_bullet.setSpeed(angle,speed)
                    new_bullet.loadColor('white')
                    bullets.add(new_bullet)
            if inSpellFrame%freeze_interval==0 and inSpellFrame!=0:
                global_var.set_value('midPathSpell3Signal',True)
                global_var.get_value('spell_end').stop()
                global_var.get_value('spell_end').play()
                new_effect=Effect.wave()
                new_effect.initial((self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1]),900,20,(255,255,255),8)
                effects.add(new_effect)

            if inSpellFrame%freeze_interval==1:
                global_var.set_value('midPathSpell3Signal',False)
                global_var.set_value('midPathSpell3Warn',False)
                self.warnFrame=0
                global_var.set_value('midPathSpell3WarnFrame',self.warnFrame)

            if inSpellFrame%freeze_interval==freeze_interval-100:
                global_var.get_value('ch00_sound').stop()
                global_var.get_value('ch00_sound').play()
                global_var.set_value('midPathSpell3Warn',True)
                new_effect=Effect.powerUp()
                new_effect.initial((self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1]),300,100,(30,224,255),20,1,0)
                effects.add(new_effect)
                self.attackAnimeSign=True
                self.attackLightEffectSign=True
            
            if inSpellFrame%freeze_interval>=freeze_interval-100:
                self.warnFrame+=1
                global_var.set_value('midPathSpell3WarnFrame',self.warnFrame)
                
        
            if inSpellFrame%freeze_interval==50:
                self.attackAnimeSign=False
                self.attackLightEffectSign=False

            if inSpellFrame%freeze_interval<=100 and inSpellFrame>100:
                self.snow_interval=5
            else:
                self.snow_interval=2
            if inSpellFrame%360==160:
                self.gotoPosition(player.cx+random.random()*60-30,random.random()*40+180,60)

        if self.health<=0 or self.frameLimit<=0:
            self.cancalAllBullet(bullets,items,effects,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            if self.frameLimit>0:
                self.createItem(items,0,5)
                self.createItem(items,1,20)
                ifBonus=player.spellBonus
            else:
                ifBonus=False
            self.drawResult(effects,self.cardBonus,ifBonus)
            if ifBonus:
                player.score+=self.cardBonus
                global_var.get_value('bonus_sound').play()
            global_var.get_value('spell_end').play()
            self.attackLightEffectSign=False
            self.attackAnimeSign=False
            self.frameLimit=20*60

def stageController(screen,frame,enemys,bullets,slaves,items,effects,backgrounds,bosses,player):

    if frame==1:# load in section, initialize background, and music
        pygame.mixer.music.stop()
        pygame.mixer.music.load('resource/bgm/yujiMidpath.mp3')   # 载入背景音乐文件
        #pygame.mixer.music.load('resource/bgm/上海アリス幻樂団 - 死体旅行~ Be of good cheer!.mp3')
        pygame.mixer.music.set_volume(0.7)                  # 设定背景音乐音量
        pygame.mixer.music.play(loops=-1)
        global_var.set_value('DuelClassLevel_ifMidpath',False)
        global_var.set_value('DeulClassLevel_midpathFrame',0)

    ifMidpath=global_var.get_value('DuelClassLevel_ifMidpath')
    midPathFrame=global_var.get_value('DeulClassLevel_midpathFrame')
    if ifMidpath:
        if frame<=8200:
            frameAfterMidpath=0
        else:
            if midPathFrame>=8200:
                frameAfterMidpath=frame-midPathFrame
            else:
                frameAfterMidpath=frame-8200

    if frame==100:
        seperate=40
        new_enemy=part1_enemy()
        new_enemy.initialize(340-seperate,0,0,-1)
        new_enemy.colorNum=4
        new_enemy.actionNum=0
        enemys.add(new_enemy)
        new_enemy=part1_enemy()
        new_enemy.initialize(340+seperate,0,0,-1)
        new_enemy.colorNum=4
        new_enemy.actionNum=0
        enemys.add(new_enemy)
    
    if frame==130:
        seperate=80
        new_enemy=part1_enemy()
        new_enemy.initialize(340,0,0,-1)
        new_enemy.colorNum=5
        new_enemy.actionNum=0
        new_enemy.speed=1.8
        new_enemy.staySec=2
        enemys.add(new_enemy)
        new_enemy=part1_enemy()
        new_enemy.initialize(340-seperate,0,0,-1)
        new_enemy.colorNum=5
        new_enemy.actionNum=1
        new_enemy.speed=1.8
        new_enemy.staySec=2
        enemys.add(new_enemy)
        new_enemy=part1_enemy()
        new_enemy.initialize(340+seperate,0,0,-1)
        new_enemy.colorNum=5
        new_enemy.actionNum=2
        new_enemy.speed=1.8
        new_enemy.staySec=2
        enemys.add(new_enemy)
    
    if frame==160:
        seperate=80
        actionList=(1,0,0,2)
        adjList=(-seperate*1.5,-seperate*0.5,seperate*0.5,seperate*1.5)
        for i in range(4):
            new_enemy=part1_enemy()
            new_enemy.initialize(340+adjList[i],0,0,-1)
            new_enemy.colorNum=6
            new_enemy.actionNum=actionList[i]
            new_enemy.speed=1.2
            new_enemy.staySec=1.5
            enemys.add(new_enemy)
        
        actionList=(1,1,0,2,2)
        adjList=(-seperate*2,-seperate*1,0,seperate*1,seperate*2)
        for i in range(5):
            new_enemy=part1_enemy()
            new_enemy.initialize(340+adjList[i],0,0,-1)
            new_enemy.colorNum=3
            new_enemy.actionNum=actionList[i]
            new_enemy.speed=0.6
            new_enemy.staySec=1.5
            enemys.add(new_enemy)
    
    if frame>=680 and frame<=1080:
        if frame%30==0:
            new_enemy=part2_enemy()
            new_enemy.initialize(random.random()*500+90,20,0,-1)
            new_enemy.colorNum=1
            new_enemy.speed=2
            enemys.add(new_enemy)
    
    if frame==1380:
        new_enemy=part3_enemy_main()
        new_enemy.initialize(50,200,0,-1)
        new_enemy.actionNum=0
        enemys.add(new_enemy)
    
    if frame>=1380 and frame<=1580:
        if frame%25==0:
            new_enemy=part3_enemy_spirite()
            new_enemy.initialize(random.random()*200+360,700,0,-1)
            new_enemy.actionNum=0
            new_enemy.colorNum=2
            enemys.add(new_enemy)
    
    if frame==2080:
        new_enemy=part3_enemy_main()
        new_enemy.initialize(630,200,0,-1)
        new_enemy.actionNum=1
        enemys.add(new_enemy)
    
    if frame>=2080 and frame<=2280:
        if frame%25==0:
            new_enemy=part3_enemy_spirite()
            new_enemy.initialize(320-random.random()*200,700,0,-1)
            new_enemy.actionNum=1
            new_enemy.colorNum=4
            enemys.add(new_enemy)
    
    if frame>=2700 and frame<=3300:
        if (frame-2800)%25==0:
            for i in range(2):
                new_enemy=part4_enemy_kedama()
                new_enemy.initialize(50,100+140*i,0,-1)
                new_enemy.actionNum=0
                new_enemy.colorNum=0
                enemys.add(new_enemy)
            
            new_enemy=part4_enemy_kedama()
            new_enemy.initialize(630,170,0,-1)
            new_enemy.actionNum=1
            new_enemy.colorNum=0
            enemys.add(new_enemy)

    if frame==3500:
        new_boss=sanaeMidpath()
        #new_boss=DADcharacter.Boss()
        new_boss.initial(340,-200)
        bosses.add(new_boss)
    
    if frame==3590:
        for boss in bosses:
            boss.gotoPosition(340,200,90)
    
    if frame==3700:
        for boss in bosses:
            boss.cardNum=1
            boss.ifSpell=True
    
    if ifMidpath and frame>=3700:

        if frame<=8200:
            if frame%50==0:
                new_enemy=support_enemy_yinyangyu()
                ex=random.random()*560+60
                new_enemy.initialize(ex,20,0,-1)
                new_enemy.selfTarget(player.cx,player.cy,2.8)
                #new_enemy.actionNum=1
                enemys.add(new_enemy)
    
    if ifMidpath and frame>=8200:
        if frameAfterMidpath>=200 and frameAfterMidpath<=400:
            if frameAfterMidpath%30==0:
                new_enemy=part5_enemy_kedama()
                new_enemy.initialize(340+160,20,0,-1)
                new_enemy.actionNum=0
                new_enemy.colorNum=0
                enemys.add(new_enemy)
        
        
                new_enemy=part5_enemy_kedama()
                new_enemy.initialize(340-160,20,0,-1)
                new_enemy.actionNum=1
                new_enemy.colorNum=0
                enemys.add(new_enemy)
        
        if frameAfterMidpath>=500 and frameAfterMidpath<=700:
            if frameAfterMidpath%30==0:
                new_enemy=part5_enemy_kedama()
                new_enemy.initialize(340+160,700,0,-1)
                new_enemy.actionNum=2
                new_enemy.colorNum=1
                enemys.add(new_enemy)
        
        
                new_enemy=part5_enemy_kedama()
                new_enemy.initialize(340-160,700,0,-1)
                new_enemy.actionNum=3
                new_enemy.colorNum=0
                enemys.add(new_enemy)
        
        if frameAfterMidpath==850:
            new_enemy=part6_winged_butterfly()
            new_enemy.actionNum=0
            new_enemy.initialize(340-170,20,0,-1)
            enemys.add(new_enemy)
        
        if frameAfterMidpath>=800 and frameAfterMidpath<=1000:
            if frameAfterMidpath%20==0:
                ex=340+140+50*random.random()
                ey=20
                new_enemy=part6_side_enemy()
                new_enemy.initialize(ex,ey,0,-1)
                enemys.add(new_enemy)
        
        if frameAfterMidpath==1300:
            new_enemy=part6_winged_butterfly()
            new_enemy.actionNum=1
            new_enemy.initialize(340+170,20,0,-1)
            enemys.add(new_enemy)

        if frameAfterMidpath>=1250 and frameAfterMidpath<=1450:
            if frameAfterMidpath%20==0:
                ex=340-140-50*random.random()
                ey=20
                new_enemy=part6_side_enemy_2()
                new_enemy.initialize(ex,ey,0,-1)
                enemys.add(new_enemy)
        
        if frameAfterMidpath>=1800 and frameAfterMidpath<=2100:
            if frameAfterMidpath%30==0:
                exList=[50,630,50,630]
                eyList=[100,190,280,370]
                for i in range(0,4):
                    new_enemy=part7_enemy_spirit()
                    new_enemy.initialize(exList[i],eyList[i],0,-1)
                    new_enemy.actionNum=i
                    new_enemy.colorNum=i+2
                    enemys.add(new_enemy)
