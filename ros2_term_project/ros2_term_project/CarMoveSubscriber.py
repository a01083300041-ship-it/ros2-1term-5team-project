import sys
import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class CarMoveSubscriber(Node):
    def __init__(self, car_id):
        super().__init__('car_move_subscriber')
        self.subscription = self.create_subscription(
            Twist,
            f'/move_car/{car_id}',
            self.listener_callback,
            10)
        self.subscription

    def listener_callback(self, msg):
        self.get_logger().info('Rl,eceived command to move car')
        self.get_logger().info('linear.x = %.3f, angular.z = %.3f' % (msg.linear.x, msg.angular.z))


def main(args=None):
    rclpy.init(args=args)
    car_id = sys.argv[1]
    car_move_subscriber = CarMoveSubscriber(car_id)
    rclpy.spin(car_move_subscriber)
    car_move_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
