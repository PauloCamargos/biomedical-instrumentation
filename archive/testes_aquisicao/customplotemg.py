# Description: Custom plot class for pyqtgraph embedded in PyQt Designer
# Author: github.com/PauloCamargos
# Dat: 08/12/2018

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import serial
import time
from numpy import clip
from pyqtgraph.ptime import time
from queue import Queue
from ArduinoHandler import ArduinoHandler
from ThreadHandler import ThreadHandler

buffer_plotter = Queue(4096)

my_arduino_handler = ArduinoHandler(port_name='COM3', baudrate=115200, qnt_ch=1)

# def data_consumer():
#     if my_arduino_handler.data_waiting:
#         print("Dado lido: ")
#         buffer_plotter.put(my_arduino_handler.buffer_acquisition.get())
#         # time.sleep(0.01) # Uncomment if you want to see the buffer_acquisition to get full

# consumer_thr = ThreadHandler(data_consumer)
my_arduino_handler.start_acquisition()

class CustomPlotEMG(pg.GraphicsWindow):
    """
        Implementing a custom class for the pyqtgraph module. It's meant to be used
        with the PyQt5 Designer. For more information, check out pyqtgraph documentation on 
        "Embedding widgets inside PyQt applications".
    """

    def __init__(self, parent=None): 
        pg.GraphicsWindow.__init__(self, parent=None)
        self.amount_of_points = 500   
        self.values = [0] * self.amount_of_points 

        self.fps = 0
        self.show_fps = True
        self.lastTime = 0

        pg.setConfigOptions(antialias=True)             # Bordas das curvas

        # self.setWindowTitle("Real Time Potentiometer")
        # window.size(600,400)
        self.useOpenGL                            # Configurando engine para renderização do gráfico
        pg.setConfigOptions(useOpenGL=True)

        limit = 600 
        self.plot = self.addPlot(title="Sinal EMG")    # Iniciando um plot
        self.plot.setRange(yRange=[-10,1050])                # Limites do gráfico
        self.plot.addLegend()                            # Inserindo lengeda
        self.plot.showGrid(x = True, y = True, alpha = 0.2)      # Grid para visualização dos valores
        self.plot.setLabel('left', 'Tensão [V]')         # Legenda do eixo y

        # self.tensao = [0] * 500 # Criando array de zeros. Vetor com os valores de tensão 
        self.curva = self.plot.plot(pen=pg.mkPen(color='b',width=1),name="[V]")   # Curva do gráfico

        # Texto mostrando valor 
        # texto = pg.TextItem(text="Valor",anchor=(0,0), border='w', fill=(0, 0, 255, 100))
        # plot.addItem(texto)

        # self.x = 0   # variável contendo o índice

        # Iniciando conexao serial
        # self.comport = commhandler.ComportHandler().get_comport() # Abrindo a conexao serial arduino/notebook
        # if not self.comport is None:
        #     time.sleep(2)                                # Aguarda um tempo para iniciar comunicação
        #     self.comport.write(b'R')                          # Escreve no arduino. Ordem para iniciar leitura ('R')
        timer = pg.QtCore.QTimer(self)         # Temporizador da biblioteca 
        timer.timeout.connect(self.update)  
        timer.start(0)    # Number of seconds for the next update
        self.x = 0

    def update(self): # este é o data consumer do pyqtgraph
        if self.show_fps:
            self.calculate_fps()
            self.plot.setTitle('<font color="red">%0.2f fps</font>' % self.fps)

        """ Updates the data and the graph"""
        # NOTE: FAZER O PLOT COM MAIS DADOS AO INVÉS DE ATUALIZAR PONTO A PONTO
        #print("Atualizando gráfico")
        points_to_add = my_arduino_handler.buffer_acquisition.qsize()
        print('POINTS TO ADD: ',points_to_add)
        if points_to_add > 60:
            for n in range(points_to_add):  # obtains the new values
                num = my_arduino_handler.buffer_acquisition.get()
                self.values.append(num)
                if len(self.values) > self.amount_of_points: # remove the oldest values
                    self.values.pop(0)
        # if self.visible:
            self.curva.setData(np.array(self.values[-self.amount_of_points:], dtype='int'))
            self.x += 1
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
    my_arduino_handler.close()