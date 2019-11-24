#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main script to run the degree management web-app.

Usage:
   application.py <port> <private-key-path>

Options:
    -h --help           Show this screen.
    <port>              Port to run the server example 8080
    <private-key-path>  Path to the private key
"""

from __future__ import absolute_import

import logging.handlers
import os

from docopt import docopt
from flask import Flask, render_template, send_file, request
from flask_bootstrap import Bootstrap
from waitress import serve
from werkzeug.utils import secure_filename

from degree import save_image, read_image, sign_degree_generator, verify_degree

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/application.log",
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

app = Flask(__name__)
app.secret_key = "zefzarega5zerg+6e5rzeafz"
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
PRIVATE_KEY_PATH = None


@app.route('/', methods=["GET", "POST"])
def home():
    """
    Display the home page.
    """
    return render_template("index.html")


@app.route("/degree_creator")
def degree_creator():
    """
    Display the degree creation page.
    """
    return render_template("degree_creator.html")


@app.route("/degree_validator")
def degree_validator():
    """
    Display the degree verification page.
    """
    return render_template("degree_validator.html")


@app.route("/download", methods=['GET', 'POST'])
def download():
    """
    Download a degree.
    """
    if request.method == 'POST':
        try:
            player_name = request.form["player_name"]
            player_score = request.form["player_score"]

            if request.form["classic"] is not None:
                output_image = sign_degree_generator(PRIVATE_KEY_PATH, player_name, int(player_score))
                save_image("generated_degree.png", output_image)
            # Neuronal method
            """elif request.form["neuronal"] is not None:
                output_image = 
                save_image("generated_degree.png", output_image)"""
            return send_file("generated_degree.png", as_attachment=True)

        except Exception as e:
            PYTHON_LOGGER.error("error in download: {}".format(e))
            return "Generation failed. Please check your input data."


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    """
    Save a file and check if it is a valid degree.
    """
    if request.method == 'POST':
        try:
            uploaded_file = request.files['uploaded_file']
            file_name = secure_filename(uploaded_file.filename)
            uploaded_file.save(file_name)
            img = read_image(file_name)

            if request.form["classic"] is not None:
                verification_message = "authentic" if verify_degree(PRIVATE_KEY_PATH, img) else "not authentic"
                return "The input degree {} is {}.".format(os.path.basename(file_name), verification_message)
            # Neuronal method
            """elif request.form["neuronal"] is not None:
                verification_message = "authentic" if verify_degree("private_key", img) else "not authentic"
                return "The input degree {} is {}.".format(os.path.basename(file_name), verification_message)"""

        except Exception as e:
            PYTHON_LOGGER.error("error in download: {}".format(e))
            return "Verification failed. Please check your input file."


if __name__ == "__main__":
    args = docopt(__doc__)
    try:
        port = int(args["<port>"])
    except ValueError:
        port = 8080
    PRIVATE_KEY_PATH = args["<private-key-path>"]
    PYTHON_LOGGER.info("Start server to the port {}".format(port))
    serve(app, host="0.0.0.0", port=port)
