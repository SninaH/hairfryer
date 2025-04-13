import cv2
from pytesseract import image_to_string
import numpy as np
import matplotlib.pyplot as plt

from src.video_utils.get_subimage import get_subimage

"""Page segmentation modes:
  0    Orientation and script detection (OSD) only.
  1    Automatic page segmentation with OSD.
  2    Automatic page segmentation, but no OSD, or OCR.
  3    Fully automatic page segmentation, but no OSD. (Default)
  4    Assume a single column of text of variable sizes.
  5    Assume a single uniform block of vertically aligned text.
  6    Assume a single uniform block of text.
  7    Treat the image as a single text line.
  8    Treat the image as a single word.
  9    Treat the image as a single word in a circle.
 10    Treat the image as a single character.
 11    Sparse text. Find as much text as possible in no particular order.
 12    Sparse text with OSD.
 13    Raw line. Treat the image as a single text line,
                        bypassing hacks that are Tesseract-specific.
"""

def get_text(img):
    # img = cv2.imread(filename)
    #resize the image to 32x32
    # print("img.shape", img.shape)
    d = 64
    img = cv2.resize(img, (d,d))
    
    
    # img = cv2.resize(img, None, fx=0.5, fy=0.5)
    HSV_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(HSV_img)
    g = 0.5
    # v = cv2.GaussianBlur(v, (g,g), 0)
    thresh = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    cv2.imwrite('1.png',thresh)
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(1, 2))
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(100,100))
    # thresh = cv2.dilate(thresh, kernel)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(2,2))
    thresh = cv2.dilate(thresh, kernel)
    cv2.imwrite('2.png',thresh)
    # txt = image_to_string(thresh, config="--psm 6 digits")
    # txt = image_to_string(thresh, config="--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789")
    # txt = image_to_string(thresh, config="--psm 10 -c tessedit_char_whitelist=0123456789")
    txt = image_to_string(thresh, lang="lets", config="--psm 8 -c tessedit_char_whitelist=0123456789")
    # txt = image_to_string(thresh, tessedit_char_whitelist="0123456789")
    return txt

def get_number(img):
    text = get_text(img).replace('\f', '')
    text = ''.join([c for c in text if c.isdigit()])
    return int(text) if len(text) > 0 else None

# ali lucka gori
def light_type(subimage, brightness_threshold=0.9):
    """
        subimage: cv2
        return: 1 if light is bright and 0 else
    """
    gray = cv2.cvtColor(subimage, cv2.COLOR_BGR2GRAY)

    # mean_brightness = cv2.mean(gray)[0]
    mean_brightness = np.median(gray)
    
    
    normalized_brightness = mean_brightness / 255.0
    # print("normalized_brightness", normalized_brightness)
    return int(normalized_brightness >= brightness_threshold)

if __name__ == "__main__":
    # for img_path in['images/one.png', 'images/two.png', 'subimage.png']:
    #     img = cv2.imread(img_path)
    #     # text = get_text(img_path).replace('\f', '')
    #     num = get_number(img)
    #     print(img_path, num)
    
    # img_path  ='images/medium/frame25200.jpg'
    # img = get_subimage(img_path, 729, 144, 27, 23)
    # plt.imshow(img)
    # plt.show()
    
    # num = get_number(img)
    # print(img_path, num)
    
    img_path  ='images/tiny/frame300.jpg'
    img = cv2.imread(img_path)
    plt.imshow(img)
    plt.show()
    # img = get_subimage(img_path, 729, 144, 27, 23)
    size = 8
    
    fields = [
        (812, 44, size, size),
        
        (775,63, size, size),
        (848,64, size, size),
        
        (737, 81, size, size),
        (812,83, size, size),
        (886,83, size, size),
        
        (774,100, size, size),
        (850, 103, size, size),
        
        (811,120, size, size)        
    
    ]
    for field in fields:
        x,y,w,h = field
        img = get_subimage(img_path, x, y, w, h)
        num = light_type(img)
        print(img_path, num)
        plt.imshow(img)
        plt.show()

    
    # num = get_number(img)
    
    