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
import lightnessLevel




#define background

angle = 0
FPS = 60 # 帧率 
fpsClock = pygame.time.Clock()
#global variable area 

#initialize gaming
frame=0
pygame.init
pygame.font.init() #initialize font
pygame.mixer.init()
pygame.mixer.set_num_channels(30)
size = width,height = 960,720
fullscreen = True
screen = pygame.display.set_mode(size,RESIZABLE|DOUBLEBUF)
#size = width, height =  pygame.display.list_modes()[0]
screen = pygame.display.set_mode(size,FULLSCREEN | HWSURFACE| DOUBLEBUF)
stage=pygame.Surface((960,720)).convert_alpha()
stage.set_clip(Rect(60,30,600,660))
global_var._init()

#test functions 
global_var.set_value('ifTest',True)
global_var.set_value('spellNum',5)
global_var.set_value('ifSpellTest',True)
testFire=400
 
#screen=pygame.display.set_mode((640,480))
pygame.display.set_caption("Touhou Star Salvation")
back=pygame.image.load('resource/background.jpg').convert_alpha()
point=pygame.image.load('resource/point.png').convert_alpha()
point2=pygame.image.load('resource/point2.png').convert_alpha()
point=pygame.transform.smoothscale(point,(96,96))
point2=pygame.transform.smoothscale(point2,(96,96))
point2.set_alpha(128)
myfont = pygame.font.SysFont('arial', 12)
bigfont= pygame.font.SysFont('arial', 24)
midfont=pygame.font.SysFont('arial', 20)
smallfont=pygame.font.SysFont('arial', 16)
levelText1 = myfont.render('Level 1', True, (0, 0, 0))
bossMagic=pygame.image.load('resource/bossMagic.png').convert_alpha()

#load background Pic
back_up=pygame.image.load('resource/up.jpg').convert_alpha()
global_var.set_value('up', back_up)
back_down=pygame.image.load('resource/down.jpg').convert_alpha()
global_var.set_value('down', back_down)
back_left=pygame.image.load('resource/left.jpg').convert_alpha()
global_var.set_value('left', back_left)
back_right=pygame.image.load('resource/right.jpg').convert_alpha()
global_var.set_value('right', back_right)

global_var.set_value('boomStatu',0)
global_var.set_value('grazeNum',0)
global_var.set_value('fpSec',0)
global_var.set_value('enemyPos',(0,0,10000))
global_var.set_value('shift_down',False)
log = open("./log.csv", 'w+')
#main loop controller 
running = True

##back.image=pygame.image.load("resource/background.jpg")
#create class

#init player position
gF.loadImage()
player = DADcharacter.Reimu()
player.tx=357.0
player.ty=600.0
###
player.power=100
if global_var.get_value('ifTest'):
    player.power=testFire
diffLevel=1
#barrier1=Bullet.bulletBarrier()
global_var.set_value('getTicksLastFrame',0)
global_var.set_value('enemySum',0)
blinder=pygame.Surface((780,200))
blinder.fill((0,0,0))
#testBullet=Bullet.small_Bullet()

bullets=pygame.sprite.Group()
bullets2=pygame.sprite.Group()
playerGuns=pygame.sprite.Group()
enemys=pygame.sprite.Group()
slaves=pygame.sprite.Group()
booms=pygame.sprite.Group()
effects=pygame.sprite.Group()
stars=pygame.sprite.Group()
items=pygame.sprite.Group()
backgrounds=pygame.sprite.Group()
bosses=pygame.sprite.Group()
gameRule.addStars(screen,stars)
gF.doBackground(screen,backgrounds)


