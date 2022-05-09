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


def stageController(screen,frame,enemys,bullets,slaves,items,effects,backgrounds,bosses,player):
    if frame==1:# load in section, initialize background, and music
        pygame.mixer.music.stop()
        pygame.mixer.music.load('resource/bgm/yujiMidpath.mp3')   # 载入背景音乐文件
        #pygame.mixer.music.load('resource/bgm/上海アリス幻樂団 - 死体旅行~ Be of good cheer!.mp3')
        pygame.mixer.music.set_volume(0.6)                  # 设定背景音乐音量
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