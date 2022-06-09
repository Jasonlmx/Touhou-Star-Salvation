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
import Item
import gameRule
from screenSettings import screen_settings


class titleStar(pygame.sprite.Sprite):
    def __init__(self):
        super(titleStar,self).__init__()
        self.amplified_times=global_var.get_value('amplified_times')
        self.tx=0.0
        self.ty=0.0
        self.speedx=0
        self.speedy=0
        self.image=pygame.Surface((round(42*self.amplified_times),round(42*self.amplified_times))).convert_alpha()
        self.image.fill((0,0,0,0))
        self.image.blit(global_var.get_value('titleStar'),(0,0),(0,0,round(42*self.amplified_times),round(42*self.amplified_times)))
        self.lastFrame=0
        self.rAngle=random.random()*360
        self.rDirection=random.randint(0,1)
        if self.rDirection==0:
            self.rDirection=-1
        self.rotation=(random.random()*1.5+1.2)*self.rDirection
        self.maxFrame=270+random.randint(0,80)
        self.shadowInt=4
        self.voidifyFrame=30
        self.speed=0
        self.dDeg=-0.07*random.random()-0.07
    def initial(self,posx,posy):
        self.tx=posx
        self.ty=posy
    
    def movement(self):
        tick=global_var.get_value('DELTA_T')
        self.tx+=self.speedx*60/1000*tick
        self.ty+=self.speedy*60/1000*tick
    
    def speedAlter(self,speedx,speedy):
        self.speedx=speedx
        self.speedy=speedy
    
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
        self.speed=speed

    def arc(self):
        if self.angle>95:
            angle=self.angle+self.dDeg
            self.setSpeed(angle,self.speed)
       
    def checkValid(self):
        if self.lastFrame>self.maxFrame:
            self.kill()
    def update(self,screen,titleDec):
        self.lastFrame+=1
        self.rAngle+=self.rotation
        self.movement()
        self.countAngle()
        self.arc()
        self.draw(screen)
        if self.lastFrame%self.shadowInt==0:
            self.newShadow(titleDec)
        self.checkValid()
    
    def newShadow(self,titleDec):
        new_shadow=starShadow((self.tx,self.ty),80,self.rAngle)
        titleDec.add(new_shadow)

    def draw(self,screen):
        w,h=self.image.get_size()
        pos=(round(self.tx-w/2),round(self.ty-h/2))
        if self.lastFrame<=self.voidifyFrame:
            tempImg=self.image
            alpha=round((256-56)*self.lastFrame/self.voidifyFrame+56)
            tempImg.set_alpha(alpha)
            gF.drawRotation(tempImg,pos,self.rAngle,screen)
        elif (self.maxFrame-self.lastFrame)<=self.voidifyFrame:
            tempImg=self.image
            alpha=round((256-56)*(self.maxFrame-self.lastFrame)/self.voidifyFrame+56)
            tempImg.set_alpha(alpha)
            gF.drawRotation(tempImg,pos,self.rAngle,screen)
        else:
            #pos=(round(self.tx)-32,round(self.ty)-32)
            gF.drawRotation(self.image,pos,self.rAngle,screen)
            #screen.blit(self.image,pos)

class starShadow(pygame.sprite.Sprite):
    def __init__(self,pos,length=20,angle=0):
        super(starShadow,self).__init__()
        self.amplified_times=global_var.get_value('amplified_times')
        self.maxFrame=length
        self.angle=angle
        self.pos=pos
        self.image=pygame.Surface((round(42*self.amplified_times),round(42*self.amplified_times))).convert_alpha()
        self.image.fill((0,0,0,0))
        self.image.blit(global_var.get_value('titleStar'),(0,0),(0,0,round(42*self.amplified_times),round(42*self.amplified_times)))
        self.lastFrame=0
        
    def checkValid(self):
        if self.lastFrame>=self.maxFrame:
            self.kill()
    
    def update(self,screen,*arg):
        self.lastFrame+=1
        self.draw(screen)
        self.checkValid()
    
    def draw(self,screen):
        self.percentage=self.lastFrame/self.maxFrame
        self.alpha=round((120-0)*(1-self.percentage)+0)
        self.size=round(22*(1-self.percentage)*self.amplified_times)+1
        tempImg=pygame.Surface((round(42*self.amplified_times),round(42*self.amplified_times))).convert_alpha()
        tempImg.fill((0,0,0,0))
        tempImg.blit(self.image,(0,0),(0,0,round(42*self.amplified_times),round(42*self.amplified_times)))
        tempImg=pygame.transform.smoothscale(tempImg,(self.size,self.size))
        tempImg.set_alpha(self.alpha)  
        x,y=self.pos
        pos=(round(x-self.size/2),round(y-self.size/2))
        gF.drawRotation(tempImg,pos,self.angle,screen)


