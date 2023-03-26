# packages

- lifemon_interfaces define: msg and srv for this project
- screensaver_srv: include python nodes

# run

- launch

```
$ ros2 launch screensaver_srv screensaver.launch.py
```

- server
```
$ ros2 run screensaver_srv service 
```

- client

```
$ ros2 run screensaver_srv client
```

# TODO
- [ ] how to handle control c in node
- [ ] config file (e.g., THRESHOLD_NO_FACE = 5)

  https://roboticsbackend.com/rclpy-params-tutorial-get-set-ros2-params-with-python/
  https://roboticsbackend.com/ros2-yaml-params/
- [ ] 
```
ykim@msi:~/devel/lifemon/screensaver$ ros2 param list
Exception while calling service of node '/screensaver_client_async': None
/screensaver_service:
  use_sim_time
ykim@msi:~/devel/lifemon/screensaver$ 
```

- [ ] dockerize
- [x] add launch

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