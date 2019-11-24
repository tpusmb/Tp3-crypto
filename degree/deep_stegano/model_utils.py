#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os
import random

import cv2
import numpy as np

from degree import read_image

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/model_utils.log",
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


def normalize_batch(imgs):
    return (imgs - np.array([0.485, 0.456, 0.406])) / np.array([0.229, 0.224, 0.225])


def denormalize_batch(imgs, should_clip=True):
    imgs = (imgs * np.array([0.229, 0.224, 0.225])) + np.array([0.485, 0.456, 0.406])

    if should_clip:
        imgs = np.clip(imgs, 0, 1)
    return imgs


def image_preparation(image):
    image = np.array(cv2.resize(image, (224, 224)), dtype=np.float32)
    image /= 255
    return normalize_batch(np.array([image]))


def read_image_set(img_secret_path, img_cover_path):
    cover_image = read_image(img_cover_path)
    secret_image = read_image(img_secret_path)
    return image_preparation(cover_image), image_preparation(secret_image)


def get_img_batch(files_list, batch_size=32, should_normalise=True):
    batch_cover = []
    batch_secret = []

    for i in range(batch_size):
        img_secret_path = random.choice(files_list)
        img_cover_path = random.choice(files_list)

        img_secret = cv2.cvtColor(read_image(img_secret_path), cv2.COLOR_BGR2RGB)
        img_cover = cv2.cvtColor(read_image(img_cover_path), cv2.COLOR_BGR2RGB)

        img_secret = np.array(cv2.resize(img_secret, (224, 224)), dtype=np.float32)
        img_cover = np.array(cv2.resize(img_cover, (224, 224)), dtype=np.float32)

        img_secret /= 255.
        img_cover /= 255.

        batch_cover.append(img_cover)
        batch_secret.append(img_secret)

    batch_cover, batch_secret = np.array(batch_cover), np.array(batch_secret)

    if should_normalise:
        batch_cover = normalize_batch(batch_cover)
        batch_secret = normalize_batch(batch_secret)

    return batch_cover, batch_secret
