import cv2
import pickle
import cvzone
import numpy as np

# Video feed
#cap = cv2.VideoCapture('carPark.mp4')
cap = cv2.VideoCapture('5587732-uhd_3700_2082_30fps.mp4')



with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

#width, height = 107, 48
width, height = 40, 20


def checkParkingSpace(imgPro):
    spaceCounter = 0
    fullCounter = 0

    for pos in posList:
        x, y = pos

        imgCrop = imgPro[y:y + height, x:x + width]
        # cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop)


        #if count < 900:
        if count < 185:
            color = (0, 255, 0)
            thickness = 2
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 1
            fullCounter +=1

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        #cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1, thickness=1, offset=0, colorR=color)

    #cvzone.putTextRect(img, f'Available: {spaceCounter}', (100, 50), scale=2, thickness=2, offset=10, colorR=(0,200,0))
    cvzone.putTextRect(img, f'Total: {len(posList)}', (700, 50), scale=1, thickness=1, offset=5, colorR=(10, 52, 122))
    cv2.putText(img, f"Available: {spaceCounter} spots" , (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(img, f"parked: {fullCounter} spots" , (50, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

success = True
while success:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    img = cv2.resize(img, ((1100,720)))
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)
    
    #cv2.imshow("ImageBlur", imgBlur)
    cv2.imshow("ImageThres", imgMedian)
    cv2.imshow("Image", img)
    cv2.waitKey(10)

cv2.destroyAllWindows()
cap.release()