class Menu():
    def __init__(self):
        super(Menu,self).__init__()
        self.image=pygame.image.load('resource/title/menu0.png').convert()
        self.image=pygame.transform.smoothscale(self.image,(global_var.get_value('screen_width'),global_var.get_value('screen_height')))
        self.sign=global_var.get_value('menuSign')
        self.shadow=global_var.get_value('menuShadow')
        self.playerTitleImg=global_var.get_value('playerTitleImg')
        self.kanjiLogo=global_var.get_value('kanjiLogo')
        self.engLogo=global_var.get_value('engLogo')
        self.lightLogo=global_var.get_value('lightLogo')
        self.tachie=global_var.get_value('reimuLogo')
        self.selectImg=global_var.get_value('menuSelectImg')
        self.levelImg=global_var.get_value('levelImg')
        self.font=pygame.font.SysFont('arial', 20)
        self.selectNum=[0,1,0,0]
        self.stairMax=[7,1,1,1]
        self.menuStair=0 #0:main menu, 1 stage selection, 2 player selection, 3 practice menu
        self.playerReset=False
        self.lightStrength=0.0
        self.logoPosAdj=[0,0]
        self.lastFrame=0
        self.testSpellNum=1
        self.ifSpell=False
        self.substract=False
        self.plus=False
        self.starInt=180
        self.amplified_times=global_var.get_value('amplified_times')
    def update(self,screen,pressed_keys,pressed_keys_last,player,titleDec):
        self.lastFrame+=1
        self.addTitleStar(titleDec)
        if self.lastFrame>360:
            self.lastFrame=self.lastFrame%360
        screen.blit(self.image,(0,0))
        self.alterSelect(pressed_keys,pressed_keys_last)
        self.drawSign(screen,titleDec)
        self.doSelection(pressed_keys,pressed_keys_last,player)
    
    def addTitleStar(self,titleDec):
        if self.lastFrame%self.starInt==0:
            new_star=titleStar()
            i_x=(300+random.random()*660)*self.amplified_times/1.5
            i_y=(random.random()*5+10)*self.amplified_times/1.5
            new_star.initial(i_x,i_y)
            new_star.setSpeed(135+random.random()*10,(1.8+0.6*random.random())*self.amplified_times/1.5)
            titleDec.add(new_star)

    def alterSelect(self,pressed_keys,pressed_keys_last):
        if self.menuStair!=2 and self.menuStair!=3:
            if not (pressed_keys[K_UP] and pressed_keys_last[K_UP]):
                if pressed_keys[K_UP]:
                    self.selectNum[self.menuStair]-=1
                    global_var.get_value('select_sound').stop()
                    global_var.get_value('select_sound').play()
            if not (pressed_keys[K_DOWN] and pressed_keys_last[K_DOWN]):
                if pressed_keys[K_DOWN]:
                    self.selectNum[self.menuStair]+=1
                    global_var.get_value('select_sound').stop()
                    global_var.get_value('select_sound').play()
        elif self.menuStair==2:
            if not (pressed_keys[K_LEFT] and pressed_keys_last[K_LEFT]):
                if pressed_keys[K_LEFT]:
                    self.selectNum[self.menuStair]-=1
                    global_var.get_value('select_sound').stop()
                    global_var.get_value('select_sound').play()
            if not (pressed_keys[K_RIGHT] and pressed_keys_last[K_RIGHT]):
                if pressed_keys[K_RIGHT]:
                    self.selectNum[self.menuStair]+=1
                    global_var.get_value('select_sound').stop()
                    global_var.get_value('select_sound').play()
        elif self.menuStair==3:
            if not (pressed_keys[K_LEFT] and pressed_keys_last[K_LEFT]):
                if pressed_keys[K_LEFT]:
                    self.testSpellNum-=1
                    self.substract=True
                    global_var.get_value('select_sound').stop()
                    global_var.get_value('select_sound').play()
            if not (pressed_keys[K_RIGHT] and pressed_keys_last[K_RIGHT]):
                if pressed_keys[K_RIGHT]:
                    self.testSpellNum+=1
                    self.plus=True
                    global_var.get_value('select_sound').stop()
                    global_var.get_value('select_sound').play()
            if self.testSpellNum>10:
                self.testSpellNum=1
            elif self.testSpellNum<1:
                self.testSpellNum=10
            if not (pressed_keys[K_DOWN] and pressed_keys_last[K_DOWN]):
                if pressed_keys[K_DOWN]:
                    self.ifSpell=False
                    global_var.get_value('select_sound').stop()
                    global_var.get_value('select_sound').play()
            if not (pressed_keys[K_UP] and pressed_keys_last[K_UP]):
                if pressed_keys[K_UP]:
                    self.ifSpell=True
                    global_var.get_value('select_sound').stop()
                    global_var.get_value('select_sound').play()
            if not self.ifSpell and self.testSpellNum==10:
                if self.substract:
                    self.testSpellNum=9
                elif self.plus:
                    self.testSpellNum=1
                else:
                    self.ifSpell=True
            self.substract=False
            self.plus=False
        if (pressed_keys[K_ESCAPE]!=pressed_keys_last[K_ESCAPE] and pressed_keys[K_ESCAPE]) or (pressed_keys[K_x]!=pressed_keys_last[K_x] and pressed_keys[K_x]):
            if self.menuStair>0:
                self.menuStair-=1
                global_var.get_value('cancel_sound').play()
            else:
                if self.selectNum[0]!=7:
                    self.selectNum[0]=7
                    global_var.get_value('cancel_sound').play()
                else:
                    global_var.get_value('cancel_sound').play()
                    sys.exit()
        if self.selectNum[self.menuStair]>self.stairMax[self.menuStair]:
            self.selectNum[self.menuStair]=0
        elif self.selectNum[self.menuStair]<0:
            self.selectNum[self.menuStair]=self.stairMax[self.menuStair]
    def drawSign(self,screen,titleDec):
        #stars
        if self.menuStair!=0:
            for entity in titleDec:
                entity.update(screen,titleDec)

        if self.menuStair==0:
            screen.blit(self.tachie,(round(400*self.amplified_times),round(60*self.amplified_times)))
            for entity in titleDec:
                entity.update(screen,titleDec)
            self.logoPosAdj=[math.sin(self.lastFrame*math.pi/180)*20,math.sin(self.lastFrame*0.5*math.pi/180)*3*self.amplified_times]
            screen.blit(self.kanjiLogo,(round(66*self.amplified_times+self.logoPosAdj[0]),round(20*self.amplified_times+self.logoPosAdj[1])))
            self.lightStrength=0.5*math.sin(self.lastFrame*2*math.pi/180)+0.5
            alpha=round(self.lightStrength*256)
            self.lightLogo.set_alpha(alpha)
            screen.blit(self.lightLogo,(round(66*self.amplified_times),round(110*self.amplified_times)))
            screen.blit(self.engLogo,(round(66*self.amplified_times),round(110*self.amplified_times)))
            for i in range(0,8):
                if i!=self.selectNum[self.menuStair]:
                    screen.blit(self.shadow[i],(round(66*self.amplified_times),round((166+i*32)*self.amplified_times)))
                else:
                    screen.blit(self.sign[i],(round(66*self.amplified_times),round((166+i*32)*self.amplified_times)))
        elif self.menuStair==1:
            screen.blit(self.selectImg[0],(round(26*self.amplified_times),(round(6.6*self.amplified_times))))
            screen.blit(self.levelImg[0],(round(192*self.amplified_times),round(176*self.amplified_times)))
        elif self.menuStair==2:
            if self.selectNum[0]==0 or self.selectNum[0]==2:
                screen.blit(self.selectImg[1],(round(26*self.amplified_times),(round(6.6*self.amplified_times))))
                for i in range(0,2):
                    self.playerTitleImg[i].set_alpha(256)
                if self.selectNum[2]==0:
                    self.playerTitleImg[1].set_alpha(100)
                elif self.selectNum[2]==1:
                    self.playerTitleImg[0].set_alpha(100)
                for i in range(0,2):
                    screen.blit(self.playerTitleImg[i],(round(300*i*self.amplified_times),round(80*self.amplified_times)))
        elif self.menuStair==3:
            if self.selectNum[0]==2:
                if self.ifSpell:
                    pracText=self.font.render('Test: Start From Spell No.'+str(self.testSpellNum),True,(255,255,255))
                else:
                    pracText=self.font.render('Test: Start From non-Spell No.'+str(self.testSpellNum),True,(255,255,255))
                screen.blit(pracText,(200,300))

    def doSelection(self,pressed_keys,pressed_keys_last,player):
        if pressed_keys[K_z]!=pressed_keys_last[K_z] and pressed_keys[K_z]:
            if self.menuStair==0:
                if self.selectNum[self.menuStair]==0:
                    global_var.get_value('ok_sound').play()
                    self.menuStair+=1
                elif self.selectNum[self.menuStair]==2:
                    global_var.get_value('ok_sound').play()
                    self.menuStair+=1
                elif self.selectNum[self.menuStair]==7:
                    global_var.get_value('ok_sound').play()
                    pygame.quit()
                    sys.exit()
                else:
                    global_var.get_value('invalid_sound').stop()
                    global_var.get_value('invalid_sound').play()
            elif self.menuStair==1:
                if self.selectNum[0]==0 or self.selectNum[0]==2: 
                    if self.selectNum[self.menuStair]==0 or self.selectNum[self.menuStair]==1:
                        global_var.get_value('ok_sound').play()
                        global_var.set_value('levelSign',self.selectNum[self.menuStair])
                        self.menuStair+=1
            elif self.menuStair==2:
                if self.selectNum[0]==0:
                    if self.selectNum[self.menuStair]==0:
                        global_var.set_value('playerNum',0)
                    elif self.selectNum[self.menuStair]==1:
                        global_var.set_value('playerNum',1)
                    global_var.get_value('ok_sound').play()
                    global_var.get_value('ok_sound').play()
                    global_var.set_value('ifTest',False)
                    pygame.mixer.music.stop()
                    self.menuStair=0
                    global_var.set_value('menu',False)
                    self.playerReset=True
                if self.selectNum[0]==2:
                    if self.selectNum[self.menuStair]==0:
                        global_var.set_value('playerNum',0)
                    elif self.selectNum[self.menuStair]==1:
                        global_var.set_value('playerNum',1)
                    global_var.get_value('ok_sound').play()
                    self.menuStair+=1
            elif self.menuStair==3:
                if self.selectNum[0]==2:
                    global_var.get_value('ok_sound').play()
                    global_var.set_value('ifTest',True)
                    global_var.set_value('ifSpellTest',self.ifSpell)
                    global_var.set_value('spellNum',self.testSpellNum)
                    pygame.mixer.music.stop()
                    '''
                    pygame.mixer.music.load('resource/bgm/lightnessOnTheWay.mp3')   # 载入背景音乐文件
                    #pygame.mixer.music.load('resource/bgm/上海アリス幻樂団 - 死体旅行~ Be of good cheer!.mp3')
                    pygame.mixer.music.set_volume(0.6)                  # 设定背景音乐音量
                    pygame.mixer.music.play(loops=-1)'''
                    self.menuStair=0

                    global_var.set_value('menu',False)
                    self.playerReset=True