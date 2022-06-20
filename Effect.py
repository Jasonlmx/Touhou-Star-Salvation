import pygame,sys
import random
import math
import gF
from pygame.sprite import Sprite
import global_var


pygame.font.init()

class flyingObj(pygame.sprite.Sprite):
    def __init__(self):
        super(flyingObj,self).__init__()
        self.surf = pygame.Surface((5,5))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.tx=0.0
        self.ty=0.0
        self.type=0
        self.speedx=0
        self.speedy=0
        self.startFrame=-1
        self.angle=0
        self.fro=0 #determine where the bullet is from
        self.dx=0
        self.dy=0
        self.distance=10000
        self.graze=1
        self.cancalable=True
        self.speed=0
        self.anmStay=False
        self.createMax=0
        self.lastFrame=0
        self.ifAdjustSign=global_var.get_value('if_speedAdjusting')
        self.ifDrawCreate=global_var.get_value('if_highQuality_effect')
        self.validAccuracy=(0,0,0,0)
    def genEffect(self,effects):
        pass

    def initial(self,posx,posy,occupy):
        self.tx=posx
        self.ty=posy
        self.fro=occupy

    def truePos(self):
        self.rect.centerx=self.tx
        self.rect.centery=self.ty

    def movement(self):
        if not self.anmStay or self.lastFrame>=self.createMax:
            tick=global_var.get_value('DELTA_T')
            if self.ifAdjustSign:
                self.tx+=self.speedx*60/1000*tick
                self.ty+=self.speedy*60/1000*tick
            else:
                self.tx+=self.speedx
                self.ty+=self.speedy
        self.truePos()
    
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
        #self.speed=speed
    #def update(self):

    def checkValid(self):
        if self.rect.top>=720-30+self.validAccuracy[1]:
            self.kill()
        if self.rect.bottom<=0+30-self.validAccuracy[0]:
            self.kill()
        if self.rect.right<=0+60-self.validAccuracy[3]:
            self.kill()
        if self.rect.left>=660+self.validAccuracy[2]:
            self.kill()

class fire_effect_player(pygame.sprite.Sprite):
    def __init__(self):
        super(fire_effect_player,self).__init__()
        self.surf = pygame.Surface((5,5))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.part=0
        self.interval=3
        self.frame=0
        self.color='green'
        self.tx=0
        self.ty=0
        self.x=0
        self.y=0
        self.upper=False
        self.lower=False
    def initial(self,tx,ty,color):
        self.tx=tx
        self.ty=ty
        self.loadColor(color)

    def loadColor(self,color):
        self.image=[]
        for i in range(1,4):
            effect=pygame.image.load('resource/playerFire/'+color+'_effect'+str(i)+'.png').convert_alpha()
            effect=pygame.transform.scale(effect,(24,48))
            self.image.append(effect)
    
    def update(self,screen):
        self.frame+=1
        if self.frame==self.interval:
            self.part+=1
            self.frame=0
        if self.part==3:
            self.kill()
        if self.part<=2:
            screen.blit(self.image[self.part],(self.tx-12,self.ty-24))

class fire_effect_reimu_main(pygame.sprite.Sprite):
    def __init__(self):
        super(fire_effect_reimu_main,self).__init__()
        self.image=pygame.Surface((96,24)).convert_alpha()
        self.image.fill((0,0,0,0))
        self.image.blit(global_var.get_value('reimu_fire'),(0,0),(0,0,96,24))
        #self.image.set_alpha(180)
        self.frame=0
        self.part=0
        self.interval=5
        self.speed=4
        self.temp=[]
        for i in range(0,4):
            temp=pygame.Surface((24,24)).convert_alpha()
            temp.fill((0,0,0,0))
            temp.blit(self.image,(0,0),(0+24*i,0,24,24))
            self.temp.append(temp)
        self.tx=0
        self.ty=0
        self.x=0
        self.y=0
        self.upper=False
        self.lower=False

    def initial(self,tx,ty):
        self.tx=tx
        self.ty=ty

    def update(self,screen):
        self.frame+=1
        self.ty-=self.speed
        if self.frame==self.interval:
            self.part+=1
            self.frame=0
        if self.part==4:
            self.kill()
        if self.part<=3:
            #angle=self.frame*-25-90
            gF.drawRotation(self.temp[self.part],(round(self.tx-12),round(self.ty-12)),-90,screen)
            #screen.blit(self.temp[self.part],(round(self.tx-12),round(self.ty-12)))

