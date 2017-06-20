import sys

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QFormLayout, QStackedWidget, QListWidget, QApplication, QLineEdit, QRadioButton, QCheckBox, QLabel, QAction, qApp, QMainWindow, QInputDialog, QFileDialog

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
        file = save(name,'r')
        
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
        datafile, __ = QFileDialog.getOpenFileName(self, "Open File","","All Files (*)")
        if datafile:
            datafile = str(datafile)
            spectrum =np.genfromtxt(datafile,dtype=float,comments = "(",skip_header=1,names=True,unpack=True)
            sax = self.figure.add_subplot(111)
            sax.plot(spectrum[spectrum.dtype.names[1]], spectrum[spectrum.dtype.names[2]], '*-')

            self.canvas.draw()
           
    def clearplot(self):
        self.canvas.draw()
        
    def stack2UI(self):
        layout = QFormLayout()
        species = QtWidgets.QHBoxLayout()
        species.addWidget(QCheckBox("Two-Temp Model"))
        species.addWidget(QLineEdit())
        species.addWidget(QLineEdit())
        species.addWidget(QLineEdit())
        layout.addRow(QLabel("T_trans"))
        layout.addRow(QLabel("T_vib"))
        layout.addRow(QLabel("T_el"))
        layout.addWidget(QLineEdit())
        layout.addWidget(QLineEdit())
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
    sys.exit(app.exec_())
        
if __name__ == '__main__':
    main()
