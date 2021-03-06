import numpy as np
import cv2
import math
from Tkinter import *
from tkMessageBox import *
from tkFileDialog import *
from PIL import Image, ImageTk
from PIL.GifImagePlugin import _imaging_gif, RAWMODE, _convert_mode, getheader, getdata, get_interlace, _get_local_header
 
#GLOBAL VARIABLES
window = Tk()
filename = ['']
vidHeight = None
vidWidth = None
frame = None

def loadVideoHelper():
    global filename
    filename = askopenfilenames(filetypes=(("Video files", "*.mp4"),("All files","*.*")))
    print filename
    return filename

def loadVideo():
    """filename = loadVideoHelper()
    cap = cv2.VideoCapture(filename[0])
    i=0
    frames = cap.get(7)
    vidHeight = cap.get(4)
    vidWidth = cap.get(3)
    firstFrame = True
    palettes, occur = [], []

    while(i < 20):
        ret, frame = cap.read()
        testimg = frame
        if firstFrame:
            firstFrame = False

            im = Image.fromarray(np.roll(testimg[...,[1,0,2]], 1, axis=-1))
            im2= im.convert("P")
            text22 =im2.im.getpalette("RGB")[:768]
            palettes.append(text22)
            for palette in palettes:
                occur.append( palettes.count( palette ) )
            i = i + 4
            header1 = gifHeader()
            colorTable = palettes[occur.index(max(occur))]
            graphics = gifGraphicsControl()
            descrip = gifImageDescrip()
            header2 = gifAnimation()
            data = getdata(im2)
            fp = open("fp.gif",'wb')
            fp.write(header1)
            fp.write(colorTable)
            fp.write(graphics)
            fp.write(descrip)
            fp.write(header2)
            for s in data:
                fp.write(s)

        i = i + 4"""
    filename = loadVideoHelper()
    cap = cv2.VideoCapture(filename[0])
    i=0
    frames = cap.get(7)
    vidHeight = cap.get(4)
    vidWidth = cap.get(3)
    firstFrame = True

    while(i < frames):
        ret, frame = cap.read()
        testimg = frame
        if firstFrame:
            firstFrame = False

            im = Image.fromarray(np.roll(testimg[...,[1,0,2]], 1, axis=-1))
            im2= im.convert("P")
            first_frame = getheader(im2)[0]
            first_frame += getdata(im2, duration=0.1)
            i = i + 4
        im = Image.fromarray(np.roll(testimg[...,[1,0,2]], 1, axis=-1))
        im3 = im.convert("P")
        if i == 4:
            frametxt = getdata(im3, duration=0.1)

        frametxt += getdata(im3, duration=0.1)
        i = i + 4
    fp = open("fp.gif",'wb')
    for s in first_frame:
        fp.write(s)

    for x in frametxt:
        fp.write(x)
    #fp.write(b"\0")
    #fp.write(b";")
    fp.close() 

def toHex(x):
    x1 = x % 256
    x2 = int (x / 256)
    return chr(x1) + chr(x2)

def gifHeader():
    header = "GIF89a" #Gif Header
    header += toHex(480) #Video Width
    header += toHex(270) #Video Height
    header += "\x97" #packed field for global color table and define 8bit table
    header += "\x00\x00" #Background Color Index and Pixel Aspect Ratio
    return header

def gifGraphicsControl():
    header = "\x21\xF9" #Always 21 and F9
    header += "\x04" #Byte size
    header += "\x08" #No Transparency
    header += toHex(1) #Frame duration
    header += "\x00\x00" #Always 00
    return header

def gifImageDescrip():
    header = "\x2C" #Always 2C
    header += "\x00\x00" #Image Left position
    header += "\x00\x00" #Top position
    header += toHex(480)
    header += toHex(270)
    header += "\x00" #Local Color table flag
    return header

def gifAnimation():
    header = "\x21\xFF\x08" #Application Extension
    header += "NETSCAPE2.0"
    header += "\x03"
    header += '\x01' #Always 01
    header += toHex(65535) #Infinite Loops
    header += "\x00" #Always 00
    return header


def lzwCompress(input):
    table = dict((chr(i), chr(i)) for i in xrange(256))
    output = []
    s = ""
    size = 256

    for c in input:
        if (s + c) in table:
            s = s + c

        else:
            output.append(table[s])
            table[s+c] = size
            size = size + 1
            s = c
    if s:
        output.append(table[s])
    return output

def lzwDecompress(input):
    table = dict((chr(i), chr(i)) for i in xrange(256))
    size = 256

    output = s = input.pop(0)


    for k in input:
        if k in table:
            entry = table[k]
        elif k == size:
            entry = s + s[0]
        output += entry

        table[size] = s + entry[0]
        size = size + 1

        w = entry
    return output

def main():
    window.title("GIF Maker")
    openButton= Button(text="Open Video", width = 50, command = lambda: loadVideo())
    openButton.pack()
    window.mainloop()

main()
