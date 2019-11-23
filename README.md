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

### Creat keys

To generate RSA private key and public key you need to run this script

    python creat_rasa_keys.py key.pub key.prev

### Test image encoding

Now you can test to add an message into a image

    python image_encode.py test-img.jpg "secret message"

You can extract the message by running this command

    python image_decode.py encode.png

### Generate a degree

To generate a degree you need to run this python script

    python generate_degree.py key.prev degree Bob 1000

You can control if the degree his authentic by running this script

    python degree_verification.py key.prev degree.png