#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Encode a message into image

Usage:
  generate_degree.py <private-key-path> <output-degree-file-name> <player-name> <player-score>

Options:
  -h --help                   Show this screen.
  <private-key-path>          Path to the private key file
  <output-degree-file-name>   Name of the output degree file name
  <player-name>               Player name
  <player-score>              Score of the player
"""

from __future__ import absolute_import

import logging.handlers
import os

from docopt import docopt

from degree import save_image
from degree.degree_generator import sign_degree_generator

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/generate_degree.log",
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
output_image = sign_degree_generator(args["<private-key-path>"], args["<player-name>"], int(args["<player-score>"]))
save_image("{}.png".format(args["<output-degree-file-name>"]), output_image)
