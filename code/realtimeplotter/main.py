# -*- coding: utf-8 -*-
from pyqtgraph.Qt import QtGui, QtCore # Biblitecas para execução do programa
import numpy as np
import pyqtgraph as pg
import serial
import time

caminho_porta = "/dev/ttyACM0"      # Porta a qual o Ard. está conectado (ACM0, ACM1 OU ACM2)
baud = 115200                       # Taxa de transferência (a mesma do firm. no Ard.)
timeout = 3                        # Tempo (s) limite para de tentativa de encontar a conexao

# Iniciando conexao serial
comport = serial.Serial(caminho_porta, baud) # Abrindo a conexao serial arduino/notebook
time.sleep(2)                                # Aguarda um tempo para iniciar comunicação
comport.write(b'R')                          # Escreve no arduino. Ordem para iniciar leitura ('R')

app = QtGui.QApplication([])                   # Iniciando a aplicação

pg.setConfigOptions(antialias=True)             # Bordas das curvas

window = pg.GraphicsWindow(title="Real Time ECG")   # Titulo da janela
# window.size(600,400)
window.useOpenGL                            # Configurando engine para renderização do gráfico

plot = window.addPlot(title="Sinal ECG")    # Iniciando um plot
plot.setRange(yRange=[-3,3])                # Limites do gráfico
plot.addLegend()                            # Inserindo lengeda
plot.showGrid(x = True, y = True, alpha = 0.2)      # Grid para visualização dos valores
plot.setLabel('left', 'Tensão [V]')         # Legenda do eixo y

tensao = [0] * 500 # Criando array de zeros. Vetor com os valores de tensão 
curva = plot.plot(pen='g',name="[V]")   # Curva do gráfico
x = 0   # variável contendo o índice

def update():
    global tensao, curva, x
    leitura_arduino = comport.readline()    # Lendo o valor da arduino

    if leitura_arduino != b'\r\n'  : # Checkando se o valor é válido
        tensao.append(float(leitura_arduino)/100.0 - 2.5)   # Inserindo o valor lido ao vetor 'tensao'
        tensao.pop(0)                      # deletando o valor mais antigo do vetor 'tensao'
        tensaonp = np.array(tensao[-500:], dtype='float')   # Convertendo o vetor 'tensao' do tipo array para numpy array
        curva.setData(tensaonp) # Passando os valores do vetor para a curva
        x += 1                  # Atualizando o índice da leitura
        curva.setPos(x, 0)       # Valor do eixo x e seu deslocamento verticalmente
        app.processEvents()     # Atualizando a interface (janela do gráfico)
    
timer = QtCore.QTimer()         # Temporizador da biblioteca 
timer.timeout.connect(update)   
timer.start(0)                  

if __name__ == '__main__': # Função iniciando a execução da janela
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()