from typing import NewType
import pygame,sys
import random
import math
from pygame.locals import *
from pygame.sprite import Group
import gF
import Bullet
import Slave
import global_var
import Effect
import Item
import danmaku

class enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(enemy,self).__init__()
        self.surf = pygame.Surface((70,70))
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect()
        self.tx=0.0
        self.ty=0.0
        self.health=200
        self.startFrame=-1
        self.occupy=0
        self.aiType=0
        self.speedx=0
        self.speedy=0
        self.screenRe=0
        self.angle=0
        self.dx=0
        self.dy=0
        self.lastFrame=0
        self.deadImage=pygame.image.load('resource/sprite/sprite_dead.png')
    def checkValid(self,effects,items,bullets):
        if self.rect.bottom<=30 or self.rect.top>=700:
            self.kill()
        if self.rect.right<=20 or self.rect.left>700:
            self.kill()
        if self.health<=0:
            self.doKill(effects,items,bullets)
    
    def speedAlter(self,speedx,speedy):
        self.speedx=speedx
        self.speedy=speedy
    
    def selfTarget(self,playercx,playercy,speed):
        mycx=self.tx
        mycy=self.ty
        dif=math.sqrt(math.pow(playercx-mycx,2)+math.pow(playercy-mycy,2))
        times=dif/speed
        speedx=(playercx-mycx)/times
        speedy=(playercy-mycy)/times
        self.speedAlter(speedx,speedy)

    def setSpeed(self,angle,speed):
        s=math.sin(math.radians(angle))
        c=math.cos(math.radians(angle))
        self.speedy=s*speed
        self.speedx=c*speed

    def initialize(self,centerx,centery,occupy,aiType):
        self.tx=centerx
        self.ty=centery
        self.occupy=occupy
        self.aiType=aiType
        if occupy==2:
            self.screenRe=400
    def truePos(self):
        self.rect.centerx=round(self.tx)
        self.rect.centery=round(self.ty)

    def countAngle(self):
        if self.speedx!=0:
            t=self.speedy/self.speedx
            deg=math.atan(t)*180/math.pi
        else: 
            if self.speedy>0:
                deg=90
            if self.speedy<0:
                deg=270
            if self.speedy==0:
                deg=90
        if deg<0:
            deg+=360
        if self.speedy>0 and deg>=180:
            deg=deg-180
        if self.speedy<0 and deg<=180:
            deg=deg+180
        if self.speedy==0 and self.speedx<0:
            deg=180
        self.angle=deg

    def update(self,screen,frame,bullets,bullets2,effects,items):
        if self.startFrame==-1:
            self.startFrame=frame
        existFrame=frame-self.startFrame
        self.lastFrame+=1
        if existFrame>=10:
            self.checkValid(effects,items,bullets)
        if self.aiType==0:
            self.ai_left()
        if self.aiType==1:
            self.ai_right()
        if self.aiType==2:
            self.ai_down()
        if self.aiType==3:
            self.ai_incline()
        if self.aiType==-1:
            self.ai_move()
        self.tx+=self.speedx
        self.ty+=self.speedy
        self.truePos()
        self.fire(frame,bullets,effects)
        self.draw(screen,frame)
        self.checkDistance()
    
    def checkDistance(self):
        px=global_var.get_value('player1x')
        py=global_var.get_value('player1y')
        dx=px-self.tx
        dy=py-self.ty
        dist=math.sqrt(dx**2+dy**2)
        minDist=global_var.get_value('enemyPos')[2]
        if self.tx<660 and self.tx>60 and self.ty<690 and self.ty>30 and dist<minDist:
            global_var.set_value('enemyPos',(self.tx,self.ty,dist))

    def ai_move(self):
        pass

    def ai_left(self):
        self.speedx=-3
        self.speedy=-7*math.cos((self.tx-self.screenRe)/180*math.pi*2)
    def ai_right(self):
        self.speedx=4
        self.speedy=-7*math.cos((self.tx-self.screenRe)/180*math.pi*2)
    def ai_incline(self):
        self.speedx=1.5
        self.speedy=-1.5
    def ai_down(self):
        if self.ty>=100 and self.speedy>0 and self.tx<self.screenRe+200:
            self.speedy-=0.1
            self.speedx+=0.1
        elif self.tx>=self.screenRe+200 and self.speedx>0:
            self.speedx-=0.1
            self.speedy+=0.1
        else:
            self.speedy=2
    def fire(self,frame,bullets,effects):
        pass

    def draw(self,screen,frame):
        screen.blit(self.surf,self.rect)
    
    def createItem(self,items,Type,num):
        for i in range(0,num):
            dx=random.random()*120-60
            dy=random.random()*120*-1-10
            new_item=Item.item()
            new_item.type=Type
            x_now=self.tx+dx
            y_now=self.ty+dy
            if x_now<80:
                x_now=80
            if x_now>640:
                x_now=640
            new_item.initial(x_now,y_now)
            items.add(new_item)

    def dropItem(self,items):
        pass
    def doKill(self,effects,items,bullets):
        global_var.get_value('enemyDead_sound').play()
        new_effect=Effect.enemyDead()
        new_effect.initial(self.deadImage,self.rect.centerx,self.rect.centery)
        effects.add(new_effect)
        self.dropItem(items)
        self.kill()

class butterfly(enemy):
    def __init__(self):
        super(butterfly,self).__init__()
        self.health=1000
        self.down=[]
        self.deadImage=pygame.image.load('resource/sprite/sprite_dead.png').convert_alpha()

        for i in range(1,6):
            down1=pygame.image.load('resource/enemy/butterfly_down_'+str(i)+'.png').convert_alpha()
            down1=pygame.transform.scale(down1,(98,98))
            self.down.append(down1)
        self.right=[]
        for i in range(1,4):
            right1=pygame.image.load('resource/enemy/butterfly_right_'+str(i)+'_1.png').convert_alpha()
            right2=pygame.image.load('resource/enemy/butterfly_right_'+str(i)+'_2.png').convert_alpha()
            right1=pygame.transform.scale(right1,(98,98))
            right2=pygame.transform.scale(right2,(98,98))
            self.right.append(right1)
            self.right.append(right2)
        self.left=[]
        for i in range(1,4):
            left1=pygame.image.load('resource/enemy/butterfly_right_'+str(i)+'_1.png').convert_alpha()
            left2=pygame.image.load('resource/enemy/butterfly_right_'+str(i)+'_2.png').convert_alpha()
            left1=pygame.transform.flip(left1,True,False)
            left2=pygame.transform.flip(left2,True,False)
            left1=pygame.transform.scale(left1,(98,98))
            left2=pygame.transform.scale(left2,(98,98))
            self.left.append(left1)
            self.left.append(left2)
        self.action=0
        self.frame=0
    def draw(self,screen,frame):
        self.frame+=1
        if frame%7==0:
            self.action+=1
        self.countAngle()
        if (self.angle>100) and (self.angle<260):
            if self.angle>=180:
                screen.blit(self.left[self.action%2],(self.rect.centerx-49,self.rect.centery-49))
            elif self.angle>135:
                screen.blit(self.left[2+self.action%2],(self.rect.centerx-49,self.rect.centery-49))
            else:
                screen.blit(self.left[4+self.action%2],(self.rect.centerx-49,self.rect.centery-49))
        elif (self.angle>280) or (self.angle<80):
            if (self.angle<360) and (self.angle>280):
                screen.blit(self.right[self.action%2],(self.rect.centerx-49,self.rect.centery-49))
            elif (self.angle<45):
                screen.blit(self.right[2+self.action%2],(self.rect.centerx-49,self.rect.centery-49))
            else:
                screen.blit(self.right[4+self.action%2],(self.rect.centerx-49,self.rect.centery-49))

        else:
            screen.blit(self.down[self.action%5],(self.rect.centerx-49,self.rect.centery-49))

    def fire(self,frame,bullets,effects):
        if frame%5==0:
            if not global_var.get_value('enemyFiring3'):
                global_var.get_value('enemyGun_sound3').play()
                global_var.set_value('enemyFiring3',True)
            new_bullet=Bullet.orb_Bullet()
            new_bullet.initial(self.rect.centerx,self.rect.centery,self.occupy)
            new_bullet.selfTarget(global_var.get_value('player1x'),global_var.get_value('player1y'),3.5)
            new_bullet.countAngle()
            new_bullet.loadColor('green')
            angle=new_bullet.angle
            bullets.add(new_bullet)
            for i in range(-3,4):
                if i!=0:
                    new_bullet=Bullet.orb_Bullet()
                    new_bullet.initial(self.rect.centerx,self.rect.centery,self.occupy)
                    new_bullet.setSpeed(angle+10*i,3.5)
                    new_bullet.loadColor('green')
                    bullets.add(new_bullet)
                    
class spirit(enemy):
    def __init__(self):
        super(spirit,self).__init__()
        self.health=1500
        self.frame=0
        self.colorNum=random.randint(0,7)
        self.direction=0
        self.angleNum=0
        self.interval=5
        self.part=0
        self.lockNum=0
        self.lock=0
    def draw(self,screen,frame):
        image=pygame.Surface((48,48)).convert_alpha()
        #image.set_alpha(256)
        #image=image.convert_alpha()
        #image.set_colorkey((0, 0, 0))
        image.fill((0,0,0,0))
        self.frame+=1
        self.countAngle()
        if self.frame>=self.interval:
            self.frame=0
            self.part+=1
        if self.part>=5:
            self.part=0

        if self.angle<100 and self.angle>80:
            self.angleNum=0
            self.lock=0
        elif self.angle<125 and self.angle>55:
            self.lock=1
            self.lockNum=5
        elif self.angle<145 and self.angle>35:
            self.lock=1
            self.lockNum=6
        else:
            self.lock=0
            self.angleNum=7

        if self.angle>250 and self.angle<280:
            self.lock=0
            self.angleNum=0

        if self.lock==1:
            image.blit(global_var.get_value('spirit'),(0,0),(48*self.lockNum,48*self.colorNum,48,48))
        else:
            image.blit(global_var.get_value('spirit'),(0,0),(48*(self.angleNum+self.part),48*self.colorNum,48,48))
        
        if self.angle>100 and self.angle<270:
            image=pygame.transform.flip(image,True,False)
        
        screen.blit(image,(self.rect.centerx-24,self.rect.centery-24))

    def doKill(self,effects,items,bullets):
        global_var.get_value('enemyDead_sound').play()
        new_effect=Effect.enemyDead()
        new_effect.initial(self.deadImage,self.rect.centerx,self.rect.centery)
        effects.add(new_effect)
        self.createItem(items,1,2)
        self.createItem(items,0,2)
        self.kill()

class ghost(enemy):
    def __init__(self):
        super(ghost,self).__init__()
        self.health=500
        self.frame=0
        self.colorNum=random.randint(0,3)
        self.direction=0
        self.interval=2
        self.part=0
        self.nimbusAngle=0
    def draw(self,screen,frame):
        nimbusImage=pygame.Surface((48,48))
        nimbusImage=nimbusImage.convert_alpha()
        nimbusImage.fill((0,0,0,0))
        
        #nimbusImage.set_colorkey((0, 0, 0))
        nimbusImage.blit(global_var.get_value('nimbus'),(0,0),(48*self.colorNum,0,48,48))
        gF.drawRotation(nimbusImage,(self.rect.centerx-24,self.rect.centery-24),self.nimbusAngle,screen)
        image=pygame.Surface((48,48))
        image.set_alpha(256)
        image=image.convert_alpha()
        image.set_colorkey((0, 0, 0))
        self.frame+=1
        self.nimbusAngle+=4
        self.countAngle()
        if self.frame>=self.interval:
            self.frame=0
            self.part+=1
        if self.part>=8:
            self.part=0
        if self.angle>=90 and self.angle<270:
            self.direction=1
        else:
            self.direction=0
        image.blit(global_var.get_value('ghost'),(0,0),(48*self.part,48*self.colorNum,48,48))
        if self.direction==0:
            image=pygame.transform.flip(image,True,False)
        screen.blit(image,(self.rect.centerx-24,self.rect.centery-24))
        '''
        num=5
        if self.frame%3==0:
            for i in range(0,3):
                rx=random.random()*-20+10
                ry=random.random()*-30
                randomPoint=(rx+self.tx,ry+self.ty)
                dis=math.sqrt(rx**2+ry**2)
                size=round(image.get_width()*(36.06-dis)/36.06)
                #print(dis,' ',size)
                tempImage=pygame.transform.scale(image,(size,size))
                screen.blit(tempImage,(randomPoint[0]-round(1/2*size),randomPoint[1]-round(1/2*size)))
        '''

class spirit_test(spirit):
    def __init__(self):
        super(spirit_test,self).__init__()
    
    def fire(self,frame,bullets,effects):
        if frame%200==0:
            if not global_var.get_value('enemyFiring2'):
                global_var.get_value('enemyGun_sound2').play()
                global_var.set_value('enemyFiring2',True)
            basicSpeed=3
            basicAngle=random.random()*360
            for j in range(0,3):
                speed=basicSpeed-j*0.5
                angle=basicAngle-j*8
                for i in range(1,10):
                    new_bullet=Bullet.orb_Bullet()
                    new_bullet.initial(self.rect.centerx,self.rect.centery,self.occupy)
                    new_bullet.setSpeed(angle+40*i,speed)
                    new_bullet.loadColor('blue')
                    bullets.add(new_bullet)

class spirit_part1_1(spirit):
    def __init__(self,angle=0,speed=3):
        super(spirit_part1_1,self).__init__()
        self.health=300
        self.colorNum=3
        self.moveAngle=angle
        self.speed=speed
        self.fireFrame=random.randint(0,40)
        self.bulletColor='lemonYellow'
    def ai_move(self):
        '''
        if self.lastFrame<60:
            self.speedx=-3
        if self.lastFrame>=60:
            if self.lastFrame<=90:
                self.setSpeed(180+3*(self.lastFrame-60),3)
            if self.lastFrame>90:
                self.speedx=0
                self.speedy=-3.1
        '''
        if self.lastFrame==1:
            self.setSpeed(self.moveAngle,self.speed)
        self.countAngle()
        self.fireFrame+=1
    def fire(self,frame,bullets,effects):
        if self.fireFrame%40<=8 and self.fireFrame%4==0:
            if not global_var.get_value('enemyFiring2'):
                global_var.get_value('enemyGun_sound2').stop()
                global_var.get_value('enemyGun_sound2').play()
                global_var.set_value('enemyFiring2',True)
            new_bullet=Bullet.rice_Bullet()
            new_bullet.initial(self.rect.centerx,self.rect.centery,self.occupy)
            px=global_var.get_value('player1x')
            py=global_var.get_value('player1y')
            new_bullet.selfTarget(px,py,7.2)
            new_bullet.countAngle()
            angle=new_bullet.angle
            new_bullet.loadColor(self.bulletColor)
            bullets.add(new_bullet)
            '''
            new_effect=Effect.bulletCreate(6)
            new_effect.initial(self.tx,self.ty,64,32,15)
            effects.add(new_effect)
            '''
            for i in range(1,3):
                new_bullet=Bullet.rice_Bullet()
                new_bullet.initial(self.rect.centerx,self.rect.centery,self.occupy)
                new_bullet.setSpeed(angle+(i-1.5)*120,7.2)
                new_bullet.loadColor(self.bulletColor)
                bullets.add(new_bullet)
        if self.fireFrame==80:
            '''
            new_effect=Effect.bulletCreate(3)
            new_effect.initial(self.tx,self.ty,84,48,20)
            effects.add(new_effect)
            '''
            if not global_var.get_value('enemyFiring2'):
                global_var.get_value('enemyGun_sound2').stop()
                global_var.get_value('enemyGun_sound2').play()
                global_var.set_value('enemyFiring2',True)
            angle=random.random()*60
            for i in range(0,12):
                new_bullet=Bullet.rice_Bullet()
                new_bullet.initial(self.rect.centerx,self.rect.centery,self.occupy)
                new_bullet.setSpeed(angle+i*(360/12),3.5)
                new_bullet.loadColor('pink')
                bullets.add(new_bullet)
        

    def dropItem(self,items):
        self.createItem(items,0,5)
        self.createItem(items,1,2)

class spirit_part1_2(spirit_part1_1):
    def __init__(self,angle=0,speed=3):
        super(spirit_part1_2,self).__init__()
        self.colorNum=4
        self.moveAngle=angle
        self.speed=speed
        self.fireFrame=random.randint(0,40)
        self.bulletColor='blue'

class ghost_part2_1(ghost):
    def __init__(self):
        super(ghost_part2_1,self).__init__()
        self.health=200
        self.colorNum=2
        self.fireFrame=random.randint(0,40)
    def fire(self,frame,bullets,effects):
        self.fireFrame+=1
        if self.fireFrame%40==0:
            if not global_var.get_value('kiraing'):
                global_var.get_value('kira_sound').stop()
                global_var.get_value('kira_sound').play()
                global_var.set_value('kiraing',True)
            new_effect=Effect.bulletCreate(3)
            new_effect.initial(self.tx,self.ty,84,64,4)
            effects.add(new_effect)
            for i in range(0,5):
                for j in range(0,2):
                    new_bullet=Bullet.rice_Bullet()
                    new_bullet.initial(self.rect.centerx,self.rect.centery,self.occupy)
                    if j==0:
                        new_bullet.setSpeed(90,6-i*0.7)
                    else:
                        new_bullet.setSpeed(-90,6-i*0.7)
                    new_bullet.loadColor('blue')
                    bullets.add(new_bullet)

    def dropItem(self,items):
        self.createItem(items,0,3)
        self.createItem(items,1,2)
    def doKill(self,effects,items,bullets):
        global_var.get_value('enemyDead_sound').play()
        new_effect=Effect.enemyDead()
        new_effect.initial(self.deadImage,self.rect.centerx,self.rect.centery)
        effects.add(new_effect)
        new_effect=Effect.bulletCreate(1)
        new_effect.initial(self.tx,self.ty,144,64,5)
        effects.add(new_effect)
        self.dropItem(items)
        new_bullet=Bullet.scale_Bullet()
        new_bullet.initial(self.tx,self.ty,1)
        px=global_var.get_value('player1x')
        py=global_var.get_value('player1y')
        new_bullet.selfTarget(px,py,5)
        new_bullet.countAngle()
        angle=new_bullet.angle
        for i in range(-1,2):
            for j in range(0,4):
                new_bullet=Bullet.scale_Bullet()
                new_bullet.initial(self.tx,self.ty,1)
                new_bullet.setSpeed(angle+i*2,4.5-j*0.3)
                new_bullet.loadColor('blue')
                bullets.add(new_bullet)
        self.kill()

class ghost_part3_1(ghost_part2_1):
    def __init__(self):
        super(ghost_part3_1,self).__init__()
        self.health=200
        self.colorNum=0

    def doKill(self,effects,items,bullets):
        global_var.get_value('enemyDead_sound').play()
        new_effect=Effect.enemyDead()
        new_effect.initial(self.deadImage,self.rect.centerx,self.rect.centery)
        effects.add(new_effect)
        new_effect=Effect.bulletCreate(1)
        new_effect.initial(self.tx,self.ty,144,64,5)
        effects.add(new_effect)
        self.dropItem(items)
        new_bullet=Bullet.scale_Bullet()
        new_bullet.initial(self.tx,self.ty,1)
        px=global_var.get_value('player1x')
        py=global_var.get_value('player1y')
        new_bullet.selfTarget(px,py,5)
        new_bullet.countAngle()
        angle=new_bullet.angle
        for i in range(-1,2):
            for j in range(0,5):
                new_bullet=Bullet.scale_Bullet()
                new_bullet.initial(self.tx,self.ty,1)
                new_bullet.setSpeed(angle+i*2,4.7-j*0.4)
                new_bullet.loadColor('red')
                bullets.add(new_bullet)
        self.kill()

    def fire(self,frame,bullets,effects):
        self.fireFrame+=1
        if self.fireFrame%35==0:
            if not global_var.get_value('kiraing'):
                global_var.get_value('kira_sound').stop()
                global_var.get_value('kira_sound').play()
                global_var.set_value('kiraing',True)
            new_effect=Effect.bulletCreate(3)
            new_effect.initial(self.tx,self.ty,84,64,4)
            effects.add(new_effect)
            for i in range(0,5):
                for j in range(0,2):
                    new_bullet=Bullet.rice_Bullet()
                    new_bullet.initial(self.rect.centerx,self.rect.centery,self.occupy)
                    if j==0:
                        new_bullet.setSpeed(90,6-i*0.7)
                    else:
                        new_bullet.setSpeed(-90,6-i*0.7)
                    new_bullet.loadColor('red')
                    bullets.add(new_bullet)
    
