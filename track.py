import cv2
import sys
import numpy as np

def nothing(x):
    pass

camera = cv2.VideoCapture(0)

width = 1920
height = 1080

camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

#滑动式调色板
cv2.namedWindow('Trackbars')
cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)


while True:
    ret, frame = camera.read()
    if not ret: 
        print("无法读取视频")
        sys.exit()
    if ret:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        l_h = cv2.getTrackbarPos("L - H", "Trackbars")
        l_s = cv2.getTrackbarPos("L - S", "Trackbars")
        l_v = cv2.getTrackbarPos("L - V", "Trackbars")
        u_h = cv2.getTrackbarPos("U - H", "Trackbars")
        u_s = cv2.getTrackbarPos("U - S", "Trackbars")
        u_v = cv2.getTrackbarPos("U - V", "Trackbars")

        lower_green = np.array([l_h, l_s, l_v])
        upper_green = np.array([u_h, u_s, u_v])
        mask = cv2.inRange(hsv, lower_green, upper_green)

        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        result = cv2.bitwise_and(frame, frame, mask=mask)

        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 100 and h > 100:
                cv2.rectangle(frame, (x, y), (x + w, y + h), ((l_h+u_h)/2, (l_s+u_s)/2, (l_v+u_v)/2), 3)
        
        cv2.putText(frame, '(' + str(x+w/2) + ' ' + str(y+h/2) + ')', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (51, 0, 204), 2)
        #cv2.putText(frame, "y=" + str(y), (100, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (51, 0, 204), 2)
        #cv2.putText(frame, "w=" + str(w), (100, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (51, 0, 204), 2)
        #cv2.putText(frame, "h=" + str(h), (100, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (51, 0, 204), 2)

        cv2.imshow('Image', frame)
        #cv2.imshow("mask", mask)
        #cv2.imshow("result", result)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows() 
           

""" import cv2
import numpy as np

def track_green_object():
    # 打开默认摄像头
    cap = cv2.VideoCapture(0)


    while True:
        # 读取摄像头的帧
        ret, frame = cap.read()

        if not ret:
            print("无法读取视频流")
            break

        # 将 BGR 格式的图像转换为 HSV 格式
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 设定绿色物体的范围
        lower_green = np.array([35, 50, 50])
        upper_green = np.array([90, 255, 255])

        # 根据设定的范围创建掩膜
        mask = cv2.inRange(hsv, lower_green, upper_green)

        # 对掩膜进行形态学操作，以减少噪音
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # 寻找绿色物体的轮廓
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            # 找到最大的轮廓
            c = max(contours, key=cv2.contourArea)
            # 计算最小外接圆
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            # 计算轮廓的中心
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # 显示绿色物体的中心坐标
            cv2.putText(frame, f'Center: {center}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # 只有当半径大于10时才显示轮廓
            if radius > 10:
                # 绘制轮廓和中心
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

        # 显示帧
        cv2.imshow('Frame', frame)

        # 按下 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放摄像头并关闭窗口
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    track_green_object()
  """