class fire_effect_reimu_target(pygame.sprite.Sprite):
    def __init__(self):
        super(fire_effect_reimu_target,self).__init__()
        self.image=pygame.Surface((96,24)).convert_alpha()
        self.image.fill((0,0,0,0))
        self.image.blit(global_var.get_value('reimu_fire'),(0,0),(0,24,96,24))
        #self.image.set_alpha(180)
        self.frame=0
        self.part=0
        self.interval=5
        self.speed=4
        self.temp=[]
        for i in range(0,4):
            temp=pygame.Surface((24,24)).convert_alpha()
            temp.fill((0,0,0,0))
            temp.blit(self.image,(0,0),(0+24*i,0,24,24))
            self.temp.append(temp)
        self.tx=0
        self.ty=0
        self.x=0
        self.y=0
        self.upper=False
        self.lower=False

    def initial(self,tx,ty):
        self.tx=tx
        self.ty=ty

    def update(self,screen):
        self.frame+=1
        self.ty-=self.speed
        if self.frame==self.interval:
            self.part+=1
            self.frame=0
        if self.part==4:
            self.kill()
        if self.part<=3:
            gF.drawRotation(self.temp[self.part],(round(self.tx-12),round(self.ty-12)),self.frame*-12-90,screen)
            #screen.blit(self.image[self.part],(self.tx-12,self.ty-24))

class bulletVanish(pygame.sprite.Sprite):
    def __init__(self):
        super(bulletVanish,self).__init__()
        self.frame=0
        self.image=global_var.get_value("watcher")
        self.dx=0
        self.dy=0
        self.cx=0
        self.cy=0
        self.interval=2
        self.part=0
        self.upper=False
        self.lower=False
    def initial(self,image,cx,cy,dx,dy):
        self.image=image
        self.cx=cx
        self.cy=cy
        self.dx=dx
        self.dy=dy

    def update(self,screen):
        self.frame+=1
        self.part=math.floor(self.frame/self.interval)
        w,h=self.image.get_size()
        n=1-0.12*self.part
        w_now=round(w*n)
        h_now=round(h*n)
        cR=n
        tempImage=pygame.transform.scale(self.image,(w_now,h_now)).convert_alpha()
        #tempImage.set_alpha(256-40*self.part)
        screen.blit(tempImage,(self.cx-round(self.dx*cR),self.cy-round(self.dy*cR)))
        if self.part>=6:
            self.kill()

class enemyDead(pygame.sprite.Sprite):
    def __init__(self):
        super(enemyDead,self).__init__()
        self.frame=0
        self.image=pygame.image.load('resource/sprite/sprite_dead.png')
        self.decorate=pygame.transform.scale(self.image,(84,16))
        self.deco_rotation=random.random()*180-90
        self.cx=0
        self.cy=0
        self.interval=1
        self.part=0
        self.coef=0.10
        self.upper=False
        self.lower=False
    def initial(self,image,cx,cy):
        self.image=image
        self.cx=cx
        self.cy=cy

    def update(self,screen):
        self.frame+=1
        self.part=math.floor(self.frame/self.interval)
        '''
        w,h=self.image.get_size()
        w_now=round(w*(1+self.coef*self.part))
        h_now=round(h*(1+self.coef*self.part))
        cR=1+self.coef*self.part
        tempImage=pygame.transform.scale(self.image,(w_now,h_now))
        tempImage.set_alpha(220-20*self.part)
        screen.blit(tempImage,(self.cx-round(w_now/2),self.cy-round(h_now/2)))
        '''
        w_d,h_d=self.decorate.get_size()
        w_d_now=round(w_d*(1+self.coef*self.part))
        h_d_now=round(0.127*self.part**2+1)
        tempDec=pygame.transform.smoothscale(self.decorate,(w_d_now,h_d_now))
        tempDec.set_alpha(246-8*self.part)
        for i in range(0,3):
            gF.drawRotation(tempDec,(self.cx-round(w_d_now/2),self.cy-round(h_d_now/2)),self.deco_rotation+(360/3)*i,screen)

        if self.part>=24:
            self.kill()

class itemFade(pygame.sprite.Sprite):
    def __init__(self):
        super(itemFade,self).__init__()
        self.frame=0
        self.image=pygame.image.load('resource/sprite/sprite_dead.png')
        self.cx=0
        self.cy=0
        self.interval=4
        self.part=0
        self.upper=False
        self.lower=False
    def initial(self,image,cx,cy):
        self.image=image
        self.cx=cx
        self.cy=cy

    def update(self,screen):
        self.frame+=1
        self.part=math.floor(self.frame/self.interval)
        self.image.set_alpha(256-48*self.part)
        screen.blit(self.image,(self.cx-12,self.cy-12-self.frame*3))
        if self.part>=4:
            self.kill()

