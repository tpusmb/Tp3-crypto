#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Control if the degree his authentic

Usage:
  degree_verification.py <private-key-path> <degree-image-path>

Options:
  -h --help                   Show this screen.
  <private-key-path>          Path to the private key file
  <degree-image-path>         Name of degree image to do the verification
"""

from __future__ import absolute_import

import logging.handlers
import os

from docopt import docopt

from degree import read_image
from degree import verify_degree

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/degree_verification.log",
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
img = read_image(args["<degree-image-path>"])
verification_message = "authentic" if verify_degree(args["<private-key-path>"], img) else "not authentic"
PYTHON_LOGGER.info("The input degree {} is {}".format(os.path.basename(args["<degree-image-path>"]),
                                                      verification_message))
