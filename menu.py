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

class Menu():
    def __init__(self):
        super(Menu,self).__init__()
        self.image=pygame.image.load('resource/title/menu.png').convert()
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
        self.selectNum=[0,0,0,0]
        self.stairMax=[7,0,1,1]
        self.menuStair=0 #0:main menu, 1 stage selection, 2 player selection, 3 practice menu
        self.playerReset=False
        self.lightStrength=0.0
        self.logoPosAdj=[0,0]
        self.lastFrame=0
        self.testSpellNum=1
        self.ifSpell=False
        self.substract=False
        self.plus=False
    def update(self,screen,pressed_keys,pressed_keys_last,player):
        self.lastFrame+=1
        if self.lastFrame>360:
            self.lastFrame=self.lastFrame%360
        screen.blit(self.image,(0,0))
        self.alterSelect(pressed_keys,pressed_keys_last)
        self.drawSign(screen)
        self.doSelection(pressed_keys,pressed_keys_last,player)
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
    def drawSign(self,screen):
        if self.menuStair==0:
            self.logoPosAdj=[math.sin(self.lastFrame*math.pi/180)*20,math.sin(self.lastFrame*0.5*math.pi/180)*5]
            screen.blit(self.kanjiLogo,(100+self.logoPosAdj[0],30+self.logoPosAdj[1]))
            self.lightStrength=0.5*math.sin(self.lastFrame*2*math.pi/180)+0.5
            alpha=round(self.lightStrength*256)
            self.lightLogo.set_alpha(alpha)
            screen.blit(self.lightLogo,(100-5,164))
            screen.blit(self.engLogo,(100,164))
            screen.blit(self.tachie,(600,90))
            for i in range(0,8):
                if i!=self.selectNum[self.menuStair]:
                    screen.blit(self.shadow[i],(100,250+i*48))
                else:
                    screen.blit(self.sign[i],(100,250+i*48))
        elif self.menuStair==1:
            screen.blit(self.selectImg[0],(40,10))
            screen.blit(self.levelImg[0],(288,264))
        elif self.menuStair==2:
            if self.selectNum[0]==0 or self.selectNum[0]==2:
                screen.blit(self.selectImg[1],(40,10))
                for i in range(0,2):
                    self.playerTitleImg[i].set_alpha(256)
                if self.selectNum[2]==0:
                    self.playerTitleImg[1].set_alpha(100)
                elif self.selectNum[2]==1:
                    self.playerTitleImg[0].set_alpha(100)
                for i in range(0,2):
                    screen.blit(self.playerTitleImg[i],(450*i,120))
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
                    sys.exit()
                else:
                    global_var.get_value('invalid_sound').stop()
                    global_var.get_value('invalid_sound').play()
            elif self.menuStair==1:
                if self.selectNum[0]==0 or self.selectNum[0]==2: 
                    if self.selectNum[self.menuStair]==0:
                        global_var.get_value('ok_sound').play()
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
                    pygame.mixer.music.load('resource/bgm/lightnessOnTheWay.mp3')   # 载入背景音乐文件
                    #pygame.mixer.music.load('resource/bgm/上海アリス幻樂団 - 死体旅行~ Be of good cheer!.mp3')
                    pygame.mixer.music.set_volume(0.6)                  # 设定背景音乐音量
                    pygame.mixer.music.play(loops=-1)
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
                    pygame.mixer.music.load('resource/bgm/lightnessOnTheWay.mp3')   # 载入背景音乐文件
                    #pygame.mixer.music.load('resource/bgm/上海アリス幻樂団 - 死体旅行~ Be of good cheer!.mp3')
                    pygame.mixer.music.set_volume(0.6)                  # 设定背景音乐音量
                    pygame.mixer.music.play(loops=-1)
                    self.menuStair=0
                    global_var.set_value('menu',False)
                    self.playerReset=True