class butterfly_part4_1(butterfly):
    def __init__(self):
        super(butterfly_part4_1,self).__init__()
        self.health=6000
        self.lastFrame=0
        self.fireAngle=random.random()*60

    def ai_move(self):
        if self.lastFrame<=80:
            self.speedy=1.6
        elif self.lastFrame<=440:
            self.speedy=0
        else:
            self.speedy=-3
    
    def fire(self,frame,bullets,effects):
        if self.lastFrame>=80 and self.lastFrame%8==0:
            self.fireAngle-=6
            '''
            new_effect=Effect.bulletCreate(3)
            new_effect.initial(self.tx,self.ty,256,128,8)
            effects.add(new_effect)
            '''
            if not global_var.get_value('kiraing'):
                global_var.get_value('kira_sound').stop()
                global_var.get_value('kira_sound').play()
                global_var.set_value('kiraing',True)
            for i in range(0,10):
                new_bullet=Bullet.star_Bullet_Part4_Hex()
                new_bullet.initial(self.tx,self.ty,self.occupy)
                new_bullet.direction=1
                new_bullet.setSpeed(self.fireAngle-i*36,5)
                new_bullet.speed=5
                new_bullet.rotationAngle=0.8
                new_bullet.loadColor('purple')
                bullets.add(new_bullet)
    
    def dropItem(self,items):
        self.createItem(items,3,1)
        self.createItem(items,1,8)

class spirit_part4_1(spirit):
    def __init__(self):
        super(spirit_part4_1,self).__init__()
        self.health=400
        self.colorNum=3
        self.fireFrame=random.randint(0,30)
    def ai_move(self):
        self.speedy=0
        self.speedx=4
    
    def fire(self,frame,bullets,effects):
        self.fireFrame+=1
        if self.lastFrame%30==0:
            new_effect=Effect.bulletCreate(0)
            new_effect.initial(self.tx,self.ty,84,32,4)
            effects.add(new_effect)
            if not global_var.get_value('enemyFiring2'):
                global_var.get_value('enemyGun_sound2').play()
                global_var.set_value('enemyFiring2',True)
            new_bullet=Bullet.small_Bullet()
            new_bullet.initial(self.rect.centerx,self.rect.centery,self.occupy)
            px=global_var.get_value('player1x')
            py=global_var.get_value('player1y')
            new_bullet.selfTarget(px,py,7)
            new_bullet.countAngle()
            angle=new_bullet.angle
            new_bullet.loadColor('white')
            bullets.add(new_bullet)
            for i in range(1,5):
                new_bullet=Bullet.small_Bullet()
                new_bullet.initial(self.rect.centerx,self.rect.centery,self.occupy)
                new_bullet.setSpeed(angle,7-i*0.8)
                new_bullet.loadColor('white')
                bullets.add(new_bullet)
    
    def dropItem(self,items):
        self.createItem(items,0,1)
        self.createItem(items,1,1)

class butterfly_part5_1(butterfly):
    def __init__(self):
        super(butterfly_part5_1,self).__init__()
        self.health=9000
        self.lastFrame=0
        self.fireAngle=random.random()*60

    def ai_move(self):
        if self.lastFrame<=60:
            self.speedy=2.4
        elif self.lastFrame<=640:
            self.speedy=0
        else:
            self.speedy=-3
    
    def fire(self,frame,bullets,effects):
        if self.lastFrame>=80 and self.lastFrame%30==0:
            self.fireAngle=random.random()*360
            '''
            new_effect=Effect.bulletCreate(7)
            new_effect.initial(self.tx,self.ty,256,128,8)
            effects.add(new_effect)
            '''
            if not global_var.get_value('kiraing'):
                global_var.get_value('kira_sound').stop()
                global_var.get_value('kira_sound').play()
                global_var.set_value('kiraing',True)
            for i in range(0,16):
                for j in range(0,3):
                    new_bullet=Bullet.orb_Bullet()
                    new_bullet.initial(self.tx,self.ty,self.occupy)
                    new_bullet.setSpeed(self.fireAngle+i*(360/16)+(j-1)*2,4)
                    new_bullet.loadColor('orange')
                    bullets.add(new_bullet)
    
    def dropItem(self,items):
        self.createItem(items,3,1)
        self.createItem(items,1,8)

class spirit_part5_1(spirit):
    def __init__(self,typ=0):
        super(spirit_part5_1,self).__init__()
        self.health=400
        self.colorNum=3
        self.fireFrame=random.randint(0,50)
        self.type=typ
    def ai_move(self):
        self.speedy=0
        if self.type==0:
            self.speedx=-4
        elif self.type==1:
            self.speedx=4
    
    def fire(self,frame,bullets,effects):
        self.fireFrame+=1
        if self.fireFrame%50==0:
            new_effect=Effect.bulletCreate(3)
            new_effect.initial(self.tx,self.ty,144,64,10)
            effects.add(new_effect)
            if not global_var.get_value('enemyFiring1'):
                global_var.get_value('enemyGun_sound1').play()
                global_var.set_value('enemyFiring1',True)
            for i in range(0,5):
                angle=random.random()*360
                new_bullet=Bullet.orb_Bullet_gravity()
                new_bullet.initial(self.tx,self.ty,1)
                color=random.randint(0,6)
                new_bullet.setGravity(0.1+0.05*random.random())
                new_bullet.setGravMax(3+1*random.random())
                new_bullet.setSpeed(angle,random.random())
                new_bullet.doColorCode(color)
                bullets.add(new_bullet)
    
    def dropItem(self,items):
        self.createItem(items,0,1)
        self.createItem(items,1,1)

class spirit_part6_1(spirit):
    def __init__(self):
        super(spirit_part6_1,self).__init__()
        self.health=700
        self.num=0
        self.colorNum=random.randint(4,7)
        self.positive=random.randint(0,1)
        if self.positive==0:
            self.positive=-1
        self.fireFrame=random.randint(0,40)
    def ai_move(self):
        if self.lastFrame<=40:
            if self.num==0:
                self.speedy=3
            if self.num==1:
                self.speedy=5
        elif self.lastFrame<=120:
            self.speedy=0
        elif self.lastFrame==121:
            self.setSpeed(random.random()*180,4)
        if self.lastFrame==1:
            self.health=9999
        if self.lastFrame==40:
            self.health=700
    def fire(self,frame,bullets,effects):
        self.fireFrame+=1
        if frame>=3000:
            interval=18
            code=0
            intense=round(30*(3300-frame)/300+30)
            changeSpeed=4
        else:
            interval=25
            code=2
            intense=12
            changeSpeed=6
        if self.fireFrame%interval==0 and self.ty<=500:
            angle=random.random()*360
            if not global_var.get_value('enemyFiring2'):
                global_var.get_value('enemyGun_sound2').play()
                global_var.set_value('enemyFiring2',True)
            if code==2:
                new_effect=Effect.bulletCreate(5)
            else:
                new_effect=Effect.bulletCreate(1)
            new_effect.initial(self.tx,self.ty,128,64,6)
            effects.add(new_effect)
            new_effect.initial(self.tx,self.ty,128,64,6)
            effects.add(new_effect)
            for i in range(0,intense):
                new_bullet=Bullet.orb_Bullet_Part6_delay()
                new_bullet.initial(self.rect.centerx,self.rect.centery,self.occupy)
                new_bullet.setSpeed(angle+i*(360/intense),15)
                #new_bullet.doColorCode(code)
                if code==0:
                    new_bullet.loadColor('blue')
                else:
                    new_bullet.loadColor('red')
                new_bullet.changeAngle=self.positive*90                    
                new_bullet.speed=0.5
                new_bullet.changeSpeed=changeSpeed
                bullets.add(new_bullet)

    def dropItem(self,items):
        self.createItem(items,0,2)
        self.createItem(items,1,1)

class spirit_part7_1(spirit):
    def __init__(self):
        super(spirit_part7_1,self).__init__()
        self.health=600
        self.colorNum=5
        self.fireFrame=random.randint(0,40)
    
    def ai_move(self):
        if self.lastFrame<60:
            self.speedx=-3
        if self.lastFrame>=60:
            if self.lastFrame<=90:
                self.setSpeed(180+3*(self.lastFrame-60),3)
            if self.lastFrame>90:
                self.speedx=0
                self.speedy=-3.1
        self.countAngle()

    def fire(self,frame,bullets,effects):
        self.fireFrame+=1
        if self.fireFrame%40==0:
            angle=random.random()*360
            intense=6
            if not global_var.get_value('enemyFiring2'):
                global_var.get_value('enemyGun_sound2').stop()
                global_var.get_value('enemyGun_sound2').play()
                global_var.set_value('enemyFiring2',True)
            for j in range(0,3):
                for i in range(0,intense):
                    new_bullet=Bullet.scale_Bullet()
                    new_bullet.initial(self.rect.centerx,self.rect.centery,self.occupy)
                    new_bullet.setSpeed(angle+i*(360/intense)-20*j,2-0.4*j)
                    new_bullet.loadColor('green')
                    bullets.add(new_bullet)
        if self.fireFrame%30<=10 and self.fireFrame%2==0:
            if not global_var.get_value('enemyFiring2'):
                global_var.get_value('enemyGun_sound2').stop()
                global_var.get_value('enemyGun_sound2').play()
                global_var.set_value('enemyFiring2',True)
            new_bullet=Bullet.scale_Bullet()
            new_bullet.initial(self.tx,self.ty,1)
            px=global_var.get_value('player1x')
            py=global_var.get_value('player1y')
            new_bullet.selfTarget(px,py,5.5)
            new_bullet.countAngle()
            angle=new_bullet.angle
            for i in range(0,2):
                new_bullet=Bullet.scale_Bullet()
                new_bullet.initial(self.tx,self.ty,1)
                new_bullet.setSpeed(angle+2*(i-0.5)*20,5.5-self.fireFrame%30/2*0.3)
                new_bullet.loadColor('blue')
                bullets.add(new_bullet)

    def doKill(self,effects,items,bullets):
        global_var.get_value('enemyDead_sound').play()
        self.dropItem(items)
        new_effect=Effect.enemyDead()
        new_effect.initial(self.deadImage,self.rect.centerx,self.rect.centery)
        effects.add(new_effect)
        for i in range(0,1):
            new_bullet=Bullet.laser_Bullet_main()
            new_bullet.length=20
            new_bullet.ratio=5
            new_bullet.initial(self.rect.centerx,self.rect.centery,self.occupy)
            px=global_var.get_value('player1x')
            py=global_var.get_value('player1y')
            new_bullet.selfTarget(px,py,6+i*0.5)
            new_bullet.speed=6+i*0.5+1
            new_bullet.doColorCode(2)
            #new_bullet.loadColor('red')
            bullets.add(new_bullet)
        self.kill()

    def dropItem(self,items):
        self.createItem(items,0,2)
        self.createItem(items,1,1)

class spirit_part7_2(spirit_part7_1):
    def __init__(self):
        super(spirit_part7_2,self).__init__()
        self.health=600
        self.colorNum=5
        self.fireFrame=random.randint(0,19)
    
    def ai_move(self):
        if self.lastFrame<60:
            self.speedx=3
        if self.lastFrame>=60:
            if self.lastFrame<=90:
                self.setSpeed(0-3*(self.lastFrame-60),3)
            if self.lastFrame>90:
                self.speedx=0
                self.speedy=-3.1
        self.countAngle()
    
class butterfly_part8_1(butterfly):
    def __init__(self):
        super(butterfly_part8_1,self).__init__()
        self.health=12000
        self.lastFrame=0
        self.fireAngle=random.random()*360
        self.fireAngle2=random.random()*360
        self.adjAngle=45
    def ai_move(self):
        if self.lastFrame<=60:
            self.speedy=3.5
        elif self.lastFrame<=940:
            self.speedy=0
        else:
            self.speedy=-3
        if self.lastFrame==1:
            self.health=90000
        elif self.lastFrame==200:
            self.health=(self.health/90000)*12000
    def fire(self,frame,bullets,effects):
        if self.lastFrame>=80 and self.lastFrame%26==0:
            self.fireAngle+=40+20*random.random()
            if not global_var.get_value('kiraing'):
                global_var.get_value('kira_sound').stop()
                global_var.get_value('kira_sound').play()
                global_var.set_value('kiraing',True)
            if not global_var.get_value('enemyFiring2'):
                global_var.get_value('enemyGun_sound2').stop()
                global_var.get_value('enemyGun_sound2').play()
                global_var.set_value('enemyFiring2',True)
            angleRnd=-2.6-0.22*random.random()
            dAngleRnd=-0.010-0.002*random.random()
            for i in range(0,12):
                new_bullet=Bullet.mid_Bullet_Part8_acc()
                new_bullet.initial(self.tx,self.ty,self.occupy)
                new_bullet.setSpeed(self.fireAngle-i*(360/12)-self.adjAngle,0.5)
                new_bullet.speedNow=0.5
                new_bullet.changeAngle1=angleRnd
                new_bullet.dAngle=dAngleRnd
                new_bullet.loadColor('pink')
                bullets.add(new_bullet)
        if self.lastFrame>=80 and self.lastFrame%26==13:
            self.fireAngle2-=40+20*random.random()
            if not global_var.get_value('kiraing'):
                global_var.get_value('kira_sound').stop()
                global_var.get_value('kira_sound').play()
                global_var.set_value('kiraing',True)
            if not global_var.get_value('enemyFiring2'):
                global_var.get_value('enemyGun_sound2').stop()
                global_var.get_value('enemyGun_sound2').play()
                global_var.set_value('enemyFiring2',True)
            angleRnd=2.6+0.22*random.random()
            dAngleRnd=0.010+0.002*random.random()
            for i in range(0,12):
                new_bullet=Bullet.mid_Bullet_Part8_acc()
                new_bullet.initial(self.tx,self.ty,self.occupy)
                new_bullet.setSpeed(self.fireAngle2-i*(360/12)+self.adjAngle,0.5)
                new_bullet.speedNow=0.5
                new_bullet.changeAngle1=angleRnd
                new_bullet.dAngle=dAngleRnd
                new_bullet.loadColor('pink')
                bullets.add(new_bullet)

    
    def dropItem(self,items):
        self.createItem(items,0,10)
        self.createItem(items,2,5)

class butterfly_part9_1(butterfly):
    def __init__(self):
        super(butterfly_part9_1,self).__init__()
        self.health=12000
        self.lastFrame=0
        self.fireAngle=random.random()*360
        self.fireAngle2=random.random()*360
        self.adjAngle=45
        self.no=0
    def ai_move(self):
        if self.lastFrame<=60:
            self.speedy=2.4
        elif self.lastFrame<=640:
            self.speedy=0
        else:
            self.speedy=-3
    
    def fire(self,frame,bullets,effects):
        if self.lastFrame>=80 and self.lastFrame%10==0:
            if not global_var.get_value('kiraing'):
                global_var.get_value('kira_sound').stop()
                global_var.get_value('kira_sound').play()
                global_var.set_value('kiraing',True)
            if not global_var.get_value('enemyFiring2'):
                global_var.get_value('enemyGun_sound2').stop()
                global_var.get_value('enemyGun_sound2').play()
                global_var.set_value('enemyFiring2',True)
            if self.no==0:
                angleRnd=3.6+0.02*random.random()
                dAngleRnd=0.020+0.0001*random.random()
                self.fireAngle+=40+20*random.random()
            else:
                angleRnd=-3.6-0.02*random.random()
                dAngleRnd=-0.020-0.0001*random.random()
                self.fireAngle-=40+20*random.random()
            for i in range(0,9):
                new_bullet=Bullet.mid_Bullet_Part8_acc()
                new_bullet.initial(self.tx,self.ty,self.occupy)
                new_bullet.setSpeed(self.fireAngle-i*(360/9),0.1)
                new_bullet.speedNow=0.1
                new_bullet.changeAngle1=angleRnd
                new_bullet.dAngle=dAngleRnd
                new_bullet.loadColor('blue')
                bullets.add(new_bullet)
        if self.lastFrame>=80 and self.lastFrame%100==0:
            if not global_var.get_value('enemyFiring1'):
                global_var.get_value('enemyGun_sound1').stop()
                global_var.get_value('enemyGun_sound1').play()
                global_var.set_value('enemyFiring1',True)
            new_bullet=Bullet.circle_Bullet()
            new_bullet.initial(self.tx,self.ty,1)
            new_bullet.doColorCode(5)
            px=global_var.get_value('player1x')
            py=global_var.get_value('player1y')
            new_bullet.selfTarget(px,py,5.5)
            bullets.add(new_bullet)
    def dropItem(self,items):
        self.createItem(items,3,1)
        self.createItem(items,2,2)

class butterfly_part9_2(butterfly_part9_1):
    def __init__(self):
        super(butterfly_part9_2,self).__init__()

    def fire(self,frame,bullets,effects):
        if self.lastFrame>=80 and self.lastFrame%10==0:
            self.fireAngle-=6
            if not global_var.get_value('kiraing'):
                global_var.get_value('kira_sound').stop()
                global_var.get_value('kira_sound').play()
                global_var.set_value('kiraing',True)
            for i in range(0,14):
                new_bullet=Bullet.mid_Bullet_Part8_acc()
                new_bullet.initial(self.tx,self.ty,self.occupy)
                new_bullet.setSpeed(self.fireAngle-i*(360/14),1)
                new_bullet.speedLimit=5.0
                new_bullet.loadColor('blue')
                bullets.add(new_bullet)

class ghost_slytherin_spirit(spirit):
    def __init__(self):
        super(ghost_slytherin_spirit,self).__init__()
        self.health=9999999
        self.colorNum=2
        self.adjMax=40
        self.maxLastFrame=800
        self.endAngle=0
    def ai_move(self):
        if self.lastFrame<=self.maxLastFrame:
            px=global_var.get_value('player1x')
            py=global_var.get_value('player1y')
            self.selfTarget(px,py,1.5)
            self.countAngle()
            angle=self.angle
            self.endAngle=angle
        else:
            angle=self.endAngle
        if self.lastFrame%72==0:
            self.adjMax=random.random()*60+10
        angleAdjust=self.adjMax*math.sin(self.lastFrame/180*math.pi*5)
        self.setSpeed(angle+angleAdjust,2.2)
    
    def update(self,screen,frame,bullets,bullets2,effects,items):
        if self.startFrame==-1:
            self.startFrame=frame
        existFrame=frame-self.startFrame
        self.lastFrame+=1
        if existFrame>=10:
            self.checkValid(effects,items,bullets)
        if self.aiType==0:
            self.ai_left()
        if self.aiType==1:
            self.ai_right()
        if self.aiType==2:
            self.ai_down()
        if self.aiType==3:
            self.ai_incline()
        if self.aiType==-1:
            self.ai_move()
        self.tx+=self.speedx
        self.ty+=self.speedy
        self.truePos()
        self.fire(frame,bullets,effects)
        self.draw(screen,frame)
    
    def fire(self,frame,bullets,effects):
        if self.lastFrame%2==0:
            new_effect=Effect.bulletCreate(5)
            new_effect.initial(self.tx,self.ty,64,16,16)
            effects.add(new_effect)
            if not global_var.get_value('enemyFiring2'):
                global_var.get_value('enemyGun_sound2').stop()
                global_var.get_value('enemyGun_sound2').play()
                global_var.set_value('enemyFiring2',True)
            new_bullet=Bullet.laser_bullet_decline(300,7)
            new_bullet.speed=4
            self.countAngle()
            new_bullet.angle=self.angle
            new_bullet.doColorCode(10)
            new_bullet.initial(self.tx,self.ty,1)
            bullets.add(new_bullet)
        
    
