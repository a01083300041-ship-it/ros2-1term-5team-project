
import time
import cv2

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from ros2_term_project.line_tracker import LineTracker
from sensor_msgs.msg import LaserScan
import cv_bridge


class LineFollower(Node):

    def __init__(self, line_tracker: LineTracker):
        super().__init__('line_follower')
        self.line_tracker = line_tracker
        self.bridge = cv_bridge.CvBridge()
        self._subscription = self.create_subscription(Image, '/camera1/image_raw', self.image_callback, 10)  # auto create topic name
        self._subscription2 = self.create_subscription(Image, '/camera3/image_raw', self.image_callback2, 10)  # auto create topic name

        self.lidar_subscription = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)

        self._publisher = self.create_publisher(Twist, 'cmd_vel', 1)  # create publisher
        self.twist = Twist()
        self.twist.linear.x = 6.0  # car speed
        self.a = 800
        self.b = 100
        self.img = None
        self.target_x = 6.0
        self.count = 0
        self.obstacle_found = False
        self.timer = None
        self.stop_timer = time.time()

    def image_callback(self, msg: Image):
        if self.obstacle_found: return
        if self.count >= 3:
            return
        img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        self.line_tracker.process(img)
        print("speed : %f " % self.twist.linear.x)
        if abs(self.line_tracker._delta) > 15:
            self.twist.linear.x = 1.0
            if self.b < self.a:
                self.twist.angular.z = (-1) * self.line_tracker._delta / self.b
                self.b += 1
            elif self.b >= 800:
                self.b = 400

        else:
            self.b = 50
            self.target_x = 6.0
            if self.twist.linear.x < self.target_x:
                if self.twist.linear.x + 0.1 <= 6 :
                    self.twist.linear.x += 0.1
                else:
                    self.twist.linear.x == 6.0
            self.twist.angular.z = (-1) * self.line_tracker._delta / self.a

        self._publisher.publish(self.twist)

    def image_callback2(self, msg: Image):
        img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        white_pixels : int = self.line_tracker.detect_stop_line(img)
        if white_pixels > 150:  # 정지선을 감지하면
            print(self.count)
            if time.time() - self.stop_timer > 5:
                self.count += 1
                if self.count >= 3:  # count가 3 이상이면
                    self.stop()  # 차량을 정지
                    return
                self.stop()
                time.sleep(3)  # 3초간 대기
                self.stop_timer = time.time()
            self.twist.linear.x = 4.0 # 대기 후 다시 속도를 설정

        cv2.waitKey(3)

    def stop(self):  # for robot stop
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0
        self._publisher.publish(self.twist)

    @property
    def publisher(self):
        return self._publisher

    def scan_callback(self, msg: LaserScan):
        min_distance = min(msg.ranges)
        if not self.obstacle_found and min_distance < 5.0:
            self.stop()
            self.obstacle_found = True
        else:
            self.obstacle_found = False


    def restart(self):
        # Reset the flag
        self.obstacle_found = False
        # Increase the speed
        self.twist.linear.x = 6.0
        self._publisher.publish(self.twist)
        # Cancel the timer
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None


def main():
    rclpy.init()
    tracker = LineTracker()
    follower = LineFollower(tracker)
    try:
        rclpy.spin(follower)
    except KeyboardInterrupt:
        follower.stop()
        follower.stop()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
