import psycopg2
import os
#from boto.s3.connection import S3Connection


def getDatatbase():
    try:
        # sse = S3Connection(os.environ['DB_NAME'], os.environ['DB_USER'], os.environ['DB_PASS'], os.environ['DB_HOST'], os.environ['DB_PORT'], )
        conn = psycopg2.connect(database=os.getenv("DB_NAME"),
                                user=os.getenv("DB_USER"),
                                password=os.getenv("DB_PASS"),
                                host=os.getenv("DB_HOST"),
                                port=os.getenv("DB_PORT"),
                                sslmode='require')
        # conn = psycopg2.connect(database=DB_NAME,
        #                         user=DB_USER,
        #                         password=DB_PASS,
        #                         host=DB_HOST,
        #                         port=DB_PORT)
        print("Database connected successfully")
        if (conn == None):
            print("Error: psycopg2.connect() was unsuccessful in connecting...")
            return None
        return conn

    except Exception as e:
        print("Database not connected successfully")
        print(e)

    try:
        pass
    except Exception as e:
        print("did not create the tables successfully")
        print(e)

def getAllPinData(conn):
    """
    Function that gets all pin data from the pinData table in the database
    @param conn: the database connection
    @return: the data in a json object
    """
    cursor = conn.cursor()
    sql = '''SELECT pinData.imageURL, pinData.name, pinData.isEdible, pinData.location, pinData.harvestDate, noteData.message
            FROM pinData
            LEFT JOIN noteData ON pinData.ID = noteData.pin_id;'''
    cursor.execute(sql)
    pinData = cursor.fetchall()
    label = ["imageURL", "name", "isEdible", "location", "harvestData", "notes"]
    return createJsonObj(label, pinData)

def postPinData(conn,data):
    """
    Function to post imageURL, name, isEdible, location, harvestDate, and message to the pinData and noteData table
    @param conn: the database connection
    @return: the data in a json object
    """
    cursor = conn.cursor()

    # Sql Statement for Pin
    sqlPin = '''INSERT INTO pinData (imageURL, name, isEdible, location, harvestDate)
                VALUES (%s, %s, %s, %s, NOW()) RETURNING id;'''

    # Sql Statement for Note
    sqlNote = '''INSERT INTO noteData (message, pin_id)
                VALUES (%s, %s);
                '''

    # Adding Pin information to Table
    cursor.execute(sqlPin, (data['imageUrl'], data['name'], data['isEdible'], data['location']))
    new_id = cursor.fetchone()[0]
    conn.commit()

    # Adding note to table
    cursor.execute(sqlNote,(data['note'],new_id))
    conn.commit()

    return 1

    # jsonObj = {}
    # array = []
    # for pin in pinData:
    #     jsonObj["imageURL"] = pin[0]
    #     jsonObj["name"] = pin[1]
    #     jsonObj["isEdible"] = pin[2]
    #     jsonObj["location"] = pin[3]
    #     jsonObj["harvestData"] = pin[4]
    #     jsonObj["notes"] = pin[5]
    #     array.append(jsonObj.copy())
    # print(array)
    # return array

# label = ["imageURL", "name", "isEdible", "location", "harvestData", "notes"]
# data = [
#           ["link","apple",false,"(1,2)",null,"cool"],
#           ["link","orange",false,"(1,2)","2023-04-01T16:48:24.801400",null]
#         ]


def createJsonObj(label, data):
    """
    Creates a generic json object
    @param label: an array of labels corresponding to the order of the data
    @param data: the data fetched from the database
    @return: a structured object to be sent to the frontend
    """
    jsonObj = {}
    array = []
    for subData in data:
        for index, dataVal in enumerate(subData):
            jsonObj[str(label[index])] = dataVal
        array.append(jsonObj.copy())
    return array

