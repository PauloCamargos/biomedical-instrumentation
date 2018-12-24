from ArduinoHandler import ArduinoHandler
from queue import Queue
from ThreadHandler import ThreadHandler
from collections import deque # testando este novo tipo de dado

my_arduino_handler = ArduinoHandler(port_name="COM3",baudrate=115200, qnt_ch=1)
my_arduino_handler.start_acquisition()
limit_size = 500
buffer_svm = deque(maxlen=limit_size) 
buffer_plotter = deque(maxlen=limit_size) 
    

def consumer_data():
    #global my_arduino_handler
    if my_arduino_handler.buffer_acquisition:
        _val = my_arduino_handler.buffer_acquisition.get()
        print(f"Valor atual: {_val}")
        buffer_svm.append(_val) 
        buffer_plotter.append(_val)
    if buffer_plotter.count() > limit_size -1:
        # buffer_plotter.get()
        print(f"[INFO] Buffer plotter estourando: {buffer_plotter.count()}")
    if buffer_svm.count() > limit_size -1:
        # buffer_svm.get()    
        print(f"[INFO] Buffer SVM estourando: {buffer_svm.count()}")



consumer_thr = ThreadHandler(consumer_data)
consumer_thr.start()