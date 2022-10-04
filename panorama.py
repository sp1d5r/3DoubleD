import numpy as np
import cv2
import random


""" INITIALISE VIDEO INPUT STREAMS """
WIDTH = 640
HEIGHT = 480

# Video Streams
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

cap1.set(3, WIDTH)  # set Width
cap1.set(4, HEIGHT)  # set Height
cap2.set(3, WIDTH)
cap2.set(4, HEIGHT)

""" GETTING THE KEYPOINTS """
def get_keypoints(frame):
    sift = cv2.SIFT_create()
    keypoints, features = sift.detectAndCompute(frame, None)

    return keypoints, features


""" MATCHING THE KEYPOINTS """
def match_keypoints(keypoint1, keypoint2):
    matches = []

    return matches


""" RUNNING THE PANORAMA """

while (True):
    _, frame1 = cap1.read()
    _, frame2 = cap2.read()
    # frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
    # frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)

    # Get the keypoints from this image.
    keypoints1, features1 = get_keypoints(frame1)
    keypoints2, features2 = get_keypoints(frame2)

    cv2.drawKeypoints(frame1, keypoints1, frame1)
    cv2.drawKeypoints(frame1, keypoints2, frame1)

    # feature matching
    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

    matches = bf.match(features2, features1)
    matches = sorted(matches, key=lambda x: x.distance)

    frame3 = cv2.drawMatches(frame2, keypoints2, frame1, keypoints1, matches[:50], frame1, flags=2)


    cv2.imshow('matches', frame3)
    # cv2.imshow('Webcam', frame2)
    # cv2.imshow('gray', gray)

    k = cv2.waitKey(30) & 0xff
    if k == 27:  # press 'ESC' to quit
        break

cap1.release()
# cap2.release()
cv2.destroyAllWindows()