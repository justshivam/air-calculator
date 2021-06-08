from HandTrackingModule import handDetector as hd
import numpy as np
import cv2


def countFingersInHand(hand):
    x = 0
    tips = [20, 16, 12, 8]
    anchors = [19, 15, 11, 7]
    for i in range(4):
        if hand[tips[i]][2] <= hand[anchors[i]][2] and hand[tips[i]][2] <= hand[anchors[i]+1][2]:
            x += 1
    if hand[17][1] < hand[4][1]:
        if hand[4][1] >= hand[5][1]:
            x += 1
    else:
        if hand[4][1] <= hand[5][1]:
            x += 1
    return x


def fingers(img):
    count = 0
    for i in range(detector.numberOfHands()):
        lmList = detector.findPosition(img, draw=False, handNo=i)
        count += countFingersInHand(lmList)
    return count


def getResult():
    if op == 2:
        return num1 + num2
    if op == 4:
        return num1 - num2
    if op == 6:
        return num1 * num2
    if op == 8:
        return num1 / num2


arr = np.zeros(50)
ind = 0
num1, num2, op = None, None, None
fontsize = 1
thickness = 2
stage1, stage2, stage3, stage4 = False, False, False, False
cap = cv2.VideoCapture(0)
detector = hd()

run = True
while run:
    success, img = cap.read()
    img = detector.findHands(img)
    handcount = detector.numberOfHands()
    h, w, c = img.shape
    if not stage1:
        if handcount in [0, 1]:
            cv2.putText(img, "Show Both Hands to Initialise", (10, 20),
                        cv2.FONT_HERSHEY_PLAIN, fontsize, (255, 255, 255), thickness)
        else:
            if ind < 50:
                arr[ind] = handcount
                ind += 1
            else:
                ind = 0
                vals, counts = np.unique(arr, return_counts=True)
                mode_value = vals[np.argmax(counts)]
                if mode_value == 2:
                    stage1 = True
    elif stage1 and not stage2:
        cv2.putText(img, "Show First Number", (10, 20),
                    cv2.FONT_HERSHEY_PLAIN, fontsize, (255, 255, 255), thickness)
        if handcount != 0:
            if ind < 50:
                arr[ind] = fingers(img)
                ind += 1
            else:
                ind = 0
                vals, counts = np.unique(arr, return_counts=True)
                num1 = int(vals[np.argmax(counts)])
                stage2 = True
        else:

            ind = 0
            cv2.putText(img, "NO HANDS DETECTED", (w-200, 20),
                        cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
    elif stage2 and not stage3:
        cv2.putText(img, f'First number is : {num1}', (10, 20),
                    cv2.FONT_HERSHEY_PLAIN, fontsize, (255, 255, 255), thickness)
        cv2.putText(img, "Enter Second Number", (10, 40),
                    cv2.FONT_HERSHEY_PLAIN, fontsize, (255, 255, 255), thickness)
        if handcount != 0:
            if ind < 50:
                arr[ind] = fingers(img)
                ind += 1
            else:
                ind = 0
                vals, counts = np.unique(arr, return_counts=True)
                num2 = int(vals[np.argmax(counts)])
                stage3 = True
        else:
            ind = 0
            cv2.putText(img, "NO HANDS DETECTED", (w-200, 20),
                        cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
    elif stage3 and not stage4:
        cv2.putText(img, f'First number is : {num1}', (10, 20),
                    cv2.FONT_HERSHEY_PLAIN, fontsize, (255, 255, 255), thickness)
        cv2.putText(img, f'Second number is : {num2}', (10, 40),
                    cv2.FONT_HERSHEY_PLAIN, fontsize, (255, 255, 255), thickness)
        cv2.putText(img, f'2 for "+"\n4 for "-"\n6 for "*"\n8 for "/"\n', (10, 60),
                    cv2.FONT_HERSHEY_PLAIN, fontsize, (255, 255, 255), thickness)
        if handcount != 0:
            if ind < 50:
                temp = fingers(img)
                if temp in [2, 4, 6, 8]:
                    arr[ind] = temp
                    ind += 1
                else:
                    ind = 0
                    cv2.putText(img, "INVALID OPTION", (w-200, 20),
                                cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
            else:
                ind = 0
                vals, counts = np.unique(arr, return_counts=True)
                op = int(vals[np.argmax(counts)])
                stage4 = True
        else:
            ind = 0
            cv2.putText(img, "NO HANDS DETECTED", (w-200, 20),
                        cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
    elif stage4:
        cv2.putText(img, f'First number is : {num1}', (10, 20),
                    cv2.FONT_HERSHEY_PLAIN, fontsize, (255, 255, 255), thickness)
        cv2.putText(img, f'Second number is : {num2}', (10, 40),
                    cv2.FONT_HERSHEY_PLAIN, fontsize, (255, 255, 255), thickness)
        cv2.putText(img, f'Result is : {getResult()}', (10, 60),
                    cv2.FONT_HERSHEY_PLAIN, fontsize, (255, 255, 255), thickness)
        cv2.putText(img, "Show Both Hands to Initialise", (10, 80),
                    cv2.FONT_HERSHEY_PLAIN, fontsize, (255, 255, 255), thickness)
        if not handcount in [0, 1]:
            if ind < 50:
                arr[ind] = handcount
                ind += 1
            else:
                ind = 0
                vals, counts = np.unique(arr, return_counts=True)
                mode_value = vals[np.argmax(counts)]
                if mode_value == 2:
                    stage1 = False
                    stage2 = False
                    stage3 = False
                    stage4 = False

    cv2.imshow("Air-Calculator by Shivam", img)
    keypress = cv2.waitKey(1)
    if keypress == ord('q'):
        break
cv2.destroyAllWindows()
