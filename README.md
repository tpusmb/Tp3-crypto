# Tp3-crypto

BLANC Swan & LE BRAS Clément

## Apt to install

You will need the following package:
    
    sudo apt install python3
    sudo apt install virtualenv
    sudo apt install python3-pip
    sudo apt install python3-tk
    sudo apt install cmake

## Python env preparation

Prepare your virtualenv:

    virtualenv -p python3 venv
    . venv/bin/activate

install all requirements

    pip install -r requirements.txt  

If you want to exit your virtualenv:

    deactivate

## Quick start

This project implement 2 way to control if the degree his authentic.

* classic method: We use RSA to creat a signature and a stegano technique to add the signature into the degree image.
* Neuronal method: We train a neural network to fusion 2 image. In or case we take a water mark. Hide into the degree.
Then to control if his authentic. The neural network can extract water mark in the image. 
Then we apply an image match between the original water mark.


### Creat keys

To generate RSA private key and public key you need to run this script

    python creat_rasa_keys.py key.pub key.prev

### Start the web interface

To test the project you can run the flask web interface.

    python application.py 8080 key.prev mona_lisa_water.jpg

### Test image encoding (classic method)

Now you can test to add an message into a image

    python image_encode.py test-img.jpg "secret message"

You can extract the message by running this command

    python image_decode.py encode.png

### Generate a degree (classic method)

To generate a degree you need to run this python script

    python generate_degree.py key.prev degree Bob 1000

You can control if the degree his authentic by running this script

    python degree_verification.py key.prev degree.png


## Project struct

* `application.py`: Web interface
* `degree`: Main package
    * `degree/deep_stegano`: Package with the neural network model.
    * `degree/data`: All data for the project
    * `degree/deep_water_mark.py`: Main script to user the deep Stagano model
    * `degree/degree_generator.py`: Script to generate degree (classic method, Neuronal method)
    * `degree/encryption.py`: RSA encryption
    * `degree/signature.py`: RSA signature
    * `degree/stegano.py`: Simple steganographie technique