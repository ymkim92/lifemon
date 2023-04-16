"""client: detect face"""

import time
import rclpy
from lifemon_interfaces.srv import ActivateScreenSaver
from rclpy.node import Node

from .facedetcam import FaceDetection

DEFAULT_NO_FACE_TIMES = 3
DEFAULT_INTERVAL_SEC_CAMERA_CAPTURE = 2

class ScreenSaverClientAsync(Node):
    """ros2 node"""

    def __init__(self):
        super().__init__('screensaver_client_async')

        self.prev_has_face = False

        self.declare_parameter("no_face_times", DEFAULT_NO_FACE_TIMES)
        self.declare_parameter("interval_camera_capture", DEFAULT_INTERVAL_SEC_CAMERA_CAPTURE)
        self.no_face_times = self.get_parameter("no_face_times").get_parameter_value().integer_value
        self.interval_camera_capture = self.get_parameter("interval_camera_capture").get_parameter_value().integer_value
        self.get_logger().info(f"no_face_times: {self.no_face_times}")
        self.get_logger().info(f"interval_camera_capture: {self.interval_camera_capture} s")

        self.face_det = FaceDetection(self.no_face_times)

        self.timer = self.create_timer(1, self.timer_callback)

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

    def timer_callback(self):
        """ configure parameter"""
        self.no_face_times = self.get_parameter("no_face_times").get_parameter_value().integer_value
        self.interval_camera_capture = self.get_parameter("interval_camera_capture").get_parameter_value().integer_value
        self.get_logger().info(f"interval_camera_capture..: {self.interval_camera_capture}")


def main():
    """main"""

    rclpy.init()
    screensaver_client = ScreenSaverClientAsync()
    rclpy.spin(screensaver_client)
    try:
        # TODO
        # This needs to be run in seperate thread
        # HOW? thread or ros node?
        while rclpy.ok():
            screensaver_client.face_det.threshold_no_face = screensaver_client.no_face_times
            has_face = screensaver_client.face_det.get_face_detected(show_image=False)
            screensaver_client.get_logger().info(f"main loop has_face {has_face}")
            if screensaver_client.prev_has_face != has_face:
                screensaver_client.prev_has_face = has_face
                response = screensaver_client.send_request(has_face)
                screensaver_client.get_logger().info(
                    f'Result of activate_screensaver: {response.ret}'
                )
            
            time.sleep(screensaver_client.interval_camera_capture)

            rclpy.spin_once(screensaver_client)
    except KeyboardInterrupt:
        pass

    screensaver_client.destroy_node()
    # rclpy.shutdown()


if __name__ == '__main__':
    main()
