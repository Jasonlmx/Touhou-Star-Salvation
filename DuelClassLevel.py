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
import danmaku

def backgroundFade(backgrounds):
    for item in backgrounds:
        item.fadeSign=True

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

class sanae_noneSpell_1_orb_bullet(part2_acc_bullet):
    def __init__(self):
        super(sanae_noneSpell_1_orb_bullet,self).__init__()
        self.stdAngle=0
        self.stdSpeed=0
        self.sideNum=3
        self.color='green'
        self.length=12
    def update(self, screen, bullets, effects):
        self.lastFrame+=1
        self.movement()
        self.motionStrate()
        self.split(bullets)
        if self.lastFrame<=self.createMax and self.ifDrawCreate:
            self.drawCreateImg(screen)
        else:
            self.drawBullet(screen)
        self.checkValid()
    
    def split(self,bullets):
        if self.lastFrame==self.accFrame+self.accStart:
            sendKiraSound()
            danmaku.polyByLength(bullets,Bullet.orb_Bullet,self.length,self.sideNum,self.stdSpeed,self.stdAngle,(self.tx,self.ty),self.color,False)
            self.kill()

class sanae_spell_1_rice_bullet(Bullet.rice_Bullet):
    def __init__(self):
        super(sanae_spell_1_rice_bullet,self).__init__()
        self.actionNum=0
        self.splitNumber=1
        self.splitAngle=random.random()*360
        self.sideCode=0
        self.fireAngle=0
        self.bulletColorDict=(4,7,9,13,15)
    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.split(bullets)
        if self.lastFrame<=self.createMax and self.ifDrawCreate:
            self.drawCreateImg(screen)
        else:
            self.drawBullet(screen)
        self.checkValid()
    
    def split(self,bullets):
        if self.tx>=560+60 or self.tx<=60 or self.ty<=30:
            if self.tx>=560+60:
                self.sideCode=0
                self.fireAngle=random.random()*180+90
            elif self.tx<=60:
                self.sideCode=1
                self.fireAngle=random.random()*180-90
            elif self.ty<=30:
                self.sideCode=2
                self.fireAngle=random.random()*180


            sendKiraSound()
            for i in range(self.splitNumber):
                new_bullet=sanae_spell_1_gravity_bullet()
                new_bullet.gravePerSec=0.05
                new_bullet.initial(self.tx,self.ty,0)
                new_bullet.setSpeed(self.fireAngle,1)
                new_bullet.maxSpeed=3.7
                #new_bullet.setAccSpeed(self.splitAngle+i*(360/self.splitNumber),2,4,80,60)
                new_bullet.doColorCode(self.bulletColorDict[self.actionNum])
                bullets.add(new_bullet)
                self.kill()

class sanae_spell_1_gravity_bullet(part4_gravity_bullet):
    def __init__(self):
        super(sanae_spell_1_gravity_bullet,self).__init__()          
        self.validAccuracy=(10,10,10,10)

class sanae_spell_2_lightning_bullet(Bullet.satsu_Bullet):
    def __init__(self):
        super(sanae_spell_2_lightning_bullet,self).__init__()
        self.speedMax=7.2
        self.changeFrame=3
        self.movingFrame=10
        self.stayFrame=3
        self.speedNow=self.speedMax+0.1
        self.angleNow=0
        self.stdAngle=40
        self.turnCount=0
        self.ifAddHitPoint=False
    def update(self, screen, bullets, effects):
        self.lastFrame+=1
        self.movement()
        self.motionStrate()
        self.addHitPoint(bullets)
        if self.lastFrame<=self.createMax and self.ifDrawCreate:
            self.drawCreateImg(screen)
        else:
            self.drawBullet(screen)
        self.checkValid()
        #screen.blit(self.surf,self.rect)

    def addHitPoint(self,bullets):
        judgeFrame=(self.lastFrame+self.changeFrame)%(self.changeFrame*2+self.movingFrame+self.stayFrame)
        if judgeFrame<=self.changeFrame+self.movingFrame and judgeFrame>self.changeFrame and self.ifAddHitPoint:
            if self.distance<=40:
                angleDict=[0,180,180,180]
                radius=[0,self.speedMax*2,self.speedMax*4,self.speedMax*6]
                for i in range(4):
                    new_bullet=Bullet.laser_line_sub()
                    angle=self.angleNow+angleDict[i]
                    nx=self.tx+radius[i]*math.cos(angle/180*math.pi)
                    ny=self.ty+radius[i]*math.sin(angle/180*math.pi)
                    new_bullet.initial(nx,ny,0)
                    bullets.add(new_bullet)
    def motionStrate(self):
        judgeFrame=(self.lastFrame+self.changeFrame)%(self.changeFrame*2+self.movingFrame+self.stayFrame)
        if judgeFrame<=self.changeFrame:
            self.speedNow+=self.speedMax/self.changeFrame
            self.setSpeed(self.angleNow,self.speedNow)
        elif judgeFrame<=self.changeFrame+self.movingFrame:
            pass
        elif judgeFrame<=self.changeFrame*2+self.movingFrame:
            self.speedNow-=self.speedMax/self.changeFrame
            self.setSpeed(self.angleNow,self.speedNow)
        else:
            if judgeFrame==self.changeFrame*2+self.movingFrame+self.stayFrame-1:
                self.turnCount+=1
                if self.turnCount%2==0:
                    self.angleNow-=self.stdAngle*2
                else:
                    self.angleNow+=self.stdAngle*2
                self.setSpeed(self.angleNow,self.speedNow)

class sanae_spell_3_leaf_bullet(Bullet.scale_Bullet):
    def __init__(self):
        super(sanae_spell_3_leaf_bullet,self).__init__()
        self.ifTp=False
        self.ifBounce=False
        self.validAccuracy=(5,5,5,5)
        self.signal=0
    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.getSignal()
        self.movement()
        self.motionStrate()
        
        if self.lastFrame<=self.createMax and self.ifDrawCreate:
            self.drawCreateImg(screen)
        else:
            self.drawBullet(screen)
        self.checkValid()
    
    def getSignal(self):
        self.signal=global_var.get_value('endStageSpell3Signal')
    
    def motionStrate(self):
        if not self.ifTp and self.signal==1:
            if self.tx<=60:
                self.tx=620
                self.ifTp=True
                #print('a')
            elif self.tx>=620:
                self.tx=60
                self.ifTp=True
                #print('b')
        
        if not self.ifBounce and self.signal==2:
            if self.tx<=60 or self.tx>=620:
                self.speedx=-self.speedx
                self.ifBounce=True

class sanae_noneSpell_4_bounce_rice_bullet(Bullet.sharp_Bullet):
    def __init__(self):
        super(sanae_noneSpell_4_bounce_rice_bullet,self).__init__()
        self.maxBounce=2
        self.validAccuracy=(10,10,10,10)
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
        if self.maxBounce>0:
            if self.tx<=60:
                self.speedx=-self.speedx
                self.tx=60+abs(60-self.tx)
                self.maxBounce-=2
            elif self.tx>=620:
                self.speedx=-self.speedx
                self.tx=620-abs(620-self.tx)
                self.maxBounce-=2
            elif self.ty<=30:
                self.maxBounce-=1
                self.speedy=-self.speedy
                self.ty=30+abs(30-self.ty)

class sanae_noneSpell_4_bounce_scale_bullet(Bullet.mid_Bullet):
    def __init__(self):
        super(sanae_noneSpell_4_bounce_scale_bullet,self).__init__()
        self.maxBounce=2
        self.validAccuracy=(10,10,10,10)
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
        if self.maxBounce>0:
            if self.tx<=60:
                self.speedx=-self.speedx
                self.tx=60+abs(60-self.tx)
                self.maxBounce-=2
            elif self.tx>=620:
                self.speedx=-self.speedx
                self.tx=620-abs(620-self.tx)
                self.maxBounce-=2
            elif self.ty<=30:
                self.maxBounce-=1
                self.speedy=-self.speedy
                self.ty=30+abs(30-self.ty)

