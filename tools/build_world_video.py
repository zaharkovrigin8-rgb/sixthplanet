#!/usr/bin/env python3
"""Build the Russian SixthPlanet WORLD 2.2 narrated trailer with captions."""
import os, math, subprocess, wave, tempfile
from PIL import Image, ImageDraw, ImageFont

OUT=os.getcwd()
W,H=1280,720
REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def font(n,b=False): return ImageFont.truetype(BOLD if b else REG,n)
slides=[
("SIXTHPLANET","WORLD · ЖИВОЙ МИР","Новая дипломатия и торговля\nмежду соседними поселениями",
 "В SixthPlanet появился новый раздел «Живой мир». Он добавляет дипломатические отношения, торговые пути и летопись событий между соседними поселениями."),
("ДИПЛОМАТИЯ","ОТНОШЕНИЯ С СОСЕДЯМИ","Нейтралитет · Дружба · Союз\nВражда · Война",
 "У каждого поселения есть собственный показатель отношений. Он меняется от дипломатических действий и событий, а статус зависит от уровня доверия."),
("ПОСОЛЬСТВА И ПАКТЫ","ДИПЛОМАТИЧЕСКИЕ РЕШЕНИЯ","Посольство улучшает отношения\nПакт требует доверия\nРазрыв договора обостряет конфликт",
 "Можно направлять посольства, заключать пакты о ненападении при достаточном доверии или разрывать договоры. Решения отражаются в отношениях и летописи."),
("ТОРГОВЫЕ ПУТИ","КАРАВАНЫ И РАЗВИТИЕ","Открывай маршрут\nУкрепляй его до 3 уровня\nСледи за отношениями",
 "Торговый путь учитывает регулярные караванные рейсы. Его можно укреплять до третьего уровня. Если отношения становятся отрицательными, маршрут закрывается."),
("ЛЕТОПИСЬ ПЛАНЕТЫ","ИСТОРИЯ ТВОИХ РЕШЕНИЙ","Дипломатические события\nКараванные рейсы\nИзменения отношений",
 "Вкладка летописи записывает важные новости: дипломатические решения, торговые события и перемены настроения соседей. История хранится в сохранении браузера."),
("WORLD · BETA 2.2","МИР СТАНОВИТСЯ ЖИВЫМ","Посольства. Договоры. Торговля.\nИ последствия каждого решения.",
 "Открой кнопку «Живой мир» в игре и проверь новые вкладки: поселения, торговля и летопись. Это первый этап большого обновления WORLD.")
]
def wrap(draw,txt,f,maxw):
    lines=[]
    for para in txt.split("\n"):
        line=""
        for word in para.split():
            candidate=(line+" "+word).strip()
            if draw.textbbox((0,0),candidate,font=f)[2] <= maxw: line=candidate
            else:
                if line: lines.append(line)
                line=word
        if line: lines.append(line)
    return lines
def draw_slide(i,item,path):
    eyebrow,title,subtitle,_=item
    im=Image.new("RGB",(W,H),(13,15,13)); p=im.load()
    for y in range(H):
        for x in range(W):
            glow=max(0,1-math.sqrt(((x-930)/900)**2+((y-280)/700)**2))
            p[x,y]=(int(13+glow*18),int(15+glow*16),int(13+glow*10))
    d=ImageDraw.Draw(im,"RGBA")
    for j in range(95):
        x=(j*197+i*73)%W; y=(j*113+i*41)%H
        d.ellipse((x,y,x+2,y+2),fill=(224,204,155,70))
    d.rounded_rectangle((55,48,1225,672),radius=30,outline=(167,137,83,150),width=2,fill=(10,12,10,95))
    d.text((94,88),eyebrow,font=font(21,True),fill=(161,197,133,255))
    d.text((94,142),title,font=font(48,True),fill=(240,220,178,255))
    yy=230
    for line in wrap(d,subtitle,font(31,True),690):
        d.text((96,yy),line,font=font(31,True),fill=(227,218,196,255)); yy+=48
    cx,cy=970,385
    d.ellipse((790,205,1160,575),fill=(36,55,48,110),outline=(173,145,91,160),width=3)
    d.ellipse((830,245,1120,535),outline=(126,160,115,100),width=2)
    nodes=[(970,278),(1085,360),(1035,490),(880,455),(855,330)]
    for nx,ny in nodes:
        d.line((cx,cy,nx,ny),fill=(191,157,95,170),width=4)
        d.ellipse((nx-28,ny-28,nx+28,ny+28),fill=(80,91,65,255),outline=(225,197,139,255),width=3)
        d.polygon([(nx-15,ny+2),(nx,ny-13),(nx+15,ny+2)],fill=(229,207,159,255))
        d.rectangle((nx-11,ny+2,nx+11,ny+15),fill=(229,207,159,255))
    d.ellipse((cx-42,cy-42,cx+42,cy+42),fill=(143,111,62,255),outline=(240,217,165,255),width=4)
    d.ellipse((cx-16,cy-16,cx+16,cy+16),fill=(244,224,174,255))
    d.rounded_rectangle((95,590,1185,630),radius=16,fill=(255,255,255,18))
    d.rounded_rectangle((95,590,95+1090*(i+1)/len(slides),630),radius=16,fill=(173,139,79,220))
    d.text((96,642),"SIXTHPLANET  /  WORLD SYSTEMS",font=font(13,True),fill=(168,161,143,220))
    im.save(path)
