# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 10:03:22 2017

@author: Jonathan
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
        helpAction = QAction('&Help', self)
        helpAction.setShortcut('Ctrl+H')                        
        helpAction.setStatusTip('Help')   
        helpAction.triggered.connect(self.helpFileDialog)
        self.statusBar()                                       

        menubar = self.menuBar()                                
        menubar.setToolTip('This is a <b>QWidget</b> for MenuBar')               

        fileMenu = menubar.addMenu('&File')                     
        fileMenu.addAction(exitAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(helpAction)
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        toolbar.addAction(openAction)
        toolbar.addAction(saveAction)
        toolbar.addAction(helpAction)
        self.content = Widgettown(self)
        self.setCentralWidget(self.content)
        self.show()
        
    def openFileNameDialog(self):
        name, _ = QFileDialog.getOpenFileName(self, "Open File","","All Files (*)")
        if name:
            print(name)
            
    def helpFileDialog(self):
        self.helpfile = MyHelpWidget(self)
        
 
    def saveFileDialog(self):   #MASTER WRITE CAPABILITY
        name = QFileDialog.getSaveFileName(self,"Save File","","All Files (*);;Text Files (*.txt)")
        f = open(name[0], 'w')
        f.write("15.0\n")
        f.write("----\n")
        for i in range(len(self.content.il2s)):
            if self.content.il2s[i].isChecked() == True:
                data = self.content.il2info[i]
                data = data[data.find("(")+1:data.find(")")].split()[0]
                f.write(data)
                if i == 0 or i == 3:
                    data = str(2)
                    f.write(data)
        f.write("\n\n")
        f.write("----\n")
        for i in range(len(self.content.il3s)):
            if self.content.il3s[i].isChecked() == True:
                data = self.content.il3info[i]
                data = data[data.find("(")+1:data.find(")")].split()[0]
                f.write(data)
                if "Non" in self.content.il3s[i].text() and self.content.il3s[i].isChecked() == True:
                    if self.content.nbdrop1.currentIndex() != 0:
                        ind = self.content.nbdrop1.currentIndex()
                        data = self.content.nbdrop1.itemText(ind)
                        data = data[data.find("(")+1:data.find(")")].split()[0]
                        f.write(" "+data)
                    ind = self.content.nbdrop2.currentIndex()
                    data = self.content.nbdrop2.itemText(ind)
                    data = data[data.find("(")+1:data.find(")")].split()[0]
                    f.write(" "+data)
                    f.write("\n")
        f.write("\n\n")
        f.write("----\n")
        for i in range(len(self.content.il4s)):
            if self.content.il4s[i].isChecked() == True:
                data = self.content.il4info[i]
                data = data[data.find("(")+1:data.find(")")].split()[0]
                f.write(data)
        f.write("\n\n")
        f.write("----\n")
        for i in range(len(self.content.il5s)):
            if self.content.il5s[i].isChecked() == True:
                data = self.content.il5info[i]
                data = data[data.find("(")+1:data.find(")")].split()[0]
                f.write(data)
        f.write("\n\n")
        f.write("----\n")
        for i in range(len(self.content.speclist)):
            if self.content.bs[i].isChecked() == True:
                filedata =self.content.speclist[i] 
                f.write(filedata+" ")
                if len(self.content.bs[i].text()) == 1 or (len(self.content.bs[i].text()) == 2 and "+" in self.content.bs[i].text()):
                    for j in range(3):
                        if self.content.cs[i,j].isChecked() == True:
                            f.write(self.content.aband[j]+" ")
                    f.write("\n")
                if not "+" in self.content.bs[i].text():
                    if "NO" in self.content.bs[i].text():
                        for j in range(len(self.content.noband)):
                            if self.content.cs[i,j].isChecked() == True:
                                f.write(self.content.noband[j]+" ")
                        f.write("\n")
                    if "N2" in self.content.bs[i].text():
                        for j in range(len(self.content.n2band)):
                            if self.content.cs[i,j].isChecked() == True:
                                f.write(self.content.n2band[j]+" ")
                        f.write("\n")
                    if "O2" in self.content.bs[i].text():
                        for j in range(len(self.content.o2band)):
                            if self.content.cs[i,j].isChecked() == True:
                                f.write(self.content.o2band[j]+" ")
                        f.write("\n")
        f.write("\n")
        f.write("----\n")
        for i in range(self.content.regionbox.value()):
            if self.content.il6s[i,0].text() != "0.0":
                for j in range(2):
                    dataw1w2 = self.content.il6s[i,j].text()
                    f.write(dataw1w2+" ")
                ind = self.content.nbdrop3.currentIndex()
                datanb = self.content.nbdrop3.itemText(ind)
                dataam = self.content.il6s[i,2].text()
                if self.content.il6s[i,3].isChecked() == True:
                    f.write(datanb+" "+dataam+" R "+self.content.il6s[i,4].text())
                
        f.write("\n\n")
        f.write("----\n")
        for i in range(self.content.regionbox.value()):
            if self.content.il6s[i,0].text() != "0.0":    
                datal71 = self.content.il7s[i,j].text()
                ind = self.content.nbdrop4.currentIndex()
                line_s = self.content.nbdrop4.itemText(ind)
                f.write(datal71+" "+line_s)
                for j in range(3):
                    datal72 = self.content.il7s[i,j].text()
                    f.write(" "+datal72)
        f.write("\n\n")
        f.write("----\n")
        f.close()
        ## try actually writing all of the variables out first and then format one f.write function
        ##this may cut down on the cost of the things.
        
class Widgettown(QWidget): #WHERE ALL OF THE FUNCTIONALITY IS LOCATED
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.speclist = None

        self.leftlist = QListWidget ()
        self.leftlist.insertItem (0, 'Plots' )
        self.leftlist.insertItem (1, 'Spectral Fit - Generate LOS file' )
        self.leftlist.insertItem (2, 'NEQAIR Simulation - Provide LOS and Write .inp' )
        
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

        
    def stack2UI(self): #THE LOS DATA CAPABILITY
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
        linedits = {}
        if self.speclist:
            for i in range(len(self.speclist)):
                self.mylinedit = QtWidgets.QLineEdit("0.0")
                linedits[i] = self.mylinedit
                layout.addWidget(linedits[i],i,1)
                layout.addWidget(QLabel(self.speclist[i]),i,0,QtCore.Qt.AlignRight)

        self.stack2.setLayout(layout)
        
    def stack3UI(self): #THE NEQAIR MODEL INPUT CAPABILITY
    ######################################################TABS#####################################################
    ################################################################################################################
        self.il2info = ["(I)ntensity.out", "Intensity_(S)canned.out", "(L)OS.out", "(P)opulation","(A)bsorbance/Emittance","(C)oupling.out",
"(M) stdout"]
        self.il3info = ["(B) Boltzmann","(N) Non-Boltzmann","(Q) Traditional QSS ","(T) Time derivative limited","(R) Reaction residual limited ",
"(F) Flux limited","(C) Constant escape factor","(L) Local Escape factor","(F) Full local calculation","(N) Non-local coupling",
"(S) Saha","(F) Input from File","(A) absorption/emission coefficients from File"]
        self.il4info = ["(T) Tangent Slab","(C) Spherical Cap","(S) Shock Tube","(L) Line of Sight","(B) Blackbody","(P) Calculate Populations",
"(X) Perform scan on existing intensity.out"]
        self.il5info = ["(B) Blackbody","(I) read Intensity.in","(N) no initial radiance","(I) read emissivity.in","(G) Greybody","(B) Blackbody"]
        self.il6info = ["WL1","WL2","A","M","Delta","R","dd"]
        self.il7info = ["ICCD1","ICCD2","Voigt","Gauss"]
        #create the dictionaries to place the widgets within for each tab.
        self.il2s = {}
        self.il3s = {}
        self.il4s = {}
        self.il5s = {}
        self.il6s = {}
        self.il7s = {}
        
        self.layout3 = QtWidgets.QVBoxLayout(self)
        self.tabs = QtWidgets.QTabWidget() #create the tabs
        self.tab1 = QWidget()	
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        
        self.tabs.addTab(self.tab1,"File Setup") # Add tabs
        self.tabs.addTab(self.tab2,"Species Information")
        self.tabs.addTab(self.tab3,"Geometry \& Boundary Conditions")
        self.tabs.addTab(self.tab4,"Regions")
        self.tabs.addTab(self.tab5,"Line Style")
        
       # Create first tab - Generic File information (sim type and such)
        self.tab1.layout3 = QGridLayout()      
        count = 0
        for i in range(7): #INPUT LINE 2
            self.il2 = QtWidgets.QCheckBox(self.il2info[i],self)
            self.il2s[i] = self.il2
            self.tab1.layout3.addWidget(self.il2s[i],i+1,0)
            #self.tab1.layout3.addWidget(QLabel(il2info[i]),i+1,1)
            if "(I)" in self.il2info[i] or "(S)" in self.il2info[i]:
                self.il2 = QtWidgets.QCheckBox("Column Format?",self)
                self.il2s[i] = self.il2
                self.tab1.layout3.addWidget(self.il2s[i],i+1,2,QtCore.Qt.AlignRight)
                count+=1                
            count+=1          
        for i in range(2): #INPUT LINE 3
            self.il3 = QtWidgets.QCheckBox(self.il3info[i],self)
            self.il3s[i] = self.il3
            self.tab1.layout3.addWidget(self.il3s[i],count+i+1,0)
            if "Non-B" in self.il3info[i]:
                self.nbdrop1 = QtWidgets.QComboBox()
                self.nbdrop1.addItem("--optional--")
                self.nbdrop1.addItems(self.il3info[2:5])
                self.nbdrop2 = QtWidgets.QComboBox()
                self.nbdrop2.addItems(self.il3info[6:9])
                self.tab1.layout3.addWidget(self.nbdrop1,count+i+1,2)
                self.tab1.layout3.addWidget(self.nbdrop2,count+i+1,3)
        for i in range(3):
            self.il3 = QtWidgets.QCheckBox(self.il3info[i+10],self)
            self.il3s[i+2] = self.il3
            self.tab1.layout3.addWidget(self.il3s[i+2],count+i+3,0)
            
        self.tab1.setLayout(self.tab1.layout3)
       
        # Create second tab
        self.tab2.layout3 = QGridLayout()
        self.losopen = QtWidgets.QPushButton("Read LOS")
        self.losopen.clicked.connect(self.ReadLOS) #define the button's functionality
        self.tab2.layout3.addWidget(self.losopen,0,0)
        self.tab2.setLayout(self.tab2.layout3)
        
        #Create third tab
        self.tab3.layout3 = QGridLayout()
        self.tab3.layout3.addWidget(QLabel("GEOMETRY"),0,0,QtCore.Qt.AlignTop)
        self.tab3.layout3.addWidget(QLabel("BOUNDARY CONDITIONS"),0,1,QtCore.Qt.AlignTop)
        for i in range(len(self.il4info)): #INPUT LINE 4
            self.il4 = QtWidgets.QCheckBox(self.il4info[i],self)
            self.il4s[i] = self.il4
            self.tab3.layout3.addWidget(self.il4s[i],count+i+2,0)
        for i in range(len(self.il5info)): #INPUT LINE 5
            self.il5 = QtWidgets.QCheckBox(self.il5info[i],self)
            self.il5s[i] = self.il5
            self.tab3.layout3.addWidget(self.il5s[i],count+i+2,1)
        self.tab3.setLayout(self.tab3.layout3)
       
        #Create fourth tab
        self.tab4.layout3 = QGridLayout()
        self.regionbox = QtWidgets.QSpinBox(self)
        self.regionbox.setValue(4)
        self.tab4.layout3.addWidget(self.regionbox,0,2,1,2)
        self.regionbox.valueChanged.connect(self.regionchange)
        for i in range(self.regionbox.value()): #create default number of tables
            for j in range(2):
                self.il6 = QtWidgets.QLineEdit("0.0",self)
                self.il6s[i,j] = self.il6
                self.tab4.layout3.addWidget(self.il6s[i,j],i+1,j)
            self.nbdrop3 = QtWidgets.QComboBox()
            self.nbdrop3.addItems(self.il6info[2:4])
            self.tab4.layout3.addWidget(self.nbdrop3,i+1,2)  
            self.il6 = QtWidgets.QLineEdit("0.0",self)
            self.il6s[i,2] = self.il6
            self.tab4.layout3.addWidget(self.il6s[i,2],i+1,3)
            self.il6s[i,3] = QtWidgets.QCheckBox("R",self)
            self.tab4.layout3.addWidget(self.il6s[i,3],i+1,4)
            self.il6s[i,4] = QtWidgets.QLineEdit("0.0",self)
            self.tab4.layout3.addWidget(self.il6s[i,4],i+1,5)
            
        self.tab4.setLayout(self.tab4.layout3)
        
        #Creates fifth tab
        self.tab5.layout3 = QGridLayout()

        for i in range(self.regionbox.value()): #create default number of tables
            self.il7 = QtWidgets.QLineEdit("0.0",self)
            self.il7s[i,0] = self.il7
            self.tab5.layout3.addWidget(self.il7s[i,0],i+1,0)
            self.nbdrop4 = QtWidgets.QComboBox()
            self.nbdrop4.addItems(self.il7info[:])
            self.tab5.layout3.addWidget(self.nbdrop4,i+1,1)
            for j in range(3):
                self.il7 = QtWidgets.QLineEdit("0.0",self)
                self.il7s[i,j+1] = self.il7
                self.tab5.layout3.addWidget(self.il7s[i,j+1],i+1,j+2)
            
        self.tab5.setLayout(self.tab5.layout3)
            
        # Add tabs to widget        
        self.layout3.addWidget(self.tabs)
        self.stack3.setLayout(self.layout3)
        ####################################################FUNCTIONS#######################################################
        ###################################################################################################################
    def readplot(self): #OPENING AND READING FIGURE IN
        self.figure.clf()

        datafile, __ = QFileDialog.getOpenFileName(self, "Open File","","All Files (*)")
        if datafile:
            datafile = str(datafile)
            spectrum =np.genfromtxt(datafile,dtype=float,comments = "(",skip_header=1,names=True,unpack=True)
            sax = self.figure.add_subplot(111)
            sax.plot(spectrum[spectrum.dtype.names[1]], spectrum[spectrum.dtype.names[2]], '*-') #need controls for one vs. another
            self.canvas.draw()
                  
    
    def ReadLOS(self): #OPENING LOS.DAT FILE TO READ COLUMN HEADERS
        self.aband = ["bb","bf","ff"]
        self.n2band = ["1+", "2+", "BH2", "LBH", "BH1", "WJ", "CY"]
        self.o2band = ["SR"]
        self.noband = ["beta", "gam", "del", "eps", "bp", "gp", "IR"]
        datafile, __ = QFileDialog.getOpenFileName(self, "Open File","","All Files (*)")
        if datafile:
            datafile = str(datafile)
            spectrum =np.genfromtxt(datafile,dtype=None,skip_header=21,names=True)
            self.speclist = spectrum.dtype.names[7:-1]#omitting all of the n, n_total stuff
            self.speclist = [w.replace('_1','+') for w in self.speclist] #erasing the nasty characters and replacing with user-identifiables
            self.speclist.sort() #sort the list
            self.bs = {}  #create dictionary (jus so I can later call on values?)
            self.cs = {}
            self.allcheck = QtWidgets.QCheckBox()
            self.allcheck.clicked.connect(self.checkemalll)    
            self.tab2.layout3.addWidget(self.allcheck,0,1)
            self.tab2.layout3.addWidget(QLabel("Check All Bands"),0,2,1,7,QtCore.Qt.AlignLeft)
            
            #self.allcheck.connect(self.CheckAll) add the check all features!!!!!!!!
            for i in range(len(self.speclist)):

                self.b = QtWidgets.QPushButton(self.speclist[i], self)
                print(self.b.objectName())
                self.bs[i] = self.b 
                self.bs[i].setCheckable(True)
                self.tab2.layout3.addWidget(self.bs[i],i+1, 0)
                if len(self.speclist[i]) == 1:
                    for j in range(3): #making specific bands for atomic molecules (bf, bb, ff)
                        self.c = QtWidgets.QCheckBox(self.aband[j])
                        self.cs[i,j] = self.c
                        self.tab2.layout3.addWidget(self.cs[i,j],i+1,j*2+1)
                if len(self.speclist[i]) == 2 and "+" in self.speclist[i]: #making specific bands for atomic molecules (bf, bb, ff)
                     for j in range(3):
                        self.c = QtWidgets.QCheckBox(self.aband[j])
                        self.cs[i,j] = self.c
                        self.tab2.layout3.addWidget(self.cs[i,j],i+1,j*2+1)
                if "N2" in self.speclist[i]:
                    for j in range(len(self.n2band)):
                        self.c = QtWidgets.QCheckBox(self.n2band[j])
                        self.cs[i,j] = self.c
                        self.tab2.layout3.addWidget(self.cs[i,j],i+1,j*2+1)
                if "O2" in self.speclist[i]:
                    for j in range(len(self.o2band)):
                        self.c = QtWidgets.QCheckBox(self.o2band[j])
                        self.cs[i,j] = self.c
                        self.tab2.layout3.addWidget(self.cs[i,j],i+1,j*2+1)
                if "NO" in self.speclist[i]:
                    for j in range(len(self.noband)):
                        self.c = QtWidgets.QCheckBox(self.noband[j])
                        self.cs[i,j] = self.c
                        self.tab2.layout3.addWidget(self.cs[i,j],i+1,j*2+1)

    def regionchange(self):
        count = self.regionbox.value() #tables want
        print(count)
        clayout = (self.tab4.layout3.count()-1)/6 #widgets have (includes spinbox)
        print(clayout)
        if count < clayout:
            for k in range(6):
                regionToRemove = self.tab4.layout3.itemAtPosition(clayout,k).widget()
                regionToRemove.setParent(None)
                self.tab4.layout3.removeWidget(regionToRemove)
            for kk in range(5):
                lineToRemove = self.tab5.layout3.itemAtPosition(clayout,kk).widget()
                lineToRemove.setParent(None)
                self.tab5.layout3.removeWidget(lineToRemove)              
        elif count > clayout:
            for j in range(2):
                self.il6 = QtWidgets.QLineEdit("0.0",self)
                self.il6s[count,j] = self.il6
                self.tab4.layout3.addWidget(self.il6s[count,j],count,j)
            self.nbdrop3 = QtWidgets.QComboBox()
            self.nbdrop3.addItems(self.il6info[2:4])
            self.tab4.layout3.addWidget(self.nbdrop3,count,2)  
            self.il6 = QtWidgets.QLineEdit("0.0",self)
            self.il6s[count,2] = self.il6
            self.tab4.layout3.addWidget(self.il6s[count,2],count,3)
            self.il6s[count,3] = QtWidgets.QCheckBox("R",self)
            self.tab4.layout3.addWidget(self.il6s[count,3],count,4)
            self.il6s[count,4] = QtWidgets.QLineEdit("0.0",self)
            self.tab4.layout3.addWidget(self.il6s[count,4],count,5)
                
            self.il7 = QtWidgets.QLineEdit("0.0",self)
            self.il7s[count,0] = self.il7
            self.tab5.layout3.addWidget(self.il7s[count,0],count,0)
            self.nbdrop4 = QtWidgets.QComboBox()
            self.nbdrop4.addItems(self.il7info[:])
            self.tab5.layout3.addWidget(self.nbdrop4,count,1)
            for jj in range(3):
                self.il7 = QtWidgets.QLineEdit("0.0",self)
                self.il7s[count,jj+1] = self.il7
                self.tab5.layout3.addWidget(self.il7s[count,jj+1],count,jj+2)
            self.tab5.setLayout(self.tab5.layout3)
        
    def checkemalll(self):
        if self.allcheck.isChecked():
            print("true true")
            self.cs[1,1].setChecked(True) #expand this to the rest of the check boxes
            
    def clearplot(self):
        self.figure.clf()
        self.canvas.draw()
        
    def display(self,i):
        self.Stack.setCurrentIndex(i)
        
class MyHelpWidget(QWidget):        
   def __init__(self, parent):   
        super(QWidget, self).__init__(parent)
        text_edit = QtWidgets.QPlainTextEdit()
        text=open('help.txt').read()
        text_edit.setPlainText(text)
       
def main():
    app = QApplication(sys.argv)
    ex = Window()
    ex.setWindowTitle('NeQtPy v0.1')
    sys.exit(app.exec_())
        
if __name__ == '__main__':
    main()