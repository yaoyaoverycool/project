import serial
from time import sleep
import mediapipe as mp
import cv2
import media3
import usart

if __name__ == '__main__':
    ser=serial.Serial('COM5',9600,timeout=0.5)
    if ser.isOpen():
        print('open success')
    else:
        print('open failed')

    hands = mp.solutions.hands.Hands()  # 打开手部识别传感器
    draw = mp.solutions.drawing_utils   # 画出手部识别点
    img_shape = (1000, 800)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        # 不停地从摄像头提取每一帧的图像
        ret, img = cap.read()
        # 如果成功读取摄像头数据，则将该数据拿出
        img = cv2.resize(img, img_shape)
        if ret:
            # 调用findHands函数找到手的特征
            hand_landmarks = media3.findHands(img, hands, draw)
            # 调用detectNumber函数来识别手势对应的数字
            if hand_landmarks:
                detected_number = media3.detectNumber(hand_landmarks, img)
                if detected_number >= 0:
                    # 把这个数字显示到视频窗口
                    cv2.putText(img, str(detected_number),
                                (int(img_shape[0] / 2), 200), cv2.FONT_HERSHEY_PLAIN, 20, (255, 0, 0), 10)
                    usart.send(ser,str(detected_number))
                    #sleep(0.5)
                    data = usart.recv(ser)
                    #        print('data=',data,'|')
                    if data != '':
                        print("receive:", data)
                        #           print(type(data))
                        if data == '71':
                            print('exit')
                            break
            cv2.imshow("capture", img)
        # 如果用户按下q键，则退出窗口
        if cv2.waitKey(1) == ord('q'):
            break
    ser.close()
    cap.release()
    cv2.destroyAllWindows()