class ghost_hufflepuff_spirit(spirit):
    def __init__(self):
        super(ghost_hufflepuff_spirit,self).__init__()
        self.health=3000
        self.colorNum=4
        self.bounceLim=5
        self.speed_now=10
        self.x_bouncing=False
        self.y_bouncing=False
        self.fireWatcher=False
        self.fireDensity=12
        self.deadFire=False
        self.distance=0
        self.startAngle=random.random()*360
        self.startAngle2=random.random()*360
    def ai_move(self):
        if self.lastFrame==1:
            angle=random.random()*360
            self.setSpeed(angle,self.speed_now)
        self.bounce()

    def getDistance(self):
            px=global_var.get_value('player1x')
            py=global_var.get_value('player1y')
            dx=self.tx-px
            dy=self.ty-py
            self.distance=math.sqrt(dx**2+dy**2)
    def bounce(self):
        if self.bounceLim>0:
            if (self.tx<=60 or self.tx>=660) and self.x_bouncing!=True:
                self.speedx=-self.speedx
                self.countAngle()
                self.speed_now-=1.5
                self.setSpeed(self.angle,self.speed_now)
                self.x_bouncing=True
                self.bounceLim-=1
                #print(self.tx,' ',self.ty,self.bouncing)
            elif (self.ty>=690 or self.ty<=30) and self.y_bouncing!=True:
                self.speedy=-self.speedy
                self.countAngle()
                self.speed_now-=1.5
                self.setSpeed(self.angle,self.speed_now)
                self.y_bouncing=True
                self.bounceLim-=1
                #print(self.tx,' ',self.ty,self.bouncing)
            if self.tx>60 and self.tx<660:
                self.x_bouncing=False
            if self.ty<690 and self.ty>30:
                self.y_bouncing=False
        else:
            self.health=0
        
        
    def fire(self,frame,bullets,effects):

        if (self.x_bouncing or self.y_bouncing):
            if not self.fireWatcher and self.bounceLim>0:
                self.fireDensity=round(self.fireDensity*1.2)
                angle=random.random()*360
                for i in range(0,self.fireDensity):
                    new_bullet=Bullet.star_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.loadColor('blue')
                    new_bullet.setSpeed(angle+i*(360/self.fireDensity),2.5)
                    bullets.add(new_bullet)
                self.fireWatcher=True
            global_var.get_value('water_sound').play()
            #new_effect=Effect.wave()
            #new_effect.initial([self.tx,self.ty],700,30)
            #effects.add(new_effect)
        else:
            self.fireWatcher=False
        
        if self.bounceLim==0 and not self.deadFire:
            angle=random.random()*360
            for i in range(0,20):
                for j in range(0,6):
                    new_bullet=Bullet.orb_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.loadColor('blue')
                    new_bullet.setSpeed(angle+i*(360/20),3-0.2*j)
                    bullets.add(new_bullet)
            self.deadFire=True
        
        if self.lastFrame%4==0:
            self.getDistance()
            if self.distance>=60:
                self.startAngle+=28.1
                new_bullet=Bullet.orb_bullet_delay()
                new_bullet.retainFrame=120
                new_bullet.startSpeed=0.1
                new_bullet.endSpeed=4
                new_bullet.accFrame=60
                new_bullet.initial(self.tx,self.ty,1)
                new_bullet.setSpeed(self.startAngle,0.1)
                new_bullet.loadColor('blue')
                bullets.add(new_bullet)
                self.startAngle2-=35.4
                new_bullet=Bullet.orb_bullet_delay()
                new_bullet.retainFrame=120
                new_bullet.startSpeed=0.1
                new_bullet.endSpeed=5
                new_bullet.accFrame=60
                new_bullet.initial(self.tx,self.ty,1)
                new_bullet.setSpeed(self.startAngle2,0.1)
                new_bullet.loadColor('blue')
                bullets.add(new_bullet)
        
    def update(self,screen,frame,bullets,bullets2,effects,items):
            if self.startFrame==-1:
                self.startFrame=frame
            existFrame=frame-self.startFrame
            self.lastFrame+=1
            if existFrame>=10:
                self.checkValid(effects,items,bullets)
            if self.aiType==0:
                self.ai_left()
            if self.aiType==1:
                self.ai_right()
            if self.aiType==2:
                self.ai_down()
            if self.aiType==3:
                self.ai_incline()
            if self.aiType==-1:
                self.ai_move()
            self.tx+=self.speedx
            self.ty+=self.speedy
            self.truePos()
            self.fire(frame,bullets,effects)
            self.draw(screen,frame)


class ghost_gryffindor_spirit(spirit):
    def __init__(self):
        super(ghost_gryffindor_spirit,self).__init__()
        self.health=6000
        self.colorNum=5
        self.targetPos=[0,0]
        self.targetAngle=0
        self.speed=0
        self.maxSpeed=6
        self.accFrame=20
        self.holdFrame=40
        self.actionFrame=0
        self.maxLastFrame=650
        self.time=0
    def ai_move(self):
        self.actionFrame+=1
        px=global_var.get_value('player1x')
        py=global_var.get_value('player1y')
        if self.actionFrame>=1:
            if self.actionFrame==1:
                self.selfTarget(px,py,3)
                self.targetPos=[px,py]
                self.countAngle()
                self.targetAngle=self.angle
                self.setSpeed(self.angle,0)
            
            if self.actionFrame<=self.accFrame:
                self.speed+=self.maxSpeed/self.accFrame
            
            if self.actionFrame>=self.accFrame+self.holdFrame:
                self.speed-=self.maxSpeed/self.accFrame

            if self.actionFrame>=self.accFrame*2+self.holdFrame:
                self.speed=0
                self.actionFrame=-50
                self.time+=1
                self.holdFrame+=30
                global_var.get_value("kira1_sound").stop()
                global_var.get_value("kira1_sound").play()
            self.setSpeed(self.targetAngle,self.speed)
        if self.lastFrame>=self.maxLastFrame:
            self.health=0
        
        if self.tx>=660:
            self.tx=61
        if self.tx<=60:
            self.tx=659
        if self.ty>=720:
            self.ty=31
        if self.ty<=30:
            self.ty=729
    
    def checkValid(self,effects,items,bullets):
        if self.health<=0:
            self.doKill(effects,items,bullets)
    
    def update(self,screen,frame,bullets,bullets2,effects,items):
        if self.startFrame==-1:
            self.startFrame=frame
        existFrame=frame-self.startFrame
        self.lastFrame+=1
        if existFrame>=10:
            self.checkValid(effects,items,bullets)
        if self.aiType==0:
            self.ai_left()
        if self.aiType==1:
            self.ai_right()
        if self.aiType==2:
            self.ai_down()
        if self.aiType==3:
            self.ai_incline()
        if self.aiType==-1:
            self.ai_move()
        self.tx+=self.speedx
        self.ty+=self.speedy
        self.truePos()
        self.fire(frame,bullets,effects)
        self.draw(screen,frame)
    
    def fire(self,frame,bullets,effects):
        if self.actionFrame>=self.accFrame and self.actionFrame<=self.accFrame+self.holdFrame:
            d_Frame=self.actionFrame-self.accFrame
            maxRandom=round(70-d_Frame*3)
            if maxRandom<10:
                maxRandom=10
            if d_Frame%15==0:
                if not global_var.get_value('enemyFiring3'):
                    global_var.get_value('enemyGun_sound3').stop()
                    global_var.get_value('enemyGun_sound3').play()
                    global_var.set_value('enemyFiring3',True)
                for i in range(0,9):
                    for j in range(0,2):
                        if j==0:
                            direct=-1
                        else:
                            direct=1
                        new_bullet=Bullet.mid_bullet_delay()
                        new_bullet.setDelay(40,9-i*0.9)
                        new_bullet.initial(self.tx,self.ty,1)
                        new_bullet.setSpeed(self.targetAngle+90*direct,0.2-0.02*i)
                        new_bullet.loadColor('red')
                        bullets.add(new_bullet)
            if d_Frame%2==0:
                if not global_var.get_value('enemyFiring1'):
                    global_var.get_value('enemyGun_sound1').stop()
                    global_var.get_value('enemyGun_sound1').play()
                    global_var.set_value('enemyFiring1',True)
                for i in range(3):
                    new_bullet=Bullet.star_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    r=random.random()*maxRandom-round(maxRandom/2)
                    s=random.random()*2-1
                    new_bullet.setSpeed(self.angle-180+r,9+s)
                    new_bullet.loadColor('red')
                    bullets.add(new_bullet)

class ghost_ravenclaw_spirit(spirit):
    def __init__(self):
        super(ghost_ravenclaw_spirit,self).__init__()
        self.health=6000
        self.colorNum=3
        self.radius=0
        self.circular=random.random()*360
        self.wSpeed=1.0
        self.rSpeed=0
        self.orientPos=[0,0]
        self.maxLastFrame=350
        self.fireAngle=random.random()*360
        self.direct=1
    def orient(self,pos):
        self.orientPos=pos
    def ai_move(self):
        self.radius=120
        self.circular+=self.wSpeed
        now_x=self.orientPos[0]+math.sin(self.circular/180*math.pi)*self.radius
        now_y=self.orientPos[1]-math.cos(self.circular/180*math.pi)*self.radius
        self.tx=now_x
        self.ty=now_y
    def checkValid(self,effects,items,bullets):
        if self.health<=0:
            self.doKill(effects,items,bullets)
        if self.lastFrame>=self.maxLastFrame:
            self.doKill(effects,items,bullets)
    
    def update(self,screen,frame,bullets,bullets2,effects,items):
        if self.startFrame==-1:
            self.startFrame=frame
        existFrame=frame-self.startFrame
        self.lastFrame+=1
        if existFrame>=10:
            self.checkValid(effects,items,bullets)
        if self.aiType==0:
            self.ai_left()
        if self.aiType==1:
            self.ai_right()
        if self.aiType==2:
            self.ai_down()
        if self.aiType==3:
            self.ai_incline()
        if self.aiType==-1:
            self.ai_move()
        self.tx+=self.speedx
        self.ty+=self.speedy
        self.truePos()
        self.fire(frame,bullets,effects)
        self.draw(screen,frame)

    def fire(self,frame,bullets,effects):
        if self.lastFrame%9==0:
            self.fireAngle+=8.3*self.direct
            if not global_var.get_value('enemyFiring2'):
                global_var.get_value('enemyGun_sound2').stop()
                global_var.get_value('enemyGun_sound2').play()
                global_var.set_value('enemyFiring2',True)
            for i in range(0,4):
                for j in range(0,3):
                    new_bullet=Bullet.scale_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.setSpeed(self.fireAngle+i*(360/4)-1*j*self.direct,4.5-0.8*j)
                    new_bullet.loadColor('yellow')
                    bullets.add(new_bullet)
        if self.lastFrame%200>=100:
            self.direct=1
        else:
            self.direct=-1
    
#class-> player
class  Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.surf = pygame.Surface((5,5))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.tx=0.0
        self.ty=0.0
        self.cx=0.0
        self.cy=0.0
        self.life=2
        self.immune=0
        self.impStartFrame=-1
        self.boom=3
        self.skillpoint=800
        self.bulletSurpress=0
        self.deadFrame=10
        self.deadStatu=0
        self.boomStatu=0
        self.direction=0
        self.holdFrame=0
        self.itemCollectDistance=0
        self.power=100
        self.powerLevel=1
        self.score=0
        self.lastLevel=1
        self.lastLife=self.life
        self.spellBonus=True
        self.midPath=False
        self.vertical=False
        self.horizontal=False
        self.graze=0
        self.highSpeed=7.0
        self.lowSpeed=2.5
        self.unhitFrame=0
        self.unhitable=False
        self.boomUnhitMax=100
    #key dictionary

    def unhitSetter(self,unhitFrame):
        self.unhitFrame=unhitFrame

    def doUnhit(self):
        if self.unhitFrame>0:
            self.unhitFrame-=1
            self.unhitable=True
        else:
            self.unhitable=False

    def getBoomStatu(self):
        self.boomStatu=global_var.get_value('boomStatu')

    def getGraze(self):
        self.graze=global_var.get_value('grazeNum')
    def decreaseDeadFrame(self):
        if self.deadStatu==1 and self.deadFrame>=0:
            self.deadFrame-=1
        elif self.deadFrame<0:
            self.deadStatu=0

    def immunePlayer(self,frame):
        if self.immune==1:
            if self.impStartFrame==-1:
                self.impStartFrame=frame
            existFrame=frame-self.impStartFrame
            if existFrame>=200:
                self.immune=0
                self.impStartFrame=-1
                self.deadFrame=10
                self.deadStatu=0
    
    def checkPower(self):
        if self.power>400:
            self.power=400
        if self.power<100:
            self.power=100
        self.powerLevel=math.floor(self.power/100)
        if self.lastLevel<self.powerLevel:
            global_var.get_value('powerup_sound').play()
        self.lastLevel=self.powerLevel
    
    def checkLife(self):
        self.lastLife=self.life
    
    def checkGraze(self):
        self.lastGraze=self.graze
    
    def customizeFloat(self):
        pass

    def update(self,pressed_keys,frame):
        speed=self.highSpeed
        f=frame
        self.checkPower()
        self.checkLife()
        self.checkGraze()
        self.customizeFloat()
        self.direction=0
        if pressed_keys[K_LSHIFT]:
            speed=self.lowSpeed
        if pressed_keys[K_UP] or pressed_keys[K_DOWN]:
            self.vertical=True
        else:
            self.vertical=False
        if pressed_keys[K_LEFT] or pressed_keys[K_RIGHT]:
            self.horizontal=True
        else:
            self.horizontal=False
        if self.vertical and self.horizontal:
            if pressed_keys[K_UP]:
                #self.rect.move_ip(0,-speed)
                self.ty=self.ty-speed*math.sqrt(2)/2
            if pressed_keys[K_DOWN]:
                #self.rect.move_ip(0,speed)
                self.ty=self.ty+speed*math.sqrt(2)/2
            if pressed_keys[K_LEFT]:
                #self.rect.move_ip(-speed,0)
                self.tx=self.tx-speed*math.sqrt(2)/2
                self.direction=1
                if not pressed_keys[K_RIGHT]:
                    self.holdFrame+=1
                else:
                    self.holdFrame-=1
            if pressed_keys[K_RIGHT]:
                #self.rect.move_ip(speed,0)
                self.tx=self.tx+speed*math.sqrt(2)/2
                if self.direction!=1:
                    self.direction=2
                else:
                    self.direction=0
                if not pressed_keys[K_LEFT]:
                    self.holdFrame+=1
                else:
                    self.holdFrame-=1
        else:
            if pressed_keys[K_UP]:
                #self.rect.move_ip(0,-speed)
                self.ty=self.ty-speed
            if pressed_keys[K_DOWN]:
                #self.rect.move_ip(0,speed)
                self.ty=self.ty+speed
            if pressed_keys[K_LEFT]:
                #self.rect.move_ip(-speed,0)
                self.tx=self.tx-speed
                self.direction=1
                if not pressed_keys[K_RIGHT]:
                    self.holdFrame+=1
                else:
                    self.holdFrame-=1
            if pressed_keys[K_RIGHT]:
                #self.rect.move_ip(speed,0)
                self.tx=self.tx+speed
                if not pressed_keys[K_LEFT]:
                    self.holdFrame+=1
                else:
                    self.holdFrame-=1
                if self.direction!=1:
                    self.direction=2
                else:
                    self.direction=0
        if not (pressed_keys[K_LEFT] or pressed_keys[K_RIGHT]):
            self.holdFrame-=1
        if self.holdFrame<0:
            self.holdFrame=0
        elif self.holdFrame>=40:
            self.holdFrame=39
        if self.tx < 60+20:
            self.tx = 60+20
        elif self.tx+5 > 660-20:
            self.tx = 660-20-5
        if self.ty <= 30+20:
            self.ty = 30+20
        elif self.ty+5 >=720-50:
            self.ty = 720-50-5
        self.rect.left=round(self.tx)
        self.rect.top=round(self.ty)
        self.cx=self.rect.centerx
        self.cy=self.rect.centery
        self.immunePlayer(f)
        self.doUnhit()
        self.getBoomStatu()
        self.getGraze()
        self.decreaseDeadFrame()

    def fire(self,frame,screen,playerGuns):
        pass

class  player_float_gun(pygame.sprite.Sprite):
    def __init__(self):
        super(player_float_gun,self).__init__()
        self.surf = pygame.Surface((5,5))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.tx=0.0
        self.ty=0.0
        self.cx=0.0
        self.cy=0.0

