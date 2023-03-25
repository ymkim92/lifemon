import sys

import rclpy
from rclpy.node import Node

from lifemon_interfaces.srv import ActivateScreenSaver

from .facedetcam import FaceDetection


class ScreenSaverClientAsync(Node):

    def __init__(self):
        super().__init__('screensaver_client_async')
        self.cli = self.create_client(ActivateScreenSaver, 'activate_screensaver')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = ActivateScreenSaver.Request()

    def send_request(self, has_face):
        self.req.has_face = has_face
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def main():
    prev_has_face = False

    rclpy.init()
    screensaver_client = ScreenSaverClientAsync()
    face_det = FaceDetection()
    try:
        while True:
            has_face = face_det.get_face_detected(show_image=False)
            if prev_has_face != has_face:
                prev_has_face = has_face
                response = screensaver_client.send_request(has_face)
                screensaver_client.get_logger().info(
                    f'Result of activate_screensaver: {response.ret}'
                )
    except KeyboardInterrupt:
        pass

    screensaver_client.destroy_node()
    # rclpy.shutdown()


if __name__ == '__main__':
    main()