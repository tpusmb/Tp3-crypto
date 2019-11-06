#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import os
import timeit
import logging.handlers

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/signature.log",
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

RSA_KEY = RSA.generate(2048)


def generate_private_key():
    """
    Create a file with a new generated private key.
    :return: Nothing
    """
    file_out = open("private_key", "wb")
    file_out.write(RSA_KEY.export_key())


def generate_public_key():
    """
    Create a file with a new generated public key.
    :return: Nothing
    """
    file_out = open("public_key", "wb")
    file_out.write(RSA_KEY.publickey().export_key())


def encrypt(message):
    """
    Create a file that contains the encrypted message.
    :param message: (String) The message to encrypt.
    :return: Nothing
    """
    data = message.encode("utf-8")
    file_out = open("encrypted_message", "wb")

    public_key = RSA.import_key(open("public_key").read())
    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(public_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the message with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)
    [file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]


def decrypt(file_name):
    """
    Decrypt an encrypted message from a file.
    :param file_name: (String) Name of the file.
    :return: (String) The decrypted message.
    """
    file_in = open(file_name, "rb")

    private_key = RSA.import_key(open("private_key").read())

    enc_session_key, nonce, tag, ciphertext = \
        [file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the message with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    return data.decode("utf-8")
