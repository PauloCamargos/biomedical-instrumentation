# Description: Custom plot class for pyqtgraph embedded in PyQt Designer
# Author: github.com/PauloCamargos
# Dat: 08/12/2018

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import serial
import time
import commhandler
from queue import Queue

class PyQtGraphSeries:
    def __init__(self, parent=None, pen=(0, 0, 255), name="Curve"):
        """
        Initializes a custom PyQtGraphCurve with a auxiliary vector of values and a buffer.
        :param parent: The parent, it should contains a PyQtPlotWidget that will own this curve.
        :param pen: The RGB color of the curve. Default is blue.
        :param name: The name of the curve. Default is 'Curve'
        """
        self.parent = parent  # Save the parent in a attribute.
        self.values = [0] * self.parent.qnt_points  # Initilizes a zero-filled vector
        # Creates and adds the curve to the plotwidget.
        self.curve = self.parent.plotWidget.plot(self.values, pen=pen, name=name)
        self.visible = True
        self.buffer = Queue(self.parent.qnt_points)

    def set_visible(self, visible):
        """
        Adds or removes the curve of the parent plot widget.
        :param visible: Boolean telling that the curve should appear (True) or hide (False).
        """
        self.visible = visible  # Save the argument as as attribute
        if not self.visible:
            self.parent.plotWidget.removeItem(self.curve)
        else:
            self.parent.plotWidget.addItem(self.curve)

    def update_values(self):
        """
        This method is called automatically, you should not call it by yourself.

        It verifies how many points are in the buffer,
        then remove one by one, and add to the auxiliary vector.
        This auxiliary vector is set as the data source of the curve in the plot.
        """
        points_to_add = self.buffer.qsize()
        if points_to_add > 0:
            for n in range(points_to_add):  # obtains the new values
                num = self.buffer.get()
                self.values.append(num)
                if len(self.values) > self.parent.qnt_points:
                    self.values.pop(0)
        if self.visible:
            self.curve.setData(self.values)

    def get_buffers_status(self):
        """
        Returns a string like:
            Plot:    4/1024
        :return: A string containing the status of the plot buffer for this curve.
        """
        return "Plot: %4d" % (self.buffer.qsize()) + '/' + str(self.buffer.maxsize)

class CustomPlotEMG(pg.GraphicsWindow):
    """
        Implementing a custom class for the pyqtgraph module. It's meant to be used
        with the PyQt5 Designer. For more information, check out pyqtgraph documentation on 
        "Embedding widgets inside PyQt applications".
    """

    def __init__(self, parent=None):
        self.amount_of_points = 10       
        pg.GraphicsWindow.__init__(self, parent=None)
        pg.setConfigOptions(antialias=True)             # Bordas das curvas
        # self.setWindowTitle("Real Time Potentiometer")
        # window.size(600,400)
        self.useOpenGL                            # Configurando engine para renderização do gráfico
        pg.setConfigOptions(useOpenGL=True)

        limit = 2 
        plot = self.addPlot(title="Sinal EMG")    # Iniciando um plot
        plot.setRange(yRange=[-limit,limit])                # Limites do gráfico
        plot.addLegend()                            # Inserindo lengeda
        plot.showGrid(x = True, y = True, alpha = 0.2)      # Grid para visualização dos valores
        plot.setLabel('left', 'Tensão [V]')         # Legenda do eixo y

        self.tensao = [0] * 500 # Criando array de zeros. Vetor com os valores de tensão 
        self.curva = plot.plot(pen=pg.mkPen(color='y',width=0.5),name="[V]")   # Curva do gráfico

        # Texto mostrando valor 
        # texto = pg.TextItem(text="Valor",anchor=(0,0), border='w', fill=(0, 0, 255, 100))
        # plot.addItem(texto)

        self.x = 0   # variável contendo o índice

        # Iniciando conexao serial
        # self.comport = commhandler.ComportHandler().get_comport() # Abrindo a conexao serial arduino/notebook
        # if not self.comport is None:
        #     time.sleep(2)                                # Aguarda um tempo para iniciar comunicação
        #     self.comport.write(b'R')                          # Escreve no arduino. Ordem para iniciar leitura ('R')
        #     timer = pg.QtCore.QTimer(self)         # Temporizador da biblioteca 
        #     timer.timeout.connect(self.update)  
        #     timer.start(0)    # Number of seconds for the next update

    def update(self):
        """ Updates the data and the graph"""
        
        # tensao = self.tensao
        # curva = self.curva
        # x = self.x
        # leitura_arduino = self.comport.readline()    # Lendo o valor da arduino

        # if leitura_arduino != b'\r\n' and leitura_arduino != b'\n': # Checkando se o valor é válido
        #     tensao_ecg = float(leitura_arduino) / 100.0 - 1.65
        #     # tensao_ecg = float(leitura_arduino)/100.0 - 1.65
        #     tensao.append(tensao_ecg)   # Inserindo o valor lido ao vetor 'tensao'
        #     tensao.pop(0)                      # deletando o valor mais antigo do vetor 'tensao'
        #     tensaonp = np.array(tensao[-500:], dtype='float')   # Convertendo o vetor 'tensao' do tipo array para numpy array
        #     curva.setData(tensaonp) # Passando os valores do vetor para a curva
        #     x += 1                  # Atualizando o índice da leitura
        #     curva.setPos(x, 0)       # Valor do eixo x e seu deslocamento verticalmente
        #     # self.plot.setLabel('bottom',"Tensão [V]: " + "{0:.2f}".format(tensaonp.item(499)))


if __name__ == '__main__': # Função iniciando a execução da janela
    # import sys
    # if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    #     QtGui.QApplication.instance().exec_()
    w = CustomPlotEMG()
    w.show()
    QtGui.QApplication.instance().exec_()