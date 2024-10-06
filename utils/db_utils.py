import psycopg
import numpy as np
DATABASE_HOST = "postgresql://postgres:postgres@localhost:5432/"
DATABASE_NAME = "vectors"
DATABASE_URL = DATABASE_HOST + DATABASE_NAME
def lanternConnect(url):
    conn = psycopg.connect(url)
    print("Lantern connected!")
    return conn

def lanternDisconnect(conn):
    conn.close()
    print("Lantern disconnected!")

def createPGVectorArrayTable(conn, tablename,row_size):
    conn.execute("""DROP TABLE IF EXISTS """ + tablename)
    conn.execute("""
        CREATE TABLE """ + tablename + """ (
            id SERIAL PRIMARY KEY,
            gesture TEXT,
            vectors vector(3)["""+
            str(row_size)+
            """]
        )
    """)
    conn.commit()
    print(str(tablename) + " table created!")

def createRealsArrayTable(conn, tablename,row_size):
    conn.execute("""DROP TABLE IF EXISTS """ + tablename)
    conn.execute("""
        CREATE TABLE """ + tablename + """ (
            id SERIAL PRIMARY KEY,
            gesture TEXT,
            landmarks REAL["""+
            str(row_size)+
            """]
        )
    """)
    conn.commit()
    print(str(tablename) + " table created!")

def listToPGArray(gesture_reals)->str:
    return "{" + ",".join([str(x) for x in gesture_reals]) + "}"

def insertRealsArray(conn, tablename, gesture_reals, gesture_name)->None:
    cursor = conn.cursor()
    cursor.execute("""
              INSERT INTO """ + tablename + """ (gesture, landmarks)
              VALUES ('""" + gesture_name + """', '""" + listToPGArray(gesture_reals) + """')
            """)
    conn.commit()

def gestureVectorsToPGVectorArray(gesture_vectors)->str:
    vectors_string = ""
    for vector in gesture_vectors:
        vectors_string += "'[" + ','.join([str(x) for x in vector])  + "]'::vector(3),"
    vectors_string = vectors_string[:-1]
    return vectors_string

def insertGesture(conn, tablename, gesture_vectors, gesture_name)->None:
    cursor = conn.cursor()
    vectors_string = gestureVectorsToPGVectorArray(gesture_vectors)
    cursor.execute("""
                INSERT INTO """ + tablename + """ (gesture, vectors)
                VALUES ('""" + gesture_name + """', ARRAY[""" + vectors_string + """])
            """)
    conn.commit()

def getData(conn, tablename)->list[list[str,np.ndarray]]:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT gesture,vectors FROM """ + tablename
    )
    hands = cursor.fetchall()
    handsList = []
    for hand in hands:
        gesture_name = hand[0]
        vectorsstring = hand[1].replace("{","").replace("}","").replace('[', '').replace(']', '').replace('"', '')
        components = np.fromstring(vectorsstring, sep=',')
        componentslength = int(len(components)/3)
        array = components.reshape(componentslength,3)
        handsList.append([gesture_name, array])
    return handsList

def getRandomGesture(conn, tablename)->list[list[str,np.ndarray]]:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT gesture,vectors FROM """ + tablename + """ ORDER BY random() LIMIT 1"""
    )
    hands = cursor.fetchall()
    handsList = []
    for hand in hands:
        gesture_name = hand[0]
        vectorsstring = hand[1].replace("{","").replace("}","").replace('[', '').replace(']', '').replace('"', '')
        components = np.fromstring(vectorsstring, sep=',')
        componentslength = int(len(components)/3)
        array = components.reshape(componentslength,3)
        handsList.append([gesture_name, array])
    return handsList

def createAndLoadTable(conn, tablename, vectors)->None:
    createPGVectorArrayTable(conn, tablename,len(vectors[vectors.keys().__iter__().__next__()][0]))
    for gesture_name, gestures in vectors.items():
      for gesture_vectors in gestures:
        insertGesture(conn, tablename, gesture_vectors,gesture_name)
    print(str(len(getData(conn,tablename))) + ' vectors inserted!')