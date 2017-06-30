# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 10:03:22 2017

@author: Jonathan Morgan
"""

import sys
import re
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import  QWidget, QFormLayout, QStackedWidget, QListWidget, QApplication, QLineEdit, QCheckBox, QLabel, QAction, qApp, QMainWindow, QInputDialog, QFileDialog, QGridLayout

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

    def openFileNameDialog(self): #MASTER READ CAPABILITY (AND POPULATE WIDGETS)
        name, _ = QFileDialog.getOpenFileName(self, "Open File","","All Files (*);;Input Files (*.inp)")
        if name:
            print("Opening Input File:",name)
            line_num=2
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
                        count=1
                        l_input['Line'+str(line_num)] = np.empty(shape=(1,1),dtype='<U25')
                        while re.match('(.)',line1) is not None:
                            tmp=line1.split()
                            for i in range(len(tmp)):
                                tmp[i] = str(tmp[i])
                            l_input['Line'+str(line_num)]=np.resize(l_input['Line'+str(line_num)],[count,len(tmp)])
                            for i in range(len(tmp)):
                                l_input['Line'+str(line_num)][count-1,i]=tmp[i]
                            line1= input_line.readLine()
                            count+=1
                        line_num+=1
            tmp = list(l_input['Line2'][-1,0])
            l_input['Line2'] = np.resize(l_input['Line2'],[1,len(tmp)])
            for ll in range(len(tmp)):
                l_input['Line2'][0,ll] = tmp[ll]
            ###now going to compare the entries in the dictionary to buttons
        for i in range(2,10,1): #starting from line 2
            if l_input['Line'+str(i)] is not None:
                for m in range(len(l_input['Line'+str(i)])):
                    for n in range(len(l_input['Line'+str(i)][m])):
                            print("COLUMNSSSS",'Line'+str(i),l_input['Line'+str(i)][m,n])                            
                            for g in range(len(self.content.il['Line'+str(i)])):
                                print("into g")
                                for h in range(len(self.content.il['Line'+str(i)][g])):
                                    print("into h")
                                    if i != 6:
                                        if i == 3 and self.content.il['Line'+str(i)][1,0].isChecked() == True:
                                            if hasattr(self.content.il['Line'+str(i)][g,h],'currentIndex') and "("+l_input['Line'+str(i)][m,n]+")" in self.content.il['Line'+str(i)][g,h].itemText():
                                                print(l_input['Line'+str(i)][m,n],"trying to go in",self.content.il['Line'+str(i)][g,h].text())
                                                self.content.il['Line'+str(i)][g,h].setChecked(True)
                                        if hasattr(self.content.il['Line'+str(i)][g,h],'setChecked') and "("+l_input['Line'+str(i)][m,n]+")" in self.content.il['Line'+str(i)][g,h].text():
                                            print(l_input['Line'+str(i)][m,n],"trying to go in",self.content.il['Line'+str(i)][g,h].text())
                                            self.content.il['Line'+str(i)][g,h].setChecked(True)
                            
                                
    def helpFileDialog(self):
        self.helpfile = MyHelpWidget(self)


    def saveFileDialog(self):   #MASTER WRITE CAPABILITY
        name = QFileDialog.getSaveFileName(self,"Save File","","All Files (*);;Input Files (*.inp)")
        print("Writing out to:",name[0])
        f = open(name[0], 'w')
        f.write("15.0\n*******\n")
        f.write("Line 0: Header - anything between here and the ---'s writes to stdout\n\
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa <- 1st format line\n\
--------------------------\n\
/share/apps/neqair/v15.0-prerelease/DATABASES")
        for i in range(len(self.content.il['Line2'])):
            for j in range(2):
                if hasattr(self.content.il['Line2'][i,j],'setChecked') and self.content.il['Line2'][i,j].isChecked()==True:
                    data = self.content.il['Line2'][i,j].text()
                    data = data[data.find("(")+1:data.find(")")].split()[0]
                    f.write(data)
        print("Filetype Written")
        f.write("\n\n")
        f.write("----\n")
        for i in range(len(self.content.il['Line3'])):
            for j in range(3):
                if hasattr(self.content.il['Line3'][i,j],'setChecked') and self.content.il['Line3'][i,j].isChecked() == True:
                    data = self.content.il3info[i]
                    data = data[data.find("(")+1:data.find(")")].split()[0]
                    f.write(data)
                    if "Non" in self.content.il['Line3'][i,j].text() and self.content.il['Line3'][i,j].isChecked() == True:
                        if self.content.il['Line3'][i,1].currentIndex() != 0:
                            ind = self.content.il['Line3'][i,1].currentIndex()
                            data = self.content.il['Line3'][i,1].itemText(ind)
                            data = data[data.find("(")+1:data.find(")")].split()[0]
                            f.write(" "+data)
                            ind = self.content.il['Line3'][i,2].currentIndex()
                            data = self.content.il['Line3'][i,2].itemText(ind)
                            data = data[data.find("(")+1:data.find(")")].split()[0]
                            f.write(" "+data)
                            f.write("\n")
        print("State Pop Method Written")
        f.write("\n\n")
        f.write("----\n")
        for i in range(len(self.content.il['Line4'])):
            if hasattr(self.content.il['Line4'][i,0],'setChecked') and self.content.il['Line4'][i,0].isChecked() == True:
                data = self.content.il4info[i]
                data = data[data.find("(")+1:data.find(")")].split()[0]
                f.write(data)
        f.write("\n\n")
        f.write("----\n")
        print("Geometry Written")
        for i in range(len(self.content.il['Line5'])):
            if hasattr(self.content.il['Line5'][i,0],'setChecked') and self.content.il['Line5'][i,0].isChecked() == True:
                data = self.content.il5info[i]
                data = data[data.find("(")+1:data.find(")")].split()[0]
                f.write(data)
        print("Boundary Written")
        f.write("\n\n")
        f.write("----\n")
        for i in range(len(self.content.speclist)):
            if hasattr(self.content.il['Line6'][i],'setChecked') and self.content.il['Line6'][i].isChecked() == True:
                print("Writing",self.content.il['Line6'][i].text())
                filedata =self.content.il['Line6'][i].text()
                f.write(filedata)
                if len(self.content.il['Line6'][i].text()) == 1:
                    for j in range(len(self.content.aband)):
                        if self.content.il['Line6CB'][i,j].isChecked() == True:
                            f.write(" "+self.content.il['Line6CB'][i,j].text())
                    f.write("\n")
                if "NO" in self.content.il['Line6'][i].text():
                    for j in range(len(self.content.noband)):
                        if self.content.il['Line6CB'][i,j].isChecked() == True:
                            f.write(" "+self.content.il['Line6CB'][i,j].text())
                    f.write("\n")
                if "N2" in self.content.il['Line6'][i].text():
                    for j in range(len(self.content.n2band)):
                        if self.content.il['Line6CB'][i,j].isChecked() == True:
                            f.write(" "+self.content.il['Line6CB'][i,j].text())
                    f.write("\n")
                if "O2" in self.content.il['Line6'][i].text():
                    for j in range(len(self.content.o2band)):
                        if self.content.il['Line6CB'][i,j].isChecked() == True:
                            f.write(" "+self.content.il['Line6CB'][i,j].text())
                    f.write("\n")
        print("Species Bands Written")
        f.write("\n")
        f.write("----\n")
        for i in range(self.content.regionbox.value()):
            if self.content.il['Line7'][i,0].text() != "0.0":
                for j in range(len(self.content.il['Line7'][0,:])-1):
                    if hasattr(self.content.il['Line7'][i,j],'text') and not hasattr(self.content.il['Line7'][i,j],'isChecked'):
                        dataw1w2 = self.content.il['Line7'][i,j].text()
                        f.write(" "+dataw1w2)
                    if hasattr(self.content.il['Line7'][i,j],'currentIndex'):
                        ind = self.content.il['Line7'][i,j].currentIndex()
                        dataam = self.content.il['Line7'][i,j].itemText(ind)
                        f.write(" "+dataam)
                    if hasattr(self.content.il['Line7'][i,j],'isChecked') and self.content.il['Line7'][i,j].isChecked() == True:
                        f.write(" R "+self.content.il['Line7'][i,j+1].text())
                f.write("\n")
        print("Regions Written")
        f.write("\n")
        f.write("----\n")
        for i in range(self.content.regionbox.value()):
            if self.content.il['Line8'][i,0].text() != "0.0":
                for j in range(len(self.content.il['Line8'][0,:])):
                    if hasattr(self.content.il['Line8'][i,j],'text'):
                        dataw1w2 = self.content.il['Line8'][i,j].text()
                        f.write(" "+dataw1w2)
                    if hasattr(self.content.il['Line8'][i,j],'currentIndex'):
                        ind = self.content.il['Line8'][i,j].currentIndex()
                        dataam = self.content.il['Line8'][i,j].itemText(ind)
                        f.write(" "+dataam)
                f.write("\n")
        print("Scan Written")
        f.write("\n")
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
        self.tab6 = QWidget()

        self.tabs.addTab(self.tab1,"File Setup") # Add tabs
        self.tabs.addTab(self.tab2,"Species Information")
        self.tabs.addTab(self.tab3,"Geometry \& Boundary Conditions")
        self.tabs.addTab(self.tab4,"Regions")
        self.tabs.addTab(self.tab5,"Scan Style")
        self.tabs.addTab(self.tab6,"Spatial Scan")


       # Create first tab - Generic File information (sim type and such)
        self.tab1.layout3 = QGridLayout()
        count = 0
        tmp_arr = np.empty(shape=(len(self.il2info),2),dtype=object)
        for i in range(7): #INPUT LINE 2
            tmp_arr[i,0] = QtWidgets.QCheckBox(self.il2info[i],self)
            self.tab1.layout3.addWidget(tmp_arr[i,0],i+1,0)
            if "(I)" in self.il2info[i] or "(S)" in self.il2info[i]:
                tmp_arr[i,1] = QtWidgets.QCheckBox("(2)Column Format?",self)
                self.tab1.layout3.addWidget(tmp_arr[i,1],i+1,2,QtCore.Qt.AlignRight)
                count+=1
            count+=1
        self.il['Line2'] = tmp_arr #Creates the OutPut type dictionary section
        print("created FileOutput")
        tmp_arr = np.empty(shape=(5,3),dtype=object)
        for i in range(5): #INPUT LINE 3
            if i < 2:
                tmp_arr[i,0] = QtWidgets.QCheckBox(self.il3info[i],self)
                self.tab1.layout3.addWidget(tmp_arr[i,0],count+i+1,0)
                if "Non-B" in self.il3info[i]: #Filling the combo boxes out and adding to dict
                    tmp_arr[i,1] = QtWidgets.QComboBox()
                    tmp_arr[i,1].addItem("--optional--")
                    tmp_arr[i,1].addItems(self.il3info[2:5])
                    tmp_arr[i,2] = QtWidgets.QComboBox()
                    tmp_arr[i,2].addItems(self.il3info[6:9])
                    self.tab1.layout3.addWidget(tmp_arr[i,1],count+i+1,2)
                    self.tab1.layout3.addWidget(tmp_arr[i,2],count+i+1,3)
            if i >= 2:
                tmp_arr[i,0]= QtWidgets.QCheckBox(self.il3info[i+8],self)
                self.tab1.layout3.addWidget(tmp_arr[i,0],count+i+1,0)
        self.tab1.setLayout(self.tab1.layout3)
        self.il['Line3'] = tmp_arr #creates the State Pop Method Dictionary section
        print("created State Population")

        #---- Create second tab
        self.tab2.layout3 = QGridLayout()
        self.losopen = QtWidgets.QPushButton("Read LOS")
        self.losopen.clicked.connect(self.ReadLOS) #define the button's functionality
        self.tab2.layout3.addWidget(self.losopen,0,0)
        self.tab2.setLayout(self.tab2.layout3)

        #---- Create third tab
        self.tab3.layout3 = QGridLayout()
        self.tab3.layout3.addWidget(QLabel("GEOMETRY"),0,0,QtCore.Qt.AlignTop)
        self.tab3.layout3.addWidget(QLabel("BOUNDARY CONDITIONS"),0,1,QtCore.Qt.AlignTop)
        tmp_arr = np.empty(shape=(len(self.il4info),1),dtype=object)
        for i in range(len(self.il4info)): #INPUT LINE 4
            tmp_arr[i,0] = QtWidgets.QCheckBox(self.il4info[i],self)
            self.tab3.layout3.addWidget(tmp_arr[i,0],count+i+2,0)
        self.il['Line4'] = tmp_arr #creates the Geometry Section of the dictionary
        tmp_arr = np.empty(shape=(len(self.il5info),1),dtype=object)
        for i in range(len(self.il5info)): #INPUT LINE 5
            tmp_arr[i,0] = QtWidgets.QCheckBox(self.il5info[i],self)
            self.tab3.layout3.addWidget(tmp_arr[i,0],count+i+2,1)
        self.il['Line5'] = tmp_arr #creates the Boundary Condition section of the dictionary
        self.tab3.setLayout(self.tab3.layout3)
        print("created Boundary/Geometry")

        #---- Create fourth tab
        self.tab4.layout3 = QGridLayout()
        self.regionbox = QtWidgets.QSpinBox(self)
        self.regionbox.setValue(4)
        self.tab4.layout3.addWidget(self.regionbox,0,0,1,6)
        self.regionbox.valueChanged.connect(self.regionchange)

        tmp_arr = np.empty(shape=(self.regionbox.value(),6),dtype=object)
        for i in range(self.regionbox.value()): #create default number of tables
            for j in range(6):
                if j<2 or j ==3 or j == 5:
                    tmp_arr[i,j] = QtWidgets.QLineEdit("0.0",self)
                    self.tab4.layout3.addWidget(tmp_arr[i,j],i+1,j)
                if j ==2:
                    tmp_arr[i,j] = QtWidgets.QComboBox()
                    tmp_arr[i,j].addItems(self.il6info[2:4])
                    self.tab4.layout3.addWidget(tmp_arr[i,j],i+1,j)
                if j ==4:
                    tmp_arr[i,j] = QtWidgets.QCheckBox("R",self)
                    self.tab4.layout3.addWidget(tmp_arr[i,j],i+1,j)
        self.il['Line7'] = tmp_arr #creates the Regions section of the dictionary
        self.tab4.setLayout(self.tab4.layout3)
        print("created Regions")

        #---- Creates fifth tab
        self.tab5.layout3 = QGridLayout()
        tmp_arr1 = np.empty(shape=(self.regionbox.value(),5),dtype=object)
        for i in range(self.regionbox.value()): #create default number of tables...too
            tmp_arr1[i,0] = QtWidgets.QLineEdit("0.0",self)
            self.tab5.layout3.addWidget(tmp_arr1[i,0],i+1,0)
            tmp_arr1[i,1] = QtWidgets.QComboBox()
            tmp_arr1[i,1].addItems(self.il7info[:])
            self.tab5.layout3.addWidget(tmp_arr1[i,1],i+1,1)
            for j in range(3):
                tmp_arr1[i,j+2] = QtWidgets.QLineEdit("0.0",self)
                self.tab5.layout3.addWidget(tmp_arr1[i,j+2],i+1,j+2)
        self.il['Line8'] = tmp_arr1  #creates the Scan portion of the dictionary. only required for shock tube
        self.tab5.setLayout(self.tab5.layout3)
        print("created Scan")

        #---- Creates sixth tab
        self.tab6.layout3 = QGridLayout()
        tmp_arr1 = np.empty(shape=(self.regionbox.value(),3),dtype=object)

        tmp_arr1[0,0] = QtWidgets.QComboBox()
        tmp_arr1[0,0].addItem('Triangle')
        tmp_arr1[0,0].addItem('Trapezoid')
        self.tab6.layout3.addWidget(tmp_arr1[0,0],0,0)
        tmp_arr1[0,1] = QtWidgets.QLineEdit("0.0",self)
        self.tab6.layout3.addWidget(tmp_arr1[0,1],0,1)
        tmp_arr1[0,2] = QtWidgets.QLineEdit("0.0",self)
        self.tab6.layout3.addWidget(tmp_arr1[0,2],0,2)
        tmp_arr1[1,0] = QtWidgets.QComboBox()
        tmp_arr1[1,0].addItems(self.il7info[:])
        self.tab6.layout3.addWidget(tmp_arr1[1,0],1,0)
        tmp_arr1[1,1] = QtWidgets.QLineEdit("0.0",self)
        self.tab6.layout3.addWidget(tmp_arr1[1,1],1,1)
        tmp_arr1[1,2] = QtWidgets.QLineEdit("0.0",self)
        self.tab6.layout3.addWidget(tmp_arr1[1,2],1,2)
        tmp_arr1[2,0] = QtWidgets.QLineEdit("0.0",self)
        self.tab6.layout3.addWidget(tmp_arr1[2,0],2,0)
        self.il['Line9'] = tmp_arr1  #creates the Scan portion of the dictionary. only required for shock tube
        self.tab6.setLayout(self.tab6.layout3)
        print("created Spatial Scan")

        # Add tabs to widget
        self.layout3.addWidget(self.tabs)
        self.stack3.setLayout(self.layout3)
        del tmp_arr, tmp_arr1

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
            print("Opening LOS File:",datafile)
            datafile = str(datafile)
            spectrum =np.genfromtxt(datafile,dtype=None,skip_header=21,names=True)
            self.spec = spectrum.dtype.names[7:-1]#omitting all of the n, n_total stuff
            self.spec = [w.replace('_1','+') for w in self.spec] #erasing the nasty characters and replacing with user-identifiables
            self.spec.sort() #sort the list

            #################### This next little piece of code is dumb and inefficient, should replace with something more elegant
            xcount=0
            for i in range(len(self.spec)):
                if "+" not in self.spec[i]:
                    xcount+=1
            self.speclist = [None]*xcount
            k = 0
            for i in range(len(self.spec)):
                if "+" not in self.spec[i]:
                    self.speclist[k] = self.spec[i]
                    k+=1
            ###################
            self.allcheck = QtWidgets.QCheckBox()
            self.allcheck.clicked.connect(self.checkemalll)
            self.tab2.layout3.addWidget(self.allcheck,0,1)
            self.tab2.layout3.addWidget(QLabel("Check All Bands"),0,2,1,7,QtCore.Qt.AlignLeft)

            tmp_arrb = [None]*len(self.speclist)
            tmp_arrcb = np.empty(shape=(xcount,len(self.n2band)),dtype=object)
            for i in range(len(self.speclist)):
                    tmp_arrb[i] = QtWidgets.QPushButton(self.speclist[i], self)
                    tmp_arrb[i].setCheckable(True)
                    self.tab2.layout3.addWidget(tmp_arrb[i],i+1, 0)

                    if len(self.speclist[i]) == 1:
                        for j in range(3): #making specific bands for atoms (bf, bb, ff)
                            tmp_arrcb[i,j] = QtWidgets.QCheckBox(self.aband[j])
                            self.tab2.layout3.addWidget(tmp_arrcb[i,j],i+1,j*2+1)
                    if "N2" in self.speclist[i] and len(self.speclist[i]) == 2:
                        for j in range(len(self.n2band)):
                            tmp_arrcb[i,j] = QtWidgets.QCheckBox(self.n2band[j])
                            self.tab2.layout3.addWidget(tmp_arrcb[i,j],i+1,j*2+1)
                    if "O2" in self.speclist[i] and len(self.speclist[i]) == 2:
                        for j in range(len(self.o2band)):
                            tmp_arrcb[i,j] = QtWidgets.QCheckBox(self.o2band[j])
                            self.tab2.layout3.addWidget(tmp_arrcb[i,j],i+1,j*2+1)
                    if "NO" in self.speclist[i] and len(self.speclist[i]) == 2:
                        for j in range(len(self.noband)):
                            tmp_arrcb[i,j] = QtWidgets.QCheckBox(self.noband[j])
                            self.tab2.layout3.addWidget(tmp_arrcb[i,j],i+1,j*2+1)
                    xcount+=1
            self.il['Line6'] = tmp_arrb # The press buttons for each species
            self.il['Line6CB'] = tmp_arrcb # the check buttons for each species

    def regionchange(self):
        count = self.regionbox.value() #tables want
        clayout = int((self.tab4.layout3.count()-1)/6) #widgets have (includes spinbox)
        print("count is: ",count,"clayout is: ",clayout)
        if count < clayout:
            for k in range(6):
                self.il['Line7'][clayout-1,k] = None #the spacing is offset from that array loc by 1
                regionToRemove = self.tab4.layout3.itemAtPosition(clayout,k).widget()
                regionToRemove.setParent(None)
                self.tab4.layout3.removeWidget(regionToRemove)
            for kk in range(5):
                self.il['Line8'][clayout-1,kk] = None
                lineToRemove = self.tab5.layout3.itemAtPosition(clayout,kk).widget()
                lineToRemove.setParent(None)
                self.tab5.layout3.removeWidget(lineToRemove)
        elif count > clayout:
            self.il['Line7'] = np.resize(self.il['Line7'],[count,len(self.il6info)-1])
            for j in range(6):
                if j<2 or j ==3 or j == 5:
                    self.il['Line7'][count-1,j] = QtWidgets.QLineEdit("0.0",self)
                    self.tab4.layout3.addWidget(self.il['Line7'][count-1,j],count,j)
                if j ==2:
                    self.il['Line7'][count-1,j] = QtWidgets.QComboBox()
                    self.il['Line7'][count-1,j].addItems(self.il6info[2:4])
                    self.tab4.layout3.addWidget(self.il['Line7'][count-1,j],count,j)
                if j ==4:
                    self.il['Line7'][count-1,j] = QtWidgets.QCheckBox("R",self)
                    self.tab4.layout3.addWidget(self.il['Line7'][count-1,j],count,j)
            self.tab4.setLayout(self.tab4.layout3)

            self.il['Line8'] = np.resize(self.il['Line8'],[count,5])
            self.il['Line8'][count-1,0] = QtWidgets.QLineEdit("0.0",self)
            self.tab5.layout3.addWidget(self.il['Line8'][count-1,0],count,0)
            self.il['Line8'][count-1,0] = QtWidgets.QComboBox()
            self.il['Line8'][count-1,0].addItems(self.il7info[:])
            self.tab5.layout3.addWidget(self.il['Line8'][count-1,0],count,1)
            for j in range(3):
                self.il['Line8'][count-1,j+2] = QtWidgets.QLineEdit("0.0",self)
                self.tab5.layout3.addWidget(self.il['Line8'][count-1,j+2],count,j+2)
            self.tab5.setLayout(self.tab5.layout3)

    def checkemalll(self):
        if self.allcheck.isChecked():
            for i in range(len(self.speclist)):
                self.il['Line6'][i].setChecked(True)
                for j in range(len(self.n2band)):
                    if hasattr(self.il['Line6CB'][i,j],'setChecked'):
                        self.il['Line6CB'][i,j].setChecked(True)

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