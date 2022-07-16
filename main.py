import requests, json, urllib.request, os, subprocess, appscript
from sys import platform
from PIL import Image, ImageDraw, ImageFont


def getImage():
    r = requests.get('https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY').text
    data = json.loads(r)
    hdURL = data['hdurl']
    title = data['title']
    print(title)
    #Get image from url
    urllib.request.urlretrieve(hdURL, "image.png")
    path = (os.getcwd() + "/image.png")

    infoList =  []
    infoList.append(path)
    infoList.append(title)

    return infoList

def setImageAsBackground(filePath):
    filePath = filePath[0]

    if platform == "linux" or platform == "linux2":
        pass
    elif platform == "darwin":
        systemEvents = appscript.app("System Events")
        desktops = systemEvents.desktops.display_name.get()
        for d in desktops:
            desk = systemEvents.desktops[appscript.its.display_name == d]
            desk.picture.set(appscript.mactypes.File(filePath))
        subprocess.call(['killall', 'Dock'])
        
def manImage(filePath):
    title = filePath[1]
    filePath = filePath[0]
    print(title)
    DISPLAY_SIZE = (2560,1440)


    image = Image.open(filePath)
    image.thumbnail(DISPLAY_SIZE, Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(image)
    
    #Scale font to image size
    fontsize = 1
    imageFraction = 0.20
    dirr = os.getcwd()
    font = ImageFont.truetype(dirr +'/BlackPink-Cursive-Demo.ttf', fontsize)
    while font.getsize(title)[0] < imageFraction * image.size[0]:
        fontsize += 1
        font = ImageFont.truetype(dirr + "/BlackPink-Cursive-Demo.ttf", fontsize)


    draw.text((50, 230), title, font=font, fill=(255,255,255))

    image.save(filePath, "PNG")






def main():
    path =  getImage()
    manImage(path)
    setImageAsBackground(path)

main()