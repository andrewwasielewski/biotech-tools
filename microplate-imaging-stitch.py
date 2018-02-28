import cv2
import numpy
import glob
import os
import sys

print('running big image...')

while True:
    try:
        num_cols = int(input('How many images would you like to combine horizontally? '))
        break
    except ValueError:
        print('Not a valid integer! Please try again ...')

dir = "."
ext = ".nd2"
pathname = os.path.join(dir, "*" + ext)
images = [cv2.imread(img) for img in glob.glob(pathname)]
num_rows = int(len(images) / num_cols)

for img in glob.glob(pathname):
	print(img[2:-len(ext)])

print(len(images), 'images found.  Will create big image ,', num_cols,'x', num_rows)
continuation = input('Is this correct? [y]/n ')
if continuation == 'n' or continuation == 'N':
	print('exiting...')
	exit()

height = 0
for i in range(0, num_rows):
    height += images[i*num_cols].shape[0]
width = 0
for i in range(0, num_cols):
    width += images[i].shape[1]

output = numpy.zeros((height,width,3))

print('height: ', height)
print('width: ', width)
print('output: ', output.shape)

y = 0
for image in images:
    h,w,d = image.shape
    output[y:y+h,0:w] = image
    y += h

# cv2.imwrite("test.jpg", output)