def stamp(sec,dot=False):
    ms=round(sec*1000); h=ms//3600000; ms%=3600000; m=ms//60000; ms%=60000; s=ms//1000; ms%=1000
    return f"{h:02}:{m:02}:{s:02}{'.' if dot else ','}{ms:03}"
def main():
    with tempfile.TemporaryDirectory() as td:
        wavs=[]; durations=[]; captions=[]; cursor=0.0
        for i,item in enumerate(slides):
            img=os.path.join(td,f"scene{i}.png"); draw_slide(i,item,img)
            wav=os.path.join(td,f"voice{i}.wav")
            subprocess.run(["espeak","-v","ru","-s","148","-p","42","-a","175","-w",wav,item[3]],check=True)
            with wave.open(wav,"rb") as f: duration=f.getnframes()/f.getframerate()
            wavs.append(wav); durations.append(duration+0.65)
            captions.append((cursor,cursor+duration,item[3])); cursor+=duration+0.65
        silence=os.path.join(td,"silence.wav")
        subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=22050:cl=mono","-t","0.65",silence],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
        audio_list=os.path.join(td,"audio.txt")
        with open(audio_list,"w") as f:
            for i,w in enumerate(wavs):
                f.write(f"file '{w}'\n")
                if i<len(wavs)-1: f.write(f"file '{silence}'\n")
        audio=os.path.join(td,"voice.wav")
        subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",audio_list,"-c","copy",audio],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
        scenes=os.path.join(td,"scenes.txt")
        with open(scenes,"w") as f:
            for i,dur in enumerate(durations):
                f.write(f"file '{os.path.join(td,f'scene{i}.png')}'\nduration {dur:.3f}\n")
            f.write(f"file '{os.path.join(td,f'scene{len(slides)-1}.png')}'\n")
        srt=[]; vtt=["WEBVTT",""]
        for i,(a,b,txt) in enumerate(captions,1):
            srt.extend([str(i),f"{stamp(a)} --> {stamp(b)}",txt,""])
            vtt.extend([str(i),f"{stamp(a,True)} --> {stamp(b,True)}",txt,""])
        open(os.path.join(OUT,"world-massive.ru.srt"),"w",encoding="utf-8").write("\n".join(srt))
        open(os.path.join(OUT,"world-massive.ru.vtt"),"w",encoding="utf-8").write("\n".join(vtt))
        vf="subtitles=world-massive.ru.srt:force_style='FontName=DejaVu Sans,FontSize=17,PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,BackColour=&H90000000,BorderStyle=3,Outline=1,Shadow=0,MarginV=18'"
        subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",scenes,"-i",audio,"-vf",vf,"-c:v","libx264","-preset","medium","-crf","27","-pix_fmt","yuv420p","-r","25","-c:a","aac","-b:a","96k","-shortest","-movflags","+faststart","world-massive-trailer.mp4"],check=True)
if __name__=="__main__": main()
