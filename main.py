import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random


cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
Score = [0,0] # [Ai,user]



while True:
    imgBg = cv2.imread("resources/BG.png")

    success , img = cap.read()

    imgScaled = cv2.resize(img,(0,0),None,0.875,0.875)
    imgScaled = imgScaled[:,80:480]

    # recognize a hand for playing
    hands, img = detector.findHands(imgScaled)

    if startGame:

        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBg,str(int(timer)),(605,435),cv2.FONT_HERSHEY_PLAIN,6,(255,0,255),4)

            if timer>3:
                stateResult = True
                timer = 0

                if hands:
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    #  Rock hand moving
                    if fingers == [0,0,0,0,0]:
                        Player_Moving = 1

                    # Paper hand moving
                    if fingers == [1, 1, 1, 1, 1]:
                        Player_Moving = 2

                    # scissors hand moving
                    if fingers == [0,1,1,0,0]:
                        Player_Moving = 3

                    RandomNumber = random.randint(1,3)
                    ImgAi = cv2.imread(f"resources/{RandomNumber}.png",cv2.IMREAD_UNCHANGED)
                    imgBg = cvzone.overlayPNG(imgBg,ImgAi,(149,310))

                    # User wins
                    if (Player_Moving == 1 and RandomNumber == 2) or \
                        (Player_Moving == 2 and RandomNumber == 3) or \
                        (Player_Moving == 3 and RandomNumber == 1):
                        Score[0] +=1

                        # Artificial intelligence player wins
                    if (Player_Moving == 1 and RandomNumber == 3) or \
                        (Player_Moving == 2 and RandomNumber == 1) or \
                        (Player_Moving == 3 and RandomNumber == 2):
                        Score[1] += 1


    imgBg[234:654,795:1195] = imgScaled
    if stateResult:
        imgBg = cvzone.overlayPNG(imgBg, ImgAi, (149, 310))


    cv2.putText(imgBg, str(Score[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBg, str(Score[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    #cv2.imshow("image",img)
    cv2.imshow("BG",imgBg)
    #cv2.imshow("scaled",imgScaled)
    key = cv2.waitKey(1)
    if key == ord('A'):
        startGame = True
        initialTime =  time.time()
        stateResult = False