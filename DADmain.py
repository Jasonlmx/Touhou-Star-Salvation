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
import menu

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
#screen = pygame.display.set_mode(size,FULLSCREEN | HWSURFACE| DOUBLEBUF)
stage=pygame.Surface((960,720)).convert_alpha()
stage.set_clip(Rect(60,30,600,660))
global_var._init()

#test functions 
global_var.set_value('ifTest',False)
global_var.set_value('spellNum',1)
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
global_var.set_value('pause',False)
global_var.set_value('escPressing',False)
global_var.set_value('pauseScreen',0)
global_var.set_value('ifStopPressing',False)
global_var.set_value('menu',True)
global_var.set_value('ifGameOver',False)
global_var.set_value('bgmPauseFlag',0)
global_var.set_value('bgmContinuePos',[0,0])#[0]->for mid stage,[1]->for boss fight
log = open("./log.csv", 'w+')
#main loop controller 
running = True

##back.image=pygame.image.load("resource/background.jpg")
#create class

#init player position
gF.loadImage()
playerNum=0
global_var.set_value('playerNum',playerNum)
if playerNum==0:
    player = DADcharacter.Reimu()
elif playerNum==1:
    player = DADcharacter.Marisa()
player.tx=357.0
player.ty=600.0
###
player.power=100
if global_var.get_value('ifTest'):
    player.power=testFire
diffLevel=1
mainMenu=menu.Menu()
pressed_keys_last=pygame.key.get_pressed()
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
pause_sound=pygame.mixer.Sound('resource/sound/se_pause.wav')
pause_sound.set_volume(0.35)
global_var.set_value('pause_sound',pause_sound)
select_sound=pygame.mixer.Sound('resource/sound/se_select00.wav')
select_sound.set_volume(0.35)
global_var.set_value('select_sound',select_sound)
ok_sound=pygame.mixer.Sound('resource/sound/se_ok00.wav')
ok_sound.set_volume(0.35)
global_var.set_value('ok_sound',ok_sound)
cancel_sound=pygame.mixer.Sound('resource/sound/se_cancel00.wav')
cancel_sound.set_volume(0.35)
global_var.set_value('cancel_sound',cancel_sound)
invalid_sound=pygame.mixer.Sound('resource/sound/se_invalid.wav')
invalid_sound.set_volume(0.35)
global_var.set_value('invalid_sound',invalid_sound)
reimuBoom_sound=pygame.mixer.Sound('resource/sound/se_tan00.wav')
reimuBoom_sound.set_volume(0.40)
global_var.set_value('reimuBoom_sound',reimuBoom_sound)


pygame.mixer.music.load('resource/bgm/mainTitle.mp3')
pygame.mixer.music.set_volume(0.6)   
pygame.mixer.music.play(loops=-1)

global_var.set_value('ifBoss',False)
global_var.set_value('pressingX',False)
global_var.set_value('DELTA_T',17)
if global_var.get_value('ifTest'):
    frame=10020#for test
global_var.set_value('ifShaking',False)
global_var.set_value('shakeFrame',0)
global_var.set_value('restarting',False)
d_x=random.randint(-2,2)
d_y=random.randint(-8,8)
pygame.mouse.set_visible(False)

# Main loop
while running:
    #check keys
    pressed_keys = pygame.key.get_pressed()
    if not global_var.get_value('menu'):
        gF.doPause(pressed_keys,stage)
        if not global_var.get_value('pause'):
            gameRule.checkLife(player,stage)

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
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    if pressed_keys[K_F11]:
            sys.exit()

    if not global_var.get_value('menu'):
        bulletSum=0
        enemySum=0
        boomSum=0
        if not global_var.get_value('pause'):
            frame+=1
            if global_var.get_value('restarting'):
                frame=0
                if global_var.get_value('ifTest'):
                    frame=10020#for test
                global_var.set_value('restarting',False)
        frameText = myfont.render('F: '+str(frame), True, (255, 255, 255))
        
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
        

        
        global_var.set_value('escPressing',pressed_keys[K_ESCAPE])
        if not global_var.get_value('pause'):
            player.update(pressed_keys,frame) 
        global_var.set_value('player1x', player.cx)
        global_var.set_value('player1y', player.cy)
        
        
        

        #create enemy
        #Enemy generator now disabled and substituted by stage controller
        if not global_var.get_value('pause'):
            lightnessLevel.stageController(stage,frame,enemys,bullets,slaves,items,effects,backgrounds,bosses,player)

        #draw objects
        if not global_var.get_value('ifBoss') and frame<=10600:
            stage.fill((0,0,0)) #remeber to fill the screen background first

        if not global_var.get_value('pause'):

            global_var.set_value('ifStopPressing',False)
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
                boom.update(stage,effects)
                #if boom.lastFrame==598:
                    #slash_sound.play()
                if player.__class__.__name__=="Marisa":
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
                if player.__class__.__name__=="Reimu":
                    boomSum+=1
            if player.__class__.__name__=="Reimu":
                if boomSum==0:
                    global_var.get_value("nep_sound").stop()
                    global_var.set_value('boomStatu',0)
            #key
            if pressed_keys[K_LSHIFT]:
                gF.drawRotation(point,(player.rect.centerx-48,player.rect.centery-48),angle,stage)


            

            

            #detect enemy hitten
            gameRule.hitEnemy(enemys,playerGuns,booms,bullets,effects,frame,player,items,bosses,slaves)
            
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
        gF.pauseScreen(pressed_keys,pressed_keys_last,screen,frame,enemys,bullets,slaves,items,effects,backgrounds,bosses,player,booms,playerGuns)
        gF.drawBackground(screen)
        pygame.draw.rect(screen,(255,255,255),(58,28,603,663),2)
        missFrame=myfont.render('miss: '+str(player.deadFrame), True, (255, 255, 255))
        screen.blit(missFrame,(250,0))
        gF.displayMenu(screen,stars)
        for boss in bosses:
            boss.drawHealthBar(screen)
            boss.drawTimer(screen,midfont)
            if not global_var.get_value('pause'):
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
    else:
        mainMenu.update(screen,pressed_keys,pressed_keys_last,player)
        if mainMenu.playerReset:
            if global_var.get_value('playerNum')==0:
                player=DADcharacter.Reimu()
            elif global_var.get_value('playerNum')==1:
                player=DADcharacter.Marisa()
            mainMenu.playerReset=False
            player.tx=357.0
            player.ty=600.0
            ###
            player.power=100
            if global_var.get_value('ifTest'):
                player.power=testFire
                frame=10020
    pressed_keys_last=pressed_keys
    pygame.display.flip()
    #pygame.display.update()
    
    


