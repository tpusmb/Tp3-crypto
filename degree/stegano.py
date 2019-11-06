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

    :param message:
    :return:
    """
    for c in message:
        yield ord(c)


def gcd(x, y):
    """

    :param x:
    :param y:
    :return:
    """
    while y:
        x, y = y, x % y
    return x


def encode_image(img, msg):
    """

    :param img:
    :param msg:
    :return:
    """
    msg_gen = char_generator(msg)
    pattern = gcd(len(img), len(img[0]))
    for i in range(len(img)):
        for j in range(len(img[0])):
            if (i + 1 * j + 1) % pattern == 0:
                try:
                    img[i - 1][j - 1][0] = next(msg_gen)
                except StopIteration:
                    img[i - 1][j - 1][0] = 0
                    return img


def decode_image(img):
    """

    :param img:
    :return:
    """
    pattern = gcd(len(img), len(img[0]))
    message = ''
    for i in range(len(img)):
        for j in range(len(img[0])):
            if (i - 1 * j - 1) % pattern == 0:
                if img[i - 1][j - 1][0] != 0:
                    message = message + chr(img[i - 1][j - 1][0])
                else:
                    return message
