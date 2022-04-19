import sys
import pygame

def HSB2RGB(hues):
    rgb=[0.0,0.0,0.0]
    hues=hues%360
    i = int(hues/60)%6
    f = hues/60 -i
    if i == 0:
        rgb[0] = 1; rgb[1] = f; rgb[2] = 0
    elif i == 1:
        rgb[0] = 1-f; rgb[1] = 1; rgb[2] = 0
    elif i == 2:
        rgb[0] = 0; rgb[1] = 1; rgb[2] = f
    elif i == 3:
        rgb[0] = 0; rgb[1] = 1-f; rgb[2] = 1
    elif i == 4:
        rgb[0] = f; rgb[1] = 0; rgb[2] = 1
    elif i == 5:
        rgb[0] = 1; rgb[1] = 0; rgb[2] = 1-f
    rgb[0]=round(rgb[0]*255)
    rgb[1]=round(rgb[1]*255)
    rgb[2]=round(rgb[2]*255)
    return rgb

def doPic(pic):
    picList=[]
    for k in range(60):
        color=HSB2RGB(k*6)
        tSurf=pygame.Surface((256,256)).convert_alpha()
        fadeRate=0.8
        try:
            tSurf.fill(color)
        except:
            print(color)
        tArray=pygame.PixelArray(tSurf)
        pArray=pygame.PixelArray(pic)
        #print(pArray)
    
        for i in range(256):
            for j in range(256):
                temp=pic.unmap_rgb(pArray[i][j])
                #print(temp)
                tArray[i][j]=(int(color[0]*fadeRate),int(color[1]*fadeRate),int(color[2]*fadeRate),int(temp[3]*0.2))
                #print(temp)
                #tSurf.set_at((i,j),pygame.Color(int(color[0]*fadeRate),int(color[1]*fadeRate),int(color[2]*fadeRate),int(temp[3]*0.5)))
        del tArray
        del pArray
        tSurf=pygame.transform.smoothscale(tSurf,(384,384))
        picList.append(tSurf)
    return picList
    