# -*- coding: utf-8 -*-
import os
from os import walk, getcwd
from PIL import Image

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

"""map class with their 1st four syllable"""
classes=['warping','stringing','contamination','layer separation']
clss=[]
for t in classes:
    clss.append(t[0:4])
print(clss)


""" Configure Paths"""   
mypath = "./dataset/"
outpath = "./result/"
json_backup ="./json_backup/"

wd = getcwd()
#list_file = open('%s_list.txt'%(wd), 'w')

""" Get input json file list """
json_name_list = []
for file in os.listdir(mypath):
    if file.endswith(".json"):
        json_name_list.append(file)
    

""" Process """
for json_name in json_name_list:
    txt_name = json_name.rstrip(".json") + ".txt"
    """ Open input text files """
    txt_path = mypath + json_name
    print("Input:" + txt_path)
    txt_file = open(txt_path, "r")
    
    """ Open output text files """
    txt_outpath = outpath + txt_name
    print("Output:" + txt_outpath)
    txt_outfile = open(txt_outpath, "a")

    """ Convert the data to YOLO format """ 
    lines = txt_file.read().split('\n')   # "\n" for windows, "\r\n" for ubuntu
    for idx, line in enumerate(lines):
        if ("lineColor" in line):
            break 	#skip reading after find lineColor
        if ("label" in line):
            x1 = float(lines[idx+3].rstrip(','))
            y1 = float(lines[idx+4])
            x2 = float(lines[idx+7].rstrip(','))
            y2 = float(lines[idx+8])
            cl = line[16:20]
            cls=clss.index(cl)
            #in case when labelling, points are not in the right order
            xmin = min(x1,x2)
            xmax = max(x1,x2)
            ymin = min(y1,y2)
            ymax = max(y1,y2)
            img_path = str('%s/dataset/%s.jpg'%(wd, os.path.splitext(json_name)[0]))

            im=Image.open(img_path)
            w= int(im.size[0])
            h= int(im.size[1])

            print(w, h)
            print(xmin, xmax, ymin, ymax)
            b = (xmin, xmax, ymin, ymax)
            bb = convert((w,h), b)
            print(bb)
            txt_outfile.write(str(cls) + " " + " ".join([str(a) for a in bb]) + '\n')
            txt_file.close()#close opened file
            
    os.rename(txt_path,json_backup+json_name)	