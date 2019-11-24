#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import binascii
import logging.handlers
import os

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/encryption.log",
                                                 when="midnight", backupCount=60)
STREAM_HDLR = logging.StreamHandler()
FORMATTER = logging.Formatter("%(asctime)s %(filename)s [%(levelname)s] %(message)s")
HDLR.setFormatter(FORMATTER)
STREAM_HDLR.setFormatter(FORMATTER)
PYTHON_LOGGER.addHandler(HDLR)
PYTHON_LOGGER.addHandler(STREAM_HDLR)
PYTHON_LOGGER.setLevel(logging.DEBUG)

# Absolute path to the folder location of this python file
FOLDER_ABSOLUTE_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))


def generate_keys(path_public, path_private, length=2048):
    """
    Create a RSA file with a new generated private key.
    :param path_public: (string) File name to the public key
    :param path_private: (string) File name to the private key
    :param length: (int) Length of the key we recommande 2048
    :return: Nothing
    """
    rsa_key = RSA.generate(length)
    file_out = open(path_private, "wb")
    file_out.write(rsa_key.export_key())
    file_out.close()
    file_out = open(path_public, "wb")
    file_out.write(rsa_key.publickey().export_key())


def encrypt(message, path_public_key):
    """
    encrypt a message
    :param message: (String) The message to encrypt.
    :param path_public_key: (string) File name to the public key
    :return: (string) Encrypt message
    """
    msg = message.encode()
    public_key = RSA.import_key(open(path_public_key).read())
    encryptor = PKCS1_OAEP.new(public_key)
    encrypted = encryptor.encrypt(msg)
    return binascii.hexlify(encrypted).decode()


def decrypt(encrypt_message, path_private_key):
    """
    Decrypt an encrypted message
    :param encrypt_message: (string) Encrypt message generate by encrypt function
    :param path_private_key: (string) File name to the private key
    :return: (String) The decrypted message.
    """
    encrypt_message = binascii.unhexlify(encrypt_message.encode())
    private_key = RSA.import_key(open(path_private_key).read())
    decryptor = PKCS1_OAEP.new(private_key)
    decrypted = decryptor.decrypt(encrypt_message)
    return decrypted.decode()
