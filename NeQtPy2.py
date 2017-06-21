import sys
import math

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QFormLayout, QStackedWidget, QListWidget, QApplication, QLineEdit, QRadioButton, QCheckBox, QLabel, QAction, qApp, QMainWindow, QInputDialog, QFileDialog, QGridLayout

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()
        
    def initUI(self):               
        #defining the exitting,saving and opening of files
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')                        
        exitAction.setStatusTip('Exit/Terminate application')   
        exitAction.triggered.connect(self.close)     
        openAction = QAction('&Open', self)
        openAction.setShortcut('Ctrl+O')                        
        openAction.setStatusTip('Open File')   
        openAction.triggered.connect(self.openFileNameDialog)
        saveAction = QAction('&Save', self)
        saveAction.setShortcut('Ctrl+S')                        
        saveAction.setStatusTip('Save File')   
        saveAction.triggered.connect(self.saveFileDialog)
        self.statusBar()                                       

        menubar = self.menuBar()                                
        menubar.setToolTip('This is a <b>QWidget</b> for MenuBar')               

        fileMenu = menubar.addMenu('&File')                     
        fileMenu.addAction(exitAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        toolbar.addAction(openAction)
        toolbar.addAction(saveAction)
        content = Widgettown(self)
        self.setCentralWidget(content)
        self.show()
        
    def openFileNameDialog(self):
        name, _ = QFileDialog.getOpenFileName(self, "Open File","","All Files (*)")
        if name:
            print(name)
 
    def saveFileDialog(self):    
        name = QFileDialog.getSaveFileName(self,"Save File","","All Files (*);;Text Files (*.txt)")
        f = open(filename, 'w')
        filedata = self.Stack2.toPlainText()
        filedata = str(filedata)+"\n"
        f.write(filedata)
        filedata = self.textEdit2.toPlainText()
        filedata = str(filedata)+"\n"
        f.write(filedata)
        filedata = self.textEdit3.toPlainText()
        filedata = str(filedata)+"\n"
        f.write(filedata)
        f.close()   
        
        
class Widgettown(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.leftlist = QListWidget ()
        self.leftlist.insertItem (0, 'Plots' )
        self.leftlist.insertItem (1, 'LOS Inputs' )
        self.leftlist.insertItem (2, 'NEQAIR Inputs' )
        
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        
        self.stack1UI()
        self.stack2UI()
        self.stack3UI()
        
        self.Stack = QStackedWidget (self)
        self.Stack.addWidget (self.stack1)
        self.Stack.addWidget (self.stack2)
        self.Stack.addWidget (self.stack3)
        
        hbox = QtWidgets.QHBoxLayout(self)
        hbox.addWidget(self.leftlist)
        hbox.addWidget(self.Stack)

        self.setLayout(hbox)
        self.leftlist.currentRowChanged.connect(self.display)
        self.setGeometry(10, 10, 10, 10)
        self.setWindowTitle('StackedWidget demo')
        self.show()
        
    def openFileNameDialog(self):
        name, _ = QFileDialog.getOpenFileName(self, "Open File","","All Files (*)")
        
    def stack1UI(self):
        
        #figure painting from matplot
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        #toolbar addition
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.show()


        #some buttons for functionality
        self.button = QtWidgets.QPushButton('ReadPlot')
        self.button.clicked.connect(self.readplot)
        self.button2 = QtWidgets.QPushButton('ClearPlot')
        self.button2.clicked.connect(self.clearplot)
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        layout.addWidget(self.button2)
        self.stack1.setLayout(layout)

    def readplot(self):
        self.figure.clf()

        datafile, __ = QFileDialog.getOpenFileName(self, "Open File","","All Files (*)")
        if datafile:
            datafile = str(datafile)
            spectrum =np.genfromtxt(datafile,dtype=float,comments = "(",skip_header=1,names=True,unpack=True)
            sax = self.figure.add_subplot(111)
            sax.plot(spectrum[spectrum.dtype.names[1]], spectrum[spectrum.dtype.names[2]], '*-')
            self.canvas.draw()
           
    def clearplot(self):
        self.figure.clf()
        self.canvas.draw()
        
    def stack2UI(self):
        speclist = ["CO","CO2","N","N2","NO","O","O2"]
        layout = QGridLayout()
        layout.setColumnStretch(1,6)
        layout.setColumnStretch(2,6)
        #temps
        layout.addWidget(QLineEdit(),1,4)
        layout.addWidget(QLineEdit(),2,4)
        layout.addWidget(QLineEdit(),3,4)
        layout.addWidget(QLabel("T_trans"),1,3,QtCore.Qt.AlignCenter)
        layout.addWidget(QLabel("T_vib"),2,3,QtCore.Qt.AlignCenter)
        layout.addWidget(QLabel("T_el"),3,3,QtCore.Qt.AlignCenter)
        layout.addWidget(QCheckBox(),4,4)
        layout.addWidget(QLabel("T-Temp Model"),4,3)
        #number densities
        for i in range(len(speclist)):
            layout.addWidget(QLineEdit(),i,1)
            layout.addWidget(QLabel(speclist[i]),i,0,QtCore.Qt.AlignRight)

        self.stack2.setLayout(layout)
        
    def stack3UI(self):
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QLabel("Bands maybe"))
        layout.addWidget(QCheckBox("b-f"))
        layout.addWidget(QCheckBox("f-f"))
        self.stack3.setLayout(layout)
        
    def display(self,i):
        self.Stack.setCurrentIndex(i)
def main():
    app = QApplication(sys.argv)
    ex = Window()
    ex.setWindowTitle('NeQtPy')
    sys.exit(app.exec_())
        
if __name__ == '__main__':
    main()