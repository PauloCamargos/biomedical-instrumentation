# Description: Custom plot class for pyqtgraph embedded in PyQt Designer
# Author: github.com/PauloCamargos
# Dat: 08/12/2018

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import serial
import time as py_time
from numpy import clip
from pyqtgraph.ptime import time
from queue import Queue
from ArduinoHandler import ArduinoHandler
from ThreadHandler import ThreadHandler
from collections import deque
from threading import Thread 

my_arduino_handler = ArduinoHandler.instance(port_name='COM3', baudrate=115200, qnt_ch=2)
my_arduino_handler.start_acquisition()


class OneInstaceConsumer():
    _buffer_value = None

    @staticmethod
    def consumer():
        print('Consumer called')
        if not OneInstaceConsumer._buffer_value:
            _buffer_value = deque(maxlen=1024)
            
        if my_arduino_handler.data_waiting > 0:
            _buffer_value.append(my_arduino_handler.buffer_acquisition.get())
            py_time.sleep(0.1)
            print(_buffer_value)
        
        if len(_buffer_value) > 5: #_buffer_value.maxlen:
            print('Buffer bloqueado')

        return _buffer_value

# thr_consumer = ThreadHandler(OneInstaceConsumer.consumer)


class CustomPlotEMG(pg.GraphicsWindow):
    """
        Implementing a custom class for the pyqtgraph module. It's meant to be used
        with the PyQt5 Designer. For more information, check out pyqtgraph documentation on 
        "Embedding widgets inside PyQt applications".
    """

    def __init__(s elf, parent=None,whoami=1): 
        pg.GraphicsWindow.__init__(self, parent=None)
        self.whoami = whoami
        self.amount_of_points = 1024*8 
        self.values = deque(maxlen=self.amount_of_points) # [0] * self.amount_of_points 

        self.fps = 0
        self.show_fps = True
        self.lastTime = 0

        pg.setConfigOptions(antialias=True)             # Bordas das curvas
        self.useOpenGL                            # Configurando engine para renderização do gráfico
        pg.setConfigOptions(useOpenGL=True)

        limit = 600 
        self.plot = self.addPlot(title="Sinal EMG")    # Iniciando um plot
        self.plot.setRange(yRange=[-10,1050])                # Limites do gráfico
        self.plot.addLegend()                            # Inserindo lengeda
        # self.plot.showGrid(x = True, y = True, alpha = 0.2)      # Grid para visualização dos valores
        self.plot.setLabel('left', 'Tensão [V]')         # Legenda do eixo y

        if whoami == 1:
            name = 'CH1'
            color = 'r'
        else:
            name = 'CH2'
            color = 'b'

        self.curva = self.plot.plot(pen=pg.mkPen(color=color,width=1),name=name)   # Curva do gráfico

        timer = pg.QtCore.QTimer(self)         # Temporizador da biblioteca 
        timer.timeout.connect(self.update)  
        timer.start(2)   
        self.x = 0
        
    def update(self): # este é o data consumer do pyqtgraph
        """ Updates the data and the graph"""
        # if self.show_fps:
        #     self.calculate_fps()
        #     self.plot.setTitle('<font color="red">%0.2f fps</font>' % self.fps)

        # py_time.sleep(1)
        buffer_plotter =  my_arduino_handler.buffer_acquisition

        # points_to_add = buffer_plotter.qsize()
        points_to_add = len(buffer_plotter)

        if points_to_add > 10:
            for n in range(points_to_add):  # obtains the new value
                # num = buffer_plotter[-1]
                #print("Points to add :", points_to_add)

                if self.whoami == 1:
                    _val = buffer_plotter[-1][0]
                else:
                    _val = buffer_plotter[-1][1]
                    buffer_plotter.pop()

                #print(f"I'm {self.whoami} and val: {_val}")
                self.values.append(_val)
                if len(self.values) > self.amount_of_points: # remove the oldest values
                    self.values.popleft()

            self.x += 1
        self.curva.setData(self.values)
        self.curva.setPos(self.x, 0)

    def calculate_fps(self):
        """
        If defined, it this method is called automatically by the update function.
        Updating the value of the fps attribute.
        """
        now = time()
        dt = now - self.lastTime
        self.lastTime = now
        if self.fps is None:
            self.fps = 1.0 / dt
        else:
            s = clip(dt * 3., 0, 1)
            self.fps = self.fps * (1 - s) + (1.0 / dt) * s


if __name__ == '__main__': # Função iniciando a execução da janela
    w = CustomPlotEMG()
    w.show()
    QtGui.QApplication.instance().exec_()

