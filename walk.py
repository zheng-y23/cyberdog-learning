import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from ultrasonic import UltrasonicSensor
from backward import BackwardController
from forward import ForwardController
from rotate import RotateController
from step import StepController

class ObstacleAvoidanceNode(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance_node')
        self.declare_parameter('dog_name', 'cyberdog')
        dog_name = self.get_parameter('dog_name').get_parameter_value().string_value
        
        # 初始化各个控制器
        self.backward_ctrl = BackwardController()
        self.forward_ctrl = ForwardController()
        self.rotate_ctrl = RotateController()
        self.step_ctrl = StepController()

        # 初始化超声波传感器
        self.ultrasonic_sensor = UltrasonicSensor(self)

        # 订阅超声波数据
        self.subscription = self.create_subscription(
            Range,
            f'/{dog_name}/ultrasonic_payload',
            self.ultrasonic_callback,
            10)
        self.subscription  # prevent unused variable warning

        # 设置初始状态
        self.stand_ctrl.execute()

    def ultrasonic_callback(self, msg):
        distance = msg.data  # 获取超声波测得的距离

        if distance < 0.5:  # 若距离过近，执行紧急停止并坐下
            self.stop_all()
            self.sit_ctrl.execute(12)
        elif distance < 1.0:  # 若距离适中，尝试后退并旋转避开障碍物
            self.backward_ctrl.execute()
            self.rotate_ctrl.execute(90)  # 旋转90度以避开障碍物
        else:  # 距离足够远时，继续前进或行走
            self.forward_ctrl.execute()
            self.step_ctrl.execute()

    def stop_all(self):
        self.backward_ctrl.stop()
        self.forward_ctrl.stop()
        self.rotate_ctrl.stop()
        self.sit_ctrl.stop()
        self.stand_ctrl.stop()
        self.step_ctrl.stop()

def main(args=None):
    rclpy.init(args=args)
    obstacle_avoidance_node = ObstacleAvoidanceNode()
    rclpy.spin(obstacle_avoidance_node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()