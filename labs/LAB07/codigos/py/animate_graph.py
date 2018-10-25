import matplotlib.pyplot as plt     # Importando bibliotecas necessárias para execução do programa
import matplotlib.animation as animation
import serial   
import time
from matplotlib import style

style.use("fivethirtyeight") # Estilo do gráfico (cor da linha, traçado...)

caminho_porta = "/dev/ttyACM0"      # Porta a qual o Ard. está conectado (ACM0, ACM1 OU ACM2)
baud = 115200                       # Taxa de transferência (a mesma do firm. no Ard.)
timeout = 3                        # Tempo (s) limite para de tentativa de encontar a conexao

# Iniciando conexao serial
comport = serial.Serial(caminho_porta, baud) # Abrindo a conexao serial arduino/notebook
time.sleep(2)
comport.write(b'R') # Valor escrito para o arduino; 'R' para começar a ler

# Figura em que o gráfico será renderizado
fig = plt.figure()              # criando uma nova figura
ax1 = fig.add_subplot(1,1,1)    # subplot 

tensao = [0] # Vetor que armazena valor do arduino
tempo = [0]  # Vetor que armazena indices de leitura

# Função/método que le os dados e insere no gráfico
def animate(i):
    # print("Iniciando a animacao")
    leitura_arduino = comport.readline()

    # print(f"leitura arduino {leitura_arduino}")
    if leitura_arduino != b'\r\n'  : # Checkando se o valor é válido
        tensao.append(float(leitura_arduino)/100.0) # Convetendo para float (0 - 5.5)
        tempo.appendtempo[-1] + 1)                 # Atualizando indice
        ax1.clear()                                 # Limpa o plot
        ax1.plot(tempo, tensao, label=f"Tensão: {tensao[-1]}V") # Ploat os novos valores
        ax1.legend(loc="upper left")                # Inserindo legenda

        if len(tensao)>50:  # Se o gráfico tem mais de 50 pontos
            tensao.pop(0)   # exlclui o valor mais antigo                               
            tempo.pop(0)    # exlclui o valor mais antigo


ani = animation.FuncAnimation(fig, animate, interval=100) # funcao responsável pela animacao
plt.show()  # Exibindo o plot no monitor do notebook
