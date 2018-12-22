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

class CustomPlotEMG(pg.GraphicsWindow):
    """
        Implementing a custom class for the pyqtgraph module. It's meant to be used
        with the PyQt5 Designer. For more information, check out pyqtgraph documentation on 
        "Embedding widgets inside PyQt applications".
    """

    def __init__(self, parent=None,): 
        pg.GraphicsWindow.__init__(self, parent=None)
        self.amount_of_points = 1024*20
        self.values_ch1 = deque([0 for x in range(self.amount_of_points)], maxlen=self.amount_of_points) # [0] * self.amount_of_points 
        self.values_ch2 = deque([0 for x in range(self.amount_of_points)], maxlen=self.amount_of_points) # [0] * self.amount_of_points 
        self.x_tick = deque([0 for x in range(self.amount_of_points)], maxlen=self.amount_of_points)

        self.fps = 0
        self.show_fps = True
        self.lastTime = 0

        pg.setConfigOptions(antialias=True)             # Bordas das curvas
        self.useOpenGL                            # Configurando engine para renderização do gráfico
        pg.setConfigOptions(useOpenGL=True)
        pg.setConfigOption('background', 'w')

        limit = [-10, 1100]
        
        self.plot_ch1 = self.addPlot(title="CH1", row=1, col=1)    # Iniciando um plot
        self.plot_ch2 = self.addPlot(title="CH2", row=2, col=1)
        
        self.plot_ch1.setRange(yRange=limit)                # Limites do gráfico
        self.plot_ch2.setRange(yRange=limit)                # Limites do gráfico

        self.plot_ch1.addLegend()                            # Inserindo lengeda
        self.plot_ch2.addLegend()                            # Inserindo lengeda

        # self.plot.showGrid(x = True, y = True, alpha = 0.2)      # Grid para visualização dos valores
        self.plot_ch1.setLabel('left', 'CH1 [V]')         # Legenda do eixo y
        self.plot_ch2.setLabel('left', 'CH2 [V]')         # Legenda do eixo y

        self.curva_ch1 = self.plot_ch1.plot(pen=pg.mkPen(color='g',width=1),name='CH1')   # Curva do gráfico
        self.curva_ch2 = self.plot_ch2.plot(pen=pg.mkPen(color='b',width=1),name='CH2')   # Curva do gráfico
        self.plot_ch1.hideAxis('bottom')
        
        # x axis values
        self.x = 0   
        
        timer = pg.QtCore.QTimer(self)         # Temporizador da biblioteca 
        timer.timeout.connect(self.update)  
        timer.start(0)   
        
    def update(self): # este é o data consumer do pyqtgraph
        """ Updates the data and the graph"""
        if self.show_fps:
            self.calculate_fps()
            self.plot_ch1.setTitle('<font color="red">%0.2f fps</font>' % self.fps)

        # py_time.sleep(1)
        buffer_plotter =  my_arduino_handler.buffer_acquisition

        # points_to_add = buffer_plotter.qsize()
        points_to_add = len(buffer_plotter)
        # print("Buffer size: ", points_to_add)

        if points_to_add > 0:
            for n in range(points_to_add):  # obtains the new value
                num = buffer_plotter.pop()
                # print("Read value: ", num)
                self.values_ch1.append(num[0])
                self.values_ch2.append(num[1])

                self.x_tick.append(self.x)

                if len(self.values_ch1) > self.amount_of_points: # remove the oldest values
                    self.values_ch1.popleft()
                if len(self.values_ch2) > self.amount_of_points: # remove the oldest values
                    self.values_ch2.popleft()

                if len(self.x_tick) > self.amount_of_points:
                    self.x_tick.popleft()

                self.x += 1
            self.curva_ch1.setData(y=np.array(list(self.values_ch1),dtype='float'))
            self.curva_ch2.setData(y=np.array(list(self.values_ch2),dtype='float'))
            self.curva_ch1.setPos(self.x, 0)
            self.curva_ch2.setPos(self.x, 0)

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

