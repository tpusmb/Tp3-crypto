#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creat a water mark template

Usage:
  water_mark_generator.py <path-to-water-mark>

Options:
  -h --help                   Show this screen.
  <path-to-water-mark>        Path to the image water mark
"""

from __future__ import absolute_import

import logging.handlers
import os
from docopt import docopt

from degree import read_image, save_image
from degree.deep_water_mark import DeepWaterMark
import cv2

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/test_deep.log",
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

args = docopt(__doc__)
deep_water_mark = DeepWaterMark()
# deep_water_mark.creat_water_mark(read_image(args["<path-to-water-mark>"]))
#
template = read_image("water_mark_template.jpg")
#
# hiden = deep_water_mark.creat_image_with_water_mark(template, read_image("generated_degree.png"))
#
# save_image("hiden.jpg", cv2.resize(hiden, (486, 686)))

print(deep_water_mark.verify_image(template, read_image("hiden.jpg")))
