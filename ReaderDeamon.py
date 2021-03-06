import board
import busio
import requests
import mysql.connector
from hashlib import md5
from json import dumps
from time import sleep
from digitalio import DigitalInOut
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B
from adafruit_pn532.i2c import PN532_I2C

BLOCK_N = 4 # The number of the block to read
hashedID = ""
# The key used to acces the card
key = b'\xFF\xFF\xFF\xFF\xFF\xFF'

# Connection to the DataBase
mydb = mysql.connector.connect(
  host="localhost",
  user="test",
  passwd="test",
  database="TestBadge"
)
cursor = mydb.cursor()

# Creating the NFCReader object
i2c = busio.I2C(board.SCL, board.SDA)
pn532 = PN532_I2C(i2c, debug=False)
ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

pn532.SAM_configuration()

while True:
    hashedID = ""
    print("Waiting for RFID/NFC card!")
    while True:
        # Check if a card is available to read
        uid = pn532.read_passive_target(timeout=0.5)
        # Try again if no card is available.
        if uid is not None:
            break

    # Begin the reading process
    authenticated = pn532.mifare_classic_authenticate_block(uid, BLOCK_N, MIFARE_CMD_AUTH_B, key) # Authentication process

    if authenticated:
        data = bytearray(16)
        data = ([hex(x) for x in pn532.mifare_classic_read_block(BLOCK_N)])

    # Decoding the userID
    for element in data:
        hashedID += element[2:]

    # Query to the database

    sql = "SELECT userID, userName, userSurname, userRole FROM Utenti WHERE hashedID = %s"
    val = (hashedID,)

    cursor.execute(sql, val)
    result = cursor.fetchone()

    # Creating the json file
    jsonDictionary = {}
    jsonDictionary["userID"] = result[0]
    jsonDictionary["userName"] = result[1]
    jsonDictionary["userSurname"] = result[2]
    jsonDictionary["userRole"] = result[3]

    json = dumps(jsonDictionary)

    # Sending a POST request
    response = requests.post('http://localhost:5000/post_user', json=json)

    print("Json File:", json)
    print("Response: ", response)
    sleep(1)
