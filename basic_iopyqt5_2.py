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
        #openAction = QAction('&Exit', self)
        #openAction.setShortcut('Ctrl+Q')                        
        #openAction.setStatusTip('Exit/Terminate application')   
        #openAction.triggered.connect(self.close)  
        self.statusBar()                                       

        menubar = self.menuBar()                                
        menubar.setToolTip('This is a <b>QWidget</b> for MenuBar')                                

        fileMenu = menubar.addMenu('&File')                     
        fileMenu.addAction(exitAction)                          
        toolbar = self.addToolBar('Exit')                       
        toolbar.addAction(exitAction)
        content = Widgettown(self)
       # self.openFileNameDialog()
       # self.openFileNamesDialog()
       # self.saveFileDialog()
        self.setCentralWidget(content)

        self.show()
   
 #   def openFileNameDialog(self):    
 #       options = QFileDialog.Options()
 #       options |= QFileDialog.DontUseNativeDialog
 #       fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()","","All Files (*);;Python Files (*.py)", options=options)
 #   if fileName:
 #       print(fileName)
 
 #   def openFileNamesDialog(self):    
 #       options = QFileDialog.Options()
 #       options |= QFileDialog.DontUseNativeDialog
 #       files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()","","All Files (*);;Python Files (*.py)", options=options)
 #   if files:
 #       print(files)
 
 #   def saveFileDialog(self):    
 #       options = QFileDialog.Options()
 #       options |= QFileDialog.DontUseNativeDialog
 #       fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
 #   if fileName:
 #       print(fileName)
        
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
    main.setWindowTitle('Basic1')
    main.show()

    sys.exit(app.exec_())
