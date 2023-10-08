import cv2
import numpy as np
import simpleaudio as sa
import csv
import matplotlib.pyplot as plt

import os

GR = 1.61803399

imgs_folder = 'imgs'
out_folder = 'out'
color_folder = 'color'
current_filename = ''

def fibo_segment(img, x0, y0, x1, y1, inv, inv2, cuad):
    segCount=0
    segment = img

    height = y1 - y0
    width = x1 - x0

    dirs = [0, 1, 2, 3]
    dir = 0 if height > width else 1

    if(inv):
        dir = dir + 2

    if(inv2):
        offset = -1
    else:
        offset = 1
    
    metric = [[] for _ in range(8)]
    hexcolors = []

    while(height > 1 and width > 1):
        
        height = y1 - y0
        width = x1 - x0
        
        n, m = height, width
        
        print(f'Height: {height} Width: {width}')
        print(f'x0: {x0} y0: {y0} x1: {x1} y1: {y1}')
        print(f'dir: {dir}')
        #plt.imshow(segment, cmap='gray')
        #plt.show()
        
        if(height > width):
            height = int(height/GR)

            if(dirs[dir] == 0):
                color = 0
                res=segment[y0:y0+height, x0:x0+width]
                y0 = y0 + height

            else:
                color = 100
                res=segment[y1-height:y1, x1-width:x1] 
                y1 = y1 - height

            # height = x1 - x0
                
        else:
            width = int(width/GR)

            if(dirs[dir] == 1):
                color = 180
                res=segment[y0:y0+height, x0:x0+width] 
                x0 = x0 + width

            else:
                color = 255
                res=segment[y1-height:y1, x1-width:x1]
                x1 = x1 - width

            # width = y1 - y0
        
        hsv=cv2.cvtColor(res,cv2.COLOR_BGR2HSV)
        bw=cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
        h,s,v=hsv[:,:,0],hsv[:,:,1],hsv[:,:,2]

        dynamic_range=np.max(res)-np.min(res)
        hue_range=np.max(h)-np.min(h)
        sat_range=np.max(s)-np.min(s)
        val_range=np.max(v)-np.min(v)
        hue_average = np.average(h)
        sat_average = np.average(s)
        val_average = np.average(v)
        ilum_average = np.average(bw)
        mean_color = cv2.mean(res)

        metric[0].append(dynamic_range)
        metric[1].append(hue_range)
        metric[2].append(sat_range)
        metric[3].append(val_range)
        metric[4].append(hue_average)
        metric[5].append(sat_average)
        metric[6].append(val_average)
        metric[7].append(ilum_average)
        hexcolors.append(f'{cuad} #{int(mean_color[2]):02x}{int(mean_color[1]):02x}{int(mean_color[0]):02x}')

        # datos=[[cuad, segCount, np.max(res)-np.min(res),np.max(h)-np.min(h),np.max(s)-np.min(s),np.max(v)-np.min(v), np.average(h),np.average(s),np.average(v), np.average(bw)]]

        # cv2.imshow("segmento",res)
        # cv2.waitKey()

        dir += offset
        dir = 0 if dir > 3 else dir
        dir = 3 if dir < 0 else dir
        segCount+=1

    nparrays = []

    nparrays.append(np.full(100, cuad))
    nparrays.append(np.arange(100))

    #create 

    for li in metric:
        print(li)
        original_array = np.array(li)
        indices_original = np.arange(len(original_array))
        indices_new = np.linspace(0, len(original_array)-1, 100)
        interpolated_values = np.interp(indices_new, indices_original, original_array)
        # print(interpolated_values)
        nparrays.append(interpolated_values)

    for i in range(100):
        datos = [[nparrays[j][i] for j in range(10)]] 

        with open (f'{out_folder}/{current_filename}.csv', 'a', newline='') as file:
            # print(current_filename)
            writer = csv.writer(file)
            writer.writerows(datos) 
    
    for h in hexcolors:
        with open (f'{color_folder}/{current_filename}_color.txt', 'a', newline='') as file:
            # print(current_filename)
            file.write(f'{h}\n')
            

def process(img):
    n, m, _ = img.shape

    x0 = 0
    y0 = 0
    x1 = int(m/2)
    y1 = int(n/2)

    if(n > m):
        fibo_segment(img, x0, y0, x1, y1, False, False, 0)
    else:
        fibo_segment(img, x0, y0, x1, y1, False, True,0)

    x0 = 0
    y0 = int(n/2)
    x1 = int(m/2)
    y1 = n

    if(n > m):
        fibo_segment(img, x0, y0, x1, y1, True, True,1)
    else:
        fibo_segment(img, x0, y0, x1, y1, False, False,1)

    x0 = int(m/2)
    y0 = 0
    x1 = m
    y1 = int(n/2)

    if(n > m):
        fibo_segment(img, x0, y0, x1, y1, False, True,2)
    else:
        fibo_segment(img, x0, y0, x1, y1, True, False,2)

    x0 = int(m/2)
    y0 = int(n/2)
    x1 = m
    y1 = n

    if(n > m):
        fibo_segment(img, x0, y0, x1, y1, True, False,3)
    else:
        fibo_segment(img, x0, y0, x1, y1, True, True,3)


def pipeline(filename):
    img = cv2.imread(filename)
    process(img)


def main():
    global current_filename  # Declare current_filename as global
    for filename in os.listdir(imgs_folder):
        current_filename = filename
        pipeline(f'{imgs_folder}/{filename}')


if __name__ == "__main__":
    main()