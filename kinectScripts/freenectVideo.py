#!/usr/bin/env python

#Taken mostly from:
# https://github.com/OpenKinect/libfreenect/tree/master/wrappers/python

import freenect
import cv
import frame_convert

cv.NamedWindow('Depth')
cv.NamedWindow('Video')
print('Press ESC in window to stop')

def get_video():
    return frame_convert.video_cv(freenect.sync_get_video()[0])

while 1:
    cv.ShowImage('Video', get_video())
    if cv.WaitKey(10) == 27:
        break
