import cv2
import numpy as np

def image_to_sketch(img_path):
    # loads an image from the specified file
    image = cv2.imread(img_path)  
    # convert an image from one color space to another
    grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
     # helps in masking of the image
    invert = cv2.bitwise_not(grey_img) 
    # sharp edges in images are smoothed while minimizing too much blurring
    blur = cv2.GaussianBlur(invert, (25, 25), 0)
    invertedblur = cv2.bitwise_not(blur)
    sketch = cv2.divide(grey_img, invertedblur, scale=256.0)

    return sketch
    
def quantize_img(img_path: str,factor: int): 
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE) 
    newImg = np.zeros(img.shape, np.uint8)
    h,w = img.shape
    
    for y in range(h):
        for x in range(w):
            gray_val= img[y][x]
            gray_val =  round(factor * gray_val / 255) * (255 // factor)                  
            newImg[y][x] = gray_val
    
    return newImg
            
            
            
def image_to_dithering(img_path):
    
    img= np.array(cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)) / 255
    
    h,w = img.shape
    
    for y in range(h):
        for x in range(w):
            old_val = img[y][x] 
            new_val= round(old_val)
            img[y][x] = new_val
            
            error =  old_val - int(new_val)
            if x + 1 < w:
                img[y, x + 1] += error * 0.4375 # right, 7 / 16
            if (y + 1 < h) and (x + 1 < w):
                img[y + 1, x + 1] += error * 0.0625 # right, down, 1 / 16
            if y + 1 < h:
                img[y + 1, x] += error * 0.3125 # down, 5 / 16
            if (x - 1 >= 0) and (y + 1 < h): 
                img[y + 1, x - 1] += error * 0.1875 # left, down, 3 / 16

    return (img*255).astype('uint8')


if __name__ == "__main__":
    # image_to_dithering('image.jpeg')
    quantize_img('/home/rjan/Documents/college_stuffs/applied_programming_group_project/image_to_sketch/main/image.jpeg',3)
    # image_to_sketch('image.jpeg')
