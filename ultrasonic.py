import rclpy
from rclpy.node import Node 
from sensor_msgs.msg import Range

#import threading

class UltrasonicSensor(Node):
    '''subscribe the message of sensor'''
    def __init__(self, name) -> None:
        super().__init__(name)
        self.declare_parameter('dog_name', 'cyberdog')
        dog_name = self.get_parameter('dog_name').get_parameter_value().string_value
        self.sub = self.create_subscription(Range, f'/{dog_name}/ultrasonic_payload', self.sub_callback, 10)
        self.dist = 0.0
        #self.dist_lock = threading.Lock()
        

    def sub_callback(self, msg:Range):
        #with self.dist_lock:  # 使用锁保证线程安全
        self.dist = msg.range
        self.get_logger().info(f"the distance is {self.dist}")
       
    #def get_distance(self):
        #with self.dist_lock:  # 使用锁保证线程安全
            #return self.dist

def main(args = None):
    rclpy.init(args = args)
    node = UltrasonicSensor("my_sensor")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()