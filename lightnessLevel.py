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

def stageController(screen,frame,enemys,bullets,slaves,items,effects,backgrounds,bosses,player):
    #part1 F300~F600:
    if frame>=300 and frame<=600:
        if frame%30==0:
            new_enemy=DADcharacter.spirit_part1_1()
            new_enemy.initialize(690,340,1,-1)
            enemys.add(new_enemy)
        if frame%45==0:
            new_enemy=DADcharacter.spirit_part1_2()
            new_enemy.initialize(50,340,1,-1)
            enemys.add(new_enemy)
    
    #part2 F650~1000:
    if frame>=650 and frame<=1000:
        if frame%36==0:
            new_enemy=DADcharacter.ghost_part2_1()
            new_enemy.initialize(50,190,1,1)
            enemys.add(new_enemy)
    
    #part3 F1000~1400:
    if frame>=1000 and frame<=1400:
        if frame%30==0:
            new_enemy=DADcharacter.ghost_part3_1()
            new_enemy.initialize(670,120,1,0)
            enemys.add(new_enemy)

    #part4 F=1600~1900
    if frame==1600:
        new_enemy=DADcharacter.butterfly_part4_1()
        new_enemy.initialize(360,20,1,-1)
        enemys.add(new_enemy)

    if frame>=1700 and frame<=1900:
        if frame%20==0:
            new_enemy=DADcharacter.spirit_part4_1()
            new_enemy.initialize(50,200+random.random()*50-25,1,-1)
            enemys.add(new_enemy)

    #part5 F2000~2500

    if frame==2050:
        new_enemy=DADcharacter.butterfly_part5_1()
        new_enemy.initialize(360,20,1,-1)
        enemys.add(new_enemy)
    
    if frame>=2300 and frame<=2500:
        if frame%20==0:
            new_enemy=DADcharacter.spirit_part5_1()
            new_enemy.initialize(670,200+random.random()*50-25,1,-1)
            enemys.add(new_enemy)

    #part6 F2500~3250
    if frame>=2500 and frame<=3250:
        if frame%50==0:
            if frame%250==0:
                new_enemy=DADcharacter.spirit_part6_1()
                new_enemy.initialize(460,20,1,-1)
                enemys.add(new_enemy)
            elif frame%200==0:
                new_enemy=DADcharacter.spirit_part6_1()
                new_enemy.initialize(260,20,1,-1)
                enemys.add(new_enemy)
            elif frame%150==0:
                new_enemy=DADcharacter.spirit_part6_1()
                new_enemy.initialize(510,20,1,-1)
                new_enemy.num=1
                enemys.add(new_enemy)
            elif frame%100==0:
                new_enemy=DADcharacter.spirit_part6_1()
                new_enemy.initialize(360,20,1,-1)
                new_enemy.num=1
                enemys.add(new_enemy)
            else:
                new_enemy=DADcharacter.spirit_part6_1()
                new_enemy.initialize(210,20,1,-1)
                new_enemy.num=1
                enemys.add(new_enemy)
    #part7 mid-path boss F3300~8000
    
    #bullet all cancel
    if frame==3300:
        gameRule.cancalAllBullet(bullets,items,effects,True)
        for enemy in enemys:
            enemy.health-=100000

    if frame==3301:
        for item in items:
            item.followPlayer=1
            item.followSpeed=9
        new_boss=DADcharacter.satori()
        new_boss.initial(360,200)
        bosses.add(new_boss)
        global_var.get_value('ch00_sound').play()
    '''
    if frame==3400:
        for boss in bosses:
            boss.gotoPosition(200,100,40)
    '''
    if frame==3600:
        for boss in bosses:
            boss.cardNum=1
    
    #part7* after-boss ~F8600
    if player.midPath and frame<=8600:
        if frame%60==0:
            r=random.random()*100-50
            new_enemy=DADcharacter.spirit_part7_1()
            new_enemy.initialize(680,250+r,1,-1)
            enemys.add(new_enemy)
        if frame%60==30:
            r=random.random()*100-50
            new_enemy=DADcharacter.spirit_part7_2()
            new_enemy.initialize(20,250+r,1,-1)
            enemys.add(new_enemy)
    
    #part 8 8750~9500:
    if frame==8750:
        new_enemy=DADcharacter.butterfly_part8_1()
        new_enemy.initialize(360,20,1,-1)
        enemys.add(new_enemy)
    
    #part 9 F9600~10300:
    if frame==9400:
        new_enemy=DADcharacter.butterfly_part9_1()
        new_enemy.initialize(540,20,1,-1)
        enemys.add(new_enemy)
        new_enemy=DADcharacter.butterfly_part9_2()
        new_enemy.initialize(180,20,1,-1)
        enemys.add(new_enemy)

    #part Final FF10300~ Boss fight
    if frame==10400:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('resource/bgm/lightnessBoss.mp3') 
        #pygame.mixer.music.load('resource/bgm/上海アリス幻樂団 - 死体旅行~ Be of good cheer!.mp3') 
        
        pygame.mixer.music.set_volume(0.6)       
        new_boss=DADcharacter.Dumbledore()
        new_boss.initial(800,-100)
        bosses.add(new_boss)
    if frame>=10400 and frame<=10600:
        for background in backgrounds:
            background.surf.set_alpha(200-round((frame-10400)))

    if frame>=10600 and frame<=10800:
        screen.fill((0,0,0))
        back_image=global_var.get_value('hogwarts_background')
        back_image.set_alpha(round(frame-10600)/200*256)
        screen.blit(back_image,(30,184))

    if frame==10600:
        for boss in bosses:
            boss.gotoPosition(360,220,100)
            

    if frame==10700:
        global_var.get_value('ch00_sound').play()
    if frame==10800:
        pygame.mixer.music.play(loops=-1)
        for background in backgrounds:
            background.kill()
        global_var.set_value('ifBoss',True)
    
    if frame>=10800:
        screen.fill((0,0,0))
        back_image=global_var.get_value('stars_background')
        #back_image.set_alpha(round(math.sin(((frame-300)/3)/180*math.pi)*128+128))

        lastFrame=0
        ifSpell=False
        alpha=0
        cardNum=0
        for boss in bosses:
            lastFrame=boss.lastFrame
            ifSpell=boss.ifSpell
            cardNum=boss.cardNum
        if ifSpell:
            if lastFrame<=128:
                alpha=0+round(2*lastFrame)
            else:
                #alpha=round(180+76*math.sin((lastFrame+180-128)*math.pi/180*0.5))
                alpha=256
        else:
            if cardNum==1:
                alpha=0
            else:
                if lastFrame<=128:
                    alpha=256-round(lastFrame*(256/128))
                else:
                    alpha=0
        
        back_image.set_alpha(alpha)




        screen.blit(back_image,(60,30))
        #gF.drawRotation(global_var.get_value('stars_background'),(-90,-90),round((frame%10800)/10800*360),screen)
        screen.blit(global_var.get_value('hogwarts_background'),(30,184))
        
    if frame==10900:
        for boss in bosses:
            boss.cardNum=1
            if global_var.get_value('ifTest'):
                boss.cardNum=global_var.get_value('spellNum')#for test only
                boss.ifSpell=global_var.get_value('ifSpellTest')