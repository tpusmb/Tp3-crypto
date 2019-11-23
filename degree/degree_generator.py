#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os

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
    Creat a degree with signature into the image to control if the degree is authentic
    :param path_private_key: (string) Path to the private key file
    :param player_name: (string) Name of the player
    :param score: (int) Score of the player
    :return: (ndarray) The degree image
    """
    signature = sign(path_private_key, COMPANY_NAME)
    degree_image = generate_degree_image(player_name, score)
    return encode_image(degree_image, str(signature))


def verify_degree(path_private_key, degree_image):
    """
    Verify if the input degree his authentic
    :param path_private_key: (string) Path to the private key file
    :param degree_image: (ndarray) Image of the degree to verify if his authentic
    :return: (bool) True the degree his authentic False his not authentic
    """
    extract_signature = decode_image(degree_image)
    return verify(path_private_key, COMPANY_NAME, extract_signature)
