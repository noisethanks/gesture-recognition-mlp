# import torch
from utils.db_utils import *
from utils.fs_utils import *
from utils.vector_vertices import handVectors
from utils.landmarks_utils import *


photos_path = "photocaptures/"
uncategorized_photos_path = "uncategorized/"

# boundingBoxNormalized = processCapturesFolder(boundingBoxNormalization,photos_path)
# unitVectors = processCapturesFolder(unitVectorNormalization,photos_path)

# boundingBoxNormalizedUncategorized = processCapturesFolder(boundingBoxNormalization,uncategorized_photos_path)  
# unitVectorsUncategorized = processCapturesFolder(unitVectorNormalization,uncategorized_photos_path)

conn = lanternConnect(DATABASE_URL)
# createAndLoadTable(conn,"boundingBoxedLandmarks",boundingBoxNormalized)
# createAndLoadTable(conn,"handUnitVectors",unitVectors)

# createAndLoadTable(conn,"uncategorizedBoundingBoxedLandmarks",boundingBoxNormalizedUncategorized)
# createAndLoadTable(conn,"uncategorizedHandUnitVectors",unitVectorsUncategorized)

lanternDisconnect(conn)