import cv2
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as nd



img = cv2.imread('use/jack-ma3.jpg')
#img_position = cv2.imread('use/jack-ma3.jpg')
#img = cv2.cvtColor(ori_img, cv2.COLOR_BGR2RGB)


nose_cascade = cv2.CascadeClassifier("/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_mcs_nose.xml")
eye_cascade = cv2.CascadeClassifier("/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_eye.xml")
mouth_cascade = cv2.CascadeClassifier("/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_mcs_mouth.xml")
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#eye
eyes = eye_cascade.detectMultiScale(gray,1.3, 12)
if(eyes[0,0] < eyes[1,0]):
    left_eye = eyes[0]
    right_eye = eyes[1]
else:
    left_eye = eyes[1]
    right_eye = eyes[0]

left_eye_img = img[left_eye[1]:left_eye[1]+left_eye[3],left_eye[0]:left_eye[0]+left_eye[2]]
right_eye_img = img[right_eye[1]:right_eye[1]+right_eye[3],right_eye[0]:right_eye[0]+right_eye[2]]
left_eye_img = cv2.morphologyEx(left_eye_img, cv2.MORPH_OPEN, kernel)
right_eye_img = cv2.morphologyEx(right_eye_img, cv2.MORPH_OPEN, kernel)
cv2.imwrite("use/jack-left-eye.jpg",left_eye_img)
cv2.imwrite("use/jack-right-eye.jpg",right_eye_img)


nose = nose_cascade.detectMultiScale(gray,1.3,12)
nose = nose[0]
nose_img = img[nose[1]:nose[1]+nose[3]-5,nose[0]+3:nose[0]+nose[2]+3]
nose_img = cv2.morphologyEx(nose_img, cv2.MORPH_OPEN, kernel)
cv2.imwrite("use/jack-nose.jpg",nose_img)


#mouth
mouth = mouth_cascade.detectMultiScale(gray,1.3,30)
mouth = mouth[1]
mouth_img = img[mouth[1]+6:mouth[1]+mouth[3]-10,mouth[0]:mouth[0]+mouth[2]]
mouth_img = cv2.morphologyEx(mouth_img, cv2.MORPH_OPEN, kernel)
cv2.imwrite("use/jack-mouth.jpg",mouth_img)

# cv2.imshow('img',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