class screenText(pygame.sprite.Sprite):
    def __init__(self):
        super(screenText,self).__init__()
        self.lastFrame=0
        self.maxLastFrame=180
        self.image=pygame.Surface((384,48))
        self.upper=True
        self.lower=False
    def update(self,screen):
        self.lastFrame+=1
        self.draw(screen)
        if self.lastFrame>=self.maxLastFrame:
            self.kill()
    def draw(self,screen):
        pass

class bonusText(screenText):
    def __init__(self):
        super(bonusText,self).__init__()
        self.image=pygame.Surface((384,48)).convert_alpha()
        self.image.fill((0,0,0,0))
        self.image.blit(global_var.get_value('front00'), (0, 0), (386,144,382,48))
        self.bonus=100000
        self.font=pygame.font.SysFont('arial', 28)
        self.transFrame=30
        self.lower=False
    def getBonus(self,bonus):
        self.bonus=bonus

    def draw(self,screen):
        if self.lastFrame<=self.transFrame:
            height=round(48*self.lastFrame/self.transFrame)
            #print(height)
            #screen.blit(pygame.transform.scale(self.image,(384,height)),(168,100))
            screen.blit(pygame.transform.scale(self.image,(384,height)),(148,100+(24-round(0.5*height))))
        elif self.lastFrame>=self.maxLastFrame-self.transFrame:
            height=round(48*(self.maxLastFrame-self.lastFrame)/self.transFrame)
            #screen.blit(pygame.transform.scale(self.image,(384,height)),(168,100))
            screen.blit(pygame.transform.scale(self.image,(384,height)),(148,100+(24-round(0.5*height))))
        else:
            #pass
            screen.blit(self.image,(148,100))
        bonus=self.font.render(str(self.bonus), True, (255, 255, 255))
        bonus_shade=self.font.render(str(self.bonus), True, (30, 30, 30))
        w=bonus.get_width()
        h=bonus.get_height()
        if self.lastFrame<=self.transFrame:
            height=round(h*self.lastFrame/self.transFrame)
            #print(height)
            #screen.blit(pygame.transform.scale(self.image,(384,height)),(168,100))
            screen.blit(pygame.transform.scale(bonus_shade,(w,height)),(340-round(w/2)+2,140+(round(h/2-0.5*height))+3))
            screen.blit(pygame.transform.smoothscale(bonus,(w,height)),(340-round(w/2),140+(round(h/2-0.5*height))))
        elif self.lastFrame>=self.maxLastFrame-self.transFrame:
            height=round(h*(self.maxLastFrame-self.lastFrame)/self.transFrame)
            #screen.blit(pygame.transform.scale(self.image,(384,height)),(168,100))
            screen.blit(pygame.transform.scale(bonus_shade,(w,height)),(340-round(w/2)+2,140+(round(h/2-0.5*height))+3))
            screen.blit(pygame.transform.smoothscale(bonus,(w,height)),(340-round(w/2),140+(round(h/2-0.5*height))))
        else:
            #pass
            screen.blit(bonus_shade,((340-round(w/2)+2),140+3))
            screen.blit(bonus,((340-round(w/2)),140))
        #screen.blit(bonus,((360-round(w/2)),140))
    
class failText(screenText):
    def __init__(self):
        super(failText,self).__init__()
        self.image=pygame.Surface((240,48)).convert_alpha()
        self.image.fill((0,0,0,0))
        self.image.blit(global_var.get_value('front00'), (0, 0), (386,576,238,48))
        self.transFrame=30
        self.lower=False
    def draw(self,screen):
        if self.lastFrame<=self.transFrame:
            height=round(48*self.lastFrame/self.transFrame)
            #print(height)
            #screen.blit(pygame.transform.scale(self.image,(384,height)),(168,100))
            screen.blit(pygame.transform.smoothscale(self.image,(240,height)),(220,100+(24-round(0.5*height))))
        elif self.lastFrame>=self.maxLastFrame-self.transFrame:
            height=round(48*(self.maxLastFrame-self.lastFrame)/self.transFrame)
            #screen.blit(pygame.transform.scale(self.image,(384,height)),(168,100))
            screen.blit(pygame.transform.smoothscale(self.image,(240,height)),(220,100+(24-round(0.5*height))))
        else:
            #pass
            screen.blit(self.image,(220,100))
        #screen.blit(self.image,(240,100))

