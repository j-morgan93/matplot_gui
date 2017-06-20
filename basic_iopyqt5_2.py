"""
Trying to plot with Matplot and Qt5 backend
"""
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QAction, qApp, QApplication, QMainWindow, QWidget, QInputDialog, QLineEdit, QFileDialog


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import random

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
        #toolbar = self.addToolBar('Open')
        #toolbar = self.addToolBar('Save')                       
        toolbar.addAction(exitAction)
        toolbar.addAction(openAction)
        toolbar.addAction(saveAction)
        content = Widgettown(self)
        self.setCentralWidget(content)

        self.show()
    def openFileNameDialog(self):
        name = QFileDialog.getOpenFileName(self, "Open File","","All Files (*)")
        file = open(name,'r')
 
    def saveFileDialog(self):    
        name = QFileDialog.getSaveFileName(self,"Save File","","All Files (*);;Text Files (*.txt)")
        file = save(name,'r')

        
class Widgettown(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.initUI()

    def initUI(self):    
        #figure painting from matplot
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        #toolbar addition
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.show()


        #some buttons for functionality
        self.button = QtWidgets.QPushButton('Plot')
        self.button.clicked.connect(self.plot)
        
        self.button1 = QtWidgets.QPushButton('Zoom')
        self.button1.clicked.connect(self.zoom)

        self.button2 = QtWidgets.QPushButton('Pan')
        self.button2.clicked.connect(self.pan)

        self.button3 = QtWidgets.QPushButton('Home')
        self.button3.clicked.connect(self.home)


        # set the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        self.setLayout(layout)
        #####################################################        
        
    def home(self):
        self.toolbar.home()
    def zoom(self):
        self.toolbar.zoom()
    def pan(self):
        self.toolbar.pan()
            
    def plot(self):
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.hold(False)
        ax.plot(data, '*-')
        self.canvas.draw()
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = Window()
    main.setWindowTitle('NeQtPy')
    main.show()

    sys.exit(app.exec_())
