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
        self.has_face = False
        self.prev_time_caputure = 0

        self.declare_parameter("no_face_times", DEFAULT_NO_FACE_TIMES)
        self.declare_parameter("interval_camera_capture", DEFAULT_INTERVAL_SEC_CAMERA_CAPTURE)
        self.no_face_times = self.get_parameter("no_face_times").get_parameter_value().integer_value
        self.interval_camera_capture = self.get_parameter("interval_camera_capture").get_parameter_value().integer_value
        self.get_logger().info(f"no_face_times: {self.no_face_times}")
        self.get_logger().info(f"interval_camera_capture: {self.interval_camera_capture} s")

        self.face_det = FaceDetection(self.no_face_times)

        self.timer_param = self.create_timer(1, self.timer_callback_param)
        self.timer_faces = self.create_timer(2, self.timer_callback_faces)

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

    def timer_callback_param(self):
        """ configure parameter"""
        self.no_face_times = self.get_parameter("no_face_times").get_parameter_value().integer_value
        self.interval_camera_capture = self.get_parameter("interval_camera_capture").get_parameter_value().integer_value

    def timer_callback_faces(self):
        """ get has_face"""
        curr_time = time.time()
        if (curr_time - self.prev_time_caputure) > self.interval_camera_capture:
            self.face_det.threshold_no_face = self.no_face_times
            # TODO move threshold to argument!
            self.has_face = self.face_det.get_face_detected(show_image=False)
            self.get_logger().info(f"main loop has_face {self.has_face}")
            self.prev_time_caputure = curr_time

def main():
    """main"""

    rclpy.init()
    screensaver_client = ScreenSaverClientAsync()
    try:
        while rclpy.ok():
            if screensaver_client.prev_has_face != screensaver_client.has_face:
                screensaver_client.prev_has_face = screensaver_client.has_face
                response = screensaver_client.send_request(screensaver_client.has_face)
                screensaver_client.get_logger().info(
                    f'Result of activate_screensaver: {response.ret}'
                )

            rclpy.spin_once(screensaver_client)
    except KeyboardInterrupt:
        pass

    screensaver_client.destroy_node()
    # rclpy.shutdown()


if __name__ == '__main__':
    main()