class powerMaxText(screenText):
    def __init__(self):
        super(powerMaxText,self).__init__()
        self.image=pygame.Surface((234,48)).convert_alpha()
        self.image.fill((0,0,0,0))
        self.image.blit(global_var.get_value('front00'), (0, 0), (386,240,232,48))
    
    def draw(self,screen):
        screen.blit(self.image,(223,52))
    
class extendText(screenText):
    def __init__(self):
        super(extendText,self).__init__()
        self.image=pygame.Surface((234,48)).convert_alpha()
        self.image.fill((0,0,0,0))
        self.image.blit(global_var.get_value('front00'), (0, 0), (386,333,148,48))
    
    def draw(self,screen):
        screen.blit(self.image,(266,160))

class wave(pygame.sprite.Sprite):
    def __init__(self):
        super(wave,self).__init__()
        self.pos=[0,0]
        self.radius=0
        self.lastFrame=0
        self.maxFrame=30
        self.maxRadius=100
        self.color=(255,255,255)
        self.width=6
        self.rainbow=False
        self.upper=False
        self.lower=False
    def initial(self,pos,maxRadius,maxFrame,color,width):
        self.maxRadius=maxRadius
        self.maxFrame=maxFrame
        self.pos=pos
        self.color=color
        self.width=width
    
    def update(self,screen):
        self.lastFrame+=1
        self.radius=round(self.maxRadius*(self.lastFrame/self.maxFrame))
        if not self.rainbow:
            r,g,b=self.color
            color_now=(round(r*(1-self.lastFrame/self.maxFrame)),round(g*(1-self.lastFrame/self.maxFrame)),round(b*(1-self.lastFrame/self.maxFrame)))
        else:
            r,g,b=self.getRainbowColor()
            color_now=(r,g,b)
        pygame.draw.circle(screen,color_now,self.pos,self.radius,self.width)
        if self.maxFrame<=self.lastFrame:
            self.kill()
    def getRainbowColor(self):
        max=self.maxRadius
        i=self.radius
        r=0
        g=0
        b=0
        if i<max/3:
            r=255
            g=math.ceil(255*3*i/max)
            b=0
        elif i<max/2:
            r=math.ceil(750-i*(250*6/max))
            g=255
            b=0
        elif(i<max*2/3):
            r=0
            g=255
            b=math.ceil(i*(250*6/max)-750)
        elif(i<max*5/6):
            r=0
            g=math.ceil(1250-i*(250*6/max))
            b=255
        else:
            r=math.ceil(150*i*(6/max)-750)
            g=0
            b=255
        return r,g,b
class powerUp(pygame.sprite.Sprite):
    def __init__(self):
        super(powerUp,self).__init__()
        self.pos=[0,0]
        self.radius=0
        self.lastFrame=0
        self.maxFrame=30
        self.maxRadius=900
        self.color=(255,255,255)
        self.width=6
        self.num=5
        self.interval=20
        self.upper=False
        self.lower=False
    def initial(self,pos,maxRadius,maxFrame,color,width,num,interval):
        self.maxRadius=maxRadius
        self.maxFrame=maxFrame
        self.pos=pos
        self.color=color
        self.width=width
        self.num=num
        self.interval=interval
    def update(self,screen):
        self.lastFrame+=1
        self.radius=round(self.maxRadius*(1-self.lastFrame/self.maxFrame))
        for i in range(0,self.num):
            r,g,b=self.color
            color_now=(round(r*self.lastFrame/self.maxFrame),round(g*self.lastFrame/self.maxFrame),round(b*self.lastFrame/self.maxFrame))
            pygame.draw.circle(screen,color_now,self.pos,self.radius+self.interval*i,self.width)
        if self.maxFrame<=self.lastFrame:
            self.kill()

