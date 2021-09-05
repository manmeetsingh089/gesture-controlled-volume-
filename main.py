import cv2
import mediapipe as mp
from math import hypot
import numpy as np

cap = cv2.VideoCapture(0)


#########pycaw#########
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volrange = volume.GetVolumeRange()

min_vol = volrange[0]
max_vol = volrange[1]

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    _, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)
    lmlist = []
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx,cy)
                lmlist.append([cx, cy])

                if id == 4 or id == 8:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                # if id == 8:
                #   cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    if len(lmlist) != 0:
        x1,y1=lmlist[4][0],lmlist[4][1]
        x2, y2 = lmlist[8][0], lmlist[8][1]
        length = hypot(x1-x2 , y1-y2 )
        #print(length)
        cv2.line(img, lmlist[4], lmlist[8], (0, 0, 255), 5)
        vol = np.interp(length,[17,170],[min_vol,max_vol])
        volume.SetMasterVolumeLevel(vol, None)



    cv2.imshow("image", img)
    key = cv2.waitKey(1)
    if key == 27:
        break