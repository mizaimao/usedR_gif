#!/usr/bin/env python3

import cv2
import imageio
import numpy as np
import random
import skimage


random.seed(6849815)

SIZE = 256
BACKGROUND = (255,255,255)
BACKGROUND_IMAGE = None

font = cv2.FONT_HERSHEY_COMPLEX

def load_bg():
    if not BACKGROUND_IMAGE:
        return np.full((SIZE, SIZE, 3), BACKGROUND, dtype=np.uint8)
    try:
        bg = cv2.imread(BACKGROUND_IMAGE)
    except:
        print('Cannot load background image')
        exit(1)

    resized = cv2.resize(bg, (SIZE, SIZE))
    return resized


def main():
    bg = load_bg()
    center = SIZE//2
    stage1_text = 'Used' # + '...'
    stage2_text = 'R'

    stage1_length = 12
    stage1_divider = stage1_length//4
    stage1_size = 1.0
    
    stage2_length = 24

    img_list = []
    counter = 0
    while counter < stage1_length:
        img = bg.copy()

        apd = '.' * ((counter//stage1_divider))
        new_stage1_text = stage1_text + apd

        textsize = cv2.getTextSize(new_stage1_text, font, stage1_size, 2)[0]
        textX = (SIZE - textsize[0]) // 2
        textY = (SIZE + textsize[1]) // 2
       
        cv2.putText(img, new_stage1_text, (textX, textY), font, stage1_size, (200,200,200), 2)
        counter += 1
        img_list.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        
    
    counter = 0
    while counter < stage2_length:
        # c for color; p for position; s for size
        img = bg.copy()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        s = (counter*0.25) + 1
        while True:
            c = np.random.randint(256, size=(3,), dtype=np.uint8)
            if np.std(c) > 100:
                break
        
        misposition = int((counter+1)*0.005*SIZE)
        
        textsize = cv2.getTextSize(stage2_text, font, s, 8)[0]
        textX = (SIZE - textsize[0]) / 2
        textY = (SIZE + textsize[1]) / 2
        px = np.random.randint(textX - misposition, textX + misposition, size=(1,), dtype=np.uint8)
        py = np.random.randint(textY - misposition, textY + misposition, size=(1,), dtype=np.uint8)
        
        cv2.putText(img,stage2_text, (px[0], py[0]), font, s, c.tolist(), 8)
        counter += 1

        img_list.append(img)

    imageio.mimsave('R.gif', img_list)

if __name__ == '__main__':
    main()
