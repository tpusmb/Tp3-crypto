#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os
from image_match.goldberg import ImageSignature

from degree import DeepStegano, save_image, read_image, image_preparation

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/deep_water_mark.log",
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


class DeepWaterMark:

    DISTANCE_THREALDSHOT = 0.2

    def __init__(self):
        self.deep_stegano = DeepStegano()
        self.deep_stegano.load_model(os.path.join(FOLDER_ABSOLUTE_PATH, "data", "model_1000_epochs"))
        self.gis = ImageSignature()

    def creat_water_mark(self, water_mark_image):
        """

        :param water_mark_image:
        :return:
        """
        cover_image = read_image(os.path.join(FOLDER_ABSOLUTE_PATH,
                                              "data",
                                              "pokemon_card_template.png"))
        covers = image_preparation(cover_image)
        secrets = image_preparation(water_mark_image)

        hiden, reveald = self.deep_stegano.run_model(covers, secrets)
        save_image("water_mark_template.jpg", reveald * 255)

    def creat_image_with_water_mark(self, water_mark_image, degree_image):
        """

        :param water_mark_image:
        :param degree_image:
        :return:
        """
        covers = image_preparation(degree_image)
        secrets = image_preparation(water_mark_image)
        hiden, _ = self.deep_stegano.run_model(covers, secrets)
        return hiden

    def verify_image(self, original_water_mark_template_image, degree_image):
        covers = image_preparation(degree_image)
        reveald = self.deep_stegano.revealed_image(covers)
        save_image("test.jpg", reveald)
        gis = ImageSignature()
        a = gis.generate_signature(original_water_mark_template_image)
        b = gis.generate_signature(reveald)
        return gis.normalized_distance(a, b) < self.DISTANCE_THREALDSHOT
