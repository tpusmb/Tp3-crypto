#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os

import cv2

from degree import sign, generate_degree_image, encode_image, decode_image, verify, encrypt, decrypt, read_image
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
    encrypted_score = encrypt(str(score), path_private_key)
    return encode_image(degree_image, str(signature) + "," + encrypted_score)


def sign_deep_degree_generator(path_private_key, path_to_water_mark, player_name, score, deep_water_mark):
    """
    Creat a degree with signature into the image to control if the degree is authentic
    :param path_private_key: (string) Path to the private key file
    :param path_to_water_mark: (string) Path to the water mark image
    :param player_name: (string) Name of the player
    :param score: (int) Score of the player
    :param deep_water_mark: (DeepWaterMark) Deep watermark instance
    :return: (ndarray) The degree image
    """
    degree_image = generate_degree_image(player_name, score)
    template = read_image(path_to_water_mark)
    hiden = deep_water_mark.creat_image_with_water_mark(template, degree_image)
    encrypted_score = encrypt(str(score), path_private_key)
    return encode_image(cv2.resize(hiden, (486, 686)), encrypted_score)


def verify_degree(path_private_key, degree_image):
    """
    Verify if the input degree his authentic
    :param path_private_key: (string) Path to the private key file
    :param degree_image: (ndarray) Image of the degree to verify if his authentic
    :return: (tuple bool and int) True the degree his authentic False his not authentic.
        And an interger to say the degree score
    """
    extract_signature, score = decode_image(degree_image).split(',')
    return verify(path_private_key, COMPANY_NAME, extract_signature), decrypt(score, path_private_key)


def verify_deep_degree(path_private_key, deep_water_mark, degree_image):
    """
    Verify if the input degree his authentic
    :param path_private_key: (string) Path to the private key file
    :param deep_water_mark: (DeepWaterMark) Deep watermark instance
    :param degree_image: (ndarray) Image of the degree to verify if his authentic
    :return: (tuple bool and int) True the degree his authentic False his not authentic.
        And an interger to say the degree score
    """
    template = read_image("water_mark_template.jpg")
    score = decode_image(degree_image)
    return deep_water_mark.verify_image(template, degree_image), decrypt(score, path_private_key)