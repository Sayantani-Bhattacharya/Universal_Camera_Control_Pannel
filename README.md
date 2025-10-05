# Universal Camera Control Pannel
A Universal Pannel (GUI) for controlling Camera Drivers from Linux systems. 

## Features:
1. Abstaction layer over V4L2 (Video4Linux2) API.
2. Works on System76 Ubuntu20 and RasberryPi ARM. 
3. For frames of type H.264 (Compressed). Later will extend for YUYV and RGB. 

## Directions:
1. Clone the repo and run.
    
        python3 pannel.py

2. To visualize the changes live, apt install g-streamer and run:

        gst-launch-1.0 -v v4l2src device=/dev/video4 !   'video/x-h264, width=1920, height=1080, framerate=30/1' !   h264parse ! avdec_h264 ! videoconvert ! autovideosink

## Pannel GUI:
<p align="center">
  <img src="/GUI.png" alt="Alt text" width="800"/>
</p>


## Modifiable Params: 
1. brightness
2. contrast
3. saturation
4. hue
5. white balance automatic (bool)
6. gamma
7. gain
8. power line frequency
9. white balance temperature
10. sharpness
11. backlight compensation
12. auto exposure
13. exposure time absolute
14. exposure dynamic frame rate
    
## Camera Hardware Currently tested on:
1. Blue ROV low-light monocular HD.
</br> Later:
2. Realsense D405.
3. Realsense D4xx series.
4. OAK D Lite.




