from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='screensaver_srv',
            executable='service',
            name='server'
        ),
        Node(
            package='screensaver_srv',
            # namespace='turtlesim2',
            executable='client',
            name='client'
        ),
    ])