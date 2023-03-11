import random as rd
import os
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from fontTools.ttLib import TTFont

#参数表
background_size=(200,100)
length=4
times=10
types=list(filter(lambda x:(("ttf" in x) or ("TTF" in x)),(os.listdir("C:\\windows\\fonts"))))

base_len=background_size[0]//(length+0.5)
base_height=(background_size[1]-base_len)//2

class mod_char:
    def __init__(self,_name='a',type="arial.ttf"):
        self.name=_name
        self.angle=[rd.uniform(0,15),rd.choice([0,1])]
        self.color=(rd.randint(0,200),rd.randint(0,200),rd.randint(0,200))
        self.xmove=rd.randint(-base_len//4,base_len//4)
        self.ymove=rd.randint(-(background_size[1]-base_len)//4,(background_size[1]-base_len)//4)
        try:
            if _name not in TTFont('C:\\windows\\fonts\\'+type).getGlyphOrder()[2:]:
                type="arial.ttf"
        except:
            type="arial.ttf"
        self.font=ImageFont.truetype(type, rd.randint(int(1*min(base_len,background_size[1])),int(1.5*min(base_len,background_size[1]))))
         

def rand_str(dic):
    res=""
    iter=0
    while iter<length:
        iter+=1
        choice=rd.choice(dic)
        if choice==0:
            res+=chr(rd.randint(48,57))
        elif choice==1:
            res+=chr(rd.randint(65,90))
        else:
            res+=chr(rd.randint(97,122))
    return res
    
def str_to_mod_char(str):
    return [mod_char(item,rd.choice(types)) for item in str]

def draw_one(target_char,temp,place):
    changed_place=(place[0]+target_char.xmove,place[1]+target_char.ymove)
    temp.text(xy=changed_place,text=target_char.name,fill=(target_char.color),font=target_char.font)
    
def draw_all(target_str,draft):
    temp=ImageDraw.Draw(draft)
    for item in enumerate(target_str):
        draw_one(item[1],temp,(int((item[0]+0.5)*base_len),base_height))

def draw_lines(draft,times=rd.randint(2,5)):
    temp=ImageDraw.Draw(draft)
    iter=0
    while iter<times:
        iter+=1
        color=(rd.randint(0,255),rd.randint(0,255),rd.randint(0,255))
        place=[(rd.randint(0,background_size[0]//2),rd.randint(0,background_size[1])),(rd.randint(background_size[0]//2,background_size[0]),rd.randint(0,background_size[1]))]
        temp.line(place,fill=color,width=1)

def final_process(draft):
    times=rd.randint(5,10)
    method=[ImageFilter.GaussianBlur(radius=rd.uniform(0,1)),ImageFilter.CONTOUR,ImageFilter.MinFilter(size=3),ImageFilter.EMBOSS]
    def process(draft):
        x1,y1=rd.randint(0,background_size[0]-5),rd.randint(0,background_size[1]-5)
        x2,y2=rd.randint(x1+1,background_size[0]),rd.randint(y1+1,background_size[1])
        place=(x1,y1,x2,y2)
        choice=rd.choice(method)
        process_place=draft.crop(box=place)
        process_place=process_place.filter(choice)
        if choice is ImageFilter.EMBOSS:
            data=process_place.load()
            for x in range(process_place.width):
                for y in range(process_place.height):
                    if process_place.getpixel((x,y))==(128,128,128):
                        data[x,y]=(255,255,255)
        draft.paste(process_place,place)
    iter=0
    while iter<times:
        iter+=1
        process(draft)

def main(times):
    iter=0
    while iter<times:
        iter+=1
        background=Image.new(mode='RGB',size=background_size,color="white")
        name=rand_str((0,1,2))
        draw_lines(background)#画线条
        draw_all(str_to_mod_char(name),background)
        final_process(background)#模糊处理等等
        background.save("./codes/{}.png".format(name))

main(times)

    
    
