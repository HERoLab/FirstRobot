#Run me if the kinect is not being detected!
sudo gst-launch-0.10 v4l2src device=/dev/video0 ! video/x-raw-yuv ! ffmpegcolorspace ! xvimagesink
