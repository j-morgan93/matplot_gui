# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 10:03:22 2017

@author: Jonathan Morgan
"""

import sys
import re
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
        
    def openFileNameDialog(self): #MASTER READ CAPABILITY
        name, _ = QFileDialog.getOpenFileName(self, "Open File","","All Files (*);;Input Files (*.inp)")
        if name:
            
            line_num=0
            l_input = {}
            input_text = open(name).read()
            ba = QtCore.QByteArray(input_text.encode('utf-8'))
            input_line = QtCore.QTextStream(ba)
            while input_line.atEnd()==False:
                line1 = input_line.readLine()
                if "---" in line1:
                    line1 = input_line.readLine()
                    if "Line" in line1:
                        line1= input_line.readLine()
                        count=0
                        while re.match('(.)',line1) is not None:
                            l_input['Line'+str(line_num),count]=line1
                            line1= input_line.readLine()
                            count+=1
                        line_num+=1
            temp =l_input['Line0',3]
            del l_input['Line0',1]
            del l_input['Line0',2]
            del l_input['Line0',3]
            l_input['Line0',0] = temp

##should probably create a function that handles the dictionary and           
    def helpFileDialog(self):
        self.helpfile = MyHelpWidget(self)
        
        
    def saveFileDialog(self):   #MASTER WRITE CAPABILITY
        name = QFileDialog.getSaveFileName(self,"Save File","","All Files (*);;Input Files (*.inp)")
        f = open(name[0], 'w')
        f.write("15.0\n")
        f.write("----\n")
        for i in range(len(self.content.il.get('Line2'))):
            if self.content.il['Line2',i].isChecked() == True:
                data = self.content.il2info[i]
                data = data[data.find("(")+1:data.find(")")].split()[0]
                f.write(data)
                if i == 0 or i == 3:
                    data = str(2)
                    f.write(data)
        f.write("\n\n")
        f.write("----\n")
        for i in range(len(self.content.il)):
            if self.content.il[i].isChecked() == True:
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
        self.il = {}
        
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
        tmp_dict = {}
        tmp_dict1 = {}
        for i in range(7): #INPUT LINE 2
            tmp_dict[i,0] = QtWidgets.QCheckBox(self.il2info[i],self)    
            self.tab1.layout3.addWidget(tmp_dict[i,0],i+1,0)
            if "(I)" in self.il2info[i] or "(S)" in self.il2info[i]:
                tmp_dict1[i] = QtWidgets.QCheckBox("Column Format?",self)
                self.tab1.layout3.addWidget(tmp_dict1[i],i+1,2,QtCore.Qt.AlignRight)
                count+=1                
            count+=1   
        self.il['Line2'] = tmp_dict #Creates the OutPut type dictionary section
        self.il['Line2Format'] = tmp_dict1 #creates the file format output type dictionary section
        for i in range(2): #INPUT LINE 3
            tmp_dict[i] = QtWidgets.QCheckBox(self.il3info[i],self)
            self.tab1.layout3.addWidget(tmp_dict[i],count+i+1,0)
            if "Non-B" in self.il3info[i]: #Filling the combo boxes out
                self.nbdrop1 = QtWidgets.QComboBox()
                self.nbdrop1.addItem("--optional--")
                self.nbdrop1.addItems(self.il3info[2:5])
                self.nbdrop2 = QtWidgets.QComboBox()
                self.nbdrop2.addItems(self.il3info[6:9])
                self.tab1.layout3.addWidget(self.nbdrop1,count+i+1,2)
                self.tab1.layout3.addWidget(self.nbdrop2,count+i+1,3)
        for i in range(3): 
            tmp_dict[i+2] = QtWidgets.QCheckBox(self.il3info[i+10],self)
            self.tab1.layout3.addWidget(tmp_dict[i+2],count+i+3,0)           
        self.tab1.setLayout(self.tab1.layout3)
        self.il['Line3'] = tmp_dict #creates the State Pop Method Dictionary section
        
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
            tmp_dict[i] = QtWidgets.QCheckBox(self.il4info[i],self)
            self.tab3.layout3.addWidget(tmp_dict[i],count+i+2,0)
        self.il['Line4'] = tmp_dict #creates the Geometry Section of the dictionary
        for i in range(len(self.il5info)): #INPUT LINE 5
            tmp_dict[i] = QtWidgets.QCheckBox(self.il5info[i],self)
            self.tab3.layout3.addWidget(tmp_dict[i],count+i+2,1)
        self.il['Line5'] = tmp_dict #creates the Boundary Condition section of the dictionary
        self.tab3.setLayout(self.tab3.layout3)
       
        #Create fourth tab
        self.tab4.layout3 = QGridLayout()
        self.regionbox = QtWidgets.QSpinBox(self)
        self.regionbox.setValue(4)
        self.tab4.layout3.addWidget(self.regionbox,0,2,1,2)
        self.regionbox.valueChanged.connect(self.regionchange)
        for i in range(self.regionbox.value()): #create default number of tables
            for j in range(2):
                tmp_dict['lambda',j] = QtWidgets.QLineEdit("0.0",self)
                self.tab4.layout3.addWidget(tmp_dict['lambda',j],i+1,j)
            self.nbdrop3 = QtWidgets.QComboBox()
            self.nbdrop3.addItems(self.il6info[2:4])
            self.tab4.layout3.addWidget(self.nbdrop3,i+1,2)  
            tmp_dict['delta',2] = QtWidgets.QLineEdit("0.0",self)
            self.tab4.layout3.addWidget(tmp_dict['delta',2],i+1,3)
            tmp_dict['range',3] = QtWidgets.QCheckBox("R",self)
            self.tab4.layout3.addWidget(tmp_dict['range',3],i+1,4)
            tmp_dict['range_value',4] = QtWidgets.QLineEdit("0.0",self)
            self.tab4.layout3.addWidget(tmp_dict['range_value',4],i+1,5)
        self.il['Line7'] = tmp_dict #creates the Regions section of the dictionary
        self.tab4.setLayout(self.tab4.layout3)
        
        #Creates fifth tab
        self.tab5.layout3 = QGridLayout()
        for i in range(self.regionbox.value()): #create default number of tables...too
            tmp_dict["delta",0] = QtWidgets.QLineEdit("0.0",self)
            self.tab5.layout3.addWidget(tmp_dict["delta",0],i+1,0)
            self.nbdrop4 = QtWidgets.QComboBox()
            self.nbdrop4.addItems(self.il7info[:])
            self.tab5.layout3.addWidget(self.nbdrop4,i+1,1)
            for j in range(3):
                tmp_dict["scan_params",j+1] = QtWidgets.QLineEdit("0.0",self)
                self.tab5.layout3.addWidget(tmp_dict["scan_params",j+1],i+1,j+2)
        self.il['Line8'] = tmp_dict  #creates the Scan portion of the dictionary. only required for shock tube
        self.tab5.setLayout(self.tab5.layout3)
            
        # Add tabs to widget        
        self.layout3.addWidget(self.tabs)
        self.stack3.setLayout(self.layout3)
        del tmp_dict
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
            self.spec = spectrum.dtype.names[7:-1]#omitting all of the n, n_total stuff
            self.spec = [w.replace('_1','+') for w in self.spec] #erasing the nasty characters and replacing with user-identifiables
            self.spec.sort() #sort the list
            xcount=0
            for i in range(len(self.spec)):
                if "+" not in self.spec[i]:
                    xcount+=1
            self.speclist = [None]*xcount
            print(self.speclist)
            k = 0
            for i in range(len(self.spec)):
                if "+" not in self.spec[i]:           
                    self.speclist[k] = self.spec[i]
                    k+=1
            
            print(self.speclist)
            self.allcheck = QtWidgets.QCheckBox()
            self.allcheck.clicked.connect(self.checkemalll)    
            self.tab2.layout3.addWidget(self.allcheck,0,1)
            self.tab2.layout3.addWidget(QLabel("Check All Bands"),0,2,1,7,QtCore.Qt.AlignLeft)

            tmp_dictb = [None]*len(self.speclist)
            tmp_dictcb = np.empty(shape=(xcount,len(self.n2band)),dtype=object)
            print(tmp_dictcb)
            for i in range(len(self.speclist)):                                        
                    tmp_dictb[i] = QtWidgets.QPushButton(self.speclist[i], self)
                    tmp_dictb[i].setCheckable(True)
                    self.tab2.layout3.addWidget(tmp_dictb[i],i+1, 0)
                    
                    if len(self.speclist[i]) == 1:
                        for j in range(3): #making specific bands for atoms (bf, bb, ff)
                            tmp_dictcb[i,j] = QtWidgets.QCheckBox(self.aband[j])
                            self.tab2.layout3.addWidget(tmp_dictcb[i,j],i+1,j*2+1)
                    if "N2" in self.speclist[i] and len(self.speclist[i]) == 2:
                        for j in range(len(self.n2band)):
                            tmp_dictcb[i,j] = QtWidgets.QCheckBox(self.n2band[j])
                            self.tab2.layout3.addWidget(tmp_dictcb[i,j],i+1,j*2+1)
                    if "O2" in self.speclist[i] and len(self.speclist[i]) == 2:
                        for j in range(len(self.o2band)):
                            tmp_dictcb[i,j] = QtWidgets.QCheckBox(self.o2band[j])
                            self.tab2.layout3.addWidget(tmp_dictcb[i,j],i+1,j*2+1)
                    if "NO" in self.speclist[i] and len(self.speclist[i]) == 2:
                        for j in range(len(self.noband)):
                            tmp_dictcb[i,j] = QtWidgets.QCheckBox(self.noband[j])
                            self.tab2.layout3.addWidget(tmp_dictcb[i,j],i+1,j*2+1)
                    xcount+=1
            self.il['Line6'] = tmp_dictb # The press buttons for each species
            self.il['Line6CB'] = tmp_dictcb # the check buttons for each species
            print(self.il['Line6'])
            print(self.il['Line6CB'])
    def regionchange(self):
        count = self.regionbox.value() #tables want
        clayout = (self.tab4.layout3.count()-1)/6 #widgets have (includes spinbox)
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
                self.il['Line7',count,j] = QtWidgets.QLineEdit("0.0",self)
                self.tab4.layout3.addWidget(self.il['Line7',count,j],count,j)
            self.nbdrop3 = QtWidgets.QComboBox()
            self.nbdrop3.addItems(self.il6info[2:4])
            self.tab4.layout3.addWidget(self.nbdrop3,count,2)  
            self.il['Line7',count,2] = QtWidgets.QLineEdit("0.0",self)
            self.tab4.layout3.addWidget(self.il['Line7',count,2],count,3)
            self.il['Line7',count,3] = QtWidgets.QCheckBox("R",self)
            self.tab4.layout3.addWidget(self.il['Line7',count,3],count,4)
            self.il['Line7',count,4] = QtWidgets.QLineEdit("0.0",self)
            self.tab4.layout3.addWidget(self.il['Line7',count,4],count,5)
                
            self.il['Line8',count,0] = QtWidgets.QLineEdit("0.0",self)
            self.tab5.layout3.addWidget(self.il['Line8',count,0],count,0)
            self.nbdrop4 = QtWidgets.QComboBox()
            self.nbdrop4.addItems(self.il7info[:])
            self.tab5.layout3.addWidget(self.nbdrop4,count,1)
            for jj in range(3):
                self.il['Line8',count,jj+1] = QtWidgets.QLineEdit("0.0",self)
                self.tab5.layout3.addWidget(self.il['Line8',count,jj+1],count,jj+2)
            self.tab5.setLayout(self.tab5.layout3)
        
    def checkemalll(self):
        if self.allcheck.isChecked():
            self.il['Line6CB'][0,1].setChecked(True) #expand this to the rest of the check boxes
            
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
        self.show()
       
def main():
    app = QApplication(sys.argv)
    ex = Window()
    ex.setWindowTitle('NeQtPy v0.1')
    sys.exit(app.exec_())
        
if __name__ == '__main__':
    main()