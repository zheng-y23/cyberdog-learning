import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist
import math

class ObstacleAvoidanceNode(Node):

    def __init__(self):
        super().__init__('obstacle_avoidance_node')
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.ultrasonic_subscriber = self.create_subscriber(Range, '/ultrasonic', self.callback)

    def callback(self, msg):
        self.ultrasonic = msg.range

    def forward(self):
        # 假设这个函数已经实现，使机器人向前移动
        cmd = Twist()
        cmd.linear.x = 0.1  # 向前移动
        self.cmd_vel_publisher.publish(cmd)

    def rotation(self):
        # 假设这个函数已经实现，使机器人逆时针旋转
        cmd = Twist()
        cmd.angular.z = -1.0  # 逆时针旋转
        self.cmd_vel_publisher.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    obstacle_avoidance_node = ObstacleAvoidanceNode()
    
    while rclpy.ok():
        rclpy.spin_once(obstacle_avoidance_node)
        distance = obstacle_avoidance_node.ultrasonic
        
        if distance < 0.5:
            obstacle_avoidance_node.rotation()
        elif distance > 1.0:
            obstacle_avoidance_node.forward()

    obstacle_avoidance_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()