# packages

- lifemon_interfaces define: msg and srv for this project
- screensaver_srv: include python nodes


# issue

## 1. can't find xml file during build: 2023/03/18

ykim@msi:~/devel/lifemon/screensaver$ colcon build
...
--- stderr: screensaver_srv                   
error: package directory 'haarcascade_frontalface_default/xml' does not exist
...

- solution: https://roboticsbackend.com/create-a-ros2-python-package/ 

## 2. AttributeError: module 'cv2' has no attribute 'data'

- solution:
```
pip install opencv-contrib-python --upgrade 
```