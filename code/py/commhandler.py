import serial

class ComportHandler():
    """
    Class for handling connection with COM/ttyX ports.
    """
    # self.port_path = 'COM3'                 # Porta a qual o Ard. está conectado (ACM0, ACM1 OU ACM2) for linux and COM1, COM2... for Windows
    # self.baud = 115200                      # Taxa de transferência (a mesma do firm. no Ard.)
    # self.timeout = 1                        # Tempo (s) limite para de tentativa de encontar a conexao

    def __inti__(self, port_path, baudrate=115200, timeout=0):
        self.port_path = port_path  
        self.baud = baudrate 
        self.timeout = timeout  

    @staticmethod
    def get_comport():
        """
            Returns a connection with the parameters in the Serial method.
            If no comport is found, returns None
        """
        
        port_path = 'COM3'
        baudrate = 115200
        timeout = 1
        
        try:
            # Creating connection. (path, baudrate, timeout)
            comport = serial.Serial(port_path, baudrate, timeout=timeout) 
        except:
            print("[ERROR] Comport not found. Graphics will not be shown")
            comport = None       
        
        return comport
    