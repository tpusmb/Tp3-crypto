#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os

from Crypto.Hash import SHA3_512
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

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


def sign(path_private_key, message):
    key = RSA.import_key(open(path_private_key).read())
    h = SHA3_512.new(message.encode())
    return pkcs1_15.new(key).sign(h)


def verify(path_public_key, message, signature):
    key = RSA.import_key(open(path_public_key).read())
    h = SHA3_512.new(message.encode())
    try:
        pkcs1_15.new(key).verify(h, signature)
        return True
    except Exception as e:
        PYTHON_LOGGER.error("Error verify me signature: {}".format(e))
        return False
