from PyQt5.QtWidgets import *
import main_window
import sys

class TestePyQt(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(TestePyQt, self).__init__(parent)
        self.setupUi(self)


def main():
    app = QApplication(sys.argv)
    form = TestePyQt()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()