class sanae_spell_4_changeDirect_orb_bullet(Bullet.orb_Bullet):
    def __init__(self):
        super(sanae_spell_4_changeDirect_orb_bullet,self).__init__()
        self.changeAt=7
        self.maxFrame=160
        self.changeAngle=60
        self.angle=0
        self.speed=4

    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.movement()
        self.motionStrate()
        if self.lastFrame<=self.createMax and self.ifDrawCreate:
            self.drawCreateImg(screen)
        else:
            if self.rect.top<=690 and self.rect.bottom>=30 and self.rect.left<=620 and self.rect.right>=60:
                self.drawBullet(screen)
        self.checkValid()

    def motionStrate(self):
        if self.lastFrame==self.changeAt:
            self.setSpeed(self.angle+self.changeAngle,self.speed)

    '''def checkValid(self):
        if self.lastFrame>=self.maxFrame:
            self.kill()'''

class sanae_spell_5_ringed_orb_bullet(Bullet.orb_Bullet):
    def __init__(self):
        super(sanae_spell_5_ringed_orb_bullet,self).__init__()
        self.maxFrame=600
        self.actionNum=0
        self.centerTx=0
        self.centerTy=0
        self.centerSpeedx=0
        self.centerSpeedy=0

        self.angleNow=0
        self.radius=100
        self.angleSpeed=0.7
        self.rSpeed=0.3
        self.ifDrawCircle=False
        self.maxRadius=210
        self.cancalable=False

        self.fireInterval=2
    
    def initial(self, posx, posy, occupy):
        self.centerTx=posx
        self.centerTy=posy
    
    def setSpeed(self, angle, speed):
        s=math.sin(math.radians(angle))
        c=math.cos(math.radians(angle))
        self.centerSpeedy=s*speed
        self.centerSpeedx=c*speed
    
    def selfTarget(self,playercx,playercy,speed):
        mycx=self.centerTx
        mycy=self.centerTy
        dif=math.sqrt(math.pow(playercx-mycx,2)+math.pow(playercy-mycy,2))
        times=dif/speed
        speedx=(playercx-mycx)/times
        speedy=(playercy-mycy)/times
        self.centerSpeedx=speedx
        self.centerSpeedy=speedy
        #self.speedAlter(speedx,speedy)
    
    def centerMovement(self):
        self.centerTx+=self.centerSpeedx
        self.centerTy+=self.centerSpeedy

    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.centerMovement()
        self.motionStrate()
        self.movement()
        self.drawCircle(screen)
        if self.rect.top<=690 and self.rect.bottom>=30 and self.rect.left<=620 and self.rect.right>=60:
            self.fire(effects)
        if self.lastFrame<=self.createMax and self.ifDrawCreate:
            self.drawCreateImg(screen)
        else:
            if self.rect.top<=690 and self.rect.bottom>=30 and self.rect.left<=620 and self.rect.right>=60:
                self.drawBullet(screen)
        self.checkValid()
    
    def checkValid(self):
        if self.lastFrame>=self.maxFrame:
            self.kill()

    def fire(self,effects):
        if self.lastFrame%self.fireInterval==0:
            new_effect=Effect.sanae_spell5_flame()
            new_effect.initial(self.tx,self.ty)
            new_effect.actionNum=self.actionNum
            effects.add(new_effect)
            '''new_bullet=sanae_spell_5_ringed_orb_sub()
            new_bullet.initial(self.tx,self.ty,0)
            new_bullet.setSpeed(0,0)
            new_bullet.loadColor('red')
            bullets.add(new_bullet)'''

    def motionStrate(self):
        angle=self.angleNow
        sx=self.radius*math.cos(angle/180*math.pi)
        sy=self.radius*math.sin(angle/180*math.pi)
        self.tx=self.centerTx+sx
        self.ty=self.centerTy+sy
        self.angleNow+=self.angleSpeed
        if self.maxRadius>abs(self.radius):
            self.radius+=self.rSpeed
    
    def drawCircle(self,screen):
        if self.ifDrawCircle:
            pygame.draw.circle(screen,(255,255,255),(round(self.centerTx),round(self.centerTy)),round(abs(self.radius)),1)

class sanae_spell_5_ringed_orb_sub(Bullet.orb_Bullet):
    def __init__(self):
        super(sanae_spell_5_ringed_orb_sub,self).__init__()
        self.maxFrame=10
        self.ifDrawCreate=False

        self.size=24
        self.surfSize=12
        self.tempImg=0
    def update(self,screen,bullets,effects):
        self.lastFrame+=1
        self.changeSize()
        self.movement()
        
        if self.lastFrame<=self.createMax and self.ifDrawCreate:
            self.drawCreateImg(screen)
        else:
            if self.rect.top<=690 and self.rect.bottom>=30 and self.rect.left<=620 and self.rect.right>=60:
                self.drawBullet(screen)
        self.checkValid()
    
    def drawBullet(self,screen):
        
        screen.blit(self.tempImg,(round(self.tx-self.size/2),round(self.ty-self.size/2)))
        #screen.blit(self.surf,self.rect)

    def changeSize(self):
        self.size-=24/self.maxFrame
        self.surfSize-=12/self.maxFrame

        self.surf = pygame.Surface((round(self.surfSize),round(self.surfSize)))
        self.rect = self.surf.get_rect()
        self.surf.fill((255,0,0))
        self.tempImg=pygame.Surface((24,24)).convert_alpha()
        self.tempImg.fill((0,0,0,0))
        self.tempImg.blit(self.image,(0,0))
        self.tempImg=pygame.transform.smoothscale(self.tempImg,(round(self.size),round(self.size)))


    def checkValid(self):
        if self.lastFrame>=self.maxFrame:
            self.kill()

class sanae_spell_6_big_star_bullet(Bullet.big_star_bullet_stay_acc):
    def __init__(self):
        super(sanae_spell_6_big_star_bullet,self).__init__()
        self.actionNum=0
        self.fireInterval=[20,20,20]
        self.fireMultiple=12
        self.side=5
        self.eColorCode=random.randint(0,15)
    def update(self, screen, bullets, effects):
        self.lastFrame+=1
        self.movement()
        self.motionStrate()
        self.fire(bullets)
        if self.lastFrame<=self.createMax and self.ifDrawCreate:
            self.drawCreateImg(screen)
        else:
            self.drawBullet(screen)
        self.checkValid()

    def fire(self,bullets):
        if self.lastFrame%self.fireInterval[self.actionNum]==0:
            rndA=random.random()*360
            sendFireSound(2)
            if self.actionNum==0:
                for i in range(self.fireMultiple):
                    new_bullet=Bullet.star_bullet_stay_acc()
                    new_bullet.initial(self.tx,self.ty,0)
                    new_bullet.setSpeed(rndA+i*360/self.fireMultiple,0.9)
                    new_bullet.setAccSpeed(rndA+i*360/self.fireMultiple,0.9,4,20,60)
                    new_bullet.doColorCode(self.colorNum)
                    bullets.add(new_bullet)
            elif self.actionNum==1:
                danmaku.polyByLength(bullets,Bullet.star_Bullet,6,self.side,3,rndA,(self.tx,self.ty),self.colorNum,True)
                self.side-=1
                if self.side<3:
                    self.side=3
            elif self.actionNum==2:
                '''for i in (-1,1):
                    for j in range(2):
                        speed=[2.2,4]
                        new_bullet=Bullet.orb_Bullet()
                        new_bullet.initial(self.tx,self.ty,0)
                        self.countAngle()
                        new_bullet.setSpeed(self.angle+90*i+random.random()*10-10,speed[j]+random.random()*1)
                        new_bullet.loadColor('red')
                        bullets.add(new_bullet)'''
                self.countAngle()
                danmaku.ellipseByDeg(bullets,Bullet.star_Bullet,16,40,25,-self.angle-90,2,(self.tx,self.ty),self.eColorCode,True)


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
        self.health=300
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
                angle=360*random.random()
                for i in range(30):
                    for j in range(4):
                        new_bullet=Bullet.satsu_Bullet()
                        new_bullet.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                        new_bullet.setSpeed(angle+i*(360/30),13-1.7*j)
                        new_bullet.loadColor('white')
                        bullets.add(new_bullet)

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
            self.addLastingCancel(self.tx,self.ty,slaves,15,True,cancelType=1)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            if self.frameLimit>0:
                self.createItem(items,0,10)
                self.createItem(items,1,20)
                self.createItem(items,6,1)
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

class SanaeStageFinal(sanaeMidpath):
    def __init__(self):
            super(SanaeStageFinal,self).__init__()
            self.maxSpell=9
            self.boomImmune=True
            self.deadFrame=0
    
    def attack(self, frame, items, effects, bullets, backgrounds, enemys, slaves, player):
        if self.cardNum>0:
            if self.ifSpell and self.lastFrame==1:
                for background in backgrounds:
                    background.fadeSign=True
                gF.doSpellBackground(None,backgrounds)
            elif self.ifSpell==False and self.lastFrame==1:
                for background in backgrounds:
                    background.fadeSign=True
                gF.doBackground2(None,backgrounds)
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
            if not self.ifSpell:
                self.noneSpell_4(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
            else:
                self.spell_4(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
        if self.cardNum==5:
            if not self.ifSpell:
                self.noneSpell_5(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
            else:
                self.spell_5(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
        if self.cardNum==6:
            if not self.ifSpell:
                self.noneSpell_6(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
            else:
                self.spell_6(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
        if self.cardNum==7:
            if not self.ifSpell:
                self.noneSpell_7(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
            else:
                self.spell_7(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
        if self.cardNum==8:
            self.deadFrame+=1
            if self.deadFrame==1:
                global_var.get_value('spell_end').play()
                self.doShaking(200)
                self.gotoPosition(self.tx+random.random()*100-50,self.ty+random.random()*100-50,119)
            if self.deadFrame>=120:
                global_var.get_value('bossDead_sound').play()
                Effect.bossBruster(self.tx,self.ty,effects,Effect.bossBrustMomiji,50)
                #global_var.set_value('levelPassSign',True)
                new_effect=Effect.levelEndTimer()
                effects.add(new_effect)
                self.kill()


        '''if self.cardNum==8:
            if not self.ifSpell:
                self.noneSpell_8(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
            else:
                self.spell_8(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
        if self.cardNum==9:
            if not self.ifSpell:
                self.noneSpell_9(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
            else:
                self.spell_9(frame,items,effects,bullets,backgrounds,enemys,slaves,player)'''
    

    def noneSpell_0(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        self.maxHealth=20000
        self.health=20000
        self.reset=True
        self.frameLimit=1200
    
    def noneSpell_1(self, frame, items, effects, bullets, backgrounds, enemys, slaves, player):
        if self.reset: #start reset, individualized
            self.lastFrame=0
            self.reset=False
            self.maxHealth=30000
            self.health=self.maxHealth
            self.gotoPosition(340-self.bulletAdj[0],200-self.bulletAdj[1],40)
            self.randomAngle=random.random()*360
            self.frameLimit=3600
            self.frameLimitMax=self.frameLimit
            self.startFrame=120
            self.attackAnimeSign=True
            self.attackLightEffectSign=True

            #spell zone
            self.fireInterval=120

        inSpellFrame=self.lastFrame-self.startFrame

        if self.lastFrame>=self.startFrame:
            if inSpellFrame%self.fireInterval==0:
                new_bullet=Bullet.small_Bullet()
                new_bullet.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                new_bullet.selfTarget(player.cx,player.cy,2)
                new_bullet.countAngle()
                self.fireAngle=new_bullet.angle
                stdSpeed_main=4+random.random()*2
                self.stdSpeed_sub=random.random()+1.5
                for i in range(3):
                    sendFireSound(1)
                    new_bullet=sanae_noneSpell_1_orb_bullet()
                    new_bullet.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                    new_bullet.cancalable=False
                    new_bullet.setSpeed(self.fireAngle+i*(360/3),stdSpeed_main)
                    new_bullet.setAccSpeed(self.fireAngle+i*(360/3),stdSpeed_main,0,10,20)
                    new_bullet.loadColor('lightGreen')
                    new_bullet.stdSpeed=self.stdSpeed_sub
                    new_bullet.stdAngle=self.fireAngle
                    bullets.add(new_bullet)
            
            if inSpellFrame%self.fireInterval==60:
                sendFireSound(1)
                danmaku.polyByLength(bullets,Bullet.satsu_Bullet,8,3,self.stdSpeed_sub/10*9,self.fireAngle,(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1]),'green')
                danmaku.polyByLength(bullets,Bullet.satsu_Bullet,8,3,self.stdSpeed_sub/10*9,self.fireAngle-180,(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1]),'green')
                #angle=random.random()*360
                '''for i in range(20):
                    sendFireSound(1)
                    new_bullet=Bullet.orb_Bullet()
                    new_bullet.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                    new_bullet.setSpeed(angle+i*(360/20),4)
                    new_bullet.loadColor('lightGreen')
                    bullets.add(new_bullet)'''

        
        if self.health<=0 or self.frameLimit<=0: #end check, non_spell
            self.cancalAllBullet(bullets,items,effects,True)
            self.reset=True
            self.ifSpell=True
            self.health=20000
            self.attackLightEffectSign=False
            self.attackAnimeSign=False

    def spell_1(self, frame, items, effects, bullets, backgrounds, enemys, slaves, player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            self.maxHealth=45000
            self.health=self.maxHealth
            self.gotoPosition(340-self.bulletAdj[0],220-self.bulletAdj[1],30)
            self.randomAngle=random.random()*360
            self.frameLimit=7200
            self.frameLimitMax=self.frameLimit
            self.startFrame=120
            self.framePunishment=1000
            self.fireInterval=30
            self.attackAnimeSign=True
            self.attackLightEffectSign=True

            # spell zone
            self.cardBonus=10000000
            self.spellName='Secret chant[Pray for the Harvest]'
            self.chSpellName=u'秘术「五谷丰登祈愿」'
            global_var.get_value('spell_sound').play()
            player.spellBonus=True
            # send spell effect
            new_effect=Effect.sanaeFaceSpell()
            effects.add(new_effect)
            self.doSpellCardAttack(effects)
        
        
        inSpellFrame=self.lastFrame-self.startFrame

        if self.lastFrame>=self.startFrame:
            self.cardBonus-=self.framePunishment
            if inSpellFrame%self.fireInterval>=(self.fireInterval-20):
                if inSpellFrame%self.fireInterval==(self.fireInterval-20):
                    new_bullet=Bullet.small_Bullet()
                    new_bullet.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                    new_bullet.selfTarget(player.cx,player.cy,2)
                    new_bullet.countAngle()
                    self.fireAngle=new_bullet.angle
                if (inSpellFrame%self.fireInterval-(self.fireInterval-20))%4==0:
                    sendFireSound(2)
                    if (inSpellFrame%self.fireInterval-(self.fireInterval-20))==16:
                        typ=sanae_spell_1_rice_bullet
                    else:
                        typ=sanae_spell_1_rice_bullet
                    for i in range(5):
                        new_bullet=typ()
                        new_bullet.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                        new_bullet.setSpeed(self.fireAngle+i*(360/5),7.3)
                        new_bullet.doColorCode(2)
                        new_bullet.actionNum=i
                        bullets.add(new_bullet)

        if self.health<=0 or self.frameLimit<=0:
            self.cancalAllBullet(bullets,items,effects,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            if self.frameLimit>0:
                self.createItem(items,0,10)
                self.createItem(items,1,20)
                self.createItem(items,6,1)
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


    def noneSpell_2(self, frame, items, effects, bullets, backgrounds, enemys, slaves, player):
            if self.reset: #start reset, individualized
                self.lastFrame=0
                self.reset=False
                self.maxHealth=30000
                self.health=self.maxHealth
                self.gotoPosition(340-self.bulletAdj[0],200-self.bulletAdj[1],40)
                self.randomAngle=random.random()*360
                self.frameLimit=3600
                self.frameLimitMax=self.frameLimit
                self.startFrame=120
                self.attackAnimeSign=True
                self.attackLightEffectSign=True

                #spell zone
                self.fireInterval=120

            inSpellFrame=self.lastFrame-self.startFrame

            if self.lastFrame>=self.startFrame:
                if inSpellFrame%self.fireInterval==0:
                    new_bullet=Bullet.small_Bullet()
                    new_bullet.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                    new_bullet.selfTarget(player.cx,player.cy,2)
                    new_bullet.countAngle()
                    self.fireAngle=new_bullet.angle
                    stdSpeed_main=3+random.random()*2
                    self.stdSpeed_sub=random.random()*1.6+1.9
                    for i in range(4):
                        sendFireSound(1)
                        new_bullet=sanae_noneSpell_1_orb_bullet()
                        new_bullet.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                        new_bullet.cancalable=False
                        new_bullet.setSpeed(self.fireAngle+i*(360/4),stdSpeed_main)
                        new_bullet.setAccSpeed(self.fireAngle+i*(360/4),stdSpeed_main,0,10,20)
                        new_bullet.loadColor('blue')
                        new_bullet.color='lakeBlue'
                        new_bullet.length=random.randint(7,9)
                        new_bullet.sideNum=4
                        new_bullet.stdSpeed=self.stdSpeed_sub
                        new_bullet.stdAngle=self.fireAngle
                        bullets.add(new_bullet)
                

            
            if self.health<=0 or self.frameLimit<=0: #end check, non_spell
                self.cancalAllBullet(bullets,items,effects,True)
                self.reset=True
                self.ifSpell=True
                self.health=20000
                self.attackLightEffectSign=False
                self.attackAnimeSign=False
    
    def spell_2(self, frame, items, effects, bullets, backgrounds, enemys, slaves, player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            self.maxHealth=45000
            self.health=self.maxHealth
            self.gotoPosition(340,220,30)
            self.randomAngle=random.random()*360
            self.randomAngle2=random.random()*360
            self.frameLimit=7200
            self.frameLimitMax=self.frameLimit
            self.startFrame=120
            self.fireInterval=5
            self.attackAnimeSign=False
            self.attackLightEffectSign=False

            # spell zone
            self.cardBonus=10000000
            self.spellName='Thunder Punishment[Thunder of Grand Miracle]'
            self.chSpellName=u'雷罚「大奇迹之雷」'
            global_var.get_value('spell_sound').play()
            player.spellBonus=True
            # send spell effect
            new_effect=Effect.sanaeFaceSpell()
            effects.add(new_effect)
            self.doSpellCardAttack(effects)
        
        #self.cardBonus-=self.framePunishment
        inSpellFrame=self.lastFrame-self.startFrame

        if self.lastFrame>=self.startFrame:
            self.cardBonus-=self.framePunishment
            if inSpellFrame%180<=120:
                if inSpellFrame%(self.fireInterval+2)==0:
                    sendFireSound(2)
                    numberOfLines=12
                    for i in range(numberOfLines):
                        new_bullet=sanae_spell_2_lightning_bullet()
                        new_bullet.initial(self.tx,self.ty,0)
                        new_bullet.angleNow=self.randomAngle+i*(360/numberOfLines)
                        new_bullet.speedNow=4
                        new_bullet.changeFrame=5
                        new_bullet.movingFrame=10
                        new_bullet.stayFrame=5
                        #new_bullet.changeFrame=8
                        new_bullet.setSpeed(self.randomAngle+i*(360/numberOfLines),new_bullet.speedNow)
                        new_bullet.speedMax=new_bullet.speedNow-0.1
                        new_bullet.doColorCode(13)
                        new_bullet.ifAddHitPoint=False
                        bullets.add(new_bullet)        
                    self.randomAngle-=0.8
            elif inSpellFrame%180==179:
                self.randomAngle=random.random()*360
                
            
            if (inSpellFrame%180>=120 or inSpellFrame%180<10) and inSpellFrame>20:
                sendFireSound(2)
                if inSpellFrame%self.fireInterval==0:
                    for i in range(13):
                        new_bullet=sanae_spell_2_lightning_bullet()
                        new_bullet.initial(self.tx,self.ty,0)
                        new_bullet.angleNow=self.randomAngle2+i*(360/13)
                        new_bullet.speedNow=4.2
                        new_bullet.changeFrame=5
                        new_bullet.movingFrame=15
                        new_bullet.stdAngle=30
                        new_bullet.stayFrame=5
                        new_bullet.setSpeed(self.randomAngle2+i*(360/13),new_bullet.speedNow)
                        new_bullet.speedMax=new_bullet.speedNow-0.1
                        new_bullet.doColorCode(2)
                        bullets.add(new_bullet)        
            
            if inSpellFrame%70==0:
                angle=random.random()*360
                sendFireSound(1)
                for i in range(12):
                    new_bullet=Bullet.butterfly_Bullet()
                    new_bullet.initial(self.tx,self.ty,0)
                    new_bullet.setSpeed(angle+i*360/12,4.0)
                    #new_bullet.loadColor('yellow')
                    new_bullet.doColorCode(6)
                    bullets.add(new_bullet)
                
            if inSpellFrame%180==50:
                self.randomAngle2=random.random()*360
                
        
        if inSpellFrame%180==15:
            self.gotoPosition(340-100+random.random()*200,random.random()*40+180,90)
        
        if self.health<=0 or self.frameLimit<=0:
            self.cancalAllBullet(bullets,items,effects,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            if self.frameLimit>0:
                self.createItem(items,0,15)
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
    
    def noneSpell_3(self, frame, items, effects, bullets, backgrounds, enemys, slaves, player):
            if self.reset: #start reset, individualized
                self.lastFrame=0
                self.reset=False
                self.maxHealth=30000
                self.health=self.maxHealth
                self.gotoPosition(340-self.bulletAdj[0],200-self.bulletAdj[1],40)
                self.randomAngle=random.random()*360
                self.frameLimit=3600
                self.frameLimitMax=self.frameLimit
                self.startFrame=120
                self.attackAnimeSign=True
                self.attackLightEffectSign=True

                #spell zone
                self.fireInterval=160

            inSpellFrame=self.lastFrame-self.startFrame

            if self.lastFrame>=self.startFrame:
                if inSpellFrame%self.fireInterval==0:
                    new_bullet=Bullet.small_Bullet()
                    new_bullet.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                    new_bullet.selfTarget(player.cx,player.cy,2)
                    new_bullet.countAngle()
                    self.fireAngle=new_bullet.angle
                    stdSpeed_main=3+random.random()*2
                    self.stdSpeed_sub=random.random()*1.6+1.9
                    for i in range(5):
                        sendFireSound(1)
                        new_bullet=sanae_noneSpell_1_orb_bullet()
                        new_bullet.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                        new_bullet.cancalable=False
                        new_bullet.setSpeed(self.fireAngle+i*(360/5),stdSpeed_main)
                        new_bullet.setAccSpeed(self.fireAngle+i*(360/5),stdSpeed_main,0,10,20)
                        new_bullet.loadColor('yellow')
                        new_bullet.color='lightYellow'
                        new_bullet.length=7
                        new_bullet.sideNum=5
                        new_bullet.stdSpeed=self.stdSpeed_sub
                        new_bullet.stdAngle=self.fireAngle
                        bullets.add(new_bullet)


            if self.health<=0 or self.frameLimit<=0: #end check, non_spell
                self.cancalAllBullet(bullets,items,effects,True)
                self.reset=True
                self.ifSpell=True
                self.health=20000
                self.attackLightEffectSign=False
                self.attackAnimeSign=False
    
    def spell_3(self, frame, items, effects, bullets, backgrounds, enemys, slaves, player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            self.maxHealth=50000
            self.health=self.maxHealth
            self.gotoPosition(340,220,30)
            self.randomAngle=random.random()*360
            self.randomAngle2=random.random()*360
            self.frameLimit=7200
            self.frameLimitMax=self.frameLimit
            self.startFrame=120
            self.fireInterval=4
            self.attackAnimeSign=False
            self.attackLightEffectSign=False
            global_var.set_value('endStageSpell3Signal',0)

            # spell zone
            self.cardBonus=10000000
            self.spellName='Elf Sign[Leaves of the Void]'
            self.chSpellName=u'精灵「虚空之森的落叶」'
            global_var.get_value('spell_sound').play()
            player.spellBonus=True
            # send spell effect
            new_effect=Effect.sanaeFaceSpell()
            effects.add(new_effect)
            self.doSpellCardAttack(effects)

        #self.cardBonus-=self.framePunishment
        inSpellFrame=self.lastFrame-self.startFrame

        if self.lastFrame==self.startFrame:
            self.attackAnimeSign=True
            self.attackLightEffectSign=True

        if self.lastFrame>=self.startFrame:
            self.cardBonus-=self.framePunishment
            if inSpellFrame%self.fireInterval==0:
                sendFireSound(2)
                for i in range(3):
                    self.randomAngle+=2.3
                    self.randomAngle2-=4.2
                    sendBulletRadius=40
                    sx=(self.tx+self.bulletAdj[0])+sendBulletRadius*math.cos((self.randomAngle+i*360/3)/180*math.pi)
                    sy=(self.ty+self.bulletAdj[1])+sendBulletRadius*math.sin((self.randomAngle+i*360/3)/180*math.pi)
                    for j in (0,1):
                        new_bullet=sanae_spell_3_leaf_bullet()
                        new_bullet.initial(sx,sy,0)
                        new_bullet.setSpeed(self.randomAngle2-self.randomAngle+i*360/3+j*180,4+math.sin(self.randomAngle2/180*math.pi))
                        if j==0:
                            new_bullet.loadColor('green')
                            new_bullet.ifTp=True
                        else:
                            new_bullet.loadColor('orange')
                            new_bullet.ifBounce=True
                        bullets.add(new_bullet)
        
        if inSpellFrame%840==0:
            new_effect=Effect.wave()
            new_effect.initial((self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1]),900,40,(235,184,0),6)
            effects.add(new_effect)
            global_var.get_value('kira1_sound').stop()
            global_var.get_value('kira1_sound').play()
            new_effect=Effect.sanae_spell_3_side_line()
            new_effect.actionNum=0
            effects.add(new_effect)
        elif inSpellFrame%840==400:
            new_effect=Effect.wave()
            new_effect.initial((self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1]),900,40,(137,245,78),6)
            effects.add(new_effect)
            global_var.get_value('kira1_sound').stop()
            global_var.get_value('kira1_sound').play()
            new_effect=Effect.sanae_spell_3_side_line()
            new_effect.actionNum=1
            effects.add(new_effect)

        if inSpellFrame%840<=200:
            global_var.set_value('endStageSpell3Signal',1)
        elif inSpellFrame%840<=600 and inSpellFrame%840>=400:
            global_var.set_value('endStageSpell3Signal',2)
        else:
            global_var.set_value('endStageSpell3Signal',0)
        
        if self.health<=0 or self.frameLimit<=0:
            self.cancalAllBullet(bullets,items,effects,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            if self.frameLimit>0:
                self.createItem(items,0,10)
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

    def noneSpell_4(self, frame, items, effects, bullets, backgrounds, enemys, slaves, player):
            if self.reset: #start reset, individualized
                self.lastFrame=0
                self.reset=False
                self.maxHealth=30000
                self.health=self.maxHealth
                self.gotoPosition(340-self.bulletAdj[0],200-self.bulletAdj[1],40)
                self.randomAngle=170+random.random()*60
                self.frameLimit=3600
                self.frameLimitMax=self.frameLimit
                self.startFrame=120
                self.fireInterval=120
                self.attackAnimeSign=True
                self.attackLightEffectSign=True
                self.fireCount=0

                #spell z=
                self.fireNode=2

            inSpellFrame=self.lastFrame-self.startFrame

            if self.lastFrame>=self.startFrame:
                if inSpellFrame%self.fireInterval==41:
                        
                        self.fireCount+=1
                        if self.fireCount%4==0:
                            self.randomAngle=140+random.random()*20
                        elif self.fireCount%4==1:
                            self.randomAngle=40-random.random()*20
                        else:
                            self.randomAngle=random.random()*360
                        
                        if self.fireCount%4==2 or self.fireCount%4==3:
                            self.fireNode=1
                            if self.fireCount%4==2:
                                self.gotoPosition(340-100+random.random()*200,random.random()*40+180,50)
                        else:
                            self.fireNode=2
                            if self.fireCount%4==0:
                                self.gotoPosition(340-100+random.random()*200,random.random()*40+180,50)
                if inSpellFrame%self.fireInterval<=34:
                    if inSpellFrame%self.fireInterval%self.fireNode==0:
                        sendFireSound(2)
                        for i in range(9):
                            if self.fireCount%4<=1:
                                if i%2==1:
                                    new_bullet=sanae_noneSpell_4_bounce_scale_bullet()
                                else:
                                    new_bullet=sanae_noneSpell_4_bounce_rice_bullet()
                            else:
                                if i==0:
                                    new_bullet=Bullet.scale_Bullet()
                                else:
                                    new_bullet=Bullet.rice_Bullet()
                            new_bullet.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                            new_bullet.setSpeed(self.randomAngle,12-0.5*i)
                            if self.fireCount%4<=1:
                                new_bullet.loadColor('green')
                            else:
                                new_bullet.loadColor('orange')
                            bullets.add(new_bullet)
                        if self.fireCount%4==0:
                            self.randomAngle+=14
                        elif self.fireCount%4==1:
                            self.randomAngle-=14
                        elif self.fireCount%4==2:
                            self.randomAngle+=360/16.5
                        elif self.fireCount%4==3:
                            self.randomAngle-=360/16.5


            if self.health<=0 or self.frameLimit<=0: #end check, non_spell
                self.cancalAllBullet(bullets,items,effects,True)
                self.reset=True
                self.ifSpell=True
                self.health=20000
                self.attackLightEffectSign=False
                self.attackAnimeSign=False
    
    def spell_4(self, frame, items, effects, bullets, backgrounds, enemys, slaves, player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            self.maxHealth=55000
            self.health=self.maxHealth
            self.gotoPosition(340,220,30)
            self.randomAngle=random.random()*360
            self.randomAngle2=random.random()*360
            self.frameLimit=7200
            self.frameLimitMax=self.frameLimit
            self.startFrame=120
            self.fireInterval=25
            self.attackAnimeSign=True
            self.attackLightEffectSign=True
            self.fireCount=0
            self.fireCount2=0
            global_var.set_value('endStageSpell3Signal',0)

            # spell zone
            self.cardBonus=10000000
            self.spellName='Miracle[Spinning Sun]'
            self.chSpellName=u'奇迹「Spinning Sun」'
            global_var.get_value('spell_sound').play()
            player.spellBonus=True
            # send spell effect
            new_effect=Effect.sanaeFaceSpell()
            effects.add(new_effect)
            self.doSpellCardAttack(effects)

        #self.cardBonus-=self.framePunishment
        inSpellFrame=self.lastFrame-self.startFrame

        laserAttackInterval=750
        laserAttackNode=110
        laserAttackNode2=300
        fireNode2=10

        if self.lastFrame>=self.startFrame:
            self.cardBonus-=self.framePunishment
            if inSpellFrame%laserAttackInterval==0 or inSpellFrame%laserAttackInterval==laserAttackNode:
                for i in range(6):
                    new_laser=Bullet.laser_line()
                    new_laser.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                    new_laser.setFeature(self.randomAngle+i*360/6,7,125,30,64,20,5,60)
                    new_laser.furryCollide=5
                    if self.fireCount%2==0:
                        new_laser.dDegree=-0.33
                    else:
                        new_laser.dDegree=0.33
                    new_laser.ifSimplifiedMode=True
                    new_laser.widenProperty=True
                    new_laser.doColorCode(13)
                    bullets.add(new_laser)
                self.randomAngle=random.random()*360
                self.fireCount+=1
            
            elif inSpellFrame%laserAttackInterval==laserAttackNode2 or inSpellFrame%laserAttackInterval==laserAttackNode2+150:
                global_var.get_value('ch00_sound').stop()
                global_var.get_value('ch00_sound').play()
                new_effect=Effect.powerUp()
                new_effect.initial((self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1]),400,96,(254,184,80),20,1,0)
                effects.add(new_effect)
                new_bullet=Bullet.small_Bullet()
                new_bullet.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                new_bullet.selfTarget(player.cx,player.cy,2)
                new_bullet.countAngle()
                angle=new_bullet.angle
                angleInterval=40
                for i in (-2,-1,0,1,2):
                    new_laser=Bullet.laser_line()
                    new_laser.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                    new_laser.setFeature(angle+i*angleInterval,7,150,96,64,20,20,-1)
                    new_laser.furryCollide=8
                    new_laser.stopSign=True
                    new_laser.stopDFrame=96
                    new_laser.dDegree=i*-1*angleInterval/100
                    new_laser.ifSimplifiedMode=True
                    new_laser.widenProperty=True
                    new_laser.doColorCode(14)
                    bullets.add(new_laser)

            if inSpellFrame%self.fireInterval==0 or inSpellFrame%self.fireInterval==fireNode2:
                sendFireSound(2)
                cgA1=-75-10*random.random()
                cgA2=75+10*random.random()
                spd=3.9+0.20*(self.fireCount2%2)+0.3*random.random()
                for i in range(20):
                    new_bullet=sanae_spell_4_changeDirect_orb_bullet()
                    new_bullet.initial(self.tx,self.ty,0)
                    new_bullet.setSpeed(self.randomAngle2+i*360/20,5)
                    new_bullet.angle=self.randomAngle2+i*360/20
                    if self.fireCount2%2==0:
                        new_bullet.changeAngle=cgA1
                        new_bullet.loadColor('yellow')                       
                    else:
                        new_bullet.changeAngle=cgA2
                        new_bullet.loadColor('orange')
                    new_bullet.speed=spd
                    
                    bullets.add(new_bullet)
                self.fireCount2+=1
                
                self.randomAngle2=random.random()*360

            #motion control
            if inSpellFrame%laserAttackInterval==laserAttackNode2+150+20:
                self.attackLightEffectSign=False
                self.attackAnimeSign=False
            
            if inSpellFrame%laserAttackInterval==(laserAttackInterval-60):
                self.attackLightEffectSign=True
                self.attackAnimeSign=True

            if inSpellFrame%laserAttackInterval==laserAttackNode2+150+100:
                self.gotoPosition(340-100+random.random()*200,random.random()*40+180,90)
            
        
        if self.health<=0 or self.frameLimit<=0:
            self.cancalAllBullet(bullets,items,effects,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            if self.frameLimit>0:
                self.createItem(items,0,15)
                self.createItem(items,1,20)
                self.createItem(items,6,1)
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
    
    def noneSpell_5(self, frame, items, effects, bullets, backgrounds, enemys, slaves, player):
        if self.reset: #start reset, individualized
            self.lastFrame=0
            self.reset=False
            self.maxHealth=30000
            self.health=self.maxHealth
            self.gotoPosition(340-self.bulletAdj[0],200-self.bulletAdj[1],40)
            self.randomAngle=random.random()*360
            self.frameLimit=3600
            self.frameLimitMax=self.frameLimit
            self.startFrame=120
            self.attackAnimeSign=True
            self.attackLightEffectSign=True

            #spell zone
            self.fireInterval=120

        inSpellFrame=self.lastFrame-self.startFrame

        if self.lastFrame>=self.startFrame:
            if inSpellFrame%self.fireInterval==0:
                new_bullet=Bullet.small_Bullet()
                new_bullet.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                new_bullet.selfTarget(player.cx,player.cy,2)
                new_bullet.countAngle()
                self.fireAngle=new_bullet.angle
                stdSpeed_main=4+random.random()*2
                self.stdSpeed_sub=random.random()*1.3+1.5
                for i in range(6):
                    sendFireSound(1)
                    new_bullet=sanae_noneSpell_1_orb_bullet()
                    new_bullet.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                    new_bullet.cancalable=False
                    new_bullet.setSpeed(self.fireAngle+i*(360/6),stdSpeed_main)
                    new_bullet.setAccSpeed(self.fireAngle+i*(360/6),stdSpeed_main,0,15,20)
                    new_bullet.loadColor('red')
                    new_bullet.color='lightRed'
                    new_bullet.stdSpeed=self.stdSpeed_sub
                    new_bullet.length=8
                    new_bullet.stdAngle=self.fireAngle+i*(360/6)
                    bullets.add(new_bullet)
        
        if self.health<=0 or self.frameLimit<=0: #end check, non_spell
            self.cancalAllBullet(bullets,items,effects,True)
            self.reset=True
            self.ifSpell=True
            self.health=20000
            self.attackLightEffectSign=False
            self.attackAnimeSign=False

    def spell_5(self, frame, items, effects, bullets, backgrounds, enemys, slaves, player):

        if self.reset:
            self.lastFrame=0
            self.reset=False
            self.maxHealth=50000
            self.health=self.maxHealth
            self.gotoPosition(340,220,30)
            self.randomAngle=random.random()*90+45
            self.randomAngle2=random.random()*360
            self.frameLimit=7200
            self.frameLimitMax=self.frameLimit
            self.startFrame=120
            self.fireInterval=120
            self.fireInterval2=90
            self.attackAnimeSign=True
            self.attackLightEffectSign=True
            self.crazySign=False
            self.fireCount=0
            self.fireCount2=0
            global_var.set_value('sanae_spell5_laser_signal',False)

            # spell zone
            self.cardBonus=10000000
            self.spellName='Satan [Fire Rings of Hell]'
            self.chSpellName=u'撒旦「地狱火轮」'
            global_var.get_value('spell_sound').play()
            player.spellBonus=True
            # send spell effect
            new_effect=Effect.sanaeFaceSpell()
            effects.add(new_effect)
            self.doSpellCardAttack(effects)

        #self.cardBonus-=self.framePunishment
        inSpellFrame=self.lastFrame-self.startFrame

        #self.crazySign=False
        ringIntense=7
        if self.health/self.maxHealth<=0.4 or self.frameLimit<=3*600:
            if not self.crazySign:
                new_effect=Effect.powerUp()
                new_effect.initial((self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1]),500,70,(255,255,255),10,1,1)
                effects.add(new_effect)
                global_var.get_value('ch00_sound').stop()
                global_var.get_value('ch00_sound').play()
            self.crazySign=True
            ringIntense=10

        if self.lastFrame>=self.startFrame:
            self.cardBonus-=self.framePunishment
            if inSpellFrame%self.fireInterval==0:
                sendFireSound(1)
                #print(self.randomAngle)
                signList=[-1,1]
                
                agspd=(random.random()*0.5+0.6)*signList[random.randint(0,1)]
                if self.crazySign:
                    agspd=agspd*1.5
                initX=140+random.random()*400
                new_slave=Slave.sanae_spell5_laserSlave()
                new_slave.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                new_slave.selfTarget(player.cx,player.cy,2)
                new_slave.speed=2
                #slaves.add(new_slave)
                for i in range(ringIntense):
                    new_bullet=sanae_spell_5_ringed_orb_bullet()
                    new_bullet.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                    #new_bullet.setSpeed(self.randomAngle,2)
                    new_bullet.selfTarget(player.cx,player.cy,2)
                    new_bullet.angleNow=self.randomAngle2+360/ringIntense*i
                    new_bullet.angleSpeed=agspd
                    new_bullet.radius=0
                    new_bullet.rSpeed=-0.9
                    if self.crazySign:
                        new_bullet.loadColor('orange')
                        new_bullet.actionNum=1
                    else:
                        new_bullet.loadColor('red')
                    if i==0:
                        new_bullet.ifDrawCircle=False
                    bullets.add(new_bullet)
                self.randomAngle=random.random()*90+45
                self.randomAngle2=random.random()*360
            
            if inSpellFrame%self.fireInterval2==0:
                angle=random.random()*360
                frame=random.randint(25,35)
                sendFireSound(2)
                for i in range(20):
                    for j in range(2):
                        new_bullet=part2_acc_bullet()
                        new_bullet.initial(self.tx,self.ty,0)
                        new_bullet.setSpeed(angle+i*360/20,6-1.5*j)
                        new_bullet.setAccSpeed(angle+i*360/20,6-1.5*j,3-0.75*j,50,frame)
                        new_bullet.loadColor('lightRed')
                        bullets.add(new_bullet)
            
            if inSpellFrame%(self.fireInterval*2)==self.fireInterval:
                new_bullet=Bullet.small_Bullet()
                new_bullet.initial(self.tx,self.ty,0)
                px=global_var.get_value('player1x')
                py=global_var.get_value('player1y')
                new_bullet.selfTarget(px,py,2)
                new_bullet.countAngle()
                angle=new_bullet.angle
                for i in range(6):
                    for j in (-1,0,1):
                        new_bullet=Bullet.kunai_Bullet()
                        new_bullet.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                        new_bullet.setSpeed(angle+j*40,7-0.8*i)
                        new_bullet.doColorCode(14)
                        bullets.add(new_bullet)

            if inSpellFrame%240==30:
                self.gotoPosition(340-100+random.random()*200,random.random()*40+180,60)

            if inSpellFrame%self.fireInterval==60:
                global_var.set_value('sanae_spell5_laser_signal',True)
            else:
                global_var.set_value('sanae_spell5_laser_signal',False)

        if self.health<=0 or self.frameLimit<=0:
            self.cancalAllBullet(bullets,items,effects,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            if self.frameLimit>0:
                self.createItem(items,0,15)
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

    def noneSpell_6(self, frame, items, effects, bullets, backgrounds, enemys, slaves, player):
        if self.reset: #start reset, individualized
            self.lastFrame=0
            self.reset=False
            self.maxHealth=35000
            self.health=self.maxHealth
            self.gotoPosition(340-self.bulletAdj[0],200-self.bulletAdj[1],40)
            self.randomAngle=random.random()*360
            self.frameLimit=3600
            self.frameLimitMax=self.frameLimit
            self.startFrame=120
            self.attackAnimeSign=True
            self.attackLightEffectSign=True

            #spell zone
            self.fireInterval=140

        inSpellFrame=self.lastFrame-self.startFrame

        if self.lastFrame>=self.startFrame:
            if inSpellFrame%self.fireInterval==0:
                self.fireAngle=random.random()*360
                stdSpeed_main=2+random.random()*2
                self.stdSpeed_sub=random.random()*1.5+2.5
                for i in range(6):
                    sendFireSound(1)
                    new_bullet=sanae_noneSpell_1_orb_bullet()
                    new_bullet.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                    new_bullet.cancalable=False
                    new_bullet.setSpeed(self.fireAngle+i*(360/6),stdSpeed_main)
                    new_bullet.setAccSpeed(self.fireAngle+i*(360/6),stdSpeed_main,0,15,5)
                    new_bullet.loadColor('grey')
                    new_bullet.color='white'
                    new_bullet.stdSpeed=self.stdSpeed_sub
                    new_bullet.length=7
                    new_bullet.sideNum=4
                    new_bullet.stdAngle=self.fireAngle+i*(360/6)
                    bullets.add(new_bullet)
        
            if inSpellFrame%280==170:
                self.gotoPosition(340-120+random.random()*240,random.random()*60+170,60)
        
        if self.health<=0 or self.frameLimit<=0: #end check, non_spell
            self.cancalAllBullet(bullets,items,effects,True)
            self.reset=True
            self.ifSpell=True
            self.health=20000
            self.attackLightEffectSign=False
            self.attackAnimeSign=False

    def spell_6(self, frame, items, effects, bullets, backgrounds, enemys, slaves, player):

        if self.reset:
            self.lastFrame=0
            self.reset=False
            self.maxHealth=70000
            self.health=self.maxHealth
            self.gotoPosition(340,220,30)
            self.randomAngle=random.random()*360
            self.randomAngle2=random.random()*360
            self.frameLimit=7200
            self.frameLimitMax=self.frameLimit
            self.startFrame=120
            self.periodMax=12*60
            self.periodChange=5*60
            self.fireInterval=60
            self.fireInterval2=2
            self.attackAnimeSign=True
            self.attackLightEffectSign=True
            self.crazySign=False
            self.fireCount=0
            self.periodCount=0

            # spell zone
            self.cardBonus=10000000
            self.spellName='Sky Dome[Leonids Meteor Shower]'
            self.chSpellName=u'天穹「狮子座流星雨」'
            global_var.get_value('spell_sound').play()
            player.spellBonus=True
            # send spell effect
            new_effect=Effect.sanaeFaceSpell()
            effects.add(new_effect)
            self.doSpellCardAttack(effects)
        
        #self.cardBonus-=self.framePunishment
        inSpellFrame=self.lastFrame-self.startFrame

        if self.lastFrame>=self.startFrame:
            self.cardBonus-=self.framePunishment
            if inSpellFrame%4==0:
                new_bullet=Bullet.star_Bullet()
                new_bullet.initial(random.random()*560+60,30,0)
                new_bullet.setSpeed(90-5+10*random.random(),3+1.5*random.random())
                new_bullet.doColorCode(5)
                bullets.add(new_bullet)
            

            if inSpellFrame%self.periodMax>self.periodChange:
                cL=random.randint(1,7)
                cL2=cL*2
                if cL2==14:
                    cL2=15
                if inSpellFrame%self.fireInterval==0:
                    if self.periodCount%2==0:
                        rx=300+320*random.random()
                        ra=random.random()*40+105
                        rFrame=round((rx-60)/abs(math.cos(ra*math.pi/180))/12)
                        rFrame2=round((690-40)/abs(math.sin(ra*math.pi/180))/12)
                    else:
                        rx=380-320*random.random()
                        ra=-random.random()*40+75
                        rFrame=round((560+60-rx)/abs(math.cos(ra*math.pi/180))/12)
                        rFrame2=round((690-40)/abs(math.sin(ra*math.pi/180))/12)
                    
                    if rFrame>rFrame2:
                        rFrame=rFrame2

                    #print(rFrame)
                    new_laser=Bullet.laser_line_stay_acc()
                    new_laser.initial(rx,40,0)
                    new_laser.setSpeed(ra,1.3)
                    new_laser.setAccSpeed(ra,1.3,12,10,10)
                    new_laser.setFeature(ra-180,6,rFrame+5,30,32,5,5,30)
                    new_laser.furryCollide=7
                    new_laser.ifSimplifiedMode=True
                    new_laser.widenProperty=True
                    new_laser.doColorCode(cL2)
                    new_laser.cancalable=False
                    bullets.add(new_laser)

                    new_bullet=sanae_spell_6_big_star_bullet()
                    new_bullet.actionNum=random.randint(0,2)
                    new_bullet.initial(rx,40,0)
                    new_bullet.setSpeed(ra,1.3)
                    new_bullet.setAccSpeed(ra,1.3,12,10,10)
                    new_bullet.doColorCode(cL)
                    new_bullet.cancalable=False
                    #new_bullet.anmStay=True
                    bullets.add(new_bullet)
            
            if inSpellFrame%self.periodMax<=self.periodChange:
                if inSpellFrame%self.fireInterval2==0:
                    if self.periodCount%2==0:
                        self.randomAngle+=6+3*random.random()#3
                    else:
                        self.randomAngle-=6+3*random.random()
                    sendFireSound(2)
                    for i in range(3):
                        new_bullet=Bullet.star_bullet_stay_acc()
                        new_bullet.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                        new_bullet.setSpeed(self.randomAngle+120*i,7)
                        new_bullet.setAccSpeed(self.randomAngle+120*i,7,4,30,20)#5,4 ; 30,20
                        self.fireCount+=1
                        self.fireCount=self.fireCount%16
                        new_bullet.doColorCode(self.fireCount)
                        bullets.add(new_bullet)
            
            if inSpellFrame%self.periodMax==self.periodMax-1:
                self.periodCount+=1
                self.attackAnimeSign=True
                self.attackLightEffectSign=True
            
            if inSpellFrame%self.periodMax>=self.periodChange and inSpellFrame%self.periodMax%120==0:
                self.gotoPosition(340-120+random.random()*240,random.random()*60+170,60)
            
            if inSpellFrame%self.periodMax==self.periodChange:
                Effect.bossPower(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],effects,Effect.bossPowerMomiji,40)
                global_var.get_value('ch00_sound').stop()
                global_var.get_value('ch00_sound').play()

            if inSpellFrame%self.periodMax==self.periodChange+60:
                self.attackAnimeSign=False
                self.attackLightEffectSign=False
        
        if self.health<=0 or self.frameLimit<=0:
            self.cancalAllBullet(bullets,items,effects,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            if self.frameLimit>0:
                self.createItem(items,0,15)
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
    
    def noneSpell_7(self, frame, items, effects, bullets, backgrounds, enemys, slaves, player):
        if self.reset: #start reset, individualized
            self.lastFrame=0
            self.reset=False
            self.maxHealth=40000
            self.health=self.maxHealth
            self.gotoPosition(340-self.bulletAdj[0],200-self.bulletAdj[1],40)
            self.randomAngle=random.random()*360
            self.frameLimit=3600
            self.frameLimitMax=self.frameLimit
            self.startFrame=120
            self.attackAnimeSign=True
            self.attackLightEffectSign=True

            #spell zone
            self.fireInterval=140

        inSpellFrame=self.lastFrame-self.startFrame

        if self.lastFrame>=self.startFrame:
            if inSpellFrame%self.fireInterval==0:
                #c_list=['blue','darkBlue','green','grey','jade','lakeBlue','lightGreen','lightRed','lightYellow','orange','pink','purple','red','skyBlue','white','yellow']
                nNum=random.randint(3,7)
                self.fireAngle=random.random()*360
                stdSpeed_main=3+random.random()*2
                self.stdSpeed_sub=random.random()*1.5+2.5
                #color=c_list[nNum]
                for i in range(nNum):
                    sendFireSound(1)
                    new_bullet=sanae_noneSpell_1_orb_bullet()
                    new_bullet.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],0)
                    new_bullet.cancalable=False
                    new_bullet.setSpeed(self.fireAngle+i*(360/nNum),stdSpeed_main)
                    new_bullet.setAccSpeed(self.fireAngle+i*(360/nNum),stdSpeed_main,0,15,15)
                    #new_bullet.loadColor('grey')
                    new_bullet.doColorCode(nNum-3)
                    new_bullet.color=new_bullet.c_list[nNum]
                    new_bullet.stdSpeed=self.stdSpeed_sub
                    new_bullet.length=6
                    new_bullet.sideNum=10-nNum
                    new_bullet.stdAngle=self.fireAngle+i*(360/nNum)
                    bullets.add(new_bullet)
        
            if inSpellFrame%280==170:
                self.gotoPosition(340-120+random.random()*240,random.random()*60+270,60)
        
        if self.health<=0 or self.frameLimit<=0: #end check, non_spell
            self.cancalAllBullet(bullets,items,effects,True)
            self.reset=True
            self.ifSpell=True
            self.health=20000
            self.attackLightEffectSign=False
            self.attackAnimeSign=False
    
    def spell_7(self, frame, items, effects, bullets, backgrounds, enemys, slaves, player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            self.maxHealth=60000
            self.health=self.maxHealth
            self.gotoPosition(340-self.bulletAdj[0],230-self.bulletAdj[1],30)
            self.randomAngle=random.random()*360
            self.randomAngle2=random.random()*360
            self.frameLimit=7200
            self.frameLimitMax=self.frameLimit
            self.startFrame=120
            self.fireInterval=60
            self.attackAnimeSign=True
            self.attackLightEffectSign=True
            self.fireCount=0
            self.ifSoundReleased=[False,False,False,False,False]

            # spell zone
            self.cardBonus=10000000
            self.spellName='God Grant[Yamato no Ame]'
            self.chSpellName=u'神赐「大和之雨」'
            global_var.get_value('spell_sound').play()
            player.spellBonus=True
            # send spell effect
            new_effect=Effect.sanaeFaceSpell()
            effects.add(new_effect)
            self.doSpellCardAttack(effects)
        
        #self.cardBonus-=self.framePunishment
        inSpellFrame=self.lastFrame-self.startFrame

        #fireLine=5
        if self.percentHealth<=25 or self.frameLimit<=2400:
            fireLine=5
            if not self.ifSoundReleased[4]:
                self.ifSoundReleased[4]=True
                global_var.get_value('ch00_sound').stop()
                global_var.get_value('ch00_sound').play()
        elif self.percentHealth<=40:
            if not self.ifSoundReleased[3]:
                self.ifSoundReleased[3]=True
                global_var.get_value('ch00_sound').stop()
                global_var.get_value('ch00_sound').play()
            fireLine=4
            if not self.ifSoundReleased[2]:
                self.ifSoundReleased[2]=True
                global_var.get_value('ch00_sound').stop()
                global_var.get_value('ch00_sound').play()
        elif self.percentHealth<=60:
            fireLine=3
            if not self.ifSoundReleased[1]:
                self.ifSoundReleased[1]=True
                global_var.get_value('ch00_sound').stop()
                global_var.get_value('ch00_sound').play()
        elif self.percentHealth<=80:
            fireLine=2
            if not self.ifSoundReleased[0]:
                self.ifSoundReleased[0]=True
                global_var.get_value('ch00_sound').stop()
                global_var.get_value('ch00_sound').play()
        else:
            fireLine=1
         

        if self.lastFrame>=self.startFrame:
            self.cardBonus-=self.framePunishment
            if inSpellFrame%1==0:
                sendFireSound(2)
                self.randomAngle2+=0.07
                if self.randomAngle2>=360:
                    self.randomAngle2-=360
                lines=fireLine
                for i in range(0,lines):
                    new_bullet=Bullet.rice_Bullet()
                    new_bullet.initial(self.tx+self.bulletAdj[0],self.ty+self.bulletAdj[1],1)
                    #new_bullet.loadColor('purple')
                    new_bullet.doColorCode(8)
                    new_bullet.setSpeed(self.randomAngle+i*(360/lines),6.7)
                    bullets.add(new_bullet)
                self.randomAngle+=self.randomAngle2
                while self.randomAngle>=360:
                    self.randomAngle-=360
            
        if self.health<=0 or self.frameLimit<=0:
            self.cancalAllBullet(bullets,items,effects,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            if self.frameLimit>0:
                #self.createItem(items,0,5)
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



def stageController(screen,frame,enemys,bullets,slaves,items,effects,backgrounds,bosses,player):

    if frame==1:# load in section, initialize background, and music
        pygame.mixer.music.stop()
        pygame.mixer.music.load('resource/bgm/yujiMidpath.mp3')   # 载入背景音乐文件
        #pygame.mixer.music.load('resource/bgm/上海アリス幻樂団 - 死体旅行~ Be of good cheer!.mp3')
        pygame.mixer.music.set_volume(0.7)                  # 设定背景音乐音量
        pygame.mixer.music.play(loops=-1)
        gF.doBackground2(screen,backgrounds)
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
    
    if frame==540:
        new_effect=Effect.level2Title()
        effects.add(new_effect)
    
    if frame>=680 and frame<=1080:
        if frame%15==0:
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
        '''backgroundFade(backgrounds)
        gF.doSpellBackground(screen,backgrounds)'''

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

        if frameAfterMidpath==2500:
            new_boss=SanaeStageFinal()
            #new_boss=DADcharacter.Boss()
            new_boss.initial(640,-200)
            bosses.add(new_boss)
    
        if frameAfterMidpath==2590:
            for boss in bosses:
                boss.gotoPosition(340,200,90)
        
        if frameAfterMidpath==2690:
            pygame.mixer.music.fadeout(1000)

        if frameAfterMidpath==2790:
            global_var.set_value('ifBoss',True)
            pygame.mixer.music.stop()
            #pygame.mixer.music.load('resource/bgm/lightnessBoss.mp3') 
            pygame.mixer.music.load('resource/bgm/金卡雷 - 风中花，雪中月.mp3') 
            pygame.mixer.music.set_volume(0.6) 
            pygame.mixer.music.play(loops=-1)  
            for boss in bosses:
                boss.cardNum=1
                boss.ifSpell=False