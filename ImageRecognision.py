import time
import cv2
import numpy as np
cap = cv2.VideoCapture('http://192.168.2.106:21555/video')
while(True):
    cv2.namedWindow("Final", cv2.WINDOW_NORMAL)
    ret, frame = cap.read()
    # conduct color threshold
    if ret:
        mask=cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        (thresh, im_bw) = cv2.threshold(mask, 128, 255, 0)
        # find contours
        (cnts, _) = cv2.findContours(im_bw, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  
          # loop over the contours
        for c in cnts:
       # if the contour is too small, ignore it
            if cv2.contourArea(c) < 500:
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2) 

        # show the images
        cv2.imshow("Final",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break




