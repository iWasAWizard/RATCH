import binascii
import os

SECRET_KEY = binascii.b2a_hex(os.urandom(8))
