import cv2
import time
import os
import mediapipe as mp

def keypressCapture(foldername):
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=2 ,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)
    if not os.path.exists('photocaptures/'+foldername):
        os.makedirs('photocaptures/' + foldername)
    cap = cv2.VideoCapture(0)
# Check if the webcam is opened correctly
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()


    while(cap.isOpened()):
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        image.flags.writeable = True
        key = cv2.pollKey()
        if key > 0:
            if key == ord('q'):
                break
            elif key == ord('p'):
                if results.multi_hand_landmarks:
                    start_time = time.time()
                    output_filename = "photocaptures/"+ foldername + "/" +str(int(start_time)) + ".png"
                    cv2.imwrite(output_filename, image)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.imshow('ButtonCapture', image)
        cv2.setWindowProperty("ButtonCapture", cv2.WND_PROP_TOPMOST, 1)
    cap.release()
    cv2.destroyAllWindows()

# keypressCapture('fingerscrossed')

def visualizeHandInCV2(landmarks):
    drawing_utils = mp.solutions.drawing_utils