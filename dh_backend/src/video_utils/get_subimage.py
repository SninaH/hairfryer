# get sub image from image
import cv2
import numpy as np
import matplotlib.pyplot as plt

def get_subimage(image, x, y, w, h):
    """
    Extract a sub-image from the given image.

    Parameters:
        image (numpy.ndarray): The input image.
        x (int): The x-coordinate of the top-left corner of the sub-image.
        y (int): The y-coordinate of the top-left corner of the sub-image.
        w (int): The width of the sub-image.
        h (int): The height of the sub-image.

    Returns:
        numpy.ndarray: The extracted sub-image.
    """
    # return image[y:(y+h), x:(x+w)]
    img = cv2.imread(image)
    #img dim
    print(img.shape)
    print("TUKI", "x", x, "y", y, "w", w, "h", h)
    sub_img = img[y:(y+h), x:(x+w)]
    # cv2.imwrite('subimage.png', sub_img)
    return sub_img

if __name__ == "__main__":
    # lr, ud, w, h
    # img = get_subimage('images/tiny/frame0.jpg', 729, 144, 27, 23)
    # img = get_subimage('images/tiny/frame300.jpg', 805, 145, 19, 22)
    # img = get_subimage('images/tiny/frame300.jpg', 857, 145, 33, 21)
    
    # img = get_subimage('images/medium/frame25200.jpg', 729, 144, 27, 23)
    # # img = get_subimage('images/medium/frame25200.jpg', 805, 145, 19, 22)
    # img = get_subimage('images/medium/frame25200.jpg', 857, 145, 43, 21)
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
        img = get_subimage('images/medium/frame25200.jpg', x, y, w, h)
        plt.imshow(img)
        plt.show()