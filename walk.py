import sys
sys.path.append("/home/mi/workplace/src/learning/learning")

import rclpy
from rclpy.node import Node
from protocol.msg import MotionServoCmd
from ultrasonic import UltrasonicSensor
from sensor_msgs.msg import Range
#from step import StepController

#from backward import BackwardController
#from ultrasonic import UltrasonicSensor
#from rotate import RotateController

class Walk(Node):
    def __init__(self, name):
        super().__init__(name)
        self.dog_name = "cyberdog"
        self.ultra_sen = UltrasonicSensor(self.dog_name)
        self.speed_x, self.speed_y, self.speed_z = 0.3, 0.0, 0.0
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.pub = self.create_publisher(MotionServoCmd, f"/{self.dog_name}/motion_servo_cmd", 10)
        #self.backward_ctlr = BackwardController()
        
        #self.step_ctlr = StepController()
        #self.rotate_ctlr = RotateController()
        #self.ultrasonic_sen = UltrasonicSensor()
        self.dist = 0.0
        self.sub = self.create_subscription(Range, f'/{self.dog_name}/ultrasonic_payload', self.sub_callback, 10)

    def sub_callback(self, msg:Range):
        self.dist = msg.range

    def timer_callback(self):
        print(self.dist)
        if(self.dist > 0.9):
            self.speed_x = 0.2
            self.speed_z = 0.0
        else:
            self.speed_x = 0.0
            self.speed_z = -0.6

        msg = MotionServoCmd()
        msg.motion_id = 303
        msg.cmd_type = 1
        msg.value = 2
        msg.vel_des = [self.speed_x, self.speed_y, self.speed_z]
        msg.step_height = [0.02, 0.02]
        self.pub.publish(msg)

        


def main(args = None):
    rclpy.init(args = args)
    node = Walk("move_the_dog")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