class grazeEffect(pygame.sprite.Sprite):
    def __init__(self):
        super(grazeEffect,self).__init__()
        self.pos=[0,0]
        self.radius=0
        self.lastFrame=0
        self.maxFrame=30
        self.maxRadius=8
        self.color=(255,255,255)
        self.width=6
        self.num=5
        self.interval=20
        self.upper=True
        self.lower=False
        self.tx=0.0
        self.ty=0.0
        self.type=0
        self.speedx=0
        self.speedy=0
        self.direction=random.random()*360
    def movement(self):
        self.tx+=self.speedx
        self.ty+=self.speedy
    
    
    def setSpeed(self,angle,speed):
        s=math.sin(math.radians(angle))
        c=math.cos(math.radians(angle))
        self.speedy=s*speed
        self.speedx=c*speed
    
    def update(self,screen):
        self.lastFrame+=1
        self.movement()
        self.draw(screen)
        self.checkValid()


    def initial(self,pos,maxRadius,maxFrame,color,width,num,interval,speedMin=3,speedFluc=2):
        self.maxRadius=maxRadius
        self.minRadius=2
        self.maxFrame=maxFrame
        self.pos=pos
        self.tx=pos[0]
        self.ty=pos[1]
        self.color=color
        self.width=width
        self.num=num
        self.interval=interval
        self.setSpeed(self.direction,random.random()*speedFluc+speedMin)
    
    def checkValid(self):
        if self.lastFrame>=self.maxFrame:
            self.kill()

    def draw(self,screen):
        radius=round(self.maxRadius-(self.maxRadius-self.minRadius)*(self.lastFrame/self.maxFrame))
        pygame.draw.circle(screen,self.color,(round(self.tx),round(self.ty)),radius,self.width)

class bulletCreate(pygame.sprite.Sprite):
    def __init__(self,code):
        super(bulletCreate,self).__init__()
        #self.surf = pygame.Surface((32,32))
        self.colorNum=code
        self.tx=0
        self.ty=0
        self.max=64
        self.min=24
        self.maxFrame=10
        self.lastFrame=0
        self.upper=True
        self.lower=False
        self.angle=random.random()*360
        self.alpha=256
        self.lowestAlpha=200
        self.getImage()
    def getImage(self):
        self.image=pygame.Surface((32,32)).convert_alpha()
        self.image.fill((0,0,0,0))
        #self.image=self.image.convert_alpha()
        self.image.blit(global_var.get_value('bullet_create_image').convert_alpha(), (0, 0), (32*self.colorNum,0, 32, 32))
    
    def initial(self,centerx,centery,Max,Min,maxFrame):
        self.tx=centerx
        self.ty=centery
        self.max=Max
        self.min=Min
        self.maxFrame=maxFrame
    
    def checkValid(self):
        if self.lastFrame>=self.maxFrame:
            self.kill()

    def update(self,screen):
        size=round(self.max-(self.lastFrame/self.maxFrame)*(self.max-self.min))
        self.alpha=round((self.lastFrame/self.maxFrame)*(256-self.lowestAlpha)+self.lowestAlpha)
        self.temp=pygame.transform.scale(self.image,(size,size))
        #self.temp.set_alpha(self.alpha)
        self.draw(size,screen)
        self.lastFrame+=1
        self.checkValid()

    def draw(self,size,screen):
        gF.drawRotation(self.temp,(round(self.tx-size/2),round(self.ty-size/2)),self.angle,screen)
    
class bossFlame(pygame.sprite.Sprite):
    def __init__(self):
        super(bossFlame,self).__init__()
        self.effFlameImg=global_var.get_value('effFlameImg')
        self.maxFrame=30
        self.max=100
        self.min=20
        self.lastFrame=0
        self.upper=False
        self.lower=True
        self.temp=0
        self.rand=random.randint(-5,5)
    def initial(self,Max,Min,maxFrame):
        self.max=Max
        self.min=Min
        self.maxFrame=maxFrame
    
    def checkValid(self):
        if self.lastFrame>=self.maxFrame:
            self.kill()
        
    def update(self,screen):
        size=round(self.min+(self.lastFrame/self.maxFrame)*(self.max-self.min))
        alpha=round(256-(self.lastFrame/self.maxFrame)*180)
        self.temp=pygame.transform.scale(self.effFlameImg,(72,size))
        self.temp.set_alpha(alpha)
        self.draw(size,screen)
        self.lastFrame+=1
        self.checkValid()
    
    def draw(self,size,screen):
        tx=global_var.get_value('boss1x')
        ty=global_var.get_value('boss1y')
        screen.blit(self.temp,(round(tx-36+self.rand),round(ty-size)))

