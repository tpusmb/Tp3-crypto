#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import glob
import os
import logging.handlers
from degree import DeepStegano, get_img_batch, denormalize_batch
from degree.deep_stegano.const import TRAIN_PATH
import cv2
import matplotlib.pyplot as plt

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

model = "beta_0.75"
files_list = glob.glob(os.path.join(TRAIN_PATH, "*.jpg"))
covers, secrets = get_img_batch(files_list=files_list, batch_size=1)
cover = covers.squeeze()
secret = secrets.squeeze()
plt.imshow(denormalize_batch(cover))
plt.show()
plt.imshow(denormalize_batch(secret))
plt.show()

deep_stegano = DeepStegano()
deep_stegano.load_model("model_1000_epochs", model)
hiden, reveald = deep_stegano.run_model(covers, secrets)

plt.imshow(hiden)
plt.show()
plt.imshow(reveald)
plt.show()
