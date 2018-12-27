from .ArduinoHandler import ArduinoHandler
from .ThreadHandler  import ThreadHandler
from collections import deque

plot_buffer = deque(maxlen=1024*4)
arduino_handler = ArduinoHandler.instance(port_name='/dev/ttyACM0',baudrate=115200, qnt_ch=2)
arduino_handler.start_acquisition()

def global_consumer():
    if arduino_handler.data_waiting:
        _value = arduino_handler.buffer_acquisition.popleft()
        plot_buffer.append(_value)


thread_buffer = ThreadHandler(worker=global_consumer)
thread_buffer.start()

