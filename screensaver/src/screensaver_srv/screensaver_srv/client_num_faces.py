"""client: detect face"""

import rclpy
from lifemon_interfaces.srv import ActivateScreenSaver
from rclpy.node import Node

from .facedetcam import FaceDetection

DEFAULT_NO_FACE_TIMES = 5

class ScreenSaverClientAsync(Node):
    """ros2 node"""

    def __init__(self):
        super().__init__('screensaver_client_async')

        self.declare_parameter("no_face_times", DEFAULT_NO_FACE_TIMES)
        self.no_face_times = self.get_parameter("no_face_times").get_parameter_value().integer_value
        self.get_logger().info(f"no_face_times: {self.no_face_times}")

        self.cli = self.create_client(ActivateScreenSaver, 'activate_screensaver')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = ActivateScreenSaver.Request()
        self.future = None

    def send_request(self, has_face):
        """ send request"""
        self.req.has_face = has_face
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def main():
    """main"""
    prev_has_face = False

    rclpy.init()
    screensaver_client = ScreenSaverClientAsync()
    face_det = FaceDetection(screensaver_client.no_face_times)
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
