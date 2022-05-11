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
                        new_bullet=Bullet.mid_Bullet()
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
                        new_bullet=Bullet.mid_Bullet()
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
                            new_bullet.setAccSpeed(self.fireAngle+i*(360/5),1+j*0.3,self.bulletSpeed+j*(0.3+self.speedMultipler),30,30-3*self.firetime)
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
            if self.fireFrame%100==0:
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
        self.createItem(items,1,3)

def stageController(screen,frame,enemys,bullets,slaves,items,effects,backgrounds,bosses,player):
    if frame==1:# load in section, initialize background, and music
        pygame.mixer.music.stop()
        pygame.mixer.music.load('resource/bgm/yujiMidpath.mp3')   # 载入背景音乐文件
        #pygame.mixer.music.load('resource/bgm/上海アリス幻樂団 - 死体旅行~ Be of good cheer!.mp3')
        pygame.mixer.music.set_volume(0.7)                  # 设定背景音乐音量
        pygame.mixer.music.play(loops=-1)

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
    
    if frame>=2800 and frame<=3400:
        if (frame-2800)%25==0:
            for i in range(3):
                new_enemy=part4_enemy_kedama()
                new_enemy.initialize(50,100+70*i,0,-1)
                new_enemy.actionNum=0
                new_enemy.colorNum=0
                enemys.add(new_enemy)