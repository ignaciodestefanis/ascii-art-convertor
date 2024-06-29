# This disables the default warnings for the library OPENCV
import os
os.environ["OPENCV_LOG_LEVEL"]="SILENT"

import numpy as np
import sys
import cv2
import collections.abc

CHARACTERS = ['@', '>', '$', '~', '·', '%', 'A', 'O', '&', '+', '<', '#', '*', '^', '8', 'H', '=', '-', '?', '¿']

def convert_image(path, amount_of_colors):
    try:
        text = open("ascii.txt", 'w')    
    except:
        return
    
    if int(amount_of_colors) > len(CHARACTERS):
        print("The amount of colors should be less than " + str(len(CHARACTERS)) + ".")
        return
    
    characters_per_color = {}
    
    img = cv2.imread(path, cv2.IMREAD_COLOR)

    if not isinstance(img, np.ndarray):
        print("The selected image could not be opened. Please check that the path is correct.")
        return

    dim = (img.shape[0], img.shape[1])
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    Z = img.reshape((-1,3))
    
    # convert to np.float32
    Z = np.float32(Z)

    # define criteria, number of clusters(K) and apply kmeans()
    # criteria = ( type, max_iter = 10 , epsilon = 1.0 )
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)    
    K = int(amount_of_colors)
    ret, label, center = cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))    

    # Asigns a character to each color in the new image
    characters_index = 0
    for i in range(0, res2.shape[0]):
        for j in range(0, res2.shape[1]):
                (r, g, b) = res2[i, j]
                if (r, g, b) in characters_per_color:
                    text.write(characters_per_color[(r, g, b)])
                else:
                    characters_per_color[(r, g, b)] = CHARACTERS[characters_index]
                    text.write(CHARACTERS[characters_index])
                    characters_index += 1
        text.write('\n')
    
    text.close()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        convert_image(sys.argv[1], sys.argv[2])
    else:
        print("Incorrect format. You should execute this program as follows:")
        print("python main.py your_image_path amount_of_colors_to_consider")