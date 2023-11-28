import sys

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class CarStartPublisher(Node):
    def __init__(self, car_id):
        super().__init__('car_start_Publisher')
        self.publisher_ = self.create_publisher(String, f'/start_car/{car_id}', 10)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'start'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    car_id = sys.argv[1]  # 첫 번째 인자를 차량 ID로 사용
    car_start_publisher = CarStartPublisher(car_id)
    try:
        rclpy.spin(car_start_publisher)
    except KeyboardInterrupt:
        car_start_publisher.get_logger().info('User-terminated by pressing Ctrl-c...')
    finally:
        # 노드가 종료되면 cleanup 작업을 수행
        car_start_publisher.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
