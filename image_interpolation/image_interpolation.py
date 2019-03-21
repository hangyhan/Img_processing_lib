from PIL import Image
import numpy as np
import math
import os

building = "building.jpg"
cameraman = "cameraman.jpg"
lenna = "lenna.jpg"


def S(x=0.0):
    x = np.abs(x)
    if x < 1:
        return (1-2*x**2+x**3)
    if x <= 2:
        return (4-8*x+5*x**2-x**3)
    else:
        return 0


def get_img(ratio=3.0, img_name="building.jpg"):
    img_path = './' + img_name
    org_img = Image.open(img_path)
    org_img = np.array(org_img)
    org_width, org_height = org_img.shape
    new_width, new_height = math.floor(
        ratio*org_width), math.floor(ratio * org_height)
    new_img = np.zeros((new_width, new_height))
    return org_img, org_width, org_height, new_img, new_width, new_height


def nearest(ratio=3.0,img_name="building.jpg"):
    org_img, org_width, org_height, new_img, new_width, new_height = get_img(
        ratio, img_name)
    for i in range(new_width):
        for j in range(new_height):
            nearest_x = min(round(i / new_width * org_width),org_width-1)
            nearest_y = min(round(j / new_height * org_height),org_height-1)
            new_img[i][j] = org_img[nearest_x][nearest_y]
    new_img = Image.fromarray(new_img)
    new_img = new_img.convert('RGB')
    new_img.save("./"+str(ratio)+'_nearest_'+img_name)


def bilinear(ratio=3.0, img_name="building.jpg"):
    org_img, org_width, org_height, new_img, new_width, new_height = get_img(
        ratio, img_name)
    for i in range(new_width):
        for j in range(new_height):
            x = i / new_width * org_width
            y = j / new_height * org_height
            low_x = min(math.floor(x),org_width-2)
            u = x-low_x
            low_y = min(math.floor(y), org_height-2)
            v = y-low_y
            a = (1-u)*org_img[low_x][low_y] + \
                (u)*org_img[low_x+1][low_y]
            b = (1-u)*org_img[low_x][low_y+1] + \
                (u)*org_img[low_x+1][low_y+1]
            new_img[i][j] = (1-v)*a+(v)*b
            # new_img[i][j] = np.matmul([[high_x-x, x-low_x]], np.matmul(
            #    [[org_img[low_x, low_y], org_img[low_x, high_y]], [org_img[high_x, low_y], org_img[high_x, high_y]]], [[high_y-y], [y-low_y]]))
    new_img = Image.fromarray(new_img)
    new_img = new_img.convert('RGB')
    new_img.save("./"+str(ratio)+'_bilinear_'+img_name)


def bicubic(ratio=3.0, img_name="building.jpg"):
    org_img, org_width, org_height, new_img, new_width, new_height = get_img(
        ratio, img_name)
    for i in range(new_width):
        for j in range(new_height):
            x = i / new_width * org_width
            y = j / new_height * org_height
            low_x = min(math.floor(x),org_width-3)
            high_x = low_x+1
            low_y = min(math.floor(y),org_height-3)
            high_y = low_y+1
            u = x-low_x
            v = y-low_y
            A = np.mat([[S(1+v), S(v), S(1-v), S(2-v)]])
            B = np.mat(
                [[org_img[low_x-1][low_y-1], org_img[low_x][low_y-1], org_img[high_x][low_y-1], org_img[high_x+1][low_y-1]],
                [org_img[low_x-1][low_y], org_img[low_x][low_y], org_img[high_x][low_y], org_img[high_x+1][low_y]],
                [org_img[low_x-1][high_y], org_img[low_x][high_y], org_img[high_x][high_y], org_img[high_x+1][high_y]],
                [org_img[low_x-1][high_y+1], org_img[low_x][high_y+1], org_img[high_x][high_y+1], org_img[high_x+1][high_y+1]]])
            B = np.transpose(B)
            C = np.mat([[S(1+u)],[S(u)],[S(1-u)],[S(2-u)]])
            value = np.matmul(A,np.matmul(B,C)) 
            if value > 255:
                value=255
            elif value < 0:
                value = 0
            new_img[i][j]=value
            print(value)
    new_img = Image.fromarray(new_img)
    new_img = new_img.convert('RGB')
    new_img.save("./"+str(ratio)+'_bicubic_'+img_name)


nearest(ratio=3.0, img_name=building)
bilinear(ratio=3.0, img_name=building)
bicubic(ratio=3.0, img_name=building)
