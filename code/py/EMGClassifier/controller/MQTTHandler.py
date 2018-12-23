# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# FEDERAL UNIVERSITY OF UBERLÂNDIA
# FEELT- Faculty of Electrical Engineering
# GRVA - Augumented and Virtual Reality Group
# ------------------------------------------------------------------------------
# Author: Paulo Camargos
# Contact: paulocamargoss@outlook.com
# Class: MQTTHandler
# ------------------------------------------------------------------------------
# Description: Module containing a handler class for the MQTT protocol with
# Python and Mosquitto broker.
# ------------------------------------------------------------------------------
import os
import subprocess
import paho.mqtt.client as mqtt
from time import sleep
# ------------------------------------------------------------------------------


class MQTTHandler():
    def __init__(self, broker='127.0.0.1', client_name='client', topic='topic', port=1883, receive_message_back=False):
        self.broker = broker
        self.client = mqtt.Client(client_name)
        self.topic = topic
        self.receive_message_back = receive_message_back
        self.port = port

        self.setup_callback_methods()

        

    def setup_callback_methods(self):
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnet
        self.client.on_log = self.on_log
        self.client.on_message = self.on_message
        

    def open_mosquitto_broker(self):
        """
        Opens a Mosquitto broker
        """
        print('[INFO] Opening Mosquitto broker...')
        self.mosquitto_broker = os.popen('mosquitto')
        print('[OK] Success! Mosquitto sever running.')

    def close_mosquitto_broker(self):
        code =  self.mosquitto_broker.close()
        print(f'[OK] Finished Mosquitto broker. Code: {code}')
        
    def on_log(self, client, userdata, level, buf):
        print("[OK]: " + buf)

    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
            print("[OK] Connection made with Mosquitton broker")
        else:
            print("[ERROR] Connection NOT made with Mosquitton broker. Code:  ", rc )

    def on_disconnet(self, client, userdata, flags, rc=0):
        print("[OK] Disconnected. Code: ", rc)

    def on_message(self, client,userdata, msg):
        topic=msg.topic
        m_decode=str(msg.payload.decode("utf-8","ignore"))
        print('[OK] Received message') 
        print(f'> Topic: {topic}\n> Message: {m_decode}')

    def publish_message(self, message):
        self.client.publish(self.topic, message)

    def relay_message(self, message=None):
        if message is not None:
            self.connect_client()
            self.publish_message(message=message)            
            self.disconnet_client()
        else:
            print('[ERROR] No messagem to relay')

    def connect_client(self):
        self.client.connect(self.broker,port=self.port)
        # subscribing to topic
        self.client.subscribe(self.topic)
        if self.receive_message_back:
            self.client.loop_start()
            sleep(0.001)

    def disconnet_client(self):
        if self.receive_message_back:
            sleep(0.001)
            self.client.loop_stop()
        self.client.disconnect()

def test():
    mqtt_connection = MQTTHandler(topic='testing',receive_message_back=True)
    mqtt_connection.open_mosquitto_broker()
    mqtt_connection.relay_message("This message will sure be passed on!")
    mqtt_connection.close_mosquitto_broker()


if __name__ == '__main__':
    test()    