class bossLight(pygame.sprite.Sprite):
    def __init__(self):
        super(bossLight,self).__init__()
        self.effFlameImg=global_var.get_value('effLightImg')
        self.angle=random.random()*360
        self.lastFrame=0
        self.upper=False
        self.lower=True
        self.temp=0
        self.startSize=120
    def initial(self,maxFrame):
        self.maxFrame=maxFrame
    
    def checkValid(self):
        if self.lastFrame>=self.maxFrame:
            self.kill()
        
    def update(self,screen):
        size=round(self.startSize-(self.startSize-72)*(self.lastFrame/self.maxFrame))
        self.draw(screen,size)
        self.lastFrame+=1
        self.checkValid()
    
    def draw(self,screen,size):
        self.temp=pygame.transform.scale(self.effFlameImg,(size,size))
        alpha=round(156*(self.lastFrame/self.maxFrame))+100
        self.temp.set_alpha(alpha)
        tx=global_var.get_value('boss1x')
        ty=global_var.get_value('boss1y')
        gF.drawRotation(self.temp,(round(tx-size/2),round(ty-size/2)),self.angle,screen)

class bossFaceSpell(pygame.sprite.Sprite):
    def __init__(self):
        super(bossFaceSpell,self).__init__()
        self.image=global_var.get_value('satoriImg')
        #self.image.set_alpha(200)
        self.lx=660
        self.ly=-20
        self.lastFrame=0
        self.upper=True
        self.lower=False
    def update(self,screen):
        self.lastFrame+=1
        self.movement()
        screen.blit(self.image,(self.lx,self.ly))
        if self.lastFrame>=100:
            self.kill()
    def movement(self):
        if self.lastFrame<=20:
            self.lx-=23
            self.ly+=1.3
        elif self.lastFrame<=70:
            self.lx-=0.2
            self.ly-=0
        else:
            self.lx-=20
            self.ly+=3.7

class sanaeFaceSpell(bossFaceSpell):
    def __init__(self):
        super(sanaeFaceSpell,self).__init__()
        self.image=global_var.get_value('sanaeImg')
        self.lx=660
        self.ly=0
class spellAttackImage(pygame.sprite.Sprite):
    def __init__(self):
        super(spellAttackImage,self).__init__()
        self.length=800
        self.width=640-96
        self.Image=pygame.Surface((self.length,self.width)).convert_alpha()
        self.Image.fill((0,0,0,0))
        self.subImage=pygame.Surface((128*1.5,16*1.5)).convert_alpha()
        self.subImage.fill((0,0,0,0))
        self.subImage.blit(global_var.get_value('effectBar'),(0,0),(0,96*1.5,128*1.5,16*1.5))
        self.lastFrame=0
        self.maxFrame=80
        self.movingSpeed=4
        self.midSign=900
        self.transFrame=20
        self.transAlpha=7
        self.x=0
        self.y=0
        self.upper=False
        self.lower=True
        self.alpha=256
        self.midAlphaSign=200
    def initial(self,x,y):
        self.x=x
        self.y=y
    
    def imageAlpha(self):
        if self.lastFrame<self.transFrame:
            self.alpha=self.midAlphaSign-(self.transFrame-self.lastFrame)*self.transAlpha
        elif self.lastFrame>self.maxFrame-self.transFrame:
            self.alpha=self.midAlphaSign-(self.lastFrame-(self.maxFrame-self.transFrame))*self.transAlpha
        else:
            self.alpha=self.midAlphaSign
        self.Image.set_alpha(self.alpha)
    def update(self,screen):
        self.checkValid()
        self.Image.fill((0,0,0,0))
        self.lastFrame+=1
        self.midSign+=self.movingSpeed
        for i in range(0,17):
            for j in range(0,20):
                if i%2==1:
                    x=1000+128*1.5*j-self.midSign
                    y=i*32
                    if x<1000:
                        self.Image.blit(self.subImage,(x,y))
                else:
                    x=0-128*1.5*j+self.midSign
                    y=i*32
                    if x+128*1.5>0:
                        self.Image.blit(self.subImage,(x,y))
        self.imageAlpha()
        self.draw(screen)
    def checkValid(self):
        if self.lastFrame>=self.maxFrame:
            self.kill()
    
    def draw(self,screen):
        gF.drawRotation(self.Image,(self.x-self.length/2,self.y-self.width/2),20,screen)
        #screen.blit(self.Image,(self.x,self.y))

