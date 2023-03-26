""" launch file """
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """generate launch desc"""
    return LaunchDescription([
        Node(
            package='screensaver_srv',
            executable='service',
            name='screensaver_service'
        ),
        Node(
            package='screensaver_srv',
            # namespace='ns1',
            executable='client',
            name='screensaver_client_async',
            parameters=[
                {'no_face_times': 5}
            ]
        ),
    ])
