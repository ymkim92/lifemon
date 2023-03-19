import os
from glob import glob

from setuptools import setup

package_name = 'screensaver_srv'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'resource'), glob('resource/*.xml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ykim',
    maintainer_email='ymkim92@gmail.com',
    description='server activates screensaver by the number of faces from the webcam',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'service = screensaver_srv.server_screensaver:main',
            'client = screensaver_srv.client_num_faces:main',
        ],
    },
)
