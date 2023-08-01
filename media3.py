import mediapipe as mp
import cv2
import math
dist_thresh = 90


def findHands (img,hands,draw):
    # 获得MP hands和draw初始化对象
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    # 定义我们轮廓的画图风格
    handlmsstyle=draw.DrawingSpec(color=(0,0,255),thickness=5)
    handconstyle=draw.DrawingSpec(color=(0,255,0),thickness=5)
    # 需要mp去寻找视频流中的手部位置，并把所有的landmarks提取出来
    results=hands.process(imgRGB)
    # 如果找到了
    if results.multi_hand_landmarks:
        # 找出所有出现在视频中的手，并把所有手部特征都画出来
        for handLms in results.multi_hand_landmarks:
            draw.draw_landmarks(img,handLms,mp.solutions.hands.HAND_CONNECTIONS,
                                handlmsstyle,handconstyle)
    return results.multi_hand_landmarks


def detectNumber (hand_landmarks,img):
    # 图片的宽和高取出
    h,w,c=img.shape
    # 找到第一只手的特征并且提取出来
    myHand = hand_landmarks[0]
    hand_landmarks = myHand.landmark

    # 找出我们所需的手指的特征点
    thumb_tip_id=4
    index_finger_tip_id=8
    middle_finger_tip_id=12
    ring_finger_tip_id=16
    pinky_tip_id=20
    pinky_mcp_id=17
    index_finger_mcp_id = 5

    # 把上述所有的特征点的x坐标和y坐标提取出来
    # 提取y坐标
    thumb_tip_y=hand_landmarks[thumb_tip_id].y*h
    index_finger_tip_y=hand_landmarks[index_finger_tip_id].y*h
    middle_finger_tip_y=hand_landmarks[middle_finger_tip_id].y*h
    ring_finger_tip_y=hand_landmarks[ring_finger_tip_id].y*h
    pinky_tip_y=hand_landmarks[pinky_tip_id].y*h
    pinky_mcp_y=hand_landmarks[pinky_mcp_id].y*h

    # 提取x坐标
    thumb_tip_x=hand_landmarks[thumb_tip_id].x*w
    index_finger_tip_x=hand_landmarks[index_finger_tip_id].x*w
    middle_finger_tip_x=hand_landmarks[middle_finger_tip_id].x*w
    ring_finger_tip_x=hand_landmarks[ring_finger_tip_id].x*w
    pinky_tip_x=hand_landmarks[pinky_tip_id].x*w
    pinky_mcp_x=hand_landmarks[pinky_mcp_id].x*w
    index_finger_mcp_x=hand_landmarks[index_finger_mcp_id].x*w

    # 计算大拇指到所有其他点的距离
    dist_thumb2index=math.sqrt((thumb_tip_x-index_finger_tip_x)**2+
                               (thumb_tip_y-index_finger_tip_y)**2)
    dist_thumb2middle = math.sqrt((thumb_tip_x - middle_finger_tip_x) ** 2 +
                                 (thumb_tip_y - middle_finger_tip_y) ** 2)
    dist_thumb2ring = math.sqrt((thumb_tip_x - ring_finger_tip_x) ** 2 +
                                 (thumb_tip_y - ring_finger_tip_y) ** 2)
    dist_thumb2pinky = math.sqrt((thumb_tip_x - pinky_tip_x) ** 2 +
                                 (thumb_tip_y - pinky_mcp_y) ** 2)
    dist_thumb2pinkymcp = math.sqrt((thumb_tip_x - pinky_mcp_x) ** 2 +
                                 (thumb_tip_y - pinky_mcp_y) ** 2)
    dist_thumb2pinkymcp = math.sqrt((thumb_tip_x - pinky_mcp_x) ** 2 +
                                    (thumb_tip_y - pinky_mcp_y) ** 2)
    dist_index2middle = math.sqrt((index_finger_tip_x - middle_finger_tip_x) ** 2 +
                                 (index_finger_tip_y - middle_finger_tip_y) ** 2)
    dist_middle2ring = math.sqrt((middle_finger_tip_x - ring_finger_tip_x) ** 2 +
                                  (middle_finger_tip_y - ring_finger_tip_y) ** 2)

    #    print(dist_thumb2index,dist_thumb2middle,dist_thumb2ring,dist_thumb2pinky,dist_thumb2pinkymcp)
    # 识别数字3
    if dist_thumb2pinky<25 and dist_thumb2index>dist_thresh \
        and dist_thumb2middle>dist_thresh and dist_thumb2ring>dist_thresh:
        return 3
    elif dist_thumb2pinky>dist_thresh and dist_thumb2index>dist_thresh \
        and dist_thumb2middle>dist_thresh and dist_thumb2ring>dist_thresh\
        and dist_thumb2pinkymcp>dist_thresh and dist_index2middle>50 and dist_middle2ring>50:
        return 5
    elif dist_thumb2pinky<dist_thresh and dist_thumb2index>dist_thresh \
        and dist_thumb2middle>dist_thresh and dist_thumb2ring<dist_thresh:
        return 2
    elif dist_thumb2pinky<dist_thresh and dist_thumb2index>dist_thresh \
        and dist_thumb2middle<dist_thresh and dist_thumb2ring<dist_thresh:
        return 1
    elif dist_thumb2pinky<dist_thresh and dist_thumb2index<dist_thresh \
        and dist_thumb2middle<dist_thresh and dist_thumb2ring<dist_thresh:
        return 0
    elif dist_thumb2pinky>50 and dist_thumb2index>dist_thresh \
        and dist_thumb2middle>dist_thresh and dist_thumb2ring>dist_thresh\
            and dist_thumb2pinkymcp<dist_thresh:
        return 4
    elif dist_thumb2pinky>100 and dist_index2middle<40 and dist_middle2ring<40:
        return 6
    else:
        return -1