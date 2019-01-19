#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image,ImageOps
import argparse
import numpy as np
import cv2
import os,sys
from multiprocessing.pool import ThreadPool

def write_img(gray,path,i):
    global width,hsize
    gray = np.array(gray.resize((width,hsize)))
    path = path.replace("ppm","jpg")
    print("writing :{}........{}".format(path,i))
    if gray.shape[0] <= 0 or gray.shape[1] <= 0:
        return
    cv2.imwrite(path,gray)
    #cv2.imshow("resized",gray)
    cv2.waitKey(1)

parse = argparse.ArgumentParser()
parse.add_argument("-path","--path",type=str,default=None,help="Directory path for Dataset")
parse.add_argument("-o","--output",type=str,default=None,help="Directory path to output")
parse.add_argument("-t","--thread",type=bool,default=False,help="True for using Thread Processing")
parse.add_argument("-f_w","--width",type=int,default=100,help="size for resizing width")
parse.add_argument("-f_h","--height",type=int,default=100,help="size for resizing height")

if len(sys.argv) < 3:
    parse.print_help()

args = vars(parse.parse_args())
try:
    if os.path.isdir(args['path']):
        print("{} is exits (ok)".format(args['path']))
        if len(os.listdir(args['path'])) == 0:
            print("No Directory or folder in {}".format(args['path']))
            sys.exit()

    else:
        print("{} is not valid directory".format(args['path']))
        print("Please select a valid directory")
        sys.exit()

    if os.path.isdir(args['output']):
        print("{} is exits (ok)".format(args['output']))
    else:
        print("{} doesn't exits".format(args['output']))
        print('creating {}'.format(args['output']))
        os.mkdir(args['output'])
except Exception:
    sys.exit()

top_path = args['path']
width = args['width']
hsize = args['height']
threadn = cv2.getNumberOfCPUs()
pool = ThreadPool(processes=threadn)
all_images_paths = []

for (dirpath , dirnames, filenames) in os.walk(top_path):
    for filename in filenames:
        if filename.endswith('.ppm') or filename.endswith('.jpg') or filename.endswith('JPG') or filename.endswith('.pgm'):
            path = os.path.join(dirpath,filename)
            all_images_paths.append(path)

for i ,k in enumerate(all_images_paths):
    img = Image.open(k)
    gray = ImageOps.grayscale(img)
    #cv2.imshow("gray",np.array(gray))
    cv2.waitKey(1)
    
    if not os.path.exists(os.path.join(args['output'],*k.split("\\")[1:-1])):
        folder = os.path.join(args['output'],*k.split("\\")[1:-1])
        print("creating folder {}".format(folder))
        path = os.path.join(args['output'],*k.split("\\")[1:])
        os.makedirs(folder)
        # print("writing :{}".format(path))
        if args['thread']:
            pool.apply_async(write_img,(gray,path,i))
        else:
            write_img(gray,path,i)
    else:
        path = os.path.join(args['output'],*k.split("\\")[1:])
        if args['thread']:
            pool.apply_async(write_img,(gray,path,i))
        else:
            write_img(gray,path,i)