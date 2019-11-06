# Tp3-crypto

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

To generate private key and public key you need to run this script

    python creat_rasa_keys.py key.pub key.prev

### Test image encoding

    TODO