import cv2
import numpy as np
import handtracking as htm
import time
import autopy
import pyautogui
xl,yl=-1,-1
image = cv2.imread('img3.jpg')

wcam, hcam = 660, 500
frv=100#frame reduction value
cap= cv2.VideoCapture(0)
cap.set(3,wcam)#width or wcam,hcam= 660,500
cap.set(4,hcam)#height   cap.set(3,wcam);cap.set(4,hcam)
detector=htm.handDetector(maxHands=1)
wScr,hScr=autopy.screen.size()
pTime = 0
cTime = 0
#mouse location
plocx,plocy=0,0
clocx,clocy=0,0
smooth=6

while True:
    cv2.namedWindow("Display", cv2.WND_PROP_FULLSCREEN)
    cv2.imshow('Display', image)
    success ,img = cap.read()
    #frames per sec
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    #hand detection
    img=detector.findHands(img)#single o/p  to display img and hand detection
    lmList,bbox=detector.findPosition(img)#landmark detection
    # bounded box
    cv2.rectangle(img, (frv, frv), (wcam - frv, hcam - frv), (225, 255, 0), 2)
    #finger up/down
    if len(lmList)!=0:
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]
        fing=detector.fingersUp()
        #only index and mid fing are up
        if fing[1]==1 and fing[2]==0:
            x3=np.interp(x1,(frv,wcam-frv),(0,wScr))
            y3 = np.interp(y1,(frv,hcam-frv),(0,hScr))
            #smoothening mouse movement
            clocx=plocx+(x3-plocx)/smooth
            clocy = plocy + (y3 - plocy) / smooth
            #move mouse
            autopy.mouse.move(wScr-clocx,clocy)
            #detection denotation
            cv2.circle(img,(x1,y1),10,(255,250,20),cv2.FILLED)
            plocx,plocy=clocx,clocy
         #both fing up
        if fing[1] == 1 and fing[2] == 1:
           lbf ,img, lineinfo= detector.findDistance(8,12,img)#distance b/w fingers,displaied in img,line joining fingers
           if lbf<25:
               xl, yl = pyautogui.position()
               cv2.circle(img, (lineinfo[4], lineinfo[5]), 15, (0, 255, 0), cv2.FILLED)
               cv2.circle(image, (lineinfo[3], lineinfo[5]), 5, (255, 0, 0), -1)
               #cv2.circle(image,(pyautogui.position()), 5, (255, 0, 0), -1)
               print(f"Current cursor position: X = {lineinfo[4]}, Y = {lineinfo[5]}")
               print(wScr,hScr)

    cv2.imshow("webcam", img)
    cv2.waitKey(1)