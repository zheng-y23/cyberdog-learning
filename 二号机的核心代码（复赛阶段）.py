import cv2
import rclpy
from rclpy.node import Node
from protocol.msg import MotionServoCmd
from cv_bridge import CvBridge
import numpy as np
from sensor_msgs.msg import Image
from sensor_msgs.msg import Range
 
class Tracker(Node):
    def __init__(self, name):
        super().__init__(name)
        self.dog_name = "cyberdog"
        self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
        #self.qos = rclpy.qos.QosProfile(depth=10)
        #self.qos.reliability = 

        self.image = Image()
        self.dist = 0.0

        self.time = 0
        self.flag = 0

        self.id = 303

        self.bridge = CvBridge()
        self.sub1 = self.create_subscription(Image, '/camera/infra1/image_rect_raw', self.image_callback, 10)
        self.sub2 = self.create_subscription(Range, f'/{self.dog_name}/ultrasonic_payload', self.dist_callback, 10)
        #self.image = Image()
        self.timer = self.create_timer(0.05, self.timer_callback)
        self.pub = self.create_publisher(MotionServoCmd, f"/{self.dog_name}/motion_servo_cmd", 10)

        

    def image_callback(self, msg : Image):
        self.image = msg
        #print(f"Image encoding: {msg.encoding}")

    def dist_callback(self, msg : Range):
        self.dist = msg.range


    def timer_callback(self):
        cv_image = self.bridge.imgmsg_to_cv2(self.image, "mono8")
        print ("image transmitted")

        #bgr = cv2.cvtColor(cv_image, cv2.COLOR_GRAY2BGR)
        #hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        #cv2.imwrite("image.jpg", bgr)

        #image = cv2.imread('gray_image.png', cv2.IMREAD_GRAYSCALE)
        
    

        # 检查图像是否加载成功
        if cv_image is None:
            print("Error: Unable to load image")
            exit()

        # 应用阈值操作以分离深色圆形
        _, thresholded = cv2.threshold(cv_image, 50, 255, cv2.THRESH_BINARY_INV)
        #adaptive_thresholded = cv2.adaptiveThreshold(cv_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, blockSize=2, C=15)
        # 检测轮廓
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        

        # 创建一个彩色版本的图像用于显示结果
        output_image = cv2.cvtColor(cv_image, cv2.COLOR_GRAY2BGR)
        x1 = 320
        r1 = 50
        # 遍历所有检测到的轮廓
        for contour in contours:
            # 计算轮廓的面积和最小外接圆
            area = cv2.contourArea(contour)
            (x, y), radius = cv2.minEnclosingCircle(contour)
            # 忽略太小的轮廓
            if radius > 15 and radius < 100 and (area / (3.14 * radius * radius)) > 0.7:
                # 绘制圆形标记
                center = (int(x), int(y))
                x1 = x
                r1 = radius
                cv2.putText(output_image, 'radius: ' + str(radius), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (51, 0, 204), 2)
                radius = int(radius)
                cv2.circle(output_image, center, radius, (0, 255, 0), 2)

            
        cv2.putText(output_image, 'time: '+str(self.time)+'d: ' + str(self.dist), (100, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (51, 0, 204), 2)
 
        if self.flag == 0:
            self.speed_y = 0.0
            if x1 > 350:
                self.flag = -1
                #self.speed_y = -0.6
            elif x1 < 290:
                self.flag = 1
                #self.speed_y = 0.6
            else:
                self.flag = 0
                #self.speed_y = 0.00

        if self.flag == 1:
            self.speed_y = 0.6
            self.time += 1
            if self.time == 70:
                self.time = 0
                self.flag = 0
        elif self.flag == -1:
            self.speed_y = -0.6
            self.time += 1
            if self.time == 70:
                self.time = 0
                self.flag = 0

        '''if r1 > 60:
            self.speed_x = -0.3
        elif r1 < 40:
            self.speed_x = 0.3
        else:
            self.speed_x = 0.0
            #稳定计时    
            if abs(self.r - r1) < 2.0 and abs(x1 - 320) < 40 and x1 != 320:
                self.time1 += 1
            else:
                self.time1 = 0
        
        elif self.flag == 1:
            self.speed_x = 1.1
            #self.id = 305
            if self.time2 == 40:
                self.flag = 2
                self.time2 = 0
            self.time2 += 1
        else:
            self.speed_x = 0'''
            
            

            
        self.r = r1
        cv2.imwrite("image.jpg", output_image)


        msg = MotionServoCmd()
        msg.motion_id = self.id
        msg.cmd_type = 1
        msg.value = 2
        msg.vel_des = [self.speed_x, self.speed_y, self.speed_z]
        msg.step_height = [0.05, 0.05]
        self.pub.publish(msg)

def main(args = None):
    rclpy.init(args = args)
    node = Tracker("move_the_dog")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

