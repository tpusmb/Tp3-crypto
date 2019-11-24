#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os

import cv2

from .const import COMPANY_NAME, DEGREE_TEMPLATE_PATH

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/utils.log",
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


def read_image(image_path):
    """
    Read an image
    :param image_path: (string) path to the image
    :return: (ndarray) opencv BGR image
    """
    return cv2.imread(image_path)


def save_image(image_path, image):
    """
    Save an input opencv image
    :param image_path: (string) path to the image
    :param image: (ndarray) opencv BGR image
    :return: (bool) True save was success
    """
    try:
        cv2.imwrite(image_path, image)
        return True
    except Exception as e:
        PYTHON_LOGGER.error("Error to save image: {}".format(e))
        return False


def generate_degree_image(player_name, player_score):
    """
    Create the diploma from a template.
    :param player_name: (String) The player's name.
    :param player_score: (String) The player's score.
    :return: (ndarray) generate image
    """
    template = read_image(DEGREE_TEMPLATE_PATH)
    # Adding player's name
    add_text_to_image(template, player_name, 210, 88, 1.8)

    # Adding description
    add_text_to_image(template, "Congratz!", 100, 660, 2)
    add_text_to_image(template, "Now you're a true MLG membre!", 100, 720, 1)

    # Adding score
    add_text_to_image(template, "Your score", 450, 930, 1)
    add_text_to_image(template, str(player_score), 470, 1015, 1.5)

    # Adding company
    add_text_to_image(template, COMPANY_NAME, 90, 930, 2.5)

    return template


def add_text_to_image(image, text, x, y, font_size):
    """
    Put a text onto an image.
    :param image: (Image) The image.
    :param text: (String) The text.
    :param x: (Integer) The x position of the text.
    :param y: (Integer) The y position of the text.
    :param font_size: (Float) The size of the text.
    :return: Nothing
    """
    bottom_left_corner_of_text = (x, y)
    font = cv2.FONT_HERSHEY_TRIPLEX
    font_scale = font_size
    font_color = (0, 0, 0)
    line_type = 2

    cv2.putText(image, text, bottom_left_corner_of_text, font, font_scale, font_color, line_type)


def qr_code_reader(image):
    qrDecoder = cv2.QRCodeDetector()

    # Detect and decode the qrcode
    data, bbox, rectifiedImage = qrDecoder.detectAndDecode(image)
    if len(data) > 0:
        return data
    else:
        return None
