#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
import timeit
import logging.handlers

from degree import sign, generate_degree_image, encode_image, decode_image, verify
from degree.const import COMPANY_NAME

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/degree_generator.log",
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


def sign_degree_generator(path_private_key, player_name, score):
    """

    :param path_private_key:
    :param player_name:
    :param score:
    :return:
    """
    signature = sign(path_private_key, COMPANY_NAME)
    degree_image = generate_degree_image(player_name, score)
    return encode_image(degree_image, str(signature))


def verify_degree(path_private_key, degree_image):
    """

    :param path_private_key:
    :param degree_image:
    :return:
    """
    extract_signature = decode_image(degree_image)
    return verify(path_private_key, COMPANY_NAME, extract_signature)
