FROM osrf/ros:humble-desktop
ARG DEBIAN_FRONTEND=noninteractive

RUN \
  apt update && \
  apt-get install -y apt-utils && \
  apt -y upgrade && \
  apt install -y wget unzip python3-pip && \
  apt install -y vim tmux htop && \
  apt install -y x11-xserver-utils && \
  apt install -y xscreensaver && \
  pip3 install opencv-contrib-python --upgrade 

WORKDIR /root  

# RUN \
#   wget https://github.com/ymkim92/lifemon/archive/refs/heads/main.zip && \
#   unzip main.zip && \
#   cd lifemon-main && \
#   bash -c ". /opt/ros/humble/setup.bash && \
#   colcon build && \
#   . install/setup.bash && \
#   ros2 launch screensaver_srv screensaver.launch.py"