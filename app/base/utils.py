# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import hashlib
import binascii
import os
import secrets


def hash_pass(password):
    """Hash a password to be stored in the database."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                               salt, 100000)
    hash = binascii.hexlify(hash)
    return salt + hash  # This is a bytes object


def verify_pass(pw_provided, pw_stored):
    """Validate the user-provided password against the one stored in the database."""
    pw_stored = pw_stored.decode('ascii')
    salt = pw_stored[:64]
    pw_stored = pw_stored[64:]
    hash = hashlib.pbkdf2_hmac('sha512',
                               pw_provided.encode('utf-8'),
                               salt.encode('ascii'),
                               100000)
    hash = binascii.hexlify(hash).decode('ascii')
    return hash == pw_stored


def create_api_authentication_token():
    return secrets.token_urlsafe(24)