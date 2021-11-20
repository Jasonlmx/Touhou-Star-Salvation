import pygame,sys
import random
import math
import gF
from pygame.sprite import Sprite
import global_var

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
        self.image.set_alpha(180)
        self.frame=0
        self.part=0
        self.interval=5
        self.speed=3
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
            gF.drawRotation(self.temp[self.part],(round(self.tx-12),round(self.ty-12)),self.frame*-25-90,screen)
            #screen.blit(self.image[self.part],(self.tx-12,self.ty-24))

class fire_effect_reimu_target(pygame.sprite.Sprite):
    def __init__(self):
        super(fire_effect_reimu_target,self).__init__()
        self.image=pygame.Surface((96,24)).convert_alpha()
        self.image.fill((0,0,0,0))
        self.image.blit(global_var.get_value('reimu_fire'),(0,0),(0,24,96,24))
        self.image.set_alpha(180)
        self.frame=0
        self.part=0
        self.interval=5
        self.speed=3
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
        self.image=pygame.image.load('resource/bullet/small_bullet_grey.png')
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
        w_now=round(w*(1+0.2*self.part))
        h_now=round(h*(1+0.2*self.part))
        cR=1+0.2*self.part
        tempImage=pygame.transform.scale(self.image,(w_now,h_now))
        tempImage.set_alpha(256-40*self.part)
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
        self.image=pygame.Surface((384,48))
        self.image.set_alpha(256)
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
            screen.blit(pygame.transform.scale(self.image,(384,height)),(168,100+(24-round(0.5*height))))
        elif self.lastFrame>=self.maxLastFrame-self.transFrame:
            height=round(48*(self.maxLastFrame-self.lastFrame)/self.transFrame)
            #screen.blit(pygame.transform.scale(self.image,(384,height)),(168,100))
            screen.blit(pygame.transform.scale(self.image,(384,height)),(168,100+(24-round(0.5*height))))
        else:
            #pass
            screen.blit(self.image,(168,100))
        bonus=self.font.render(str(self.bonus), True, (255, 255, 255))
        bonus_shade=self.font.render(str(self.bonus), True, (30, 30, 30))
        w=bonus.get_width()
        h=bonus.get_height()
        if self.lastFrame<=self.transFrame:
            height=round(h*self.lastFrame/self.transFrame)
            #print(height)
            #screen.blit(pygame.transform.scale(self.image,(384,height)),(168,100))
            screen.blit(pygame.transform.scale(bonus_shade,(w,height)),(360-round(w/2)+2,140+(round(h/2-0.5*height))+3))
            screen.blit(pygame.transform.smoothscale(bonus,(w,height)),(360-round(w/2),140+(round(h/2-0.5*height))))
        elif self.lastFrame>=self.maxLastFrame-self.transFrame:
            height=round(h*(self.maxLastFrame-self.lastFrame)/self.transFrame)
            #screen.blit(pygame.transform.scale(self.image,(384,height)),(168,100))
            screen.blit(pygame.transform.scale(bonus_shade,(w,height)),(360-round(w/2)+2,140+(round(h/2-0.5*height))+3))
            screen.blit(pygame.transform.smoothscale(bonus,(w,height)),(360-round(w/2),140+(round(h/2-0.5*height))))
        else:
            #pass
            screen.blit(bonus_shade,((360-round(w/2)+2),140+3))
            screen.blit(bonus,((360-round(w/2)),140))
        #screen.blit(bonus,((360-round(w/2)),140))
    
class failText(screenText):
    def __init__(self):
        super(failText,self).__init__()
        self.image=pygame.Surface((240,48))
        self.image.set_alpha(256)
        self.image.blit(global_var.get_value('front00'), (0, 0), (386,576,238,48))
        self.transFrame=30
        self.lower=False
    def draw(self,screen):
        if self.lastFrame<=self.transFrame:
            height=round(48*self.lastFrame/self.transFrame)
            #print(height)
            #screen.blit(pygame.transform.scale(self.image,(384,height)),(168,100))
            screen.blit(pygame.transform.smoothscale(self.image,(240,height)),(240,100+(24-round(0.5*height))))
        elif self.lastFrame>=self.maxLastFrame-self.transFrame:
            height=round(48*(self.maxLastFrame-self.lastFrame)/self.transFrame)
            #screen.blit(pygame.transform.scale(self.image,(384,height)),(168,100))
            screen.blit(pygame.transform.smoothscale(self.image,(240,height)),(240,100+(24-round(0.5*height))))
        else:
            #pass
            screen.blit(self.image,(240,100))
        #screen.blit(self.image,(240,100))

class powerMaxText(screenText):
    def __init__(self):
        super(powerMaxText,self).__init__()
        self.image=pygame.Surface((234,48))
        self.image.set_alpha(256)
        self.image.blit(global_var.get_value('front00'), (0, 0), (386,240,232,48))
    
    def draw(self,screen):
        screen.blit(self.image,(243,52))
    
class extendText(screenText):
    def __init__(self):
        super(extendText,self).__init__()
        self.image=pygame.Surface((234,48))
        self.image.set_alpha(256)
        self.image.blit(global_var.get_value('front00'), (0, 0), (386,333,148,48))
    
    def draw(self,screen):
        screen.blit(self.image,(285,160))

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
        self.alpha=200
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
        self.temp.set_alpha(self.alpha)
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
        self.image.set_alpha(200)
        self.lx=660
        self.ly=-20
        self.lastFrame=0
        self.upper=False
        self.lower=True
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
            self.ly+=15