#loadSoundEffects
miss_sound=pygame.mixer.Sound('resource/sound/se_pldead00.wav')
miss_sound.set_volume(0.2)
shoot_sound=pygame.mixer.Sound('resource/sound/se_plst00.wav')
shoot_sound.set_volume(0.15)
hit_sound1=pygame.mixer.Sound('resource/sound/se_damage00.wav')
hit_sound1.set_volume(0.2)
global_var.set_value('hit_sound1',hit_sound1)
hit_sound2=pygame.mixer.Sound('resource/sound/se_damage01.wav')
hit_sound2.set_volume(0.2)
global_var.set_value('hit_sound2',hit_sound2)
enemyDead_sound=pygame.mixer.Sound('resource/sound/se_enep00.wav')
enemyDead_sound.set_volume(0.15)
global_var.set_value('enemyDead_sound',enemyDead_sound)
bossDead_sound=pygame.mixer.Sound('resource/sound/se_enep01.wav')
bossDead_sound.set_volume(0.30)
global_var.set_value('bossDead_sound',bossDead_sound)
enemyGun_sound1=pygame.mixer.Sound('resource/sound/se_tan00.wav')
enemyGun_sound1.set_volume(0.1)
global_var.set_value('enemyGun_sound1',enemyGun_sound1)
enemyGun_sound2=pygame.mixer.Sound('resource/sound/se_tan01.wav')
enemyGun_sound2.set_volume(0.1)
global_var.set_value('enemyGun_sound2',enemyGun_sound2)
enemyGun_sound3=pygame.mixer.Sound('resource/sound/se_tan02.wav')
enemyGun_sound3.set_volume(0.1)
global_var.set_value('enemyGun_sound3',enemyGun_sound3)
slash_sound=pygame.mixer.Sound('resource/sound/se_slash.wav')
slash_sound.set_volume(0.5)
item_get=pygame.mixer.Sound('resource/sound/se_item00.wav')
item_get.set_volume(0.12)
global_var.set_value('item_get',item_get)
life_get=pygame.mixer.Sound('resource/sound/se_extend.wav')
life_get.set_volume(0.35)
global_var.set_value('life_get',life_get)
water_sound=pygame.mixer.Sound('resource/sound/se_water.wav')
water_sound.set_volume(0.2)
global_var.set_value('water_sound',water_sound)
kira_sound=pygame.mixer.Sound('resource/sound/se_kira00.wav')
kira_sound.set_volume(0.1)
global_var.set_value('kira_sound',kira_sound)
kira1_sound=pygame.mixer.Sound('resource/sound/se_kira01.wav')
kira1_sound.set_volume(0.1)
global_var.set_value('kira1_sound',kira1_sound)
powerup_sound=pygame.mixer.Sound('resource/sound/se_powerup.wav')
powerup_sound.set_volume(0.3)
global_var.set_value('powerup_sound',powerup_sound)
ch00_sound=pygame.mixer.Sound('resource/sound/se_ch00.wav')
ch00_sound.set_volume(0.3)
global_var.set_value('ch00_sound',ch00_sound)
timeout_sound=pygame.mixer.Sound('resource/sound/se_timeout.wav')
timeout_sound.set_volume(0.25)
global_var.set_value('timeout_sound',timeout_sound)
bonus_sound=pygame.mixer.Sound('resource/sound/se_bonus.wav')
bonus_sound.set_volume(0.25)
global_var.set_value('bonus_sound',bonus_sound)
spell_sound=pygame.mixer.Sound('resource/sound/se_cat00.wav')
spell_sound.set_volume(0.50)
global_var.set_value('spell_sound',spell_sound)
laser_sound=pygame.mixer.Sound('resource/sound/se_lazer00.wav')
laser_sound.set_volume(0.18)
global_var.set_value('laser_sound',laser_sound)
option_sound=pygame.mixer.Sound('resource/sound/se_option.wav')
option_sound.set_volume(0.2)
global_var.set_value('option_sound',option_sound)
graze_sound=pygame.mixer.Sound('resource/sound/se_graze.wav')
graze_sound.set_volume(0.3)
global_var.set_value('graze_sound',graze_sound)
nep_sound=pygame.mixer.Sound('resource/sound/se_nep00.wav')
nep_sound.set_volume(0.3)
global_var.set_value('nep_sound',nep_sound)
spell_end=pygame.mixer.Sound('resource/sound/se_enep02.wav')
spell_end.set_volume(0.35)
global_var.set_value('spell_end',spell_end)

pygame.mixer.music.load('resource/bgm/lightnessOnTheWay.mp3')   # 载入背景音乐文件
#pygame.mixer.music.load('resource/bgm/上海アリス幻樂団 - 死体旅行~ Be of good cheer!.mp3')

pygame.mixer.music.set_volume(0.6)                  # 设定背景音乐音量

pygame.mixer.music.play(loops=-1)
global_var.set_value('ifBoss',False)
global_var.set_value('pressingX',False)
global_var.set_value('DELTA_T',17)
if global_var.get_value('ifTest'):
    frame=10020#for test
