import board
import busio
from hashlib import md5
from digitalio import DigitalInOut
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B
from adafruit_pn532.i2c import PN532_I2C

# The key used to acces the card
key = b'\xFF\xFF\xFF\xFF\xFF\xFF'

# Creating the NFCReader object
i2c = busio.I2C(board.SCL, board.SDA)
pn532 = PN532_I2C(i2c, debug=False)
ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

pn532.SAM_configuration()
print('Waiting for RFID/NFC card to write to!')

while True:
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)
    print('.', end="")
    # Try again if no card is available.
    if uid is not None:
        break

print("")
print('Found card with UID:', [hex(i) for i in uid])

for i in range(64):
    print('Block number' + i + [hex(x) for x in pn532.mifare_classic_read_block(i)])
