import cv2
import numpy
import glob
import os
import sys
import tkinter as tk
from tkinter import filedialog
import nd2reader

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

ext = ".nd2"
pathname = os.path.join(file_path, "*" + ext)
images = [nd2reader.Nd2(img) for img in glob.glob(pathname)]

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

print(min_y,' ', max_y)
print(min_x,' ', max_x)

height = images[0].height * (max_y - min_y)
width = images[0].width * (max_x - min_x)

output = numpy.zeros((height,width,3))

print('height: ', height)
print('width: ', width)
print('output: ', output.shape)


print(images[0].frames)
for y in range(min_y, max_y+1):
    for x in range(min_x, max_x+1):
        if os.path.isfile(os.path.join(file_path, getImageName(x, y) + ext)):
            print("T")

# for image in images:
#     h,w,d = image.shape
#     output[y:y+h,0:w] = image
#     y += h

# # cv2.imwrite("test.jpg", output)