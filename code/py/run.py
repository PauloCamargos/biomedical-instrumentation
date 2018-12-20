# Description: Module joining all other separeta modulos, such as PyQt Gui interface, Unity Com and SVM processing
# Author: Paulo Camargos
# Date: 08/12/2018

from PyQt5.QtWidgets import *
from controller.unitycommunication import unity_comm
import main_window # qt user interface file
import sys
import os
# from ThreadHandler import ThreadHandler # thanks to Ítalo and Andrei (see ThreadHandler docs.)
import threading

#     movements = {1:'abrir', 2:'fechar', 3:'flexionar', 4:'estender', 5:'supinar', 6:'pronar'}


class EmgSvmApp(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(EmgSvmApp, self).__init__(parent)
        self.setupUi(self)
        self.current_move = 1 # standard move

        # Thread for the execution of moves in unity. Blocking other buttons until 
        # the move is completed. At the end, this thread execute the
        #  method 'self.unlock_all_buttons'
        # self.thread_executing_move = ThreadHandler.ThreadHandler(
        #     worker=unity_comm.relay_movement_command,
        #     args=(self.current_move), 
        #     on_end_function=self.unlock_all_buttons)

        # Setting up the buttons to their respective methods
        self.setup_connections()        

    def setup_connections(self):
        """
            Sets up the buttons to their respective methods and initial miscellaneous configurations. 
        """
        self.btn_repouso.clicked.connect(self.execute_rest_movement)
        self.btn_abrir.clicked.connect(self.execute_open_movement)
        self.btn_fechar.clicked.connect(self.execute_close_movement)
        self.btn_extensao.clicked.connect(self.execute_extension_movement)
        self.btn_flexao.clicked.connect(self.execute_flexion_movement)
        self.btn_supinacao.clicked.connect(self.execute_supination_movement)
        self.btn_pronacao.clicked.connect(self.execute_pronation_movement)

    ### clicked.connect methods
    def execute_rest_movement(self):
        # Blocking all buttuns until the move is not completed.
        self.lock_all_buttons() 
        # Sending the move code and starting it's thread.
        self.current_move = 1
        unity_comm.relay_movement_command(1)
        self.unlock_all_buttons()
        print("[INFO] Executing 'REST' movement...")

    def execute_open_movement(self):
        # Blocking all buttuns until the move is not completed.
        self.lock_all_buttons() 
        # Sending the move code and starting it's thread.
        self.current_move = 1
        unity_comm.relay_movement_command(1)
        self.unlock_all_buttons()
        print("[INFO] Executing 'OPEN' movement...")

    def execute_close_movement(self):
        # Blocking all buttuns until the move is not completed.
        self.lock_all_buttons() 
        # Sending the move code and starting it's thread.
        self.current_move = 2
        unity_comm.relay_movement_command(1)
        self.unlock_all_buttons()
        print("[INFO] Executing 'CLOSE' movement...")

    def execute_flexion_movement(self):
        # Blocking all buttuns until the move is not completed.
        self.lock_all_buttons() 
        # Sending the move code and starting it's thread.
        self.current_move = 3
        unity_comm.relay_movement_command(1)
        self.unlock_all_buttons()
        print("[INFO] Executing 'FLEXION' movement...")
        
    def execute_extension_movement(self):
        # Blocking all buttuns until the move is not completed.
        self.lock_all_buttons() 
        # Sending the move code and starting it's thread.
        self.current_move = 4
        unity_comm.relay_movement_command(1)
        self.unlock_all_buttons()
        print("[INFO] Executing 'EXTENSION' movement...")

    def execute_supination_movement(self):
        # Blocking all buttuns until the move is not completed.
        self.lock_all_buttons() 
        # Sending the move code and starting it's thread.
        self.current_move = 5
        unity_comm.relay_movement_command(1)
        self.unlock_all_buttons()
        print("[INFO] Executing 'SUPINATION' movement...")

    def execute_pronation_movement(self):
       # Blocking all buttuns until the move is not completed.
        self.lock_all_buttons() 
        # Sending the move code and starting it's thread.
        self.current_move = 6
        unity_comm.relay_movement_command(1)
        self.unlock_all_buttons()
        print("[INFO] Executing 'PRONATION' movement...")

    def lock_all_buttons(self):
        """Blocks all move buttons"""
        self.btn_repouso.setEnabled(False)
        self.btn_abrir.setEnabled(False)
        self.btn_fechar.setEnabled(False)
        self.btn_extensao.setEnabled(False)
        self.btn_flexao.setEnabled(False)
        self.btn_supinacao.setEnabled(False)
        self.btn_pronacao.setEnabled(False)
    
    def unlock_all_buttons(self):
        """Unlock all buttons. This function is called at the end
        of the self.thread_executing_move"""
        self.btn_repouso.setEnabled(True)
        self.btn_abrir.setEnabled(True)
        self.btn_fechar.setEnabled(True)
        self.btn_extensao.setEnabled(True)
        self.btn_flexao.setEnabled(True)
        self.btn_supinacao.setEnabled(True)
        self.btn_pronacao.setEnabled(True)
    


def main():
    app = QApplication(sys.argv)
    form = EmgSvmApp()
    form.show()
    app.exec_()


if __name__ == "__main__":
    # Opening a new mosquitto broker
    unity_comm.open_mosquitto_broker()

    # Executing the interface
    main()
