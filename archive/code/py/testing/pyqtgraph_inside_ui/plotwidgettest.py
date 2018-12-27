# -*- coding: utf-8 -*-
## Description: Example of embedded pyqtgraph plot in PyQt designer.
# It plots data comming form and Arduino board. The code used in this 
# examplo for the Arduino can be found inside the .ino folder.

from pyqtgraph.Qt import QtGui, QtCore # Biblitecas para execução do programa
import numpy as np
import pyqtgraph as pg
import serial
import time
		
class PlotWidgetTest(pg.GraphicsWindow):
    """
        Implementing a custom class for the pyqtgraph module. It's meant to be used
        with the PyQt5 Designer. For more information, check out pyqtgraph documentation on 
        "Embedding widgets inside PyQt applications".
    """

    def __init__(self, parent=None):
        caminho_porta = "COM3"      # Porta a qual o Ard. está conectado (ACM0, ACM1 OU ACM2)
        baud = 115200                       # Taxa de transferência (a mesma do firm. no Ard.)
        timeout = 1                        # Tempo (s) limite para de tentativa de encontar a conexao

        # Iniciando conexao serial
        self.comport = serial.Serial(caminho_porta, baud) # Abrindo a conexao serial arduino/notebook
        time.sleep(2)                                # Aguarda um tempo para iniciar comunicação
        self.comport.write(b'R')                          # Escreve no arduino. Ordem para iniciar leitura ('R')
        
        
        pg.GraphicsWindow.__init__(self, parent=None)
        pg.setConfigOptions(antialias=True)             # Bordas das curvas
        self.setWindowTitle("Real Time Potentiometer")
        # window.size(600,400)
        self.useOpenGL                            # Configurando engine para renderização do gráfico
        pg.setConfigOptions(useOpenGL=True)

        limit = 2 
        plot = self.addPlot(title="Sinal ECG")    # Iniciando um plot
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
  
        timer = pg.QtCore.QTimer(self)         # Temporizador da biblioteca 
        timer.timeout.connect(self.update)  
        timer.start(0)    # Number of seconds for the next update

    def update(self):
        """ Updates the data and the graph"""
        tensao = self.tensao
        curva = self.curva
        x = self.x
        leitura_arduino = self.comport.readline()    # Lendo o valor da arduino

        if leitura_arduino != b'\r\n' and leitura_arduino != b'\n': # Checkando se o valor é válido
            tensao_ecg = float(leitura_arduino) / 100.0 - 1.65
            # tensao_ecg = float(leitura_arduino)/100.0 - 1.65
            tensao.append(tensao_ecg)   # Inserindo o valor lido ao vetor 'tensao'
            tensao.pop(0)                      # deletando o valor mais antigo do vetor 'tensao'
            tensaonp = np.array(tensao[-500:], dtype='float')   # Convertendo o vetor 'tensao' do tipo array para numpy array
            curva.setData(tensaonp) # Passando os valores do vetor para a curva
            x += 1                  # Atualizando o índice da leitura
            curva.setPos(x, 0)       # Valor do eixo x e seu deslocamento verticalmente
            # self.plot.setLabel('bottom',"Tensão [V]: " + "{0:.2f}".format(tensaonp.item(499)))

if __name__ == '__main__': # Função iniciando a execução da janela
    # import sys
    # if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    #     QtGui.QApplication.instance().exec_()
    
    w = PlotWidgetTest()
    w.show()
    QtGui.QApplication.instance().exec_()