class Marisa(Player):
    def __init__(self):
        super(Marisa,self).__init__()
        self.surf = pygame.Surface((7,7))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.image=global_var.get_value('pl00')
        self.image=pygame.transform.smoothscale(self.image,(384,216))
        self.interval=5
        self.part=0
        self.count2=0
        self.frame=0
        self.itemGetLine=300
        self.fireInterval=4
        self.inclineAngle1=10
        self.inclineAngle2=25
        self.inclineSpeed=40
        self.floatImage=pygame.transform.smoothscale(pygame.image.load('./resource/player/pl00/floatGun.png'),(120,24))
        self.gunCycle=0
        self.gunAdj=[0,-60]
        self.highSpeed=7.5
        self.lowSpeed=3.0
    def fire(self,frame,screen,playerGuns):
        if frame%4==0:
            new_fire=Bullet.straightGun()
            new_fire.tx=self.cx-14
            new_fire.ty=self.cy
            playerGuns.add(new_fire)

            new_fire=Bullet.straightGun()
            new_fire.tx=self.cx+14
            new_fire.ty=self.cy
            playerGuns.add(new_fire)
            shift_down=global_var.get_value('shift_down')

            #incline angle control:
            if not shift_down:
                self.inclineAngle1+=5/2
                self.inclineAngle2+=10.625/2
            else:
                self.inclineAngle1-=5/2
                self.inclineAngle2-=10.625/2
            if self.inclineAngle1>=10:
                self.inclineAngle1=10
            if self.inclineAngle1<=2:
                self.inclineAngle1=2
            if self.inclineAngle2>=25:
                self.inclineAngle2=25
            if self.inclineAngle2<=8:
                self.inclineAngle2=8
            
            
            #create fire
            if not shift_down:
                
                if self.powerLevel>=2 or frame%8==0:
                    new_fire=Bullet.inclineGun()
                    new_fire.color='blue'
                    new_fire.initial(270-self.inclineAngle1,self.cx+self.gunAdj[0],self.cy+self.gunAdj[1],self.inclineSpeed)
                    playerGuns.add(new_fire)
                    new_fire=Bullet.inclineGun()
                    new_fire.color='blue'
                    new_fire.initial(270+self.inclineAngle1,self.cx+self.gunAdj[0],self.cy+self.gunAdj[1],self.inclineSpeed)
                    playerGuns.add(new_fire)
                if self.powerLevel>=3:
                    if self.powerLevel>=4 or frame%8==0:
                        new_fire=Bullet.inclineGun()
                        new_fire.color='blue'
                        new_fire.initial(270-self.inclineAngle2,self.cx+self.gunAdj[0],self.cy+self.gunAdj[1],self.inclineSpeed)
                        playerGuns.add(new_fire)
                        new_fire=Bullet.inclineGun()
                        new_fire.color='blue'
                        new_fire.initial(270+self.inclineAngle2,self.cx+self.gunAdj[0],self.cy+self.gunAdj[1],self.inclineSpeed)
                        playerGuns.add(new_fire)
            else:
                hit=60
                if self.powerLevel>=2 or frame%8==0:
                    new_fire=Bullet.inclineGun()
                    new_fire.color='red'
                    new_fire.image=global_var.get_value('playerFire_red')
                    #new_fire.image.set_alpha(200)
                    #new_fire.image=pygame.transform.scale(new_fire.image,(48,48))
                    new_fire.hit=hit
                    new_fire.initial(270-self.inclineAngle1,self.cx+self.gunAdj[0],self.cy+self.gunAdj[1],self.inclineSpeed)
                    playerGuns.add(new_fire)
                    new_fire=Bullet.inclineGun()
                    new_fire.color='red'
                    new_fire.image=global_var.get_value('playerFire_red')
                    new_fire.hit=hit
                    #new_fire.image.set_alpha(200)
                    #new_fire.image=pygame.transform.scale(new_fire.image,(48,48))
                    new_fire.initial(270+self.inclineAngle1,self.cx+self.gunAdj[0],self.cy+self.gunAdj[1],self.inclineSpeed)
                    playerGuns.add(new_fire)
                if self.powerLevel>=3:
                    if self.powerLevel>=4 or frame%8==0:
                        new_fire=Bullet.inclineGun()
                        new_fire.color='red'
                        new_fire.image=global_var.get_value('playerFire_red')
                        #new_fire.image.set_alpha(200)
                        #new_fire.image=pygame.transform.scale(new_fire.image,(48,48))
                        new_fire.hit=hit
                        new_fire.initial(270-self.inclineAngle2,self.cx+self.gunAdj[0],self.cy+self.gunAdj[1],self.inclineSpeed)
                        playerGuns.add(new_fire)
                        new_fire=Bullet.inclineGun()
                        new_fire.color='red'
                        new_fire.image=global_var.get_value('playerFire_red')
                        #new_fire.image.set_alpha(200)
                        #new_fire.image=pygame.transform.scale(new_fire.image,(48,48))
                        new_fire.hit=hit
                        new_fire.initial(270+self.inclineAngle2,self.cx+self.gunAdj[0],self.cy+self.gunAdj[1],self.inclineSpeed)
                        playerGuns.add(new_fire)

    def draw(self,screen):
        gunMax=50
        gunFrame=3
        shift_down=global_var.get_value('shift_down')
        if shift_down:
            self.gunAdj[1]-=gunMax/gunFrame
        else:
            self.gunAdj[1]+=gunMax/gunFrame
        if self.gunAdj[1]>=gunMax:
            self.gunAdj[1]=gunMax
        if self.gunAdj[1]<=-gunMax:
            self.gunAdj[1]=-gunMax

        image=pygame.Surface((48, 72))
        image=image.convert_alpha()
        image.fill((0,0,0,0))
        #pygame.Surface.convert_alpha(image)
        #image.set_alpha(256)
        #image.set_colorkey((0, 0, 0))
        self.frame+=1
        if self.frame>=self.interval:
            self.frame=0
            self.part+=1
        if self.part>=8:
            self.part=0
        if self.direction!=0 or self.holdFrame>0:
            self.part=math.floor(self.holdFrame/self.interval)
            if self.part==7:
                if self.frame==0:
                    self.count2+=1
                if self.count2%2==0:
                    self.part=6

        image.blit(self.image, (0, 0), (48*self.part,72*self.direction, 48, 72))
        screen.blit(image,(self.rect.centerx-24,self.rect.centery-36))
        self.drawFloatA(screen,shift_down)
        #screen.blit(self.surf,self.rect)
    def drawFloatA(self,screen,shift_down):
        self.gunCycle+=1
        image=pygame.Surface((24,24))
        image=image.convert_alpha()
        image.fill((0,0,0,0))
        if shift_down:
            index_x=0
        else:
            index_x=24
        image.blit(self.floatImage,(0,0),(index_x,0,24,24))
        size=round(math.sin(self.gunCycle*math.pi/180*4)*4+24)
        image=pygame.transform.scale(image,(size,size))
        screen.blit(image,(round(self.cx-size/2+self.gunAdj[0]),round(self.cy-size/2)+self.gunAdj[1]))

class Reimu(Player):
    def __init__(self):
        super(Reimu,self).__init__()
        self.surf = pygame.Surface((6,6))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.image=global_var.get_value('pl01')
        self.image=pygame.transform.smoothscale(self.image,(384,216))
        self.interval=5
        self.part=0
        self.count2=0
        self.frame=0
        self.itemGetLine=300
        self.fireInterval=4
        self.inclineAngle1=10
        self.inclineAngle2=25
        self.inclineSpeed=14
        self.distTimes=1.5
        self.highSpeed=6.8
        self.lowSpeed=2.4
        #self.floatImage=global_var.get_value('reimu_fire')
        self.floatImage=pygame.Surface((23,23))
        self.floatImage=self.floatImage.convert_alpha()
        self.floatImage.fill((0,0,0,0))
        self.floatImage.blit(global_var.get_value('reimu_fire'),(0,0),(121-24,1,23,23))
        self.gunCycle=0
        self.gunAdj=[0,-60]
        self.boomUnhitMax=360
    def customizeFloat(self):
        shift_down=global_var.get_value('shift_down')

        if shift_down:
            self.distTimes-=0.1
        else:
            self.distTimes+=0.1
        if self.distTimes>1.5:
            self.distTimes=1.5
        if self.distTimes<1:
            self.distTimes=1

    def fire(self,frame,screen,playerGuns):
        if frame%4==0:
            new_fire=Bullet.reimuMainSatsu()
            new_fire.tx=self.cx-14
            new_fire.ty=self.cy
            playerGuns.add(new_fire)

            new_fire=Bullet.reimuMainSatsu()
            new_fire.tx=self.cx+14
            new_fire.ty=self.cy
            playerGuns.add(new_fire)
            shift_down=global_var.get_value('shift_down')
            
            #create fire
            if frame%8==0:
                if self.powerLevel==1:
                    new_fire=Bullet.reimuTargetSatsu()
                    new_fire.initial(270,self.cx+0*self.distTimes,self.cy+50+30*self.distTimes-45,self.inclineSpeed)
                    new_fire.angle=270
                    playerGuns.add(new_fire)
                elif self.powerLevel==2:
                    new_fire=Bullet.reimuTargetSatsu()
                    new_fire.initial(270,self.cx+30*self.distTimes,self.cy-30*(self.distTimes)+45,self.inclineSpeed)
                    new_fire.angle=270
                    playerGuns.add(new_fire)
                    new_fire=Bullet.reimuTargetSatsu()
                    new_fire.initial(270,self.cx-30*self.distTimes,self.cy-30*(self.distTimes)+45,self.inclineSpeed)
                    new_fire.angle=270
                    playerGuns.add(new_fire)
                elif self.powerLevel==3:
                    new_fire=Bullet.reimuTargetSatsu()
                    new_fire.initial(270,self.cx+30*self.distTimes,self.cy-30*(self.distTimes)+45,self.inclineSpeed)
                    new_fire.angle=270
                    playerGuns.add(new_fire)
                    new_fire=Bullet.reimuTargetSatsu()
                    new_fire.initial(270,self.cx-30*self.distTimes,self.cy-30*(self.distTimes)+45,self.inclineSpeed)
                    new_fire.angle=270
                    playerGuns.add(new_fire)
                    new_fire=Bullet.reimuTargetSatsu()
                    new_fire.initial(270,self.cx+0*self.distTimes,self.cy+50+30*self.distTimes-45,self.inclineSpeed)
                    new_fire.angle=270
                    playerGuns.add(new_fire)
                elif self.powerLevel==4:
                    new_fire=Bullet.reimuTargetSatsu()
                    new_fire.initial(270,self.cx+30*self.distTimes,self.cy-30*(self.distTimes)+45,self.inclineSpeed)
                    new_fire.angle=270
                    playerGuns.add(new_fire)
                    new_fire=Bullet.reimuTargetSatsu()
                    new_fire.initial(270,self.cx-30*self.distTimes,self.cy-30*(self.distTimes)+45,self.inclineSpeed)
                    new_fire.angle=270
                    playerGuns.add(new_fire)
                    new_fire=Bullet.reimuTargetSatsu()
                    new_fire.initial(270,self.cx-15*self.distTimes,self.cy+50+30*self.distTimes-45,self.inclineSpeed)
                    new_fire.angle=270
                    playerGuns.add(new_fire)
                    new_fire=Bullet.reimuTargetSatsu()
                    new_fire.initial(270,self.cx+15*self.distTimes,self.cy+50+30*self.distTimes-45,self.inclineSpeed)
                    new_fire.angle=270
                    playerGuns.add(new_fire)
            
    def draw(self,screen):
        self.gunCycle+=1
        gunMax=50
        gunFrame=3
        shift_down=global_var.get_value('shift_down')
        self.gunAdj[1]=40

        image=pygame.Surface((48, 72))
        image=image.convert_alpha()
        image.fill((0,0,0,0))
        #pygame.Surface.convert_alpha(image)
        #image.set_alpha(256)
        #image.set_colorkey((0, 0, 0))
        self.frame+=1
        if self.frame>=self.interval:
            self.frame=0
            self.part+=1
        if self.part>=8:
            self.part=0
        if self.direction!=0 or self.holdFrame>0:
            self.part=math.floor(self.holdFrame/self.interval)
            if self.part==7:
                if self.frame==0:
                    self.count2+=1
                if self.count2%2==0:
                    self.part=6

        image.blit(self.image, (0, 0), (48*self.part,72*self.direction, 48, 72))
        screen.blit(image,(self.rect.centerx-24,self.rect.centery-36))
        if self.powerLevel==1:
            self.drawFloatA(screen,shift_down,0*self.distTimes,50+30*self.distTimes-45)
        elif self.powerLevel==2:
            self.drawFloatA(screen,shift_down,30*self.distTimes,0-30*(self.distTimes)+45)
            self.drawFloatA(screen,shift_down,-30*self.distTimes,0-30*(self.distTimes)+45)
        elif self.powerLevel==3:
            self.drawFloatA(screen,shift_down,30*self.distTimes,0-30*(self.distTimes)+45)
            self.drawFloatA(screen,shift_down,-30*self.distTimes,0-30*(self.distTimes)+45)
            self.drawFloatA(screen,shift_down,0*self.distTimes,50+30*self.distTimes-45)
        elif self.powerLevel==4:
            self.drawFloatA(screen,shift_down,30*self.distTimes,0-30*(self.distTimes)+45)
            self.drawFloatA(screen,shift_down,-30*self.distTimes,0-30*(self.distTimes)+45)
            self.drawFloatA(screen,shift_down,15*self.distTimes,50+30*self.distTimes-45)
            self.drawFloatA(screen,shift_down,-15*self.distTimes,50+30*self.distTimes-45)
        #screen.blit(self.surf,self.rect)
    def drawFloatA(self,screen,shift_down,dx,dy):
        gF.drawRotation(self.floatImage,((round(self.cx-22/2+dx),round(self.cy-22/2)+dy)),-self.gunCycle*9,screen)
        #screen.blit(image,(round(self.cx-22/2+self.gunAdj[0]),round(self.cy-22/2)+self.gunAdj[1]))

