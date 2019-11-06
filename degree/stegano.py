#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/stegano.log",
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


def char_generator(message):
    """
    Generator to parse the message. On each char transform into 8 byte parse each byte
    :param message: (string) Message to parse
    """
    for c in message:
        for str_byte in '{0:08b}'.format(ord(c)):
            yield int(str_byte)


def bytes_to_char(bytes_str):
    """
    Transform a bytes
    :param bytes_str:
    :return:
    """
    return chr(int(bytes_str, 2))


def encode_image(img, msg):
    """
    Encode a message into image
    :param img: (ndarray) image to add the message
    :param msg: (string) message to add
    :return: (ndarray) image with encode message
    """
    msg_gen = char_generator(msg)
    for i in range(len(img)):
        for j in range(len(img[0])):
            try:
                img[i - 1][j - 1][0] &= 0b11111110
                img[i - 1][j - 1][0] |= next(msg_gen)
            except StopIteration:
                img[i - 1][j - 1][0] = 0
                return img


def decode_image(img):
    """
    Extract the message into the input image
    :param img: (ndarray) image to extract the message
    :return: (string) Extract message. None if no message was found
    """
    message = ''
    byt_acc = ''
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i - 1][j - 1][0] != 0:
                byt_acc += str((img[i - 1][j - 1][0] >> 0) & 1)
                if len(byt_acc) == 8:
                    message += bytes_to_char(byt_acc)
                    byt_acc = ''
            else:
                return message
