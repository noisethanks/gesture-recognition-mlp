import numpy

palmVertex = [
    [0,1],
    [0,5],
    [0,9],
    [0,13],
    [0,17]
]
palmBox = [
    [1,5],
    [5,9],
    [9,13],
    [13,17],
]
thumbToIndex = [
    [2,6],
    [3,7],
    [4,8]
]
indexToMiddle = [
    [6,10],
    [7,11],            #   print(predicted)
    [8,12]
]
middleToRing = [
    [10,14],
    [11,15],
    [12,16]
]
ringToPinky = [
    [14,18],
    [15,19],
    [16,20]
]

thumb = [
    [1,2],
    [2,3],
    [3,4],
]
forefinger = [
    [5,6],
    [6,7],
    [7,8],
]

middlefinger = [
    [9,10],
    [10,11],
    [11,12],
]
ringfinger = [
    [13,14],
    [14,15],
    [15,16],
]
pinky = [
    [17,18],
    [18,19],
    [19,20],
]

palm = palmBox+palmVertex
palm = numpy.array(palm)
crossFinger = thumbToIndex + indexToMiddle + middleToRing + ringToPinky
crossFinger = numpy.array(crossFinger)
fingerVertices = thumb+forefinger+middlefinger+ringfinger+pinky
fingerVertices = numpy.array(fingerVertices)
handVectors = numpy.concatenate((palm,crossFinger,fingerVertices))
handVectors= numpy.unique(handVectors,axis=0)
def getHandLandmarkPairs() -> numpy.ndarray:
    return handVectors

palmLandmarks = [0,1,5,9,13,17]
thumbLandmarks = [2,3,4]
forefingerLandmarks = [6,7,8]
middlefingerLandmarks = [10,11,12]
ringfingerLandmarks = [14,15,16]
pinkyLandmarks = [18,19,20]
fingersLandmarks = [2,3,4,6,7,8,10,11,12,14,15,16,18,19,20]