class scoreImage(pygame.sprite.Sprite):
    font=pygame.font.Font('./resource/font/AaBanRuoKaiShu-2.ttf', 12)
    def __init__(self,size=12):
        super(scoreImage,self).__init__()
        self.speed=1.7
        self.randPos=random.random()*8-4
        self.tx=0
        self.ty=0
        self.upper=False
        self.lower=True
        self.score=0
        self.colorDict=[(225,225,55),(223,0,38),(78,200,175),(244,244,244)]   
        self.wordDict=[u'〇',u'一',u'二',u'三',u'四',u'五',u'六',u'七',u'八',u'九']
        self.color=(255,255,255)    
        self.surf=0
        self.lastFrame=0
        self.maxFrame=50
        self.changeFrame=6
        self.width=0
        self.height=0
    def initial(self,tx,ty,score,colorType=0):
        self.tx=tx+self.randPos
        self.ty=ty
        self.score=score
        self.color=self.colorDict[colorType]
        self.makeWord(score)

    def makeWord(self,score):
        strScore=str(score)
        digit=len(strScore)
        if digit>=8:
            strScore=strScore[0:9]
        word=''
        for char in strScore:
            index=int(char)
            word=word+self.wordDict[index]
        self.surf=self.font.render(word,True,self.color)
        self.rect=self.surf.get_rect()
        self.width=self.surf.get_width()
        self.height=self.surf.get_height()
    def checkValid(self):
        if self.lastFrame>=self.maxFrame:
            self.kill()
    
    def movement(self):
        self.ty-=self.speed
        self.rect.centerx=round(self.tx)
        self.rect.centery=round(self.ty)
    
    def draw(self,screen):
        if self.lastFrame<=self.changeFrame:
            width=self.width/self.changeFrame*self.lastFrame
        elif self.lastFrame>=self.maxFrame-self.changeFrame:
            width=self.width/self.changeFrame*(self.maxFrame-self.lastFrame)
        else:
            width=self.width
        height=self.height
        screen.blit(self.surf,self.rect,(0,0,width,height))

    def update(self,screen):
        self.lastFrame+=1
        self.checkValid()
        self.movement()
        self.draw(screen)

class bossBrusterTestObj(flyingObj):
    def __init__(self):
        super(bossBrusterTestObj,self).__init__()
        self.maxFrame=80
        self.upper=False
        self.lower=True

    def update(self,screen):
        self.lastFrame+=1
        self.movement()
        self.draw(screen)
        self.checkValid()

    def draw(self,screen):
        pygame.draw.circle(screen,(253,43,124),(round(self.tx),round(self.ty)),30,6)

    def checkValid(self):
        if self.lastFrame>=self.maxFrame:
            self.kill()

class bossBrustMomiji(bossBrusterTestObj):
    def __init__(self):
        super(bossBrustMomiji,self).__init__()
        self.maxFrame=60
        self.surf=pygame.Surface((32,32)).convert_alpha()
        self.surf.fill((0,0,0,0))
        self.surf.blit(global_var.get_value('etama2'),(0,0),(32,224,32,32))
        self.angle=random.random()*360
        self.randR=[-1,1]
        self.angleInc=(3+random.random()*2)*self.randR[random.randint(0,1)]
        self.width=32
        self.widthInc=3
        self.widthMinor=-(self.width+(self.widthInc*(self.maxFrame-20)))/20+1
        self.alpha=256
        self.alphaInc=-0.8
        self.alphaMinor=-(256+self.alphaInc*(self.maxFrame-20))/20
    
    def update(self, screen):
        self.lastFrame+=1
        self.angle+=self.angleInc
        if self.lastFrame<=self.maxFrame-20:
            self.width+=self.widthInc
        else:
            self.width+=self.widthMinor
        if self.lastFrame<=self.maxFrame-20:
            self.alpha+=self.alphaInc
        else:
            self.alpha+=self.alphaMinor
        self.movement()
        self.draw(screen)
        self.checkValid()

    def draw(self,screen):
        tempImage=pygame.transform.smoothscale(self.surf,(round(self.width),round(self.width))).convert_alpha()
        tempImage.set_alpha(round(self.alpha))
        gF.drawRotation(tempImage,(round(self.tx)-self.width/2,round(self.ty)-self.width/2),self.angle,screen)
        #screen.blit(self.surf,(round(self.tx)-16,round(self.ty)-16))

class bossPowerMomiji(bossBrustMomiji):
    def __init__(self):
        super(bossPowerMomiji,self).__init__()
        self.maxFrame=60
        self.surf=pygame.Surface((32,32)).convert_alpha()
        self.surf.fill((0,0,0,0))
        self.surf.blit(global_var.get_value('etama2'),(0,0),(0,224,32,32))
        self.angle=random.random()*360
        self.randR=[-1,1]
        self.angleInc=(4+random.random()*3)*self.randR[random.randint(0,1)]
        self.width=64
        self.widthInc=-0.3
        self.widthMinor=self.widthInc
        self.alpha=100
        self.alphaInc=2.8
        self.alphaMinor=(256-(self.maxFrame-20)*self.alphaInc-100)/20
    
