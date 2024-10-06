import torch
import numpy as np
from utils.vector_vertices import *
from utils.db_utils import *
import psycopg

def calculateUnitVector(p1, p2) -> np.ndarray:
    # Calculate the vector between p1 and p2
    vector = np.array([p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]])
    # Calculate the magnitude of the vector
    magnitude = np.linalg.norm(vector)
    # Normalize the vector to unit length
    if magnitude > 0:
        unit_vector = vector / magnitude
    else:
        unit_vector = np.zeros_like(vector)  # Avoid division by zero
    return unit_vector

def unitVectorNormalization(landmarks)-> np.ndarray:
    unit_vectors = []
    landmarkPairs = getHandLandmarkPairs()
    landmarks = boundingBoxNormalization(landmarks)
    for pair in landmarkPairs:
        unit_vectors.append(calculateUnitVector(landmarks[pair[0]], landmarks[pair[1]]))
    unit_vectors = np.array(unit_vectors)
    return unit_vectors

def noLandmarkNormalization(landmarks)-> np.ndarray:
    return np.array([[lm.x, lm.y, lm.z] for lm in landmarks],dtype=np.float64)

def minMaxNormalization(landmarks)-> np.ndarray:
    landmarks = np.array([[lm.x, lm.y, lm.z] for lm in landmarks],dtype=np.float64)
    min_vals = np.min(landmarks, axis=0)
    max_vals = np.max(landmarks, axis=0)
    range_vals = max_vals - min_vals
    range_vals[range_vals == 0] = 1
    np_landmarks = (landmarks - min_vals) / range_vals
    return np_landmarks

def boundingBoxNormalization(landmarks)-> np.ndarray:
    landmarks = np.array([[lm.x, lm.y, lm.z] for lm in landmarks],dtype=np.float64)
    min_vals = np.min(landmarks, axis=0)
    max_vals = np.max(landmarks, axis=0)
    center = (max_vals + min_vals) / 2
    bbox_size = max_vals - min_vals
    bbox_size[bbox_size == 0] = 1
    np_landmarks = (landmarks - center) / bbox_size
    return np_landmarks

