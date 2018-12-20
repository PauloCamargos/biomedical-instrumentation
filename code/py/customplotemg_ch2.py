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

# my_arduino_handler = ArduinoHandler(port_name='COM3', baudrate=115200, qnt_ch=2)
my_arduino_handler = ArduinoHandler.instance(port_name='COM3', baudrate=115200, qnt_ch=2)
my_arduino_handler.start_acquisition()


class CustomPlotEMG(pg.GraphicsWindow):
    """
        Implementing a custom class for the pyqtgraph module. It's meant to be used
        with the PyQt5 Designer. For more information, check out pyqtgraph documentation on 
        "Embedding widgets inside PyQt applications".
    """

    def __init__(self, parent=None): 
        pg.GraphicsWindow.__init__(self, parent=None)
        self.amount_of_points = 2000 
        self.values_ch1 = [0] * self.amount_of_points 
        self.values_ch2 = [0] * self.amount_of_points 

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
        self.plot.showGrid(x = True, y = True, alpha = 0.2)      # Grid para visualização dos valores
        self.plot.setLabel('left', 'Tensão [V]')         # Legenda do eixo y

        self.curva_ch1 = self.plot.plot(pen=pg.mkPen(color='b',width=1),name="[CH1]")   # curva_ch1 do gráfico
        self.curva_ch2 = self.plot.plot(pen=pg.mkPen(color='r',width=1),name="[CH2]")   # curva_ch2 do gráfico

        timer = pg.QtCore.QTimer(self)         # Temporizador da biblioteca 
        timer.timeout.connect(self.update)  
        timer.start(0)   
        self.x = 0

    def update(self): # este é o data consumer do pyqtgraph
        if self.show_fps:
            self.calculate_fps()
            self.plot.setTitle('<font color="red">%0.2f fps</font>' % self.fps)

        """ Updates the data and the graph"""
        # NOTE: FAZER O PLOT COM MAIS DADOS AO INVÉS DE ATUALIZAR PONTO A PONTO
        points_to_add = my_arduino_handler.buffer_acquisition.qsize()
       # print(f"POINTS TO add: {points_to_add} ")
        if points_to_add > 15:
            for n in range(points_to_add):  # obtains the new value
                num = my_arduino_handler.buffer_acquisition.get()
                self.values_ch1.append(num[0])
                self.values_ch2.append(num[1] + 500)
                if len(self.values_ch1) > self.amount_of_points: # remove the oldest values
                    self.values_ch1.pop(0)
                if len(self.values_ch2) > self.amount_of_points: # remove the oldest values
                    self.values_ch2.pop(0)

            self.curva_ch1.setData(np.array(self.values_ch1[-self.amount_of_points:], dtype='float'))
            self.curva_ch2.setData(np.array(self.values_ch2[-self.amount_of_points:], dtype='float'))

        # self.curva_ch1.setData(self.values)
        self.x += 1
        # if self.x % 2 == 0:
        if True:
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
    my_arduino_handler.close()