# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 09:27:57 2017
This code should allow the user to plot figures, open up a DAT file for the purposes of creating a new file based on a string pulled from DAT file.
@author: jn3
"""
import sys

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
        
        self.content = Widgettown(self)
        self.setCentralWidget(self.content)
        self.show()
        
    def openFileNameDialog(self):
        name, _ = QFileDialog.getOpenFileName(self, "Open DAT File","","DAT Files (*.dat)")
        if name:
            datafile = str(name)
            spectrum =np.genfromtxt(datafile,dtype=None,skip_header=21,names=True)
            self.speclist = spectrum.dtype.names[7:-1] #omitting
            self.setCentralWidget(self.content) #can this pass the speclist variable to be used in generating widgets?
            self.show()
            
    def saveFileDialog(self):    
        name = QFileDialog.getSaveFileName(self,"Save File","","All Files (*);;Text Files (*.txt)")
        f = open(name[0], 'w')
        filedata = self.content.linedit[1].toPlainText() #unfinished save dialog...needs work
        filedata = str(filedata)+"\n"
        f.write(filedata)
        f.close()
        
        
class Widgettown(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        
        self.speclist = None #initialize the species list
        
        self.leftlist = QListWidget ()
        self.leftlist.insertItem (0, 'Plotting Things' )
        self.leftlist.insertItem (1, 'Input FILE MOD' )
        self.leftlist.insertItem (2, 'Input FILE MOD2' )
        
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
        self.leftlist.setGeometry(50, 50, 50, 50)
        self.setWindowTitle('StackedWidget demo')
        self.show()
        
    def openFileNameDialog(self):
        name, _ = QFileDialog.getOpenFileName(self, "Open File","","All Files (*)")
        
    def stack1UI(self): #THE PLOTTING CAPABILITY
        
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

        
    def stack2UI(self): #THE  MOD1 CAPABILITY
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
        
        ##where the linedits are created based on speclist length and contents
        linedits = {}
        if self.speclist:
            for i in range(len(self.speclist)):
                self.mylinedit = QtWidgets.QLineEdit("0.0")
                linedits[i] = self.mylinedit
                layout.addWidget(linedits[i],i,1)
                layout.addWidget(QLabel(self.speclist[i]),i,0,QtCore.Qt.AlignRight)

        self.stack2.setLayout(layout)
        
    def stack3UI(self): #THE  MOD2 CAPABILITY
        layout = QGridLayout()
        layout.addWidget(QLabel("Bands maybe"),1,1)
        layout.addWidget(QCheckBox("b-f"),1,2)
        layout.addWidget(QCheckBox("f-f"),1,3)
        self.losopen = QtWidgets.QPushButton('Read LOS')
        self.losopen.clicked.connect(self.ReadLOS)
        layout.addWidget(self.losopen,0,0)
        
        ##where the linedits are created based on speclist length and contents
        linedits = {}
        if self.speclist:
            for i in range(len(self.speclist)):
                self.mylinedit = QtWidgets.QLineEdit("0.0")
                linedits[i] = self.mylinedit
                layout.addWidget(linedits[i],i,1)
                layout.addWidget(QLabel(self.speclist[i]),i,0,QtCore.Qt.AlignRight)

        self.stack3.setLayout(layout)
        
    def readplot(self): #OPENING AND READING FIGURE IN
        self.figure.clf()

        datafile, __ = QFileDialog.getOpenFileName(self, "Open File","","All Files (*)")
        if datafile:
            datafile = str(datafile)
            spectrum =np.genfromtxt(datafile,dtype=float,comments = "(",skip_header=1,names=True,unpack=True)
            sax = self.figure.add_subplot(111)
            sax.plot(spectrum[spectrum.dtype.names[1]], spectrum[spectrum.dtype.names[2]], '*-')
            self.canvas.draw()
                  
    
    def ReadLOS(self): #OPENING DAT FILE TO READ COLUMN HEADERS
        datafile, __ = QFileDialog.getOpenFileName(self, "Open File","","All Files (*)")
        if datafile:
            datafile = str(datafile)
            spectrum =np.genfromtxt(datafile,dtype=None,skip_header=21,names=True)
            self.speclist = spectrum.dtype.names[7:-1] #omitting some things

                
    def clearplot(self):
        self.figure.clf()
        self.canvas.draw()
        
    def display(self,i):
        self.Stack.setCurrentIndex(i)


def main():
    app = QApplication(sys.argv)
    ex = Window()
    ex.setWindowTitle('NeQtPy')
    sys.exit(app.exec_())
        
if __name__ == '__main__':
    main()
