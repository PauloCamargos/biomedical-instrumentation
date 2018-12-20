# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# FEDERAL UNIVERSITY OF UBERLANDIA
# Faculty of Electrical Engineering
# Biomedical Engineering Lab
# ------------------------------------------------------------------------------
# Author: Italo Gustavo Sampaio Fernandes
# Contact: italogsfernandes@gmail.com
# Git: www.github.com/italogsfernandes
# Modified: Paulo Camargos
# ------------------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------------------
import serial
import serial.tools.list_ports as serial_tools
from ctypes import c_short
from ThreadHandler import ThreadHandler, InfiniteTimer
import sys
from queue import Queue
import time


class ArduinoHandler:
    """
    This class handles all the communication with a arduino board.

    It has a serialPort Object, a Buffer and a Thread for acquisition.
    Parameters
    ----------
    port_name : String containing the name of the serial port.
                Examples are: 'COM3', 'COM4', '/dev/ttyACM0'
                If it's not set, a compatible port will be searched.
    baudrate : The speed of the communication, in bits per second.
                As the communications is an asynchronous one, it should be
                set here the same of is in the arduino code.
    Examples
    --------
    See the code of the test function in this file for two command line examples.
    """
    def __init__(self, port_name=None, baudrate=115200, qnt_ch=1):
        self.PACKET_SIZE = 4
        self.PACKET_START = '$'
        self.PACKET_END = '\n'
        self.qnt_ch = qnt_ch
        self.serialPort = serial.Serial(port_name,baudrate)
        self.thread_acquisition = ThreadHandler(self.acquire_routine, self.close)
        self.buffer_acquisition = Queue(1024*4)

    @property
    def data_waiting(self):
        """
        The size of the acquisition buffer
        """
        return self.buffer_acquisition.qsize()

    def open(self):
        """
        If it is not already open, it will open the serial port and flush its buffers.
        """
        if not self.serialPort.isOpen():
            self.serialPort.open()
            self.serialPort.flushInput()
            self.serialPort.flushOutput()

    def close(self):
        """
        If the serial port is open, this method will try to close it.
        """
        if self.serialPort.isOpen():
            self.serialPort.close()

    def start_acquisition(self):
        """
        Opens the serial port and starts a thread for acquisition.
        The read objects will be in the buffer_acquisition.
        """
        self.open()
        self.thread_acquisition.start()

    def stop_acquisition(self):
        """
        Let the thread for acquisition reaches its end and, when it finally happens,
        closes the serial port.
        """
        self.thread_acquisition.stop()


    @staticmethod
    def to_int16(msb_byte, lsb_byte):
        """
        Concatenate two bytes(8 bits) into a word(16 bits).

        It will shift the msb_byte by 8 places to the right,
        then it will sum the result with the lsb_byte.

        :param msb_byte: The most significant byte.
        :param lsb_byte: The less significant byte.
        :return: The word created by the two bytes.
        """
        return c_short((msb_byte << 8) + lsb_byte).value

    def acquire_routine(self):
        """
        This routine is automatically called by the acquisition thread.
        Do not call this by yourself.

        Description
        -----------
        If the serial port is open and there is more than the size of one
        packet in the buffer. It will:
             - verify the starter byte;
             - read the data in the packet;
             - verify the end byte;
             - Put the read packet in a buffer (Queue).
        """
        if self.serialPort.isOpen():
            print('Porta aberta')
            if self.serialPort.inWaiting() >= self.PACKET_SIZE:
                print('Tamanho do pacote valido: ', self.serialPort.inWaiting())
                _starter_byte = self.serialPort.read()
                print('Byte de entrada reconhecido: ', _starter_byte)
                if chr(ord(_starter_byte)) == self.PACKET_START:
                    if self.qnt_ch == 1:
                        _msb = self.serialPort.read()
                        _lsb = self.serialPort.read()
                        _msb = ord(_msb)
                        _lsb = ord(_lsb)
                        _value_to_put = ArduinoHandler.to_int16(_msb, _lsb)
                    else:
                        _value_to_put = []
                        for n in range(self.qnt_ch):
                            _msb = self.serialPort.read()
                            _lsb = self.serialPort.read()
                            _msb = ord(_msb)
                            _lsb = ord(_lsb)
                            _value_to_put.append(ArduinoHandler.to_int16(_msb, _lsb))
                    _end_byte = self.serialPort.read()
                    if chr(ord(_end_byte)) == self.PACKET_END:
                        self.buffer_acquisition.put(_value_to_put)


    def get_buffers_status(self, separator):
        """
        Returns a string like:
            Serial:    4/1024 - Buffer:    1/1024
        :param separator: Separates the strings, example ' - ', ' | ', '\n'
        :return: A string containing the status of all the buffers involved in the acquisition
        """
        return "Serial: %4d" % (self.serialPort.inWaiting()/4 if self.serialPort.isOpen() else 0) + '/' + str(4096/4) +\
               separator + "Acq: %4d" % (self.buffer_acquisition.qsize()) + '/' + str(self.buffer_acquisition.maxsize)


def test():
    my_arduino_handler = ArduinoHandler(port_name='COM3', baudrate=115200,qnt_ch=1)

    def printer():
        time.sleep(0.5)
        if my_arduino_handler.data_waiting:
            print("Dado lido: ")
            print(my_arduino_handler.buffer_acquisition.get())
            # time.sleep(0.01) # Uncomment if you want to see the buffer_acquisition to get full

    consumer_thr = ThreadHandler(printer)

    try:
        while True:
            print('s - start Aquisition')
            print('k - kill Aquisition')
            print('-------------------------------')

            str_key = input()

            if 's' in str_key:
                print("Iniciando acq.")
                consumer_thr.start()
                my_arduino_handler.start_acquisition()
                break
            elif 'k' in str_key:
                print("Finalizando acq.")
                my_arduino_handler.stop_acquisition()
                consumer_thr.stop()
            else:
                exit()
    except:
        print('nao deu')


    

if __name__ == '__main__':
    test()
