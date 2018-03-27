import cv2
import numpy as np
import glob
import os
import sys
import tkinter as tk
from tkinter import filedialog
import nd2reader


#this is a quick demo
def getRow(imgName):
    return ord(imgName[:-1])-ord('A')

def getCol(imgName):
    return int(imgName[1:])

def getImageName(col, row):
    return chr(row + ord('A'))+str(col)

print('stitching individual microplate images...')

root = tk.Tk()
root.withdraw()
options = {}
options['title'] = 'Select directory containing microplate images'
file_path = filedialog.askdirectory(**options)

ext = ".jpg"
pathname = os.path.join(file_path, "*" + ext)

#we assume all images are the same size, gets first wildcard match
tmpImg = cv2.imread(glob.glob(pathname)[0])
imgWidth = tmpImg.shape[0]
imgHeight = tmpImg.shape[1]

image_names = list()
for img in glob.glob(pathname):
	image_names.append(img[(len(file_path)+1):-len(ext)])
min_x, max_x = getCol(image_names[0]), getCol(image_names[0])
min_y, max_y = getRow(image_names[0]), getRow(image_names[0])

for curImg in image_names:
    if getRow(curImg) < min_y:
        min_y = getRow(curImg)
    if getRow(curImg) > max_y:
        max_y = getRow(curImg)
    if getCol(curImg) < min_x:
        min_x = getCol(curImg)
    if getCol(curImg) > max_x:
        max_x = getCol(curImg)

height = imgHeight * (max_y + 1 - min_y)
width = imgWidth * (max_x + 1- min_x)
output = np.zeros((width, height, 3))

print('single image height: ', imgHeight)
print('single image width: ', imgWidth)
print('output file shape: ', output.shape)

for y in range(min_y, max_y+1):
    for x in range(min_x, max_x+1):
        imgPath = os.path.join(file_path, getImageName(x, y) + ext)
        if os.path.isfile(imgPath):
            writeImg = cv2.imread(imgPath)
            y_pos = (y - min_y) * imgHeight
            x_pos = (x - min_x) * imgWidth
            # print('y: ',y,'    ', y_pos, '-', y_pos+imgHeight)
            # print('x: ',x,'    ', x_pos, '-', x_pos+imgWidth)
            output[x_pos:x_pos+imgWidth, y_pos:y_pos+imgHeight] = writeImg

outFilePath = os.path.join(file_path,'../stitched_microplate.jpg')
cv2.imwrite(outFilePath, output)
print('created new file: ', outFilePath)

