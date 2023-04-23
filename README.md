# ROS2 Packages

- lifemon_interfaces: defines msg and srv for this project
- screensaver_srv: includes python nodes

`screensaver_src` has two different nodes:
- service: runs screen saver or screen-off by the client's request
- client: able to detect the number of faces and makes the request to the service

# Installation

## Preparation
- install a Linux to an unused old laptop which must have a camera
- install xscreensaver in the Linux, so ros2 package will use the host's xscreensaver.
- install docker

## commands
You need to get the Dockerfile from `https://github.com/ymkim92/lifemon/blob/main/Dockerfile`.

Then, create an docker image by this command:
```
$ docker build -t ${YOUR_TAG_NAME} .
```
You should be able to see the Dockerfile in the ${PWD}.


docker run --rm -ti --net=host -e DISPLAY=:0 -v .:/root --device="/dev/video0:/dev/video0" ${YOUR_TAG_NAME}

docker run --rm -ti --net=host -e DISPLAY=:0 -v .:/root --device="/dev/video0:/dev/video0" yk-ros2-humble

### compose

docker compose run screensaver