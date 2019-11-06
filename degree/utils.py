#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
import logging.handlers
import cv2

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

    :param image_path:
    :return: (ndarray) BGR image
    """
    return cv2.imread(image_path)


def save_image(image_path, image):
    """

    :param image_path:
    :param image:
    :return:
    """
    try:
        cv2.imwrite(image_path, image)
        return True
    except Exception as e:
        PYTHON_LOGGER.error("Error to save image: {}".format(e))
        return False