global_var.set_value('ifShaking',False)
global_var.set_value('shakeFrame',0)
d_x=random.randint(-2,2)
d_y=random.randint(-8,8)
pygame.mouse.set_visible(False)

# Main loop
while running:
    stage.fill((0,0,0))
    screen.fill((0,0,0))
    DELTA_T=fpsClock.tick(FPS)
    global_var.set_value('DELTA_T',DELTA_T)

    global_var.set_value('grazing',False)
    global_var.set_value('item_getting',False) 
    global_var.set_value('enemyFiring1',False)
    global_var.set_value('enemyFiring2',False)
    global_var.set_value('enemyFiring3',False)
    global_var.set_value('kiraing',False)
    global_var.set_value('hitting',False)
        

    bulletSum=0
    enemySum=0
    frame+=1
    frameText = myfont.render('F: '+str(frame), True, (255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        #if event.type == addBullet:
            
    #diffLevel:
    if frame>=600*60:
        diffLevel=5
    elif frame>=300*60:
        diffLevel=4
    elif frame>=120*60:
        diffLevel=3
    elif frame>=60*60:
        diffLevel=2
    

    #check keys
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys,frame) 
    global_var.set_value('player1x', player.cx)
    global_var.set_value('player1y', player.cy)
    
    if pressed_keys[K_F11]:
        sys.exit()
    

    #create enemy
    #Enemy generator now disabled and substituted by stage controller

    lightnessLevel.stageController(stage,frame,enemys,bullets,slaves,items,effects,backgrounds,bosses,player)

    #draw objects
    if not global_var.get_value('ifBoss') and frame<=10600:
        stage.fill((0,0,0)) #remeber to fill the screen background first

    #player fire
    if pressed_keys[K_z]:
        player.fire(frame,stage,playerGuns)
        if frame%5==0:
            shoot_sound.stop()
            shoot_sound.play()
    
    for background in backgrounds:
        background.update(stage)
    
    

    #lowspeed mode display and effect
    if pressed_keys[K_LSHIFT]:
        angle=angle-2
        global_var.set_value('shift_down', True)
        player.itemCollectDistance=100
        if angle<=0:
            angle=360
        gF.drawRotation(point2,(player.rect.centerx-48,player.rect.centery-48),-angle,stage)
    else:
        global_var.set_value('shift_down', False)
        player.itemCollectDistance=50


    #boss magic and effect

    #group update
    for playerGun in playerGuns:
        playerGun.update(stage)
    
    for effect in effects:
        if effect.lower:
            effect.update(stage)
    
    global_var.set_value('enemyPos',(0,0,10000))
    for enemy in enemys:
        enemy.update(stage,frame,bullets,bullets2,effects,items)
        enemySum+=1


    for boss in bosses:
        boss.update(stage,frame,items,effects,bullets,backgrounds,enemys,slaves,player)

    #player miss & display effect
    gameRule.drawPlayer(stage,player,frame)

    gameRule.itemAllGet(items,player,effects)

    

    for item in items:
        item.update(stage,player)
        if item.distance<=player.itemCollectDistance:
            item.followPlayer=1
        if item.type==0 and player.power==400:
            item.type=4
            item.initial(item.tx,item.ty)
            if player.lastLevel==3:
                new_effect=Effect.wave()
                new_effect.initial((item.tx,item.ty),25,8,(67,247,17),5)
                effects.add(new_effect)
        if item.type==3 and player.power==400:
            item.type=2
            item.initial(item.tx,item.ty)
            if player.lastLevel==3:
                new_effect=Effect.wave()
                new_effect.initial((item.tx,item.ty),25,8,(67,247,17),5)
                effects.add(new_effect)
    
    #watchers & effect generator
    if player.lastLevel<=3 and player.power>=400:
        new_effect=Effect.powerMaxText()
        effects.add(new_effect)

    if player.lastLife<player.life:
        new_effect=Effect.extendText()
        effects.add(new_effect)
    
    if player.lastGraze<player.graze:
        new_effect=Effect.grazeEffect()
        new_effect.initial((player.tx,player.ty),4,random.randint(15,20),(255,255,255),5,1,20)
        effects.add(new_effect)

    for effect in effects:
        if not (effect.upper or effect.lower):
            effect.update(stage)
        
    for bullet in bullets:
        bulletSum+=1
        bullet.update(stage,bullets,effects)

    for effect in effects:
        if effect.upper:
            effect.update(stage)

    
    for slave in slaves:
        slave.update(stage,frame,bullets,effects,items)

    
    
    
    for star in stars:
        pass
        #star.update(screen)

    #collide detectž
    gameRule.missDetect(player,bullets,enemys,effects,miss_sound,items,slaves)
    


    #boom key
    gameRule.doBoom(player,booms,pressed_keys,slash_sound,items)

    for boom in booms:
        boom.update(stage)
        #if boom.lastFrame==598:
            #slash_sound.play()
        if boom.lastFrame==599 and boom.ifBoss==False:
            #gameRule.cancalAllBullet(bullets,items,effects,True)
            gameRule.addLastingCancel(boom.tx,boom.ty,slaves,20,True)
            for enemy in enemys:
                enemy.health-=2000
            slash_sound.play()
            new_effect=Effect.wave()
            new_effect.initial([boom.tx,boom.ty],900,20,(244,213,87),6)
            effects.add(new_effect)
            global_var.get_value('nep_sound').stop()
        elif boom.ifBoss and boom.lastFrame==399:
            #gameRule.cancalAllBullet(bullets,items,effects,True)
            gameRule.addLastingCancel(boom.tx,boom.ty,slaves,20,True)
            for enemy in enemys:
                enemy.health-=2000
            slash_sound.play()
            new_effect=Effect.wave()
            new_effect.initial([boom.tx,boom.ty],900,20,(244,213,87),6)
            effects.add(new_effect)
            global_var.get_value('nep_sound').stop()
        if boom.lastFrame>=5 and pressed_keys[K_x] and not global_var.get_value('pressingX'):
            #gameRule.cancalAllBullet(bullets,items,effects,True)
            gameRule.addLastingCancel(boom.tx,boom.ty,slaves,20,True)
            for enemy in enemys:
                enemy.health-=2000
            slash_sound.play()
            global_var.set_value('boomStatu',0)
            boom.kill()
            new_effect=Effect.wave()
            new_effect.initial([boom.tx,boom.ty],900,20,(244,213,87),6)
            effects.add(new_effect)
            global_var.get_value('nep_sound').stop()

    #key
    if pressed_keys[K_LSHIFT]:
        gF.drawRotation(point,(player.rect.centerx-48,player.rect.centery-48),angle,stage)


    

    

    #detect enemy hitten
    gameRule.hitEnemy(enemys,playerGuns,booms,bullets,effects,frame,player,items,bosses)
    
    #avoid continues boom key
    if pressed_keys[K_x]:
        global_var.set_value('pressingX',True)
    else:
        global_var.set_value('pressingX',False)

    #life number displayment
    missText=myfont.render('Life: '+str(player.life), True, (255, 255, 255))

    stage.blit(missText,(200,0))

    gF.shakeScreen()
    #drawStage
    if global_var.get_value('ifShaking'):
        if frame%4==0:
            d_x=random.randint(-4,4)
            d_y=random.randint(-4,4)
        screen.blit(stage,(0+d_x,0+d_y))
    else:
        screen.blit(stage,(60,30),(60,30,600,660))
    
    #drawCover
    gF.drawBackground(screen)
    pygame.draw.rect(screen,(255,255,255),(58,28,603,663),2)
    missFrame=myfont.render('miss: '+str(player.deadFrame), True, (255, 255, 255))
    screen.blit(missFrame,(250,0))
    gF.displayMenu(screen,stars)
    for boss in bosses:
        boss.drawHealthBar(screen)
        boss.drawTimer(screen,midfont)
        boss.drawSpellName(screen,midfont,player)
        boss.drawCardBonus(screen,smallfont,player)
        boss.drawBossName(screen)
        boss.drawSpellNum(screen)
        boss.displayPercentHealth(screen,myfont)

    gF.showFpsBullet(screen,bigfont,frame,bulletSum,log)
    gameRule.displayUi(screen,player,bigfont)
    screen.blit(frameText,(0,0))
    gF.drawBlinder(screen,blinder)

    global_var.set_value('enemySum',enemySum)
    global_var.set_value('bulletSum',bulletSum)
    pygame.display.flip()
    #pygame.display.update()
    
    
    

