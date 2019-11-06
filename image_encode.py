#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Encode a message into image

Usage:
  image_encode.py <image-path> <message>

Options:
  -h --help            Show this screen.
  <image-path>         Path to the image to add the message on it
  <message>            Message to add
"""

from __future__ import absolute_import

import logging.handlers
import os

from docopt import docopt

from degree import read_image, encode_image, save_image, decode_image

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/image_encode.log",
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
PYTHON_LOGGER.info("Encode the message {} into the image {}".format(args["<message>"],
                                                                    os.path.basename(args["<image-path>"])))
img = read_image(args["<image-path>"])
encode_img = encode_image(img, args["<message>"])
save_image("encode.png", encode_img)
img = read_image("encode.png")
PYTHON_LOGGER.info("Decode message found: {}".format(decode_image(img)))
