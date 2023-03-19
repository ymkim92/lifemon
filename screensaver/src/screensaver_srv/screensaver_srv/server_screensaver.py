import subprocess

import rclpy
from rclpy.node import Node

from lifemon_interfaces.srv import ActivateScreenSaver


class ScreenSaverService(Node):

    def __init__(self):
        super().__init__('screensaver_service')
        self.srv = self.create_service(ActivateScreenSaver, 
                'activate_screensaver', self.activate_screensaver_callback)

    def activate_screensaver_callback(self, request, response):
        ret = None
        if request.has_face:
            ret = subprocess.run("xscreensaver-command --activate", shell=True)
        else:
            ret = subprocess.run("xset dpms force off", shell=True)
        
        self.get_logger().info(f"return code: {ret.returncode}")

        response.ret = request.returncode == 0

        return response


def main():
    rclpy.init()

    screensaver_service = ScreenSaverService()

    rclpy.spin(screensaver_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()