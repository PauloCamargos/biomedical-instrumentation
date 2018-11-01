# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'realtimeplotter.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_RealTimePlotter(object):
    def setupUi(self, RealTimePlotter):
        RealTimePlotter.setObjectName(_fromUtf8("RealTimePlotter"))
        RealTimePlotter.resize(520, 380)
        self.centralwidget = QtGui.QWidget(RealTimePlotter)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 521, 351))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        RealTimePlotter.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(RealTimePlotter)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 520, 31))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuArquivo = QtGui.QMenu(self.menubar)
        self.menuArquivo.setObjectName(_fromUtf8("menuArquivo"))
        RealTimePlotter.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(RealTimePlotter)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        RealTimePlotter.setStatusBar(self.statusbar)
        self.actionSair = QtGui.QAction(RealTimePlotter)
        self.actionSair.setObjectName(_fromUtf8("actionSair"))
        self.menuArquivo.addAction(self.actionSair)
        self.menubar.addAction(self.menuArquivo.menuAction())

        self.retranslateUi(RealTimePlotter)
        QtCore.QMetaObject.connectSlotsByName(RealTimePlotter)

    def retranslateUi(self, RealTimePlotter):
        RealTimePlotter.setWindowTitle(_translate("RealTimePlotter", "Real Time Plotter", None))
        self.menuArquivo.setTitle(_translate("RealTimePlotter", "Arquivo", None))
        self.actionSair.setText(_translate("RealTimePlotter", "Sair", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RealTimePlotter = QtGui.QMainWindow()
    ui = Ui_RealTimePlotter()
    ui.setupUi(RealTimePlotter)
    RealTimePlotter.show()
    sys.exit(app.exec_())