def bossBruster(tx,ty,effects,object=bossBrustMomiji,number=40):
    for i in range(number):
        angle=random.random()*360
        speed=2+random.random()*8
        new_effect=object()
        new_effect.initial(tx,ty,1)
        new_effect.setSpeed(angle,speed)
        effects.add(new_effect)

def bossPower(tx,ty,effects,object=bossPowerMomiji,number=40):
    initialAngle=random.random()*360
    for i in range(number):
        angle=i*(360/number)+initialAngle
        speed=6+random.random()*0.4
        new_effect=object()
        dist=speed*new_effect.maxFrame
        nx=tx+dist*math.cos(angle*math.pi/180)
        ny=ty+dist*math.sin(angle*math.pi/180)
        new_effect.initial(nx,ny,1)
        new_effect.setSpeed(angle-180,speed)
        effects.add(new_effect)

    
class sanae_spell_3_side_line(pygame.sprite.Sprite):
    def __init__(self):
        super(sanae_spell_3_side_line,self).__init__()
        self.actionNum=0
        self.lineColor=((235,184,0),(137,245,78))
        self.posXList=(63,617)
        self.maxFrame=200
        self.changeFrame=30
        self.density=1
        self.lastFrame=0
        self.upper=False
        self.lower=True

    def update(self,screen):
        self.lastFrame+=1
        self.draw(screen)
        self.checkValid()
    def checkValid(self):
        if self.lastFrame>=self.maxFrame:
            self.kill()

    def draw(self,screen):
        if self.lastFrame<=self.changeFrame:
            self.density=self.lastFrame/self.changeFrame
        elif self.lastFrame>self.maxFrame-self.changeFrame:
            self.density=(self.maxFrame-self.lastFrame)/self.changeFrame
        else:
            self.density=1
        color=self.lineColor[self.actionNum]
        r=round(color[0]*self.density)
        g=round(color[1]*self.density)
        b=round(color[2]*self.density)
        colorNow=(r,g,b)
        pygame.draw.line(screen,colorNow,(63,30),(63,690),6)
        pygame.draw.line(screen,colorNow,(617,30),(617,690),6)

class sanae_spell5_flame(pygame.sprite.Sprite):
    def __init__(self):
        super(sanae_spell5_flame,self).__init__()
        self.lastFrame=0
        self.actionNum=0
        self.size=20
        self.maxFrame=10
        self.upper=False
        self.lower=True
        self.tx=0
        self.ty=0
        self.color=((254,168,174),(250,218,132))
    def initial(self,tx,ty):
        self.tx=tx
        self.ty=ty

    def update(self, screen):
        self.lastFrame+=1
        self.changeSize()
        self.draw(screen)
        self.checkValid()
    
    def checkValid(self):
        if self.lastFrame>=self.maxFrame:
            self.kill()

    def draw(self,screen):
        pygame.draw.circle(screen,self.color[self.actionNum],(round(self.tx),round(self.ty)),round(self.size/2))

    def changeSize(self):
        self.size-=20/self.maxFrame

class level2Title(pygame.sprite.Sprite):
    def __init__(self):
        super(level2Title,self).__init__()
        self.img=global_var.get_value('level2Title')
        self.upper=True
        self.lower=False
        self.lastFrame=0
        self.maxFrame=150
        self.changeFrame=10
    def doFade(self):
        if self.lastFrame<=self.changeFrame:
            alpha=round(256/self.changeFrame*self.lastFrame)
            self.img.set_alpha(alpha)
        elif self.lastFrame>self.maxFrame-self.changeFrame:
            alpha=round(256/self.changeFrame*(self.maxFrame-self.lastFrame))
            self.img.set_alpha(alpha)
    def update(self, screen):
        self.lastFrame+=1
        self.doFade()
        self.draw(screen)
        self.checkvalid()

    def draw(self,screen):
        screen.blit(self.img,(60,30))

    def checkvalid(self):
        if self.lastFrame>=self.maxFrame:
            self.kill()

class levelEndTimer(pygame.sprite.Sprite):
    def __init__(self):
        super(levelEndTimer,self).__init__()
        self.upper=False
        self.lower=False
        self.timer=240
        self.lastFrame=0
    
    def update(self, screen):
        self.lastFrame+=1
        if self.lastFrame>=self.timer:
            global_var.set_value('levelPassSign',True)
            self.kill()
