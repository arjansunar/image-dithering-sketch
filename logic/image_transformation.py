from math import ceil, floor
import cv2
import numpy as np
import random as rnd

def image_to_sketch(img_path):
    image = cv2.imread(img_path)  # loads an image from the specified file

    # convert an image from one color space to another
    grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    invert = cv2.bitwise_not(grey_img)  # helps in masking of the image

    # sharp edges in images are smoothed while minimizing too much blurring
    blur = cv2.GaussianBlur(invert, (25, 25), 0)

    invertedblur = cv2.bitwise_not(blur)

    sketch = cv2.divide(grey_img, invertedblur, scale=256.0)

    cv2.imwrite("sketch.png", sketch)  # converted image is saved as mentioned name
    
    
def image_to_dithering(img_path):
    image = cv2.imread(img_path, cv2.IMREAD_COLOR)  # loads an image from the specified file
    quant_img= quantize_img(image, 3)
    
    for x in range(0,image.shape[0]-1):
        for y in range(1,image.shape[1]-1):
            [new_r,new_g,new_b] = quant_img[x][y]
            [old_r,old_g,old_b]= image[x][y]
            
            err_r =  old_r - int(new_r)
            err_g =  old_g - int(new_g)
            err_b =  old_b - int(new_b)
            
            r =  error_shift(image,x+1,y, 0, err_r,  7/16)
            g =  error_shift(image,x+1,y, 1, err_g,  7/16)
            b =  error_shift(image,x+1,y, 2, err_b,  7/16)
            
            image[x +1][y]= [r,g,b]
            
            
            r =  error_shift(image,x-1,y+1, 0, err_r,  3/16)
            g =  error_shift(image,x-1,y+1, 1, err_g,  3/16)
            b =  error_shift(image,x-1,y+1, 2, err_b,  3/16)
            
            image[x -1][y+1]= [r,g,b]
            
            r =  error_shift(image,x,y+1, 0, err_r,  5/16)
            g =  error_shift(image,x,y+1, 1, err_g,  5/16)
            b =  error_shift(image,x,y+1, 2, err_b,  5/16)
            
            image[x][y+1]= [r,g,b]
            
            r =  error_shift(image,x+1,y+1, 0, err_r,  1/16)
            g =  error_shift(image,x+1,y+1, 1, err_g,  1/16)
            b =  error_shift(image,x+1,y+1, 2, err_b,  1/16)
            
            image[x+1][y+1]= [r,g,b]
            
    grey_scaled = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('test.png',grey_scaled)
    
def error_shift(img,x, y,z, error,factor):
    return img[x][y][z] + error*factor

def quantize_img(img,factor: int):  
    newImg = np.zeros(img.shape, np.uint8)
    # img= cv2.bitwise_not(img)
    for y in range(0, img.shape[0] , 1):
        for x in range(0, img.shape[1], 1):

            # gray_val= img[y][x]
            # gray_val =  round(factor * gray_val / 255) * (255 // factor)
            # print(gray_val, end=" ")

            [r,g,b] = img[y][x]
            r =  round(factor * r / 255) * (255 / factor)
            g =  round(factor * g / 255) * (255 / factor)
            b =  round(factor * b / 255) * (255 / factor)
            # print(r,g,b)
            
            newImg[y][x] = [r,g,b]
            
    # grey_scaled = cv2.cvtColor(newImg, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite('test.png',grey_scaled) 
    return newImg       
            
            
            


image_to_dithering('image2.jpeg')

# image_to_sketch('image2.jpeg')
