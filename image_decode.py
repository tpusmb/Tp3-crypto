#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Extract the message into the input image

Usage:
  image_decode.py <image-path>

Options:
  -h --help            Show this screen.
  <image-path>         Path to the image to extract message
"""

from __future__ import absolute_import

import logging.handlers
import os
from degree import *
from docopt import docopt
from degree import read_image, decode_image

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/image_decode.log",
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
img = read_image(args["<image-path>"])
PYTHON_LOGGER.info("Decode message found: {}".format(decode_image(img)))

encrypt("Oh my god")
print(decrypt("encrypted_message"))

