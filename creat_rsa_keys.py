#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate public and private RSA key

Usage:
  creat_rsa_keys.py <file-name-public-key>  <file-name-private-key> [--length=<length>]

Options:
  -h --help                  Show this screen.
  <file-name-public-key>     Path to the public key to save
  <file-name-private-key>    Path to the private key to save
  --length=<length>          Length of the key [default: 2048]
"""

from __future__ import absolute_import

import logging.handlers
import os

from docopt import docopt

from degree import generate_keys

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/creat_rsa_keys.log",
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
generate_keys(args["<file-name-public-key>"], args["<file-name-private-key>"], int(args["--length"]))
