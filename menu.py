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
        self.selectNum=[0,0,0]
        self.stairMax=[7,0,1]
        self.menuStair=0 #0:main menu, 1 stage selection, 2 player selection
        self.playerReset=False
    def update(self,screen,pressed_keys,pressed_keys_last,player):
        screen.blit(self.image,(0,0))
        self.alterSelect(pressed_keys,pressed_keys_last)
        self.drawSign(screen)
        self.doSelection(pressed_keys,pressed_keys_last,player)
    def alterSelect(self,pressed_keys,pressed_keys_last):
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
        if self.selectNum[self.menuStair]>self.stairMax[self.menuStair]:
            self.selectNum[self.menuStair]=0
        elif self.selectNum[self.menuStair]<0:
            self.selectNum[0]=self.stairMax[self.menuStair]
    def drawSign(self,screen):
        if self.menuStair==0:
            for i in range(0,8):
                if i!=self.selectNum[self.menuStair]:
                    screen.blit(self.shadow[i],(100,250+i*48))
                else:
                    screen.blit(self.sign[i],(100,250+i*48))
        elif self.menuStair==1:
            pass
        elif self.menuStair==2:
            for i in range(0,2):
                self.playerTitleImg[i].set_alpha(256)
            if self.selectNum[2]==0:
                self.playerTitleImg[1].set_alpha(100)
            elif self.selectNum[2]==1:
                self.playerTitleImg[0].set_alpha(100)
            for i in range(0,2):
                screen.blit(self.playerTitleImg[i],(450*i,0))
        
    def doSelection(self,pressed_keys,pressed_keys_last,player):
        if pressed_keys[K_z]!=pressed_keys_last[K_z] and pressed_keys[K_z]:
            if self.menuStair==0:
                if self.selectNum[self.menuStair]==0:
                    global_var.get_value('ok_sound').play()
                    self.menuStair+=1
                if self.selectNum[self.menuStair]==7:
                    global_var.get_value('ok_sound').play()
                    sys.exit()
            elif self.menuStair==1:
                if self.selectNum[self.menuStair]==0:
                    global_var.get_value('ok_sound').play()
                    self.menuStair+=1
            elif self.menuStair==2:
                if self.selectNum[self.menuStair]==0:
                    global_var.set_value('playerNum',0)
                elif self.selectNum[self.menuStair]==1:
                    global_var.set_value('playerNum',1)
                global_var.get_value('ok_sound').play()
                pygame.mixer.music.load('resource/bgm/lightnessOnTheWay.mp3')   # 载入背景音乐文件
                #pygame.mixer.music.load('resource/bgm/上海アリス幻樂団 - 死体旅行~ Be of good cheer!.mp3')
                pygame.mixer.music.set_volume(0.6)                  # 设定背景音乐音量
                pygame.mixer.music.play(loops=-1)
                self.menuStair=0
                global_var.set_value('menu',False)
                self.playerReset=True