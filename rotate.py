import rclpy
from rclpy.node import Node
from protocol.msg import MotionServoCmd
import math

class RotateController(Node):
    def __init__(self, name):
        super().__init__(name)
        self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0  # 初始速度设为0
        self.dog_name = "cyberdog"
        self.pub = self.create_publisher(MotionServoCmd, f"/{self.dog_name}/motion_servo_cmd", 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.time_counter = 0.0  # 时间计数器

    def timer_callback(self):
        angle = 90  # 旋转角度，这里假设是90度
        angular_speed = 0.5  # 设置旋转的角速度，单位是弧度/秒
        time_to_rotate = abs(angle) / angular_speed  # 计算旋转需要的时间
        self.speed_z = math.copysign(angular_speed, angle)  # 根据角度确定旋转方向和速度

        msg = MotionServoCmd()
        msg.motion_id = 303
        msg.cmd_type = 1
        msg.value = time_to_rotate  # 将旋转时间设置为value字段
        msg.vel_des = [self.speed_x, self.speed_y, self.speed_z]
        msg.step_height = [0.05, 0.05]
        self.pub.publish(msg)

        self.time_counter += 0.1  # 计时器每次加0.1秒
        if self.time_counter >= time_to_rotate:  # 判断是否达到旋转时间
            self.speed_z = 0.0  # 停止旋转
            self.pub.publish(msg)  # 发布停止旋转的消息
            self.get_logger().info("Rotation completed.")
            self.timer.cancel()  # 停止定时器

def main(args = None):
    rclpy.init(args = args)
    node = RotateController("move_the_dog")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()