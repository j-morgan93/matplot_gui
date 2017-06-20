"""
Trying to plot with Matplot and Qt5 bacckend
"""
import sys
from PyQt5 import QtWidgets


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import random

class Window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)


        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.show()

        #defining the exitting,saving and opening of files


        #exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        #exitAction.setShortcut('Ctrl+Q')
        #exitAction.setStatusTip('Exit application')
        #exitAction.triggered.connect(qApp.quit)

        #menubar = self.menuBar()
        #fileMenu = menubar.addMenu('&File')
        #fileMenu.addAction(exitAction)

        #some button with listed activity
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

    def home(self):
        self.toolbar.home()
    def zoom(self):
        self.toolbar.zoom()
    def pan(self):
        self.toolbar.pan()

    def plot(self):
        ''' plot some random stuff '''
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
