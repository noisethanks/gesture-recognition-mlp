import cv2
import os
import mediapipe as mp
import numpy as np

# Process a single hand. Returns a vector of size depending on function passed in.
def processHand(hand_landmarks,f)->np.ndarray:
    vector = f(hand_landmarks)
    return vector

# Handle a single image. returns a vector of size 1 or 2 depending on number of hands detected.
def processImage(image_path,hands,f)->np.ndarray:
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Process the image and detect hands.
    results = hands.process(image_rgb)
    # If hands are detected, pass each hand landmark to processHand function.
    handsVectors = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            handsVectors.append(processHand(hand_landmarks.landmark,f))
    np_handsVectors = np.array(handsVectors)
    return np_handsVectors
# Iterate through all images in the folder. Returns list of size equal to number of hands detected.
def processImageFolder(images_path,f)->np.ndarray:
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)
    handsVectors = []
    for filename in os.listdir(images_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):  # You can add more image formats if needed
            image_path = os.path.join(images_path, filename)
            handsVectors.extend(processImage(image_path, hands,f))
    hands.close()
    cv2.destroyAllWindows()
    np_handsVectors = np.array(handsVectors)
    return np_handsVectors

# Iterate through all folders in the captures folder. returns list of size equal to number of folders.
def processCapturesFolder(f,photos_path)->dict[str,np.ndarray]:
    vectors = {}
    for folder in os.listdir(photos_path):
        if os.path.isdir(os.path.join(photos_path, folder)):
            gestureVectors = processImageFolder(os.path.join(photos_path, folder),f)
            vectors.update({folder:gestureVectors})
    return vectors


