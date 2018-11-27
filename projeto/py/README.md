# Install

## Libs and virtual environment

1. Anaconda 3.6 or greater
1. Create the environment

    `$ conda create -n inbio python=3.6 numpy scipy matplotlib pyserial pyqtgraph pandas scikit-learn`

1. Activate the environment

    `$ conda activate inbio` **or** `$ activate inbio` 

1. Install Paho Mqtt client for Python

    - If you're using a proxy
        
        `$ pip install --proxy proxy.ufu.br paho-mqtt`
    
    - Else
        
        `$ pip install paho-mqtt`

1. Ensure those packages were installed in your virtual environment

    `$ conda list`

## Installing the Mosquitto