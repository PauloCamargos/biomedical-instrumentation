# Description

This folder contains all the files used in the SVM Marchine Learning algorithms, interface (PyQt5) and Unity-Python communication. All the project in this folder was built using **Python 3.6**.

The tutorials preseted here should work both on Linux and Windows with its proper configurations and tweaks. Get in touch by email if you need help. 

# Tools
1. [PyQt5](https://pypi.org/project/PyQt5/)
1. [Anaconda or Miniconda 3](https://conda.io/miniconda.html)
1. [Mosquitto (v. 1.5.4)](https://mosquitto.org/download/)

# Installs
        Obs.: If you're working under an internet proxy, be sure to configure it properly before you download anything.
    

## Configure Anaconda/Miniconda

1. Install Anaconda/Miniconda
1. Create the environment  
    `> conda create -n inbio python=3.6 numpy scipy matplotlib pyserial pyqtgraph pandas scikit-learn` 
1. Activate the environment  
    `> conda activate inbio`  
    **or**  
    `> activate inbio` 

#### Installing the Mqtt for Python

1. Install Paho Mqtt client for Python 
    - If you're using a proxy
        `> pip install --proxy proxy.ufu.br -p 3128 paho-mqtt`
    - Else
        `> pip install paho-mqtt`
1. Ensure all packages were installed in your virtual environment  
    `> conda list`

## Installing the Mosquitto Broker

For Windows 10:

1. Go to [Mosquitto](https://mosquitto.org/download/) website and download the installer.
1. Execute the installer.
1. On the step `Dependencies`, follow the instructions and donwload the ssl certificates required.
1. Follow the remaining steps and finish the Mosquitto installer.
1. Don't forget to copy the .ssl files into the Mosquitto install directory.
1. Put the `mosquitto` install folder in your system path variables.
1. Open a new `cmd` window and execute:  
        `> mosquitto -v`
1. If everything went right, you should see your Mosquitto broker **running and listening on port 1883**.
1. To test the communication with Mqtt, you can run the example at `examples/mqtt_example.py`

# Configuring Mqtt on Unity

**Go to the `unity/README.md` file**

