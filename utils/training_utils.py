from utils.landmarks_utils import *
from utils.db_utils import *
def rotateHandX(vectors, angle:float):
    # Rotate all unit vectors around the x-axis by the given angle
    rotated_vectors = []
    rotation_matrix = np.array([[1, 0, 0],
                                    [0, np.cos(angle), -np.sin(angle)],
                                    [0, np.sin(angle), np.cos(angle)]])
    for vector in vectors:
        rotated_vector = np.dot(rotation_matrix, vector)
        rotated_vectors.append(rotated_vector)
    
    return np.array(rotated_vectors)
def rotateHandY(vectors, angle:float):
    # Rotate all unit vectors around the y-axis by the given angle
    rotated_vectors = []
    rotation_matrix = np.array([[np.cos(angle), 0, np.sin(angle)],
                                    [0, 1, 0],
                                    [-np.sin(angle), 0, np.cos(angle)]])
    for vector in vectors:
        rotated_vector = np.dot(rotation_matrix, vector)
        rotated_vectors.append(rotated_vector)
    
    return np.array(rotated_vectors)
def rotateHandZ(vectors, angle:float):
    # Rotate all unit vectors around the z-axis by the given angle
    rotated_vectors = []
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle), 0],
                                    [np.sin(angle), np.cos(angle), 0],
                                    [0, 0, 1]])
    for vector in vectors:
        rotated_vector = np.dot(rotation_matrix, vector)
        rotated_vectors.append(rotated_vector)
    
    return np.array(rotated_vectors)
def applyRandomRotations(vectors, angle:float, rotations=1):
    transformations = [rotateHandX, rotateHandY, rotateHandZ]
    for i in range(rotations):
        angle = angle * np.random.uniform(0.3, 1.0)
        transformation = np.random.choice(transformations)
        vectors = transformation(vectors, angle)
    return vectors

def generateSyntheticLandmarks(conn)-> np.ndarray:
    unCategorizedHand0 = getRandomGesture(conn,"uncategorizedBoundingBoxedLandmarks")
    unCategorizedHand1 = getRandomGesture(conn,"uncategorizedBoundingBoxedLandmarks")
    categorizedHand0 = getRandomGesture(conn,"boundingboxedlandmarks")
    hands = [unCategorizedHand0,unCategorizedHand1]
    randomHand0 = hands[np.random.randint(0,len(hands))][0]
    randomHand1 = hands[np.random.randint(0,len(hands))][0]
    syntheticHand = []
    for i in range(21):
        if(i in palmLandmarks):
            syntheticHand.append([randomHand0[1][i][0],randomHand0[1][i][1],randomHand0[1][i][2]])
        elif(i in fingersLandmarks):
            syntheticHand.append([randomHand1[1][i][0],randomHand1[1][i][1],randomHand1[1][i][2]])
    return syntheticHand

def generateSyntheticUnitVectors(conn)-> np.ndarray:
    syntheticLandmarks = generateSyntheticLandmarks(conn)
    unit_vectors = []
    landmarkPairs = getHandLandmarkPairs()
    for pair in landmarkPairs:
        unit_vectors.append(calculateUnitVector(syntheticLandmarks[pair[0]], syntheticLandmarks[pair[1]]))
    unit_vectors = np.array(unit_vectors)
    return unit_vectors