#class for the boss in the scene
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super(Boss,self).__init__()
        self.surf = pygame.Surface((100,100))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.tx=0.0
        self.ty=0.0
        self.speedx=0
        self.speedy=0
        self.movingFrame=0
        self.lastFrame=0
        self.maxHealth=10000
        self.health=10000
        self.cardNum=0
        self.frameLimit=1200
        self.ifSpell=False
        self.spellName=''
        self.cardBonus=10000000
        self.framePunishment=3700
        self.maxSpell=0
        self.magicImage=pygame.transform.scale(pygame.image.load('resource/bossMagic.png'),(252,252)).convert_alpha()
        self.magicImage.set_alpha(230)
        self.tracker=global_var.get_value('bossTracker')
        self.bossSpell=pygame.transform.smoothscale(pygame.image.load('resource/text/bossSpell.png'),(16,16)).convert_alpha()
        self.ifBlock=False
        self.maxMovingFrame=0
        self.tempx=0
        self.tempy=0
        self.deadImage=pygame.image.load('resource/sprite/sprite_dead.png').convert_alpha()
        self.percentHealth=0
    
    def doShaking(self,num):
        global_var.set_value('shakeFrame',num)
    def setSpeed(self,angle,speed):
        s=math.sin(math.radians(angle))
        c=math.cos(math.radians(angle))
        self.speedy=s*speed
        self.speedx=c*speed
    
    def checkDistance(self):
        px=global_var.get_value('player1x')
        py=global_var.get_value('player1y')
        dx=px-self.tx
        dy=py-self.ty
        dist=math.sqrt(dx**2+dy**2)
        minDist=global_var.get_value('enemyPos')[2]
        if self.tx<660 and self.tx>60 and self.ty<690 and self.ty>30 and dist<minDist:
            global_var.set_value('enemyPos',(self.tx,self.ty,dist))
    
    def initial(self,x,y):
        self.tx=x
        self.ty=y

    
    def drawMagic(self,screen,frame,effects):
        w,h=self.magicImage.get_size()
        size=round(w+math.sin(frame*math.pi/180)*1)+100
        #tempImage=pygame.transform.scale(self.magicImage,(size,size))
        temp=pygame.Surface((size,size)).convert_alpha()
        temp.fill((0,0,0,0))
        #temp=temp.convert_alpha()
        innerPeriod=480
        gF.drawRotation(pygame.transform.smoothscale(self.magicImage,(size,size)),(0,0),frame%innerPeriod*(360/innerPeriod),temp)
        rotatePeriod=840
        height=round((math.sin((frame+90)*math.pi/180*0.8)*0.25+0.75)*size)
        tempImage=pygame.transform.smoothscale(temp,(size,height))
        #screen.blit(temp,(self.rect.centerx-round(size/2),self.rect.centery-round(size/2)))
        gF.drawRotation(tempImage,(self.rect.centerx-round(size/2),self.rect.centery-round(height/2)),frame%rotatePeriod*(360/rotatePeriod),screen)

        #draw flame effect
        if self.lastFrame%7==0:
            new_effect=Effect.bossFlame()
            new_effect.initial(150,0,20)
            effects.add(new_effect)
        if self.lastFrame%3==0:
            new_effect=Effect.bossLight()
            new_effect.initial(10)
            new_effect.angle=-frame*10%360
            effects.add(new_effect)

    def drawTracker(self,screen):
        screen.blit(self.tracker,(self.rect.centerx-20,670))
    
    def drawTimer(self,screen,myfont):
        sec=math.floor(self.frameLimit/60)
        miliSec=round(self.frameLimit%60/60*1,2)
        miliSec=round(miliSec*100)
        if self.frameLimit%60==0 and sec<=10:
            global_var.get_value('timeout_sound').play()
        if sec>=10 or (self.frameLimit%60>13):
            if self.frameLimit%60!=0 and miliSec>=10:
                timerText=myfont.render(str(sec)+'.'+str(miliSec), True, (255, 255, 255))
            elif miliSec<10:
                timerText=myfont.render(str(sec)+'.0'+str(miliSec), True, (255, 255, 255))
            else:
                timerText=myfont.render(str(sec)+'.00', True, (255, 255, 255))
        else:
            if self.frameLimit%60!=0 and miliSec>=10:
                timerText=myfont.render(str(sec)+'.'+str(miliSec), True, (255, 0, 0))
            elif miliSec<10:
                timerText=myfont.render(str(sec)+'.0'+str(miliSec), True, (255, 0, 0))
            else:
                timerText=myfont.render(str(sec)+'.00', True, (255, 0, 0))
        screen.blit(timerText,(600,695))
    
    def drawHealthBar(self,screen):
        if self.lastFrame<=60:
            length=round(self.health/self.maxHealth*520/60*self.lastFrame)
        else:
            length=round(self.health/self.maxHealth*520)
        if length<=0:
            length=0
        bar=pygame.Surface((length,6))
        if not self.ifSpell:
            bar.fill((203,218,218))
        else:
            bar.fill((210,133,133))
        screen.blit(bar,(60,710))
    
    def drawSpellName(self,screen,myfont,player):
        if self.ifSpell:
            spellText=myfont.render(self.spellName, True, (255, 255, 255))
            shadowText=myfont.render(self.spellName, True, (100, 0, 0))
            w, h = spellText.get_size()
            if player.cx>=660-w and player.cy<=60+h and self.lastFrame>=70:
                self.ifBlock=True
            else:
                self.ifBlock=False
            if self.ifBlock:
                spellText.set_alpha(100)
                shadowText.set_alpha(100)
            lineColor=(210,210,210)
            if self.lastFrame<=30:
                screen.blit(shadowText,(660-w+3,690-h+2))
                screen.blit(spellText,(660-w,690-h+2))
                pygame.draw.line(screen,lineColor,(660,690+0),(660-w,690+0),2)
            elif self.lastFrame<=90:
                screen.blit(shadowText,(660-w+3,round(690-h-((657-h)/60)*(self.lastFrame-30))+2))
                screen.blit(spellText,(660-w,round(690-h-((657-h)/60)*(self.lastFrame-30))))
                pygame.draw.line(screen,lineColor,(660,round(690-h-((657-h)/60)*(self.lastFrame-30))+h+0),(660-w,round(690-h-((657-h)/60)*(self.lastFrame-30))+h+0),2)
            else:
                screen.blit(shadowText,(660-w+3,33+2))
                screen.blit(spellText,(660-w,33))
                pygame.draw.line(screen,lineColor,(660,33+h+0),(660-w,33+h+0),2)
            
    def displayPercentHealth(self,screen,myfont):
        self.percentHealth=round(self.health/self.maxHealth*100)
        percentText=myfont.render(str(self.percentHealth)+'%', True, (255, 255, 255))
        w,h=percentText.get_size()
        screen.blit(percentText,(580-w,695))

    def drawCardBonus(self,screen,myfont,player):
        if self.ifSpell:
            if player.spellBonus:
                bonusText=myfont.render('Bonus: '+str(self.cardBonus), True, (255, 255, 255))
                shadowText=myfont.render('Bonus: '+str(self.cardBonus), True, (100, 0, 0))
            else:
                bonusText=myfont.render('Bonus: Failed', True, (255, 255, 255))
                shadowText=myfont.render('Bonus: Failed', True, (0, 0, 0))
            if self.ifBlock:
                bonusText.set_alpha(100)
                shadowText.set_alpha(100)
            if self.lastFrame>=90:
                screen.blit(shadowText,(530+2,63+1))
                screen.blit(bonusText,(530,63))

    def drawResult(self,effects,bonus,ifBonus):
        if ifBonus:
            new_effect=Effect.bonusText()
            new_effect.getBonus(bonus)
            effects.add(new_effect)
        else:
            new_effect=Effect.failText()
            effects.add(new_effect)

    def drawSpellNum(self,screen):
        remainingSpell=self.maxSpell-self.cardNum
        for i in range(0,remainingSpell):
            screen.blit(self.bossSpell,(142+i*18,692))
    
    def drawBossName(self,screen):
        pass 
        #modified in childClass

    def truePos(self):
        self.rect.centerx=round(self.tx)
        self.rect.centery=round(self.ty)

    def gotoPosition(self,x,y,inFrame):
        dx=x-self.tx
        dy=y-self.ty
        distance=math.sqrt(pow(dx,2)+pow(dy,2))
        speed=distance/inFrame
        self.movingFrame=inFrame
        self.maxMovingFrame=inFrame
        self.angle=self.getAngle(dx,dy)
        self.setSpeed(self.angle,speed)
        self.tempx=0
        self.tempy=0
    def countAngle(self):
        if self.speedx!=0:
            t=self.speedy/self.speedx
            deg=math.atan(t)*180/math.pi
        else: 
            if self.speedy>0:
                deg=90
            if self.speedy<0:
                deg=270
            if self.speedy==0:
                deg=90
        if deg<0:
            deg+=360
        if self.speedy>0 and deg>=180:
            deg=deg-180
        if self.speedy<0 and deg<=180:
            deg=deg+180
        if self.speedy==0 and self.speedx<0:
            deg=180
        self.angle=deg
    
    def getAngle(self,dx,dy):
        if dx!=0:
            t=dy/dx
            deg=math.atan(t)*180/math.pi
        else: 
            if dy>0:
                deg=90
            if dy<0:
                deg=270
            if dy==0:
                deg=90
        if deg<0:
            deg+=360
        if dy>0 and deg>=180:
            deg=deg-180
        if dy<0 and deg<=180:
            deg=deg+180
        if dy==0 and dx<0:
            deg=180
        self.angle=deg
        return deg 
    def addLastingCancel(self,tx,ty,slaves,maxFrame,doBonus,harsh=True):
        new_slave=Slave.bulletCancelLasting()
        new_slave.initial(tx,ty,maxFrame,900,doBonus,harsh)
        slaves.add(new_slave)
    def movement(self):
        if self.maxMovingFrame!=0:
            if self.movingFrame<self.maxMovingFrame/2:
                self.tempx-=self.speedx/self.maxMovingFrame*4
                self.tempy-=self.speedy/self.maxMovingFrame*4
            else:
                self.tempx+=self.speedx/self.maxMovingFrame*4
                self.tempy+=self.speedy/self.maxMovingFrame*4
            #print(self.tx,' ',self.ty)

        self.tx+=self.tempx
        self.ty+=self.tempy
        self.truePos()
        if self.movingFrame<=0:
            self.tempx=0
            self.tempy=0
            self.speedx=0
            self.speedy=0
            self.movingFrame=0
    
    def syncPosition(self):
        global_var.set_value('boss1x',self.tx)
        global_var.set_value('boss1y',self.ty)
        
    def update(self,screen,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        self.movingFrame-=1
        self.frameLimit-=1
        self.lastFrame+=1
        self.checkDistance()
        self.movement()
        self.syncPosition()
        self.attack(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
        self.drawMagic(screen,frame,effects)
        self.drawTracker(screen)
        #self.drawHealthBar(screen)
        self.draw(screen)

    
    def attack(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        pass

    def draw(self,screen):
        screen.blit(self.surf,self.rect)
    
    
    def cancalAllBullet(self,bullets,items,effects,doBonus):
        exception=(5,7,10,11,12,13)
        for bullet in bullets:
            new_effect=Effect.bulletVanish()
            if not bullet.type in exception:
                new_effect.initial(bullet.image,bullet.rect.centerx,bullet.rect.centery,bullet.dx,bullet.dy)
            elif bullet.type==5:
                new_effect.initial(bullet.tempImage,bullet.rect.centerx,bullet.rect.centery,bullet.dx,bullet.dy)
            elif bullet.type==7:
                if bullet.color=='red':
                    new_effect.initial(bullet.red[0],bullet.rect.centerx,bullet.rect.centery,bullet.dx,bullet.dy)
                else:
                    new_effect.initial(bullet.blue[0],bullet.rect.centerx,bullet.rect.centery,bullet.dx,bullet.dy)
            elif bullet.type==10 or bullet.type==11 or bullet.type==12 or bullet.type==13:
                new_effect.initial(bullet.tempImage,bullet.rect.centerx,bullet.rect.centery,bullet.dx,bullet.dy)
            if doBonus:
                Bullet.createItem(bullet.tx,bullet.ty,items)
            bullet.kill()
            effects.add(new_effect)
    
    def createItem(self,items,Type,num):
        for i in range(0,num):
            dx=random.random()*120-60
            dy=random.random()*120*-1-10
            new_item=Item.item()
            new_item.type=Type
            x_now=self.tx+dx
            y_now=self.ty+dy
            if x_now<80:
                x_now=80
            if x_now>640:
                x_now=640
            new_item.initial(x_now,y_now)
            items.add(new_item)



class satori(Boss):
    def __init__(self):
        super(satori,self).__init__()
        self.health=10000
        self.reset=True
        self.randomAngle=random.random()*360
        self.randomAngle2=random.random()*360
        self.row=0
        self.column=0
        self.interval=10
        self.part=0
        self.image=global_var.get_value('boss_1')
        self.flip=0
        self.speedNum=0
        self.maxSpell=3
        self.boomImmune=False
    def draw(self,screen):
        image=pygame.Surface((72,99))
        image.set_alpha(256)
        image.set_colorkey((0, 0, 0))
        if self.speedx<0:
            self.flip=1
        if self.speedx>0:
            self.flip=0
        self.speedNum=math.floor(math.sqrt(pow(self.speedx,2)+pow(self.speedy,2)/3))
        if self.speedNum>=4:
            self.speedNum=3
        self.part+=1
        if self.part>=self.interval:
            self.part=0
            self.column+=1
        if self.column>=4:
            self.column=0
            self.row+=1
        if self.row>=2:
            self.row=0
        if self.speedx==0 and self.speedy==0:
            image.blit(self.image, (0, 0), (72*self.column,99*self.row, 72, 99))
        else:
            image.blit(self.image, (0, 0), (72*self.speedNum,99*2, 72, 99))
        if self.flip==1:
            image=pygame.transform.flip(image,True,False)
        screen.blit(image,(self.rect.centerx-36,self.rect.centery-49))

    def attack(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
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
            global_var.get_value('bossDead_sound').play()
            for background in backgrounds:
                background.surf=global_var.get_value('lake_bg')
                background.surf.convert()
                background.surf.set_alpha(200)
                background.cardBg=False
            player.midPath=True
            new_effect=Effect.enemyDead()
            new_effect.initial(self.deadImage,self.tx,self.ty)
            new_effect.coef=0.20
            new_effect.interval=1
            effects.add(new_effect)
            width=60
            maxFrame=150
            new_effect=Effect.wave()
            new_effect.initial([self.tx+width*1,self.ty],900,maxFrame,(160,160,160),10)
            effects.add(new_effect)
            new_effect=Effect.wave()
            new_effect.initial([self.tx+width*-1,self.ty],900,maxFrame,(160,160,160),10)
            effects.add(new_effect)
            new_effect=Effect.wave()
            new_effect.initial([self.tx,self.ty+width*1],900,maxFrame,(160,160,160),10)
            effects.add(new_effect)
            new_effect=Effect.wave()
            new_effect.initial([self.tx,self.ty+width*-1],900,maxFrame,(160,160,160),10)
            effects.add(new_effect)
            self.doShaking(64)
            self.kill()
    
    def noneSpell_0(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        self.maxHealth=20000
        self.health=20000
        self.reset=True
        self.frameLimit=1200
    
    def noneSpell_1(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            self.maxHealth=30000
            self.health=self.maxHealth
            self.gotoPosition(360,210,30)
            self.randomAngle=random.random()*360
            self.frameLimit=1200
        if self.lastFrame%240>=0:
            if self.lastFrame%9==0:
                for i in range(0,8):
                    if not global_var.get_value('enemyFiring2'):
                        global_var.get_value('enemyGun_sound2').play()
                        global_var.set_value('enemyFiring2',True)
                    new_bullet=Bullet.mid_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.setSpeed(self.randomAngle+i*(360/8),5)
                    new_bullet.loadColor('darkBlue')
                    bullets.add(new_bullet)
                if self.lastFrame%240>=120:
                    self.randomAngle+=6
                else:
                    self.randomAngle-=6
        else:
            self.randomAngle=random.random()*360
        
        if self.health<=0 or self.frameLimit<=0:
            self.cancalAllBullet(bullets,items,effects,True)
            self.reset=True
            self.ifSpell=True
            self.health=20000
            global_var.get_value('enemyDead_sound').play()
    
    def spell_1(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            player.spellBonus=True
            self.maxHealth=60000
            self.health=60000
            self.gotoPosition(360,200,80)
            self.frameLimit=1800
            self.cardBonus=10000000
            self.spellName='Wand Sign[Shocking Magic]'
            global_var.get_value('spell_sound').play()
            for background in backgrounds:
                background.surf=global_var.get_value('star_bg')
                background.surf.convert()
                background.surf.set_alpha(180)
                background.cardBg=True
            new_effect=Effect.bossFaceSpell()
            effects.add(new_effect)
        self.cardBonus-=self.framePunishment

        if self.lastFrame%240>=120:
            if self.lastFrame%6==0:
                for i in range(0,9):
                    if not global_var.get_value('enemyFiring2'):
                        global_var.get_value('enemyGun_sound2').stop()
                        global_var.get_value('enemyGun_sound2').play()
                        global_var.set_value('enemyFiring2',True)
                    if not global_var.get_value('kiraing'):
                        global_var.get_value('kira_sound').stop()
                        global_var.get_value('kira_sound').play()
                        global_var.set_value('kiraing',True)
                    new_bullet=Bullet.scale_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.setSpeed(self.randomAngle+i*(360/9),7)
                    new_bullet.loadColor('green')
                    bullets.add(new_bullet)
                self.randomAngle-=11
        else:
            self.randomAngle=random.random()*360
        if self.lastFrame%9==0:
            for i in range(0,12):
                if not global_var.get_value('enemyFiring3'):
                    global_var.get_value('enemyGun_sound3').stop()
                    global_var.get_value('enemyGun_sound3').play()
                    global_var.set_value('enemyFiring3',True)
                new_bullet=Bullet.small_Bullet()
                new_bullet.initial(self.tx,self.ty,1)
                new_bullet.setSpeed(self.randomAngle2+i*(360/12),4)
                new_bullet.loadColor('purple')
                bullets.add(new_bullet)
            self.randomAngle2+=8.3

        if self.lastFrame%240==60:
            new_effect=Effect.bulletCreate(5)
            new_effect.initial(self.tx,self.ty,200,84,20)
            effects.add(new_effect)
        if self.lastFrame%240==80:
            if not global_var.get_value('enemyFiring1'):
                global_var.get_value('enemyGun_sound1').stop()
                global_var.get_value('enemyGun_sound1').play()
                global_var.set_value('enemyFiring1',True)
            px=global_var.get_value('player1x')
            py=global_var.get_value('player1y')
            new_bullet=Bullet.scale_Bullet()
            new_bullet.initial(self.tx,self.ty,1)
            new_bullet.selfTarget(px,py,6)
            new_bullet.countAngle()
            angle=new_bullet.angle
            for i in range(0,30):
                new_bullet=Bullet.scale_Bullet()
                new_bullet.initial(self.tx,self.ty,1)
                randAngle=random.random()*5-2.5
                randSpeed=random.random()*0.4+6
                new_bullet.setSpeed(angle+randAngle,randSpeed-0.1*i)
                new_bullet.loadColor('lightGreen')
                bullets.add(new_bullet)

        if self.health<=0:
            self.cancalAllBullet(bullets,items,effects,True)
            self.reset=True
            self.ifSpell=True
            self.cardNum+=1
            self.health=20000
            self.createItem(items,0,5)
            self.createItem(items,1,20)
            self.drawResult(effects,self.cardBonus,player.spellBonus)
            #self.createItem(items,6,1)
            if player.spellBonus:
                player.score+=self.cardBonus
                global_var.get_value('bonus_sound').play()
            #global_var.get_value('enemyDead_sound').play()
            global_var.get_value('spell_end').play()
        
        if self.frameLimit<=0:
            self.cancalAllBullet(bullets,items,effects,True)
            self.reset=True
            self.ifSpell=True
            self.cardNum+=1
            self.health=20000
            self.drawResult(effects,self.cardBonus,False)
            #global_var.get_value('enemyDead_sound').play()
            global_var.get_value('spell_end').play()

    def spell_2(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            player.spellBonus=True
            self.maxHealth=60000
            self.health=self.maxHealth
            self.gotoPosition(360,140,80)
            self.frameLimit=8600-frame
            self.cardBonus=10000000
            self.framePunishment=800
            self.powerUp=False
            global_var.get_value('spell_sound').play()
            self.spellName='Star light[Milky Star Shower]'
            new_effect=Effect.bossFaceSpell()
            effects.add(new_effect)
        self.cardBonus-=self.framePunishment
        if not self.powerUp:
            randomBulletInterval=5
            targetBulletInterval=9
            randomBulletISpeed=5
            targetBulletISpeed=5
        else:
            randomBulletInterval=4
            targetBulletInterval=7
            randomBulletISpeed=6
            targetBulletISpeed=7
        if self.lastFrame>=80:
            if self.lastFrame%10==0:
                global_var.get_value('kira_sound').stop()
                global_var.get_value('kira_sound').play()

            if self.lastFrame%randomBulletInterval==0:
                new_effect=Effect.bulletCreate(4)
                rx=random.random()*600+60
                ry=random.random()*20+30
                new_effect.initial(rx,ry,82,48,randomBulletInterval)
                #effects.add(new_effect)
                new_bullet=Bullet.rice_Bullet()
                new_bullet.anmStay=True
                new_bullet.initial(rx,ry,1)
                new_bullet.setSpeed(random.random()*20+80,randomBulletISpeed)
                new_bullet.loadColor('blue')
                bullets.add(new_bullet)
            
            if self.lastFrame%targetBulletInterval==0:
                new_effect=Effect.bulletCreate(2)
                rx=random.random()*600+60
                ry=random.random()*20+30
                new_effect.initial(rx,ry,82,48,targetBulletInterval)
                #effects.add(new_effect)
                new_bullet=Bullet.rice_Bullet()
                new_bullet.anmStay=True
                new_bullet.initial(rx,ry,1)
                new_bullet.selfTarget(player.cx,player.cy,targetBulletISpeed)
                new_bullet.loadColor('purple')
                bullets.add(new_bullet)
            
            if self.lastFrame%180>=160:
                if self.lastFrame%2==0:
                    if not global_var.get_value('enemyFiring2'):
                        global_var.get_value('enemyGun_sound2').stop()
                        global_var.get_value('enemyGun_sound2').play()
                        global_var.set_value('enemyFiring2',True)
                    new_bullet=Bullet.satsu_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.selfTarget(player.cx,player.cy,2.5+0.4*(self.lastFrame%180-160))
                    new_bullet.countAngle()
                    angle=new_bullet.angle
                    new_bullet.loadColor('blue')
                    bullets.add(new_bullet)
                    if self.health<=15000 or self.frameLimit<=600:
                        for i in range(-1,2):
                            if i!=0:
                                new_bullet=Bullet.satsu_Bullet()
                                new_bullet.anmStay=True
                                new_bullet.initial(self.tx,self.ty,1)
                                new_bullet.setSpeed(angle+i*30,2.5+0.4*(self.lastFrame%180-160))
                                new_bullet.loadColor('blue')
                                bullets.add(new_bullet)
            if self.health<=15000 or self.frameLimit<=600:
                if self.lastFrame%180==150 and not self.powerUp:
                    global_var.get_value('ch00_sound').play()
                    self.powerUp=True
                    new_effect=Effect.powerUp()
                    new_effect.initial([self.tx,self.ty],600,50,(255,255,255),2,3,10)
                    effects.add(new_effect)
            if self.lastFrame%180==0:
                if self.tx>player.cx:
                    x=random.randint(round(player.cx),round(self.tx))
                else:
                    x=random.randint(round(self.tx),round(player.cx))
                y=random.random()*200+80
                self.gotoPosition(x,y,50)

        if self.health<=0:
            self.cancalAllBullet(bullets,items,effects,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            self.createItem(items,0,5)
            self.createItem(items,1,20)
            self.createItem(items,6,1)
            self.drawResult(effects,self.cardBonus,player.spellBonus)
            if player.spellBonus:
                player.score+=self.cardBonus
                global_var.get_value('bonus_sound').play()
            #global_var.get_value('enemyDead_sound').play()
            global_var.get_value('spell_end').play()
        
        if self.frameLimit<=0:
            self.cancalAllBullet(bullets,items,effects,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            self.drawResult(effects,self.cardBonus,False)
            #global_var.get_value('enemyDead_sound').play()
            global_var.get_value('spell_end').play()

class Dumbledore(Boss):
    def __init__(self):
        super(Dumbledore,self).__init__()
        self.health=10000
        self.reset=True
        self.randomAngle=random.random()*360
        self.row=0
        self.column=0
        self.interval=10
        self.part=0
        self.image=global_var.get_value('boss_1')
        self.flip=0
        self.speedNum=0
        self.eventNum=0
        self.callNum=0
        self.maxSpell=10
        self.powerUp=False
        self.bossName=pygame.image.load('resource/boss/dumbledoreName.png')
        self.spell10_color=['red','blue','yellow','green']
        self.spell10_time=0
        self.powerRank=0
        self.lastRank=0
        self.actionFrame=0
        self.spell10_int=[[0,0,0],[0,0,0],[0,0,750],[500,0,1000],[500,0,1000]]
        self.alpha=0
        self.deadFrame=0
        self.boomImmune=True
    def drawBossName(self,screen):
        screen.blit(self.bossName,(60,692))
    def draw(self,screen):
        image=pygame.Surface((72,99))
        image.set_alpha(256)
        image.set_colorkey((0, 0, 0))
        if self.speedx<0:
            self.flip=1
        if self.speedx>0:
            self.flip=0
        self.speedNum=math.floor(math.sqrt(pow(self.speedx,2)+pow(self.speedy,2)/3))
        if self.speedNum>=4:
            self.speedNum=3
        self.part+=1
        if self.part>=self.interval:
            self.part=0
            self.column+=1
        if self.column>=4:
            self.column=0
            self.row+=1
        if self.row>=2:
            self.row=0
        if self.speedx==0 and self.speedy==0:
            image.blit(self.image, (0, 0), (72*self.column,99*self.row, 72, 99))
        else:
            image.blit(self.image, (0, 0), (72*self.speedNum,99*2, 72, 99))
        if self.flip==1:
            image=pygame.transform.flip(image,True,False)
        screen.blit(image,(self.rect.centerx-36,self.rect.centery-49))

    def attack(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
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
            if not self.ifSpell:
                self.noneSpell_8(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
            else:
                self.spell_8(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
        if self.cardNum==9:
            if not self.ifSpell:
                self.noneSpell_9(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
            else:
                self.spell_9(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
        if self.cardNum==10:
            if not self.ifSpell:
                self.noneSpell_10(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
            else:
                self.spell_10(frame,items,effects,bullets,backgrounds,enemys,slaves,player)
        if self.cardNum==11:
            #global_var.get_value('bossDead_sound').play()
            self.deadFrame+=1
            if self.deadFrame==1:
                global_var.get_value('spell_end').play()
                self.gotoPosition(self.tx+random.random()*100-50,self.ty+random.random()*100-50,59)
            if self.deadFrame>=60:
                global_var.get_value('bossDead_sound').play()
                self.doShaking(60)
                width=60
                maxFrame=150
                new_effect=Effect.wave()
                new_effect.initial([self.tx+width*1,self.ty],900,maxFrame,(160,160,160),10)
                effects.add(new_effect)
                new_effect=Effect.wave()
                new_effect.initial([self.tx+width*-1,self.ty],900,maxFrame,(160,160,160),10)
                effects.add(new_effect)
                new_effect=Effect.wave()
                new_effect.initial([self.tx,self.ty+width*1],900,maxFrame,(160,160,160),10)
                effects.add(new_effect)
                new_effect=Effect.wave()
                new_effect.initial([self.tx,self.ty+width*-1],900,maxFrame,(160,160,160),10)
                effects.add(new_effect)
                self.kill()

    def noneSpell_0(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        self.maxHealth=20000
        self.health=20000
        self.reset=True
        self.frameLimit=1200
    
    def noneSpell_1(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            self.maxHealth=50000
            self.health=50000
            self.gotoPosition(360,170,40)
            self.randomAngle=90
            #self.randomAngle=random.random()*360
            self.randomAngle2=self.randomAngle
            self.randomAngle3=random.random()*360
            self.frameLimit=1800
            self.fireCount=0

        if self.lastFrame>=40:
            #5
            if (self.lastFrame-40)%5==0:
                '''
                new_effect=Effect.bulletCreate(5)
                new_effect.initial(self.tx,self.ty,128,32,15)
                effects.add(new_effect)
                '''
                for i in range(0,5):
                    if not global_var.get_value('enemyFiring2'):
                        global_var.get_value('enemyGun_sound2').stop()
                        global_var.get_value('enemyGun_sound2').play()
                        global_var.set_value('enemyFiring2',True)
                    new_bullet=Bullet.satsu_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.setSpeed(self.randomAngle+i*(360/5),5.3)
                    new_bullet.loadColor('lightGreen')
                    bullets.add(new_bullet)
            if (self.lastFrame-40)%5==0:
                if not global_var.get_value('enemyFiring2'):
                        global_var.get_value('enemyGun_sound2').stop()
                        global_var.get_value('enemyGun_sound2').play()
                        global_var.set_value('enemyFiring2',True)
                for j in range(0,5):
                    new_bullet=Bullet.satsu_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.setSpeed(self.randomAngle2+j*(360/5),5.3)
                    new_bullet.loadColor('lightGreen')
                    bullets.add(new_bullet)
                self.randomAngle+=5
                self.randomAngle2-=5
            
            '''
                dg=random.random()*360
                sg=random.random()*180
                self.fireCount+=1
                for i in range(0,6):
                    
                    new_bullet=Bullet.laser_line()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.setFeature(dg+i*(360/6),10,360,40)
                    new_bullet.doColorCode(6)
                    if self.fireCount%2==0:
                        new_bullet.dDegree=0.45
                    else:
                        new_bullet.dDegree=-0.45
                    new_bullet.setSpeed(sg,2.0)
                    bullets.add(new_bullet)
            '''
            '''
            if (self.lastFrame-40)%50==25:
                new_effect=Effect.bulletCreate(4)
                new_effect.initial(self.tx,self.ty,192,48,25)
                effects.add(new_effect)
            '''
            if (self.lastFrame-40)%50<=5:
                n=(self.lastFrame-40)%50
                if (self.lastFrame-40)%50==0:
                    self.randomAngle3=random.random()*360
                    n=0
                    if not global_var.get_value('enemyFiring1'):
                        global_var.get_value('enemyGun_sound1').stop()
                        global_var.get_value('enemyGun_sound1').play()
                        global_var.set_value('enemyFiring1',True)
                for i in range(0,30):
                    new_bullet=Bullet.bact_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.setSpeed(self.randomAngle3+i*(360/30),4-0.1*n)
                    new_bullet.loadColor('lightBlue')
                    bullets.add(new_bullet)

            if (self.lastFrame-40)%100==0:
                self.gotoPosition(random.random()*60+330,random.random()*20+170,40)
        

        if self.health<=0 or self.frameLimit<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,40,True)
            self.reset=True
            self.ifSpell=True
            self.health=20000
            self.lastFrame=0
            global_var.get_value('enemyDead_sound').play()
    
    def spell_1(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            player.spellBonus=True
            self.maxHealth=57000
            self.health=57000
            self.gotoPosition(360,200,80)
            self.frameLimit=3600
            self.cardBonus=10000000
            self.spellName='Glaring Star[Comets]'
            self.gotoPosition(360,120,50)
            self.framePunishment=1700
            self.bulletSpeed=3
            global_var.get_value('spell_sound').play()
            new_effect=Effect.bossFaceSpell()
            effects.add(new_effect)
        
        self.cardBonus-=self.framePunishment
        if  (self.lastFrame-50)%40==25:
            self.randomPos=(random.random()*400+160,random.random()*30+30)
            new_effect=Effect.bulletCreate(2)
            new_effect.initial(self.randomPos[0],self.randomPos[1],144,32,15)
            effects.add(new_effect)
        if self.lastFrame>=50 and (self.lastFrame-50)%40==0:
            new_bullet=Bullet.big_star_Bullet_comet(1,40)
            new_bullet.initial(self.randomPos[0],self.randomPos[1],1)
            new_bullet.setSpeed(random.random()*140+20+0,4+random.random()*3)
            new_bullet.doColorCode(2)
            bullets.add(new_bullet)
        if self.lastFrame%10==0:
                global_var.get_value('kira_sound').stop()
                global_var.get_value('kira_sound').play()

        if self.lastFrame>=300:
            if (self.lastFrame-300)%120<=40 and (self.lastFrame-300)%4==0:
                '''
                new_effect=Effect.bulletCreate(1)
                new_effect.initial(self.tx,self.ty,144,64,4)
                effects.add(new_effect)
                '''
                if not global_var.get_value('enemyFiring2'):
                    global_var.get_value('enemyGun_sound2').stop()
                    global_var.get_value('enemyGun_sound2').play()
                    global_var.set_value('enemyFiring2',True)
                if (self.lastFrame-300)%120==0:
                    self.bulletSpeed=3
                for i in range(-1,2):
                    new_bullet=Bullet.big_star_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.selfTarget(player.cx,player.cy,8)
                    new_bullet.countAngle()
                    angle=new_bullet.angle+i*28
                    new_bullet.setSpeed(angle,self.bulletSpeed)
                    ##new_bullet.loadColor('red')
                    new_bullet.doColorCode(1)
                    bullets.add(new_bullet)
                self.bulletSpeed+=0.7
                '''
                    for j in range(1,5):
                        new_bullet=Bullet.big_star_Bullet()
                        new_bullet.initial(self.tx,self.ty,1)
                        new_bullet.selfTarget(player.cx,player.cy,8)
                        new_bullet.countAngle()
                        angle=new_bullet.angle+i*28
                        new_bullet.setSpeed(angle,8-j*1.3)
                        new_bullet.doColorCode(1)
                        bullets.add(new_bullet)
                '''
                        

        if self.lastFrame>=50 and (self.lastFrame-50)%240==0:
            d=random.random()*90+30
            if self.tx>=player.cx:
                sign=-1
            else:
                sign=1
            dx=(random.random()*(d-20)+20)*sign
            y_sign=(-1,1)
            dy=math.sqrt(d**2-dx**2)*y_sign[random.randint(0,1)]
            x_now=self.tx+dx
            y_now=self.ty+dy
            if x_now<=150:
                x_now=150
            if x_now>=570:
                x_now=570
            if y_now<140:
                y_now=140
            if y_now>220:
                y_now=220
            self.gotoPosition(x_now,y_now,50)


        if self.health<=0:
            self.cancalAllBullet(bullets,items,effects,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            self.createItem(items,0,10)
            self.createItem(items,1,20)
            self.createItem(items,6,1)
            self.drawResult(effects,self.cardBonus,player.spellBonus)
            #self.createItem(items,6,1)
            self.lastFrame=0
            if player.spellBonus:
                player.score+=self.cardBonus
                global_var.get_value('bonus_sound').play()
            global_var.get_value('spell_end').play()
        
        if self.frameLimit<=0:
            self.cancalAllBullet(bullets,items,effects,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            self.lastFrame=0
            self.drawResult(effects,self.cardBonus,False)
            global_var.get_value('spell_end').play()
        
    def noneSpell_2(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            self.maxHealth=50000
            self.health=50000
            self.gotoPosition(360,170,40)
            self.randomAngle=random.random()*360
            self.randomAngle2=self.randomAngle
            self.frameLimit=1800
            self.effectSign=0
        if self.lastFrame>=80:
            if (self.lastFrame-80)%4==0:
                self.effectSign+=1
                '''
                if self.effectSign%2==0:
                    new_effect=Effect.bulletCreate(3)
                else:
                    new_effect=Effect.bulletCreate(4)
                new_effect.initial(self.tx,self.ty,128,64,8)
                effects.add(new_effect)
                '''
                for i in range(0,7):
                    if not global_var.get_value('enemyFiring1'):
                        global_var.get_value('enemyGun_sound1').stop()
                        global_var.get_value('enemyGun_sound1').play()
                        global_var.set_value('enemyFiring1',True)
                    new_bullet=Bullet.satsu_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.setSpeed(self.randomAngle+i*(360/7),4)
                    new_bullet.loadColor('blue')
                    bullets.add(new_bullet)
                for j in range(0,7):
                    new_bullet=Bullet.satsu_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.setSpeed(self.randomAngle2+j*(360/7),4)
                    new_bullet.loadColor('purple')
                    bullets.add(new_bullet)
                self.randomAngle+=6
                self.randomAngle2-=6
            if (self.lastFrame-80)%100==0:
                self.gotoPosition(random.random()*60+330,random.random()*20+170,40)

        
        if self.health<=0 or self.frameLimit<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,70,True)
            self.reset=True
            self.ifSpell=True
            self.health=20000
            self.lastFrame=0
            global_var.get_value('enemyDead_sound').play()
    
    def spell_2(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            player.spellBonus=True
            self.maxHealth=50000
            self.health=self.maxHealth
            self.gotoPosition(360,200,80)
            self.frameLimit=3600
            self.cardBonus=10000000
            self.spellName='Star Rain[Star of hometown]'
            self.gotoPosition(360,120,50)
            self.framePunishment=1700
            global_var.get_value('spell_sound').play()
            new_effect=Effect.bossFaceSpell()
            effects.add(new_effect)

        self.cardBonus-=self.framePunishment
        if self.lastFrame>=80:
            if self.lastFrame%10==0:
                global_var.get_value('kira_sound').stop()
                global_var.get_value('kira_sound').play()

            if self.lastFrame%600<=360:
                if self.lastFrame%8==0:
                    angleInc=15*math.sin(frame/180*math.pi)
                    new_bullet=Bullet.laser_Bullet_immune(60,ratio=5)
                    new_bullet.length=28
                    new_bullet.ratio=8
                    area=random.randint(0,1)
                    if area==1:
                        rx=660+random.random()*10
                        ry=random.random()*680
                        new_bullet.initial(rx,ry,1)
                    else:
                        rx=random.random()*660
                        ry=random.random()*3+27
                        new_bullet.initial(rx,ry,1)
                    ra=90+43+angleInc+random.random()*4
                    rs=7+random.random()*1.5
                    new_bullet.setSpeed(ra,rs)
                    new_bullet.speed=rs+1
                    #new_bullet.loadColor('purple')
                    new_bullet.doColorCode(random.randint(0,15))
                    bullets.add(new_bullet)


            if self.lastFrame%600>=300:
                if self.lastFrame%2==0:
                    angleInc=10*math.sin(frame/180*math.pi*2)
                    new_bullet=Bullet.star_Bullet_immune(60)
                    new_bullet.length=15
                    area=random.randint(0,1)
                    if area==1:
                        new_bullet.initial(random.random()*20,random.random()*680,1)
                    else:
                        new_bullet.initial(random.random()*680,random.random()*20,1)

                    new_bullet.setSpeed(angleInc+43+random.random()*5,5+random.random()*2.5)
                    new_bullet.loadColor('purple')
                    bullets.add(new_bullet)

            if self.lastFrame%300==0:
                self.gotoPosition(player.cx+random.random()*60-30,random.random()*40+80,50)
            
            '''
            if self.lastFrame%150==140:
                new_effect=Effect.bulletCreate(4)
                new_effect.initial(self.tx,self.ty,256,48,10)
                effects.add(new_effect)
            '''
            if self.lastFrame>=100 and self.lastFrame%150==0:
                fireAngle=random.random()*360
                if not global_var.get_value('enemyFiring1'):
                    global_var.get_value('enemyGun_sound1').stop()
                    global_var.get_value('enemyGun_sound1').play()
                    global_var.set_value('enemyFiring1',True)
                for i in range(0,40):
                    new_bullet=Bullet.big_star_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.setSpeed(fireAngle+i*(360/40),3)
                    if i%2==0:
                        new_bullet.doColorCode(3)
                    else:
                        new_bullet.doColorCode(1)
                    bullets.add(new_bullet)

        if self.health<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,70,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            self.createItem(items,0,10)
            self.createItem(items,1,20)
            self.createItem(items,3,1)
            self.drawResult(effects,self.cardBonus,player.spellBonus)
            #self.createItem(items,6,1)
            self.lastFrame=0
            if player.spellBonus:
                player.score+=self.cardBonus
                global_var.get_value('bonus_sound').play()
            global_var.get_value('spell_end').play()
        
        if self.frameLimit<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,60,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            self.lastFrame=0
            self.drawResult(effects,self.cardBonus,False)
            global_var.get_value('spell_end').play()
    
    def noneSpell_3(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            self.maxHealth=50000
            self.health=50000
            self.gotoPosition(360,200,40)
            self.randomAngle=random.random()*360
            self.randomAngle2=self.randomAngle-360/30
            self.frameLimit=1800
            #self.color=['purple','seaBlue']
            self.colorNow=-1
        if self.lastFrame>=100:
            if (self.lastFrame-100)%10==0:
                self.colorNow+=1
                if self.colorNow%4>=2:
                    color="purple"
                    speed=3.6
                else:
                    color="seaBlue"
                    speed=4.5

                for i in range(0,15):
                    if not global_var.get_value('enemyFiring2'):
                        global_var.get_value('enemyGun_sound2').stop()
                        global_var.get_value('enemyGun_sound2').play()
                        global_var.set_value('enemyFiring2',True)
                    new_bullet=Bullet.mid_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.setSpeed(self.randomAngle+i*(360/15),speed)
                    new_bullet.loadColor(color)
                    bullets.add(new_bullet)
                if self.lastFrame%80>=40:
                    self.randomAngle2+=7
                else:
                    self.randomAngle2-=7

                for i in range(0,15):
                    if not global_var.get_value('enemyFiring2'):
                        global_var.get_value('enemyGun_sound2').stop()
                        global_var.get_value('enemyGun_sound2').play()
                        global_var.set_value('enemyFiring2',True)
                    new_bullet=Bullet.mid_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.setSpeed(self.randomAngle2+i*(360/15),speed)
                    new_bullet.loadColor(color)
                    bullets.add(new_bullet)
                if self.lastFrame%80>=40:
                    self.randomAngle-=7
                else:
                    self.randomAngle+=7

        

            if (self.lastFrame-40)%90==0:
                    self.gotoPosition(random.random()*60+330,random.random()*20+160,40)
                
        if self.health<=0 or self.frameLimit<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,70,True)
            self.reset=True
            self.ifSpell=True
            self.health=20000
            self.lastFrame=0
            global_var.get_value('enemyDead_sound').play()

    def spell_3(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            player.spellBonus=True
            self.maxHealth=50000
            self.health=self.maxHealth
            self.gotoPosition(360,200,80)
            self.frameLimit=3600
            self.cardBonus=10000000
            self.framePunishment=1700
            self.spellName='Milky Way[Path of magic stardust]'
            self.gotoPosition(360,120,50)
            global_var.get_value('spell_sound').play()
            new_effect=Effect.bossFaceSpell()
            effects.add(new_effect)

        self.cardBonus-=self.framePunishment
        if self.lastFrame%10==0 and self.lastFrame>=80:
                global_var.get_value('kira_sound').stop()
                global_var.get_value('kira_sound').play()

        if self.lastFrame>=80:
            if self.lastFrame%1==0:
                new_effect=Effect.bulletCreate(1)
                path=math.sin(frame/1.3/180*math.pi)*170+360
                n=1
                if self.lastFrame%2==0:
                    n=3
                for i in range(0,n):
                    rx=random.random()*600+60
                    while rx>path-100 and rx<path+100:
                        rx=random.random()*600+60
                    if self.lastFrame%2==0:
                        new_bullet=Bullet.star_Bullet()
                    else:
                        new_bullet=Bullet.big_star_Bullet()
                    new_bullet.initial(rx,30,1)
                    new_bullet.setSpeed(89.5+random.random(),3.5+random.random()*3)
                    if self.lastFrame%2==0:
                        new_bullet.loadColor('pink')
                        new_effect.initial(rx,30,64,24,3)
                    else:
                        new_bullet.doColorCode(2)
                        new_effect.initial(rx,30,128,64,3)
                    bullets.add(new_bullet)
                    #effects.add(new_effect)
        if (self.lastFrame-40)%60==50 and self.lastFrame>=80:
            new_effect=Effect.bulletCreate(1)
            new_effect.initial(self.tx,self.ty,192,48,10)
            #effects.add(new_effect)
        if (self.lastFrame-100)%60==0 and self.lastFrame>=80:
            if not global_var.get_value('enemyFiring1'):
                global_var.get_value('enemyGun_sound1').stop()
                global_var.get_value('enemyGun_sound1').play()
                global_var.set_value('enemyFiring1',True)
            new_bullet=Bullet.big_star_Bullet()
            new_bullet.initial(self.tx,self.ty,1)
            new_bullet.selfTarget(player.cx,player.cy,4)
            new_bullet.countAngle()
            angle=new_bullet.angle
            new_bullet.doColorCode(1)
            bullets.add(new_bullet)
            for i in range(-2,3):
                if i!=0:
                    new_bullet=Bullet.big_star_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.setSpeed(angle+i*40,4)
                    new_bullet.doColorCode(1)
                    bullets.add(new_bullet)
            for i in range(1,6):
                for j in range(-2,3):
                    new_bullet=Bullet.orb_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.setSpeed(angle+j*40,4-i*0.5)
                    new_bullet.loadColor('red')
                    bullets.add(new_bullet)

        if self.lastFrame>=100 and (self.lastFrame-100)%120==0:
            self.gotoPosition(player.cx+random.random()*40-20,random.random()*60+100,50)


        if self.health<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,40,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            self.createItem(items,0,10)
            self.createItem(items,1,20)
            self.createItem(items,4,20)
            self.drawResult(effects,self.cardBonus,player.spellBonus)
            #self.createItem(items,6,1)
            self.lastFrame=0
            if player.spellBonus:
                player.score+=self.cardBonus
                global_var.get_value('bonus_sound').play()
            global_var.get_value('spell_end').play()
        
        
        if self.frameLimit<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,40,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            self.lastFrame=0
            self.drawResult(effects,self.cardBonus,False)
            global_var.get_value('spell_end').play()
        
    def noneSpell_4(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            self.maxHealth=50000
            self.health=50000
            self.gotoPosition(360,220,40)
            self.randomAngle=random.random()*360
            self.randomAngle2=random.random()*360
            self.frameLimit=1800
            self.fireCount=0
        if self.lastFrame>=100:
            if (self.lastFrame-100)%180<=102:
                if self.lastFrame%12==0:
                    self.fireCount+=1
                    if not global_var.get_value('enemyFiring2'):
                        global_var.get_value('enemyGun_sound2').stop()
                        global_var.get_value('enemyGun_sound2').play()
                        global_var.set_value('enemyFiring2',True)
                    for i in range(0,24):
                        new_bullet=Bullet.butterfly_Bullet()
                        new_bullet.initial(self.tx,self.ty,1)
                        new_bullet.doColorCode(3)
                        if self.fireCount%2==0:
                            angle=self.randomAngle+i*(360/24)
                        else:
                            angle=self.randomAngle+(i+0.5)*(360/24)
                        new_bullet.setSpeed(angle,5.3)
                        
                        bullets.add(new_bullet)
            else:
                self.randomAngle=random.random()*360
            if (self.lastFrame-100)%180>=75:
                
                if self.lastFrame%5==0:
                    if not global_var.get_value('enemyFiring1'):
                        global_var.get_value('enemyGun_sound1').stop()
                        global_var.get_value('enemyGun_sound1').play()
                        global_var.set_value('enemyFiring1',True)
                    for i in range(0,12):
                        new_bullet=Bullet.butterfly_Bullet()
                        new_bullet.initial(self.tx,self.ty,1)
                        new_bullet.doColorCode(1)
                        new_bullet.setSpeed(self.randomAngle2+i*(360/12),6.0)
                        bullets.add(new_bullet)
                    self.randomAngle2+=17
            else:
                self.randomAngle2=random.random()*360
        
        if (self.lastFrame-100)%180==90:
            self.gotoPosition(random.random()*120+300,random.random()*50+150,80)


        if self.health<=0 or self.frameLimit<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,70,True)
            self.reset=True
            self.ifSpell=True
            self.health=20000
            self.lastFrame=0
            global_var.get_value('enemyDead_sound').play()

    def spell_4(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            player.spellBonus=True
            self.maxHealth=100000
            self.health=self.maxHealth
            self.gotoPosition(360,200,80)
            self.frameLimit=7200
            self.cardBonus=10000000
            self.framePunishment=300
            self.spellName='Crossing-over[Moon rise Sun dawn]'
            self.gotoPosition(360,240,50)
            self.randomAngle=random.random()*360
            global_var.get_value('spell_sound').play()
            self.directToggle=1
            self.fireCount=0
            new_effect=Effect.bossFaceSpell()
            effects.add(new_effect)
        self.cardBonus-=self.framePunishment
        if self.lastFrame>=80:
            if (self.lastFrame-80)%250==125:
                if self.percentHealth<=25:
                    s_interval=2
                    s_speed=7
                elif self.percentHealth<=75:
                    s_interval=4
                    s_speed=5.0
                else:
                    s_interval=5
                    s_speed=3.7
                if not global_var.get_value('enemyFiring1'):
                    global_var.get_value('enemyGun_sound1').stop()
                    global_var.get_value('enemyGun_sound1').play()
                    global_var.set_value('enemyFiring1',True)
                if self.directToggle%2==0:
                    new_effect=Effect.bulletCreate(6)
                else:
                    new_effect=Effect.bulletCreate(4)
                new_effect.initial(self.tx,self.ty,128,48,16)
                effects.add(new_effect)
                for j in range(0,2):
                    #self.randomAngle=random.random()*360
                    for i in range(0,30):
                        if i%s_interval==0:
                            new_bullet=Bullet.star_bullet_side_selfTarget()
                            if self.directToggle%2==1:
                                new_bullet.loadColor('skyBlue')
                            else:
                                new_bullet.loadColor('orange')
                        else:
                            new_bullet=Bullet.star_Bullet()
                            if self.directToggle%2==1:
                                new_bullet.loadColor('skyBlue')
                            else:
                                new_bullet.loadColor('orange')
                        new_bullet.toggle=self.directToggle
                        new_bullet.initial(self.tx,self.ty,1)
                        new_bullet.setSpeed(self.randomAngle+i*(360/30),4-0.5*j)
                        new_bullet.speed=s_speed
                        
                        bullets.add(new_bullet)
                self.randomAngle=random.random()*360
            if (self.lastFrame-80)%250==0:
                self.directToggle+=1
                time=1+math.floor(self.fireCount)
                if time>7:
                    time=7
                elif self.directToggle%2==0:
                        new_effect=Effect.powerUp()
                        new_effect.initial([self.tx,self.ty],600,50,(255,255,255),2,3,10)
                        effects.add(new_effect)
                        global_var.get_value('ch00_sound').play()
                if not global_var.get_value('enemyFiring1'):
                    global_var.get_value('enemyGun_sound1').stop()
                    global_var.get_value('enemyGun_sound1').play()
                    global_var.set_value('enemyFiring1',True)
                if self.directToggle%2==0:
                    code=4
                else:
                    code=6
                new_effect=Effect.bulletCreate(code)
                new_effect.initial(self.tx,self.ty,192,80,24)
                effects.add(new_effect)
                self.randomAngle2=random.random()*360
                for i in range(0,time):
                    if self.directToggle%2==0:
                        new_bullet=Bullet.big_star_Bullet_slave(2)
                    else:
                        new_bullet=Bullet.big_star_Bullet_slave(-2)
                    new_bullet.doColorCode(code)
                    new_bullet.toggle=self.directToggle
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.setSpeed(self.randomAngle2+i*(360/time),3.5)
                    bullets.add(new_bullet)
                self.fireCount+=1

        
        if self.lastFrame>=80 and (self.lastFrame-80)%200==120:
            self.gotoPosition(random.random()*30+345,random.random()*30+225,60)


        if self.health<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,60,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            self.createItem(items,0,10)
            self.createItem(items,1,10)
            self.createItem(items,4,30)
            self.drawResult(effects,self.cardBonus,player.spellBonus)
            #self.createItem(items,6,1)
            self.lastFrame=0
            if player.spellBonus:
                player.score+=self.cardBonus
                global_var.get_value('bonus_sound').play()
            global_var.get_value('spell_end').play()
        
        
        if self.frameLimit<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,60,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            self.lastFrame=0
            self.drawResult(effects,self.cardBonus,False)
            global_var.get_value('spell_end').play()

    def noneSpell_5(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            self.maxHealth=45000
            self.health=45000
            self.gotoPosition(360,220,40)
            self.randomAngle=random.random()*360
            self.randomAngle2=0
            self.frameLimit=1800


        '''
        if self.lastFrame>=50:
            if (self.lastFrame-50)%2==0:
                self.randomAngle2+=0.34
                for i in range(0,10):
                    new_bullet=Bullet.small_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.loadColor('purple')
                    new_bullet.setSpeed(self.randomAngle+i*(360/10)+self.randomAngle2,6.5)
                    bullets.add(new_bullet)
                self.randomAngle+=5+self.randomAngle2
        '''
        if self.lastFrame>=60:
            if (self.lastFrame-60)%4==0:
                if not global_var.get_value('kiraing'):
                    global_var.get_value('kira_sound').stop()
                    global_var.get_value('kira_sound').play()
                    global_var.set_value('kiraing',True)
                self.randomAngle2+=0.84
                '''
                new_effect=Effect.bulletCreate(2)
                new_effect.initial(self.tx,self.ty,100,24,4)
                effects.add(new_effect)
                '''
                for i in range(0,8):
                    new_bullet=Bullet.scale_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.loadColor('purple')
                    new_bullet.setSpeed(self.randomAngle+i*(360/8)+self.randomAngle2,5.7)
                    bullets.add(new_bullet)
                self.randomAngle+=6+self.randomAngle2

        if self.health<=0 or self.frameLimit<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,60,True)
            self.reset=True
            self.ifSpell=True
            self.health=20000
            self.lastFrame=0
            global_var.get_value('enemyDead_sound').play()
        
    def spell_5(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            player.spellBonus=True
            self.maxHealth=50000
            self.health=self.maxHealth
            self.gotoPosition(360,200,80)
            self.frameLimit=4800
            self.cardBonus=10000000
            self.framePunishment=1300
            self.spellName='Star Fountain[Enchanted Fragments]'
            self.gotoPosition(360,240,50)
            self.randomAngle=random.random()*360
            global_var.get_value('spell_sound').play()
            new_effect=Effect.bossFaceSpell()
            effects.add(new_effect)
        self.cardBonus-=self.framePunishment
        if self.lastFrame>=70:
            if (self.lastFrame-70)%700<=400 or (self.lastFrame-70)%700==690:
                if (self.lastFrame-70)%700%200==190 or self.lastFrame==70 or (self.lastFrame-70)%700==690:
                    new_effect=Effect.bulletCreate(3)
                    new_effect.initial(self.tx,self.ty,144,64,10)
                    effects.add(new_effect)
            
            if (self.lastFrame-70)%700==540:
                new_effect=Effect.bulletCreate(3)
                new_effect.initial(self.tx,self.ty,144,64,10)
                effects.add(new_effect)
            if (self.lastFrame-70)%700<=400:
                if (self.lastFrame-70)%700%200==0:
                    new_bullet=Bullet.star_Bullet_fountain()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.selfTarget(player.cx,player.cy,5)
                    new_bullet.doColorCode(3)
                    bullets.add(new_bullet)
                    global_var.get_value('enemyGun_sound1').play()
            elif (self.lastFrame-70)%700==550:
                new_bullet=Bullet.star_Bullet_fountain()
                new_bullet.initial(self.tx,self.ty,1)
                new_bullet.selfTarget(player.cx,player.cy,5)
                new_bullet.countAngle()
                angle=new_bullet.angle-180
                new_bullet.setSpeed(angle,5)
                new_bullet.doColorCode(3)
                bullets.add(new_bullet)
                global_var.get_value('enemyGun_sound1').play()
                for i in range(-1,2):
                    if i!=0:
                        new_bullet=Bullet.star_Bullet_fountain()
                        new_bullet.initial(self.tx,self.ty,1)
                        new_bullet.setSpeed(angle+i*40,5)
                        new_bullet.doColorCode(3)
                        bullets.add(new_bullet)

        if (self.lastFrame-70)%700==450:
            global_var.get_value('ch00_sound').play()
        
        if (self.lastFrame-70)%200==50:
            self.gotoPosition(random.random()*380+170,random.random()*180+100,50)

        if self.health<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,60,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            self.createItem(items,0,20)
            self.createItem(items,1,10)
            self.createItem(items,4,30)
            self.drawResult(effects,self.cardBonus,player.spellBonus)
            #self.createItem(items,6,1)
            self.lastFrame=0
            if player.spellBonus:
                player.score+=self.cardBonus
                global_var.get_value('bonus_sound').play()
            global_var.get_value('spell_end').play()
        
        
        if self.frameLimit<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,60,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            self.lastFrame=0
            self.drawResult(effects,self.cardBonus,False)
            global_var.get_value('spell_end').play()
    
    def noneSpell_6(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            self.maxHealth=60000
            self.health=60000
            self.gotoPosition(360,220,40)
            self.randomAngle=random.random()*360
            self.randomAngle2=random.random()*360
            self.frameLimit=1800
        
        if self.lastFrame>=60:
            if (self.lastFrame-60)%13==0:
                new_effect=Effect.bulletCreate(3)
                new_effect.initial(self.tx,self.ty,192,100,13)
                #effects.add(new_effect)
                global_var.get_value('enemyGun_sound2').play()
                for i in range(0,8):
                    new_bullet=Bullet.star_Bullet_Part4_Hex()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.direction=-1
                    new_bullet.rotationAngle=0.5
                    new_bullet.speed=4
                    new_bullet.setSpeed(self.randomAngle+i*(360/8),4)
                    new_bullet.loadColor('blue')
                    bullets.add(new_bullet)
                for j in range(0,8):
                    new_bullet=Bullet.star_Bullet_Part4_Hex()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.direction=1
                    new_bullet.rotationAngle=0.5
                    new_bullet.speed=4
                    new_bullet.setSpeed(self.randomAngle2+j*(360/8),4)
                    new_bullet.loadColor('purple')
                    bullets.add(new_bullet)
                self.randomAngle+=7
                self.randomAngle2-=7
                    
        
        if self.health<=0 or self.frameLimit<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,70,True)
            self.reset=True
            self.ifSpell=True
            self.health=20000
            self.lastFrame=0
            global_var.get_value('enemyDead_sound').play()   
    
    def spell_6(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            player.spellBonus=True
            self.maxHealth=75000
            self.health=self.maxHealth
            self.gotoPosition(360,180,80)
            self.frameLimit=4800
            self.cardBonus=10000000
            self.framePunishment=1300
            self.spellName='Light-shade[FireFly and DarkStar]'
            self.gotoPosition(360,240,50)
            self.randomAngle=random.random()*360
            self.randomAngle2=random.random()*360
            global_var.get_value('spell_sound').play()
            new_effect=Effect.bossFaceSpell()
            effects.add(new_effect)
        self.cardBonus-=self.framePunishment

        if self.lastFrame>=80:
            if (self.lastFrame-80)%10==0:
                if not global_var.get_value('enemyFiring2'):
                    global_var.get_value('enemyGun_sound2').stop()
                    global_var.get_value('enemyGun_sound2').play()
                    global_var.set_value('enemyFiring2',True)
                for i in range(0,12):
                    new_bullet=Bullet.orb_Bullet_distance()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.loadColor('orange')
                    new_bullet.setSpeed(self.randomAngle+i*(360/12),3+random.random()*1.5)
                    bullets.add(new_bullet)
                self.randomAngle+=6
        
            if (self.lastFrame-80)%30==0:
                if not global_var.get_value('enemyFiring1'):
                            global_var.get_value('enemyGun_sound1').stop()
                            global_var.get_value('enemyGun_sound1').play()
                            global_var.set_value('enemyFiring1',True)
                for i in range(0,7):
                    new_bullet=Bullet.big_star_Bullet_distance()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.doColorCode(1)
                    new_bullet.setSpeed(self.randomAngle2+i*(360/7),2+random.random()*2)
                    bullets.add(new_bullet)
                self.randomAngle2=random.random()*360

        if self.health<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,70,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            self.createItem(items,0,20)
            self.createItem(items,1,15)
            self.createItem(items,4,30)
            self.drawResult(effects,self.cardBonus,player.spellBonus)
            #self.createItem(items,6,1)
            self.lastFrame=0
            if player.spellBonus:
                player.score+=self.cardBonus
                global_var.get_value('bonus_sound').play()
            global_var.get_value('spell_end').play()
        
        if (self.lastFrame-80)%100==0:
                self.gotoPosition(random.random()*60+330,random.random()*20+170,40)
        
        if self.frameLimit<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,70,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            self.lastFrame=0
            self.drawResult(effects,self.cardBonus,False)
            global_var.get_value('spell_end').play()
    
    def noneSpell_7(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            self.maxHealth=50000
            self.health=50000
            self.gotoPosition(360,270,40)
            self.randomAngle=random.random()*360
            #self.randomAngle2=random.random()*360
            self.frameLimit=2100
        
        if self.lastFrame>=80 and (self.lastFrame-80)%7==0:
            if not global_var.get_value('enemyFiring2'):
                global_var.get_value('enemyGun_sound2').stop()
                global_var.get_value('enemyGun_sound2').play()
                global_var.set_value('enemyFiring2',True)
            new_effect=Effect.bulletCreate(4)
            new_effect.initial(self.tx,self.ty,128,64,7)
            #effects.add(new_effect)

            for i in range(0,5):
                new_bullet=Bullet.mid_Bullet()
                new_bullet.initial(self.tx,self.ty,1)
                new_bullet.setSpeed(self.randomAngle+i*(360/5),5.)
                new_bullet.loadColor('blue')
                bullets.add(new_bullet)
                for j in range(-1,2):
                    if j!=0:
                        new_bullet=Bullet.mid_Bullet()
                        new_bullet.initial(self.tx,self.ty,1)
                        new_bullet.setSpeed(self.randomAngle+i*(360/5)+j*2,4.7)
                        new_bullet.loadColor('blue')
                        bullets.add(new_bullet)
            self.randomAngle-=13

        if (self.lastFrame-80)%180==90:
            self.gotoPosition(random.random()*120+300,random.random()*50+150,80)

        if self.health<=0 or self.frameLimit<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,60,True)
            self.reset=True
            self.ifSpell=True
            self.health=20000
            self.lastFrame=0
            global_var.get_value('enemyDead_sound').play()
    
    def spell_7(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            player.spellBonus=True
            self.maxHealth=80000
            self.health=self.maxHealth
            self.gotoPosition(360,180,80)
            self.frameLimit=4800
            self.cardBonus=10000000
            self.framePunishment=1300
            self.spellName='Summon[Star Duplication Curse]'
            self.gotoPosition(360,240,50)
            self.randomAngle=random.random()*360
            self.randomAngle2=random.random()*360
            global_var.get_value('spell_sound').play()
            new_effect=Effect.bossFaceSpell()
            effects.add(new_effect)
        self.cardBonus-=self.framePunishment
        if (self.lastFrame-60)%300==0:
            self.eventNum+=1
            global_var.set_value('bossEvent_'+str(self.eventNum),False)
            new_bullet=Bullet.orb_Bullet_star_pattern_main(30,9,self.eventNum)
            new_bullet.initial(self.tx,self.ty,1)
            new_bullet.selfTarget(player.cx,player.cy,new_bullet.n)
            new_bullet.countAngle()
            new_bullet.setSpeed(new_bullet.angle,new_bullet.n)
            new_bullet.countAngle()
            new_bullet.splitAngle=new_bullet.angle
            new_bullet.loadColor('orange')
            new_bullet.trackColor='orange'
            new_bullet.transColor='lakeBlue'
            bullets.add(new_bullet)

            new_bullet=Bullet.orb_Bullet_star_pattern_main(40,6,self.eventNum)
            new_bullet.initial(self.tx,self.ty,1)
            new_bullet.selfTarget(player.cx,player.cy,new_bullet.n)
            new_bullet.countAngle()
            new_bullet.setSpeed(new_bullet.angle+180,new_bullet.n)
            new_bullet.countAngle()
            new_bullet.splitAngle=new_bullet.angle
            new_bullet.loadColor('red')
            new_bullet.trackColor='red'
            new_bullet.transColor='blue'
            bullets.add(new_bullet)

        if (self.lastFrame-60)%300==150:
            self.callNum+=1
            global_var.set_value('bossEvent_'+str(self.eventNum),True)
            global_var.get_value('kira_sound').stop()
            global_var.get_value('kira_sound').play()
        
        if self.lastFrame>250 and (self.lastFrame-60)%300==250:
            global_var.get_value('kira_sound').stop()
            global_var.get_value('kira_sound').play()

        if self.health<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,90,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            self.createItem(items,0,20)
            self.createItem(items,1,15)
            self.createItem(items,4,30)
            self.drawResult(effects,self.cardBonus,player.spellBonus)
            #self.createItem(items,6,1)
            self.lastFrame=0
            if player.spellBonus:
                player.score+=self.cardBonus
                global_var.get_value('bonus_sound').play()
            global_var.get_value('spell_end').play()
        
        
        if self.frameLimit<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,90,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            self.lastFrame=0
            self.drawResult(effects,self.cardBonus,False)
            global_var.get_value('spell_end').play()

    def noneSpell_8(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            self.maxHealth=50000
            self.health=50000
            self.gotoPosition(360,230,40)
            self.randomAngle=random.random()*360
            #self.randomAngle2=random.random()*360
            self.frameLimit=2100
            self.fireCount=0
        
        if self.lastFrame>=90:
            if (self.lastFrame-90)%20==0:

                if not global_var.get_value('enemyFiring1'):
                    global_var.get_value('enemyGun_sound1').stop()
                    global_var.get_value('enemyGun_sound1').play()
                    global_var.set_value('enemyFiring1',True)
                bulletNum=random.randint(20,46)
                sx=self.tx-100+random.random()*200
                sy=self.ty-100+random.random()*200
                sspeed=180/bulletNum
                new_effect=Effect.bulletCreate(0)
                new_effect.initial(sx,sy,128,64,10)
                #effects.add(new_effect)
                #colorCode=random.randint(0,15)
            
                for i in range(0,bulletNum):
                    new_bullet=Bullet.satsu_Bullet()
                    new_bullet.initial(sx,sy,1)
                    new_bullet.anmStay=True
                    #buffAngle=(i*(360/bulletNum))%90
                    #if buffAngle<=45:
                     #   speed=sspeed/math.cos(buffAngle/180*math.pi)
                    #else:
                     #   speed=sspeed/math.cos((90-buffAngle)/180*math.pi)
                    new_bullet.setSpeed(self.randomAngle+i*(360/bulletNum),sspeed)
                    new_bullet.loadColor('purple')
                    #new_bullet.doColorCode(colorCode)
                    bullets.add(new_bullet)
                self.randomAngle=random.random()*360
                '''
                bulletTotal=50
                colorList=['purple','blue','green','pink','red','white']
                num=[12,9]
                #side=random.randint(3,10)
                #num=bulletTotal//side
                if self.fireCount%2==0:
                    pos=[[random.random()*20+100+self.tx,self.ty],[-random.random()*20-100+self.tx,self.ty]]
                else:
                    pos=[[-random.random()*20-100+self.tx,self.ty],[random.random()*20+100+self.tx,self.ty]]
                sideNum=[3,4]
                speed=[random.random()*1+3,random.random()*0.4+2]
                resAngle=[60,45]
                self.fireCount+=1
                for i in range(2):
                    colorNum=self.fireCount%5
                    new_bullet=Bullet.small_Bullet()
                    new_bullet.initial(pos[i][0],pos[i][1],1)
                    new_bullet.selfTarget(player.cx,player.cy,speed[i])
                    new_bullet.countAngle()
                    angle=new_bullet.angle
                    danmaku.polyByLength(bullets,Bullet.satsu_Bullet,num[i],sideNum[i],speed[i],angle,pos[i],colorList[colorNum])
                    danmaku.polyByLength(bullets,Bullet.satsu_Bullet,num[i],sideNum[i],speed[i],angle-resAngle[i],pos[i],colorList[colorNum])
                    self.randomAngle=random.random()*360
                '''
            if (self.lastFrame-90)%200==0:
                self.gotoPosition(280+160*random.random(),200+60*random.random(),60)
                
                 
        if self.health<=0 or self.frameLimit<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,60,True)
            self.reset=True
            self.ifSpell=True
            self.health=20000
            self.lastFrame=0
            global_var.get_value('enemyDead_sound').play()
    
    def spell_8(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            player.spellBonus=True
            self.maxHealth=80000
            self.health=self.maxHealth
            self.gotoPosition(360,180,80)
            self.frameLimit=4800
            self.cardBonus=10000000
            self.framePunishment=1300
            self.spellName='Light track[Mind confusing star]'
            self.gotoPosition(360,250,50)
            self.randomAngle=random.random()*360
            global_var.get_value('spell_sound').play()
            new_effect=Effect.bossFaceSpell()
            effects.add(new_effect)
        self.cardBonus-=self.framePunishment

        if not self.powerUp:
            interval=100
            intense=40
            color='white'
        else:
            interval=70
            intense=50
            color='grey'

        if self.lastFrame>=80:
            if (self.lastFrame-80)%interval==0:
                sx=self.tx-100+random.random()*200
                sy=self.ty-100+random.random()*150
                new_effect=Effect.bulletCreate(4)
                new_effect.initial(sx,sy,128,64,7)
                #effects.add(new_effect)
                '''
                danmaku.polyByLength(bullets,Bullet.orb_Bullet_bouncing_5,intense//6,3,2.3,self.randomAngle,[sx,sy],color)
                danmaku.polyByLength(bullets,Bullet.orb_Bullet_bouncing_5,intense//6,3,2.3,self.randomAngle-60,[sx,sy],color)
                '''
                for i in range(0,intense):
                    new_bullet=Bullet.orb_Bullet_bouncing_5()
                    new_bullet.initial(sx,sy,1)
                    new_bullet.setSpeed(self.randomAngle+i*(360/intense),2.6)
                    if not self.powerUp:
                        new_bullet.loadColor('white')
                    else:
                        new_bullet.loadColor('grey')
                    bullets.add(new_bullet)
                self.randomAngle=random.random()*360

                if not global_var.get_value('enemyFiring1'):
                    global_var.get_value('enemyGun_sound1').stop()
                    global_var.get_value('enemyGun_sound1').play()
                    global_var.set_value('enemyFiring1',True)
                
            if (self.lastFrame-80)%100==20:
                self.gotoPosition(280+160*random.random(),200+60*random.random(),60)

        if self.health<=30000 or self.frameLimit<=1200:
            if (self.lastFrame-80)%180==100 and not self.powerUp:
                global_var.get_value('ch00_sound').play()
                self.powerUp=True


        if self.health<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,70,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            self.createItem(items,0,20)
            self.createItem(items,1,25)
            self.createItem(items,4,30)
            self.drawResult(effects,self.cardBonus,player.spellBonus)
            self.lastFrame=0
            #self.createItem(items,6,1)
            if player.spellBonus:
                player.score+=self.cardBonus
                global_var.get_value('bonus_sound').play()
            global_var.get_value('spell_end').play()
        
        
        if self.frameLimit<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,70,True)
            self.reset=True
            self.ifSpell=False
            self.cardNum+=1
            self.health=20000
            self.lastFrame=0
            self.drawResult(effects,self.cardBonus,False)
            global_var.get_value('spell_end').play()
    
    def noneSpell_9(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            self.maxHealth=40000
            self.health=40000
            self.gotoPosition(360,230,80)
            self.randomAngle=random.random()*360
            #self.randomAngle2=random.random()*360
            self.frameLimit=5100
            self.directToggle=1
            self.colorCode=['darkBlue','red','orange','yellow','green','blue','blue','lakeBlue','purple','pink','white','grey','jade']
            self.releaseAngle=0
            self.fireCount=0
        if self.lastFrame>=150:
            if (self.lastFrame-150)%300<=36:
                if (self.lastFrame-150)%300==0:
                    self.laserColor=random.randint(0,15)
                    self.warnFrame=30
                    self.warnNow=self.warnFrame
                    self.fireCount=0
                    new_bullet=Bullet.small_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    px=global_var.get_value('player1x')
                    py=global_var.get_value('player1y')
                    new_bullet.selfTarget(px,py,2)
                    new_bullet.countAngle()
                    self.releaseAngle=new_bullet.angle
                if (self.lastFrame-150)%2==0:
                    num=37
                    for k in range(0,1):
                        for i in range(0,2):
                            for j in range(0,2):
                                new_bullet=Bullet.laser_line()
                                new_bullet.initial(self.tx,self.ty,1)
                                if j==0:
                                    releaseAngle=self.releaseAngle+(i-0.5)*2*self.fireCount*(360/num)
                                    color=6
                                else:
                                    releaseAngle=(self.releaseAngle+(i-0.5)*2*self.fireCount*(360/num))+180
                                    color=6
                                new_bullet.setFeature(releaseAngle,16,self.warnNow+100,self.warnNow,64,2,2,60)
                                new_bullet.ifSimplifiedMode=True
                                new_bullet.dDegree=0
                                new_bullet.doColorCode(self.laserColor)
                                bullets.add(new_bullet)
                        self.warnNow=30#round((self.warnFrame-10)*(1-((self.lastFrame-150)%300/50))+10)
                        #print(self.warnNow)
                        self.fireCount+=1
            '''
            if (self.lastFrame-150)%60==0:
                if not global_var.get_value('enemyFiring1'):
                    global_var.get_value('enemyGun_sound1').stop()
                    global_var.get_value('enemyGun_sound1').play()
                    global_var.set_value('enemyFiring1',True)
                new_bullet=Bullet.orb_Bullet()
                new_bullet.initial(self.tx,self.ty,1)
                new_bullet.selfTarget(player.cx,player.cy,5.5)
                new_bullet.countAngle()
                angle=new_bullet.angle
                new_bullet.loadColor("red")
                bullets.add(new_bullet)
                for i in range(1,10):
                    new_bullet=Bullet.orb_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.setSpeed(angle+i*5*self.directToggle,5.5)
                    new_bullet.loadColor("red")
                    bullets.add(new_bullet)
                if self.directToggle==1:
                    self.directToggle=-1
                else:
                    self.directToggle=1
            '''
        
        '''
        if self.health<=round(0.5*self.maxHealth) or self.frameLimit<=1200:
            interval=16
            inc=32
        else:
            interval=30
            inc=64
        speed=4
        if self.lastFrame>=150:
            if (self.lastFrame-150)%interval==0.5*interval:
                    if not global_var.get_value('enemyFiring2'):
                        global_var.get_value('enemyGun_sound2').stop()
                        global_var.get_value('enemyGun_sound2').play()
                        global_var.set_value('enemyFiring2',True)
                    new_bullet=Bullet.orb_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    #new_bullet.selfTarget(player.cx,player.cy,3)
                    new_bullet.setSpeed(self.randomAngle,speed)
                    new_bullet.countAngle()
                    angleN=new_bullet.angle
                    new_bullet.loadColor("jade")
                    bullets.add(new_bullet)
        
                    for i in range(-6,7):
                        if i!=0:
                            new_bullet=Bullet.orb_Bullet()
                            new_bullet.initial(self.tx,self.ty,1)
                            new_bullet.setSpeed(angleN+i*10,speed)
                            if self.directToggle==1:
                                new_bullet.loadColor(self.colorCode[-i+5])
                            else:
                                new_bullet.loadColor(self.colorCode[i+5])
                            bullets.add(new_bullet)
                    
                    #part 2
                    new_bullet=Bullet.orb_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    #new_bullet.selfTarget(player.cx,player.cy,3)
                    new_bullet.setSpeed(self.randomAngle-180,speed)
                    new_bullet.countAngle()
                    angleN=new_bullet.angle
                    new_bullet.loadColor("jade")
                    bullets.add(new_bullet)
        
                    for i in range(-6,7):
                        if i!=0:
                            new_bullet=Bullet.orb_Bullet()
                            new_bullet.initial(self.tx,self.ty,1)
                            new_bullet.setSpeed(angleN+i*10,speed)
                            if self.directToggle==1:
                                new_bullet.loadColor(self.colorCode[-i+5])
                            else:
                                new_bullet.loadColor(self.colorCode[i+5])
                            bullets.add(new_bullet)

                    



                    self.randomAngle+=inc
        '''
        if self.health<=0 or self.frameLimit<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,70,True)
            self.reset=True
            self.ifSpell=True
            self.health=20000
            self.lastFrame=0
            global_var.get_value('enemyDead_sound').play()

    def spell_9(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        #spell start
        if self.reset:
            self.lastFrame=0
            self.reset=False
            player.spellBonus=True
            self.maxHealth=80000
            self.health=self.maxHealth
            #self.gotoPosition(360,160,80)
            self.frameLimit=7200
            self.cardBonus=10000000
            self.fireCount=0
            self.framePunishment=1300
            self.spellName='Holy Spell [Magic orb]'
            self.gotoPosition(360,220,50)
            self.randomAngle=random.random()*360
            global_var.get_value('spell_sound').play()
            new_effect=Effect.bossFaceSpell()
            effects.add(new_effect)
            #self.spell9_colorList=[2,4,6,8,10]
        self.cardBonus-=self.framePunishment

        '''
        intervalAngle=50
        if self.lastFrame>=160:
            if self.lastFrame%270==140:
                new_effect=Effect.bulletCreate(5)
                new_effect.initial(self.tx,self.ty,256,144,20)
                effects.add(new_effect)
            if (self.lastFrame-160)%270==0:
                if not global_var.get_value('enemyFiring3'):
                    global_var.get_value('enemyGun_sound3').stop()
                    global_var.get_value('enemyGun_sound3').play()
                    global_var.set_value('enemyFiring3',True)
                for i in range(0,4):
                    new_bullet=Bullet.big_Bullet_tracing_test()
                    new_bullet.initial(self.tx,self.ty,3)
                    new_bullet.setSpeed(270-intervalAngle*1.5+i*intervalAngle,5)
                    new_bullet.loadColor('green')
                    bullets.add(new_bullet)

        #sound effect
        if (self.lastFrame-160)%270==240:
            global_var.get_value("ch00_sound").play()
        
        '''

        #test card 9 光彩陆离乱舞
        if self.lastFrame>=160:
            if self.lastFrame%300==0:
                global_var.get_value('enemyGun_sound1').stop()
                global_var.get_value('enemyGun_sound1').play()
                if self.fireCount%2==0:
                    direction=1
                else:
                    direction=-1
                for i in range(0,5):
                    new_bullet=Bullet.circle_laser_slave()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.setFeature(self.randomAngle+i*(360/5),direction,2,(i+1)*2)
                    new_bullet.setSpeed(self.randomAngle+i*(360/5),2)
                    bullets.add(new_bullet)
                self.randomAngle=random.random()*360
                self.fireCount+=1
        if self.lastFrame%300==260:
            new_effect=Effect.powerUp()
            new_effect.initial((self.tx,self.ty),400,40,(255,255,255),2,3,10)
            effects.add(new_effect)
        if self.lastFrame%300==0 and self.lastFrame>300:
            self.gotoPosition(random.random()*80+320,random.random()*30+200,60)
        #spell end
        if self.health<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,60,True)
            self.reset=True
            self.ifSpell=True
            self.cardNum+=1
            self.health=20000
            self.createItem(items,0,20)
            self.createItem(items,1,25)
            self.createItem(items,4,30)
            self.drawResult(effects,self.cardBonus,player.spellBonus)
            #self.createItem(items,6,1)
            self.lastFrame=0
            if player.spellBonus:
                player.score+=self.cardBonus
                global_var.get_value('bonus_sound').play()
            global_var.get_value('spell_end').play()
        
        
        if self.frameLimit<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,70,True)
            self.reset=True
            self.ifSpell=True
            self.cardNum+=1
            self.health=20000
            self.lastFrame=0
            self.drawResult(effects,self.cardBonus,False)
            global_var.get_value('spell_end').play()
        

    def spell_10(self,frame,items,effects,bullets,backgrounds,enemys,slaves,player):
        if self.reset:
            self.lastFrame=0
            self.reset=False
            player.spellBonus=True
            self.maxHealth=180000
            self.health=self.maxHealth
            #self.gotoPosition(360,160,80)
            self.frameLimit=12000
            self.cardBonus=10000000
            self.framePunishment=300
            self.spellName="[Hogwarts Four Spirits]" 
            self.gotoPosition(360,250,50)
            self.randomAngle=random.random()*360
            new_effect=Effect.bossFaceSpell()
            effects.add(new_effect)

        if self.lastFrame==1 or self.lastFrame==40 or self.lastFrame==80:
            global_var.get_value('ch00_sound').stop()
            global_var.get_value('ch00_sound').play()
        
        if self.lastFrame==120:
            global_var.get_value('spell_sound').play()
        self.cardBonus-=self.framePunishment

        basicHealth=50000
        quarterHealth=(self.maxHealth-basicHealth)/4
        self.powerRank=4-math.ceil((self.health-basicHealth)/quarterHealth)
        if self.powerRank>=4:
            self.powerRank=4
        if self.lastFrame>=120*60 and self.powerRank<4:
            self.powerRank=4
        if self.powerRank>self.lastRank:
            self.actionFrame=-1
            global_var.get_value('ch00_sound').play()
            new_effect=Effect.powerUp()
            new_effect.initial([self.tx,self.ty],600,50,(255,255,255),2,3,10)
            effects.add(new_effect)
        
        density=self.powerRank*4+12
        speed=self.powerRank*0.3+3
        interval=20-2*self.powerRank



        if self.lastFrame>=120:
            self.actionFrame+=1
            if self.actionFrame%2000==0 and self.powerRank>=4:
                new_enemy=ghost_slytherin_spirit()
                new_enemy.initialize(self.tx,self.ty,1,-1)
                enemys.add(new_enemy)
                global_var.get_value("option_sound").play()
            if self.actionFrame%1500==self.spell10_int[self.powerRank][0] and self.powerRank>=2:
                new_enemy=ghost_hufflepuff_spirit()
                new_enemy.initialize(self.tx,self.ty,1,-1)
                enemys.add(new_enemy)
                global_var.get_value("option_sound").play()
            if self.actionFrame%1500==self.spell10_int[self.powerRank][1] and self.powerRank>=3:
                new_enemy=ghost_gryffindor_spirit()
                new_enemy.initialize(self.tx,self.ty,1,-1)
                enemys.add(new_enemy)
                global_var.get_value("option_sound").play()
            if self.actionFrame%1500==self.spell10_int[self.powerRank][2] and self.powerRank>=1:
                new_enemy=ghost_ravenclaw_spirit()
                new_enemy.orient([self.tx,self.ty])
                new_enemy.initialize(self.tx,self.ty,1,-1)
                enemys.add(new_enemy)
                global_var.get_value("option_sound").play()
            if (self.lastFrame-120)%interval==0 and global_var.get_value('enemySum')<=0:
                angle=random.random()*360
                self.spell10_time+=1
                if self.spell10_time%4==0:
                    colorCode=1
                elif self.spell10_time%4==1:
                    colorCode=3
                elif self.spell10_time%4==2:
                    colorCode=6
                elif self.spell10_time%4==3:
                    colorCode=5
                new_effect=Effect.bulletCreate(colorCode)
                new_effect.initial(self.tx,self.ty,128,64,interval)
                effects.add(new_effect)
                if not global_var.get_value('enemyFiring3'):
                    global_var.get_value('enemyGun_sound3').stop()
                    global_var.get_value('enemyGun_sound3').play()
                    global_var.set_value('enemyFiring3',True)
                for i in range(0,density):
                    new_bullet=Bullet.mid_Bullet()
                    new_bullet.initial(self.tx,self.ty,1)
                    new_bullet.setSpeed(angle-i*(360/density),speed)
                    new_bullet.loadColor(self.spell10_color[self.spell10_time%4])
                    bullets.add(new_bullet)
            
            if (self.lastFrame-120)%(interval*3)==0 and global_var.get_value('bulletSum')<=20:
                direct=random.randint(0,1)
                new_effect=Effect.bulletCreate(5)
                new_effect.initial(self.tx,self.ty,144,64,10)
                effects.add(new_effect)
                if not global_var.get_value('enemyFiring1'):
                    global_var.get_value('enemyGun_sound1').stop()
                    global_var.get_value('enemyGun_sound1').play()
                    global_var.set_value('enemyFiring1',True)
                if direct==0:
                    direct=-1
                for i in range (0,10):
                    for j in range(0,3):
                        new_bullet=Bullet.mid_Bullet()
                        new_bullet.initial(self.tx,self.ty,1)
                        new_bullet.selfTarget(player.cx,player.cy,5-i*0.3)
                        new_bullet.countAngle()
                        angle=new_bullet.angle-(j-1)*30+i*0.7*direct
                        new_bullet.setSpeed(angle,5-i*0.3)
                        new_bullet.loadColor('green')
                        bullets.add(new_bullet)

        if self.lastFrame%100==0:
            pass
            #print(self.powerRank,' ',self.health)

        self.lastRank=self.powerRank
        if self.health<=0:
            self.cancalAllBullet(bullets,items,effects,True)
            self.reset=True
            self.ifSpell=True
            self.health=20000
            self.cardNum+=1
            self.lastFrame=0
            self.drawResult(effects,self.cardBonus,player.spellBonus)
            #self.createItem(items,6,1)
            if player.spellBonus:
                player.score+=self.cardBonus
                global_var.get_value('bonus_sound').play()
            #global_var.get_value('bossDead_sound').play()
            for enemy in enemys:
                enemy.doKill(effects,items,bullets)
            #self.kill()
        
        
        if self.frameLimit<=0:
            #self.cancalAllBullet(bullets,items,effects,True)
            self.addLastingCancel(self.tx,self.ty,slaves,120,True)
            self.reset=True
            self.ifSpell=True
            self.health=20000
            self.cardNum+=1
            self.lastFrame=0
            self.drawResult(effects,self.cardBonus,False)
            #global_var.get_value('bossDead_sound').play()
            for enemy in enemys:
                enemy.doKill(effects,items,bullets)
            #self.kill()
