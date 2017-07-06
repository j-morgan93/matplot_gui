# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 10:03:22 2017

@author: Jonathan Morgan
"""

import sys
import re
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QStackedWidget, QListWidget, QApplication,\
 QLineEdit, QCheckBox, QLabel, QAction, QMainWindow, QFileDialog, QGridLayout, QVBoxLayout

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()

    def initUI(self):
        # defining the exitting, saving and opening of files
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

    def openFileNameDialog(self):  # MASTER READ CAPABILITY(AND POPULATE WIDGETS)
        name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files(*);;Input Files(*.inp)")
        if name:
            # reading in the file then going to compare to existing dictionary keys
            print("Opening Input File:", name)
            line_num = 2
            l_input = {}
            input_text = open(name).read()
            ba = QtCore.QByteArray(input_text.encode('utf-8'))
            input_line = QtCore.QTextStream(ba)
            while input_line.atEnd() is False:
                line1 = input_line.readLine()
                if "---" in line1:
                    line1 = input_line.readLine()
                    if "Line" in line1:
                        line1 = input_line.readLine()
                        count = 0
                        l_input['Line'+str(line_num)] = np.empty(shape=(1, 1), dtype='<U25')
                        print("LINE"+str(line_num)," BEFORE WHILE",line1)
                        while re.match('(.)', line1) is not None:
                            tmp=line1.split()
                            for i in range(len(tmp)):
                                tmp[i] = str(tmp[i])
                            if count > 0 and len(tmp) != len(l_input['Line'+str(line_num)][count-1]):
                                if len(tmp) > len(l_input['Line'+str(line_num)][count-1]):
                                    print("MORE")
                                    dif = len(tmp) - len(l_input['Line'+str(line_num)][count-1])
                                    t = np.pad(l_input['Line'+str(line_num)][0:count-1], ((0,0),(0,dif)), 'constant',constant_values=(0,))
                                    l_input['Line'+str(line_num)] = t
                                    l_input['Line'+str(line_num)]=np.resize(l_input['Line'+str(line_num)], [count+1, len(tmp)])
                                    for i in range(len(tmp)):
                                        l_input['Line'+str(line_num)][count, i]=tmp[i]
                                    print("CHANGED",l_input['Line'+str(line_num)])
                                elif len(tmp) < len(l_input['Line'+str(line_num)][count-1]):
                                    print("LESS")
                                    w = len(l_input['Line'+str(line_num)][count-1])
                                    l_input['Line'+str(line_num)] = np.resize(l_input['Line'+str(line_num)], [count+1, w])
                                    for i in range(len(tmp)):
                                        l_input['Line'+str(line_num)][count, i]=tmp[i]
                                    print("CHANGED",l_input['Line'+str(line_num)])
                            else:
                                l_input['Line'+str(line_num)]=np.resize(l_input['Line'+str(line_num)], [count+1, len(tmp)])
                                for i in range(len(tmp)):
                                    l_input['Line'+str(line_num)][count, i]=tmp[i]
                                    print("LINPUT"+str(line_num)," =", l_input['Line'+str(line_num)][count, i], count, i)
                            line1 = input_line.readLine()
                            print("LINE"+str(line_num)," IN WHILE", line1)                
                            count += 1
                        line_num += 1
                        print(l_input)
            tmp = list(l_input['Line2'][-1, 0])
            l_input['Line2'] = np.resize(l_input['Line2'], [1, len(tmp)])
            for ll in range(len(tmp)):
                l_input['Line2'][0, ll] = tmp[ll]
            # SHOULD TRY TO MODULARIZE THIS AND GNERALIZE FOR GETTING THE INPUTS WHERE THEY NEED TO GO
            # now going to compare the entries in the dictionary to buttons
        for i in range(2, len(l_input)+2, 1):  # starting from line 2
            if l_input['Line'+str(i)] is not None:                           
                if i > 6:
                    if i == 7:
                        self.content.regionbox.setValue(len(l_input['Line'+str(i)]))
                    for g in range(len(self.content.il['Line'+str(i)])):  # for the range of the input line dictionary
                        for h in range(len(self.content.il['Line'+str(i)][g])):
                            print("IN IL THERE IS: ",self.content.il['Line'+str(i)][g, h], "at", g, "and", h)
                            try:
                                if l_input['Line'+str(i)][g, h] is not None:
                                    if "QLineEdit" in str(self.content.il['Line'+str(i)][g, h]) and any(char.isdigit() for char in l_input['Line'+str(i)][g, h]) is True:
                                        self.content.il['Line'+str(i)][g, h].setText(l_input['Line'+str(i)][g, h])
                                        print("set",l_input['Line'+str(i)][g, h],"in QLineEdit")
                                    elif hasattr(self.content.il['Line'+str(i)][g, h], 'currentIndex') is True:
                                        for k in range(self.content.il['Line'+str(i)][g, h].count()):
                                            if l_input['Line'+str(i)][g, h] in self.content.il['Line'+str(i)][g, h].itemText(k):
                                                self.content.il['Line'+str(i)][g, h].setCurrentIndex(k)
                                                print("set",l_input['Line'+str(i)][g, h],"in QComboBox")
                                    elif "QCheckBox" in str(self.content.il['Line'+str(i)][g, h]) and l_input['Line'+str(i)][g, h] is not None:
                                        self.content.il['Line'+str(i)][g, h].setChecked(True)
                                        self.content.il['Line'+str(i)][g, h+1].setText(l_input['Line'+str(i)][g, h+1])
                                        print("set",l_input['Line'+str(i)][g, h],"in QCheckBox")
                            except:
                                print("READ DID NOT FIND ENTRIES AT: OR FIELD DOES NOT EXIST", g, h)
                if i < 6:
                    for m in range(len(l_input['Line'+str(i)])):  # for the range of the input line dictionary
                         for n in range(len(l_input['Line'+str(i)][m])):
                             for g in range(len(self.content.il['Line'+str(i)])):  # for the range of the existing dictionary and corresonding lines
                                 for h in range(len(self.content.il['Line'+str(i)][g])):
                                     if i == 3 and self.content.il['Line'+str(i)][1, 0].isChecked() is True:
                                         if hasattr(self.content.il['Line'+str(i)][g, h], 'currentIndex'):
                                             for k in range(self.content.il['Line'+str(i)][g, h].count()):
                                                 if "("+l_input['Line'+str(i)][m, n]+")" in self.content.il['Line'+str(i)][g, h].itemText(k):
                                                     self.content.il['Line'+str(i)][g, h].setCurrentIndex(k)
                                                     print("COMBO DONE")
                                     elif "QCheckBox" in str(self.content.il['Line'+str(i)][g, h]) and "("+l_input['Line'+str(i)][m, n]+")" in self.content.il['Line'+str(i)][g, h].text():
                                         print(l_input['Line'+str(i)][m, n], "trying to go in", self.content.il['Line'+str(i)][g, h].text())
                                         self.content.il['Line'+str(i)][g, h].setChecked(True)
                                         print("CHECK DONE")
                                                

    def helpFileDialog(self):
        self.helpfile = MyHelpWidget(self)

    def saveFileDialog(self):  # MASTER WRITE CAPABILITY
        name = QFileDialog.getSaveFileName(self, "Save File", "", "All Files(*);;Input Files(*.inp)")
        print("Writing out to:", name[0])
        f = open(name[0], 'w')
        f.write("15.0\n*******\n")
        f.write("Line 0: Header - anything between here and the ---'s writes to stdout\n\
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa <- 1st format line\n\
--------------------------\n\
                /share/apps/neqair/v15.0-prerelease/DATABASES")
        for i in range(len(self.content.il['Line2'])):
            for j in range(2):
                if hasattr(self.content.il['Line2'][i, j], 'setChecked') and self.content.il['Line2'][i, j].isChecked() is True:
                    data = self.content.il['Line2'][i, j].text()
                    data = data[data.find("(")+1:data.find(")")].split()[0]
                    f.write(data)
        print("Filetype Written")
        f.write("\n\n")
        f.write("----\n")
        for i in range(len(self.content.il['Line3'])):
            for j in range(3):
                if hasattr(self.content.il['Line3'][i, j], 'setChecked') and self.content.il['Line3'][i, j].isChecked() is True:
                    data = self.content.il3info[i]
                    data = data[data.find("(")+1:data.find(")")].split()[0]
                    f.write(data)
                    if "Non" in self.content.il['Line3'][i, j].text() and self.content.il['Line3'][i, j].isChecked() is True:
                        if self.content.il['Line3'][i,1].currentIndex() != 0:
                            ind = self.content.il['Line3'][i, 1].currentIndex()
                            data = self.content.il['Line3'][i, 1].itemText(ind)
                            data = data[data.find("(")+1:data.find(")")].split()[0]
                            f.write(" "+data)
                            ind = self.content.il['Line3'][i, 2].currentIndex()
                            data = self.content.il['Line3'][i, 2].itemText(ind)
                            data = data[data.find("(")+1:data.find(")")].split()[0]
                            f.write(" "+data)
                            f.write("\n")
        print("State Pop Method Written")
        f.write("\n\n")
        f.write("----\n")
        for i in range(len(self.content.il['Line4'])):
            if hasattr(self.content.il['Line4'][i, 0], 'setChecked') and self.content.il['Line4'][i, 0].isChecked() is True:
                data = self.content.il4info[i]
                data = data[data.find("(")+1:data.find(")")].split()[0]
                f.write(data)
        f.write("\n\n")
        f.write("----\n")
        print("Geometry Written")
        for i in range(len(self.content.il['Line5'])):
            if hasattr(self.content.il['Line5'][i, 0], 'setChecked')\
            and self.content.il['Line5'][i, 0].isChecked() is True:
                data = self.content.il5info[i]
                data = data[data.find("(")+1:data.find(")")].split()[0]
                f.write(data)
        print("Boundary Written")
        f.write("\n\n")
        f.write("----\n")
        for i in range(len(self.content.speclist)):
            if hasattr(self.content.il['Line6'][i], 'setChecked') and self.content.il['Line6'][i].isChecked() is True:
                print("Writing", self.content.il['Line6'][i].text())
                filedata =self.content.il['Line6'][i].text()
                f.write(filedata)
                if len(self.content.il['Line6'][i].text()) == 1:
                    for j in range(len(self.content.aband)):
                        if self.content.il['Line6CB'][i, j].isChecked() is True:
                            f.write(" "+self.content.il['Line6CB'][i, j].text())
                    f.write("\n")
                if "NO" in self.content.il['Line6'][i].text():
                    for j in range(len(self.content.noband)):
                        if self.content.il['Line6CB'][i, j].isChecked() is True:
                            f.write(" "+self.content.il['Line6CB'][i, j].text())
                    f.write("\n")
                if "N2" in self.content.il['Line6'][i].text():
                    for j in range(len(self.content.n2band)):
                        if self.content.il['Line6CB'][i, j].isChecked() is True:
                            f.write(" "+self.content.il['Line6CB'][i, j].text())
                    f.write("\n")
                if "O2" in self.content.il['Line6'][i].text():
                    for j in range(len(self.content.o2band)):
                        if self.content.il['Line6CB'][i, j].isChecked() is True:
                            f.write(" "+self.content.il['Line6CB'][i, j].text())
                    f.write("\n")
        print("Species Bands Written")
        f.write("\n")
        f.write("----\n")
        for i in range(self.content.regionbox.value()):
            if self.content.il['Line7'][i,0].text() != "0.0":
                for j in range(len(self.content.il['Line7'][0, :])-1):
                    if hasattr(self.content.il['Line7'][i, j], 'text') and not hasattr(self.content.il['Line7'][i, j], 'isChecked'):
                        dataw1w2 = self.content.il['Line7'][i, j].text()
                        f.write(" "+dataw1w2)
                    if hasattr(self.content.il['Line7'][i, j], 'currentIndex'):
                        ind = self.content.il['Line7'][i, j].currentIndex()
                        dataam = self.content.il['Line7'][i, j].itemText(ind)
                        f.write(" "+dataam)
                    if hasattr(self.content.il['Line7'][i, j], 'isChecked') and self.content.il['Line7'][i, j].isChecked() is True:
                        f.write(" R "+self.content.il['Line7'][i, j+1].text())
                f.write("\n")
        print("Regions Written")
        f.write("\n")
        f.write("----\n")
        for i in range(self.content.regionbox.value()):
            if self.content.il['Line8'][i,0].text() != "0.0":
                for j in range(len(self.content.il['Line8'][0, :])):
                    if hasattr(self.content.il['Line8'][i, j], 'text'):
                        dataw1w2 = self.content.il['Line8'][i, j].text()
                        f.write(" "+dataw1w2)
                    if hasattr(self.content.il['Line8'][i, j], 'currentIndex'):
                        ind = self.content.il['Line8'][i, j].currentIndex()
                        dataam = self.content.il['Line8'][i, j].itemText(ind)
                        f.write(" "+dataam)
                f.write("\n")
        print("Scan Written")
        f.write("\n")
        f.write("----\n")
        f.close()
        # write all variables out first and then format one f.write function
        # this may cut down on the cost of the things.

class Widgettown(QWidget):  # WHERE ALL OF THE FUNCTIONALITY IS LOCATED
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.speclist = None
        self.fontss = QtGui.QFont()
        self.fontss.setBold(True)
        self.leftlist = QListWidget()
        self.leftlist.insertItem(0, 'Plots')
        self.leftlist.insertItem(1, 'Spectral Fit - Generate LOS file')
        self.leftlist.insertItem(2, 'NEQAIR Simulation Input')

        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()

        self.stack1UI()
        self.stack2UI()
        self.stack3UI()

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
        self.Stack.addWidget(self.stack3)

        hbox = QtWidgets.QHBoxLayout(self)
        hbox.addWidget(self.leftlist)
        hbox.addWidget(self.Stack)

        self.setLayout(hbox)
        self.leftlist.currentRowChanged.connect(self.display)
        self.show()

    def stack1UI(self):  # THE PLOTTING CAPABILITY

        # figure painting from matplot
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # toolbar addition
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.show()

        # some buttons for functionality
        self.button = QtWidgets.QPushButton('ReadPlot')
        self.button.clicked.connect(self.readplot)
        self.colchange1 = QtWidgets.QComboBox()
        self.colchange1.currentIndexChanged.connect(self.newplot)  # make new plot function
        self.colchange2 = QtWidgets.QComboBox()
        self.colchange2.currentIndexChanged.connect(self.newplot)  # make new plot function
        self.button2 = QtWidgets.QPushButton('ClearPlot')
        self.button2.clicked.connect(self.figure.clear)

        layout = QtWidgets.QVBoxLayout()
        glayout = QGridLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        glayout.addWidget(self.button,0,0)
        glayout.addWidget(self.button2,0,1)
        glayout.addWidget(self.colchange1,1,0)
        glayout.addWidget(self.colchange2,1,1)
        layout.addLayout(glayout)
        self.stack1.setLayout(layout)

    def stack2UI(self):  # THE LOS DATA CAPABILITY
        layout = QGridLayout()
        layout.setColumnStretch(1, 6)
        layout.setColumnStretch(2, 6)

        # temps
        layout.addWidget(QLineEdit(), 1, 4)
        layout.addWidget(QLineEdit(), 2, 4)
        layout.addWidget(QLineEdit(), 3, 4)
        layout.addWidget(QLabel("T_trans"), 1, 3, QtCore.Qt.AlignCenter)
        layout.addWidget(QLabel("T_vib"), 2, 3, QtCore.Qt.AlignCenter)
        layout.addWidget(QLabel("T_el"), 3, 3, QtCore.Qt.AlignCenter)
        layout.addWidget(QCheckBox(), 4, 4)
        layout.addWidget(QLabel("T-Temp Model"), 4, 3)

        # number densities
        linedits = {}
        if self.speclist:
            for i in range(len(self.speclist)):
                self.mylinedit = QtWidgets.QLineEdit("0.0")
                linedits[i] = self.mylinedit
                layout.addWidget(linedits[i], i, 1)
                layout.addWidget(QLabel(self.speclist[i]), i, 0, QtCore.Qt.AlignRight)

        self.stack2.setLayout(layout)

    def stack3UI(self):  # THE NEQAIR MODEL INPUT CAPABILITY
    # TABS---------------------------------
        self.il2info = ["(I)ntensity.out", "Intensity_(S)canned.out",
                        "(L)OS.out", "(P)opulation", "(A)bsorbance/Emittance",
                        "(C)oupling.out", "(M) stdout"]
        self.il3info = ["(B) Boltzmann", "(N) Non-Boltzmann",
                        "(Q) Traditional QSS ", "(T) Time derivative limited",
                        "(R) Reaction residual limited ", "(F) Flux limited",
                        "(C) Constant escape factor", "(L) Local Escape factor",
                        "(F) Full local calculation", "(N) Non-local coupling", 
                        "(S) Saha", "(F) Input from File",
                        "(A) absorption/emission coefficients from File"]
        self.il4info = ["(T) Tangent Slab", "(C) Spherical Cap",
                        "(S) Shock Tube", "(L) Line of Sight", "(B) Blackbody",
                        "(P) Calculate Populations", "(X) Perform scan on existing intensity.out"]
        self.il5info = ["(B) Blackbody", "(I) read Intensity.in",
                        "(N) no initial radiance", "(I) read emissivity.in",
                        "(G) Greybody", "(B) Blackbody"]
        self.il6info = ["WL1", "WL2", "A", "M", "Delta", "R", "dd"]
        self.il7info = ["ICCD1", "ICCD2", "Voigt", "Gauss"]
        # create the dictionaries to place the widgets within for each tab.
        self.il = {}

        self.layout3 = QtWidgets.QVBoxLayout(self)
        self.tabs = QtWidgets.QTabWidget()  # create the tabs
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tab6 = QWidget()

        self.tabs.addTab(self.tab1, "File Setup")  # Add tabs
        self.tabs.addTab(self.tab2, "Species Information")
        self.tabs.addTab(self.tab3, "Geometry \& Boundary Conditions")
        self.tabs.addTab(self.tab4, "Regions")
        self.tabs.addTab(self.tab5, "Scan Style")
        self.tabs.addTab(self.tab6, "Spatial Scan")

        # Create first tab - Generic File information(sim type and such)
        self.tab1.masterlayout = QVBoxLayout()
        self.tab1.layout1 = QGridLayout()
        self.tab1.legend1 = QLabel("File Outputs")
        self.tab1.legend2 = QLabel("Format Specifics")
        self.tab1.legend2.setFont(self.fontss)
        self.tab1.legend1.setFont(self.fontss)
        self.tab1.layout1.addWidget(self.tab1.legend1, 0, 0, QtCore.Qt.AlignCenter)
        self.tab1.layout1.addWidget(self.tab1.legend2, 0, 1, QtCore.Qt.AlignCenter)
        self.tab1.layout2 = QGridLayout()
        
        count = 0
        tmp_arr = np.empty(shape=(len(self.il2info), 2), dtype=object)
        for i in range(7):  # INPUT LINE 2
            tmp_arr[i, 0] = QtWidgets.QCheckBox(self.il2info[i], self)
            self.tab1.layout2.addWidget(tmp_arr[i, 0], i+1, 0)
            if "(I)" in self.il2info[i] or "(S)" in self.il2info[i]:
                tmp_arr[i, 1] = QtWidgets.QCheckBox("(2)Column Format?", self)
                self.tab1.layout2.addWidget(tmp_arr[i, 1], i+1, 2, QtCore.Qt.AlignRight)
                count+= 1
            count+= 1
        self.il['Line2'] = tmp_arr  # Creates the OutPut type dictionary section
        print("created FileOutput")
        self.tab1.layout3 = QGridLayout()
        self.tab1.legend3 = QLabel("State Population Methods")
        self.tab1.legend4 = QLabel("Method Specifics")
        self.tab1.legend3.setFont(self.fontss)
        self.tab1.legend4.setFont(self.fontss)      
        self.tab1.layout3.addWidget(self.tab1.legend3, 0, 0, QtCore.Qt.AlignCenter)
        self.tab1.layout3.addWidget(self.tab1.legend4, 0, 1, QtCore.Qt.AlignCenter)
        self.tab1.layout4 = QGridLayout()
        tmp_arr = np.empty(shape=(5, 3), dtype=object)
        for i in range(5):  # INPUT LINE 3
            if i < 2:
                tmp_arr[i, 0] = QtWidgets.QCheckBox(self.il3info[i], self)
                self.tab1.layout4.addWidget(tmp_arr[i, 0], count+i+1, 0)
                if "Non-B" in self.il3info[i]:  # Filling the combo boxes out and adding to dict
                    tmp_arr[i, 1] = QtWidgets.QComboBox()
                    tmp_arr[i, 1].addItem("--optional--")
                    tmp_arr[i, 1].addItems(self.il3info[2:5])
                    tmp_arr[i, 2] = QtWidgets.QComboBox()
                    tmp_arr[i, 2].addItems(self.il3info[6:9])
                    self.tab1.layout4.addWidget(tmp_arr[i, 1], count+i+1, 2)
                    self.tab1.layout4.addWidget(tmp_arr[i, 2], count+i+1, 3)
            if i >= 2:
                tmp_arr[i, 0]= QtWidgets.QCheckBox(self.il3info[i+8], self)
                self.tab1.layout4.addWidget(tmp_arr[i, 0], count+i+1, 0)
        self.tab1.masterlayout.addLayout(self.tab1.layout1)
        self.tab1.masterlayout.addLayout(self.tab1.layout2)
        self.tab1.masterlayout.addLayout(self.tab1.layout3)
        self.tab1.masterlayout.addLayout(self.tab1.layout4)
        self.tab1.setLayout(self.tab1.masterlayout)
        self.il['Line3'] = tmp_arr  # creates the State Pop Method Dictionary section
        print("created State Population")

        # ---- Create second tab
        
        self.tab2.layout3 = QGridLayout()
        self.losopen = QtWidgets.QPushButton("Read LOS")
        self.losopen.clicked.connect(self.ReadLOS)  # define the button's functionality
        self.tab2.layout3.addWidget(self.losopen, 0, 0)
        self.tab2.setLayout(self.tab2.layout3)

        # ---- Create third tab
        self.tab3.masterlayout = QVBoxLayout()
        self.tab3.layout1 = QGridLayout()
        self.tab3.legend1 = QLabel("Geometry")
        self.tab3.legend2 = QLabel("Boundary Conditions")
        self.tab3.legend2.setFont(self.fontss)
        self.tab3.legend1.setFont(self.fontss)
        self.tab3.layout1.addWidget(self.tab3.legend1, 0, 0, QtCore.Qt.AlignCenter)
        self.tab3.layout1.addWidget(self.tab3.legend2, 0, 1, QtCore.Qt.AlignCenter)
        self.tab3.layout2 = QGridLayout()
        
        tmp_arr = np.empty(shape=(len(self.il4info), 1), dtype=object)
        for i in range(len(self.il4info)):  # INPUT LINE 4
            tmp_arr[i, 0] = QtWidgets.QCheckBox(self.il4info[i], self)
            self.tab3.layout2.addWidget(tmp_arr[i, 0], count+i+2, 0)
        self.il['Line4'] = tmp_arr  # creates the Geometry Section of the dictionary
        tmp_arr = np.empty(shape=(len(self.il5info), 1), dtype=object)
        for i in range(len(self.il5info)):  # INPUT LINE 5
            tmp_arr[i, 0] = QtWidgets.QCheckBox(self.il5info[i], self)
            self.tab3.layout2.addWidget(tmp_arr[i, 0], count+i+2, 1)
        self.il['Line5'] = tmp_arr  # creates the Boundary Condition section of the dictionary
        self.tab3.masterlayout.addLayout(self.tab3.layout1)
        self.tab3.masterlayout.addLayout(self.tab3.layout2)
        self.tab3.setLayout(self.tab3.masterlayout)
        print("created Boundary/Geometry")

        # ---- Create fourth tab
        self.tab4.masterlayout = QVBoxLayout()
        self.tab4.layout1 = QGridLayout()
        self.tab4.legend1 = QLabel("Number of Regions")
        self.tab4.legend1.setFont(self.fontss)
        self.tab4.layout1.addWidget(self.tab4.legend1, 0, 0, QtCore.Qt.AlignCenter)
        self.tab4.layout2 = QGridLayout()
        self.regionbox = QtWidgets.QSpinBox(self)
        self.regionbox.setValue(4)
        self.tab4.layout2.addWidget(self.regionbox, 0, 0, 1, 6)
        self.regionbox.valueChanged.connect(self.regionchange)

        self.tab4.layout3 = QGridLayout()
        self.tab4.legend2 = QLabel("Min Wavelength")
        self.tab4.legend3 = QLabel("Max Wavelength")
        self.tab4.legend4 = QLabel("Grid Spacing")
        self.tab4.legend5 = QLabel("Delta")
        self.tab4.legend6 = QLabel("Range?")
        self.tab4.legend7 = QLabel("Range Value")
        self.tab4.legend2.setFont(self.fontss)
        self.tab4.legend3.setFont(self.fontss)
        self.tab4.legend4.setFont(self.fontss)
        self.tab4.legend5.setFont(self.fontss)
        self.tab4.legend6.setFont(self.fontss)
        self.tab4.legend7.setFont(self.fontss)
        
        self.tab4.layout3.addWidget(self.tab4.legend2, 0, 0, QtCore.Qt.AlignCenter)
        self.tab4.layout3.addWidget(self.tab4.legend3, 0, 1, QtCore.Qt.AlignCenter)
        self.tab4.layout3.addWidget(self.tab4.legend4, 0, 2, QtCore.Qt.AlignCenter)
        self.tab4.layout3.addWidget(self.tab4.legend5, 0, 3, QtCore.Qt.AlignCenter)
        self.tab4.layout3.addWidget(self.tab4.legend6, 0, 4, QtCore.Qt.AlignCenter)
        self.tab4.layout3.addWidget(self.tab4.legend7, 0, 5, QtCore.Qt.AlignCenter)
        self.tab4.layout4 = QGridLayout()
        tmp_arr = np.empty(shape=(self.regionbox.value(), 6), dtype=object)
        for i in range(self.regionbox.value()):  # create default number of tables
            for j in range(6):
                if j<2 or j == 3 or j == 5:
                    tmp_arr[i, j] = QtWidgets.QLineEdit("0.0", self)
                    tmp_arr[i, j].setValidator(QtGui.QDoubleValidator())
                    self.tab4.layout4.addWidget(tmp_arr[i, j], i+1, j)
                if j == 2:
                    tmp_arr[i, j] = QtWidgets.QComboBox()
                    tmp_arr[i, j].addItems(self.il6info[2:4])
                    self.tab4.layout4.addWidget(tmp_arr[i, j], i+1, j)
                if j == 4:
                    tmp_arr[i, j] = QtWidgets.QCheckBox("R", self)
                    self.tab4.layout4.addWidget(tmp_arr[i, j], i+1, j)
        self.il['Line7'] = tmp_arr  # creates the Regions section of the dictionary
        self.tab4.masterlayout.addLayout(self.tab4.layout1)
        self.tab4.masterlayout.addLayout(self.tab4.layout2)
        self.tab4.masterlayout.addLayout(self.tab4.layout3)
        self.tab4.masterlayout.addLayout(self.tab4.layout4)
        
        self.tab4.setLayout(self.tab4.masterlayout)
        print("created Regions")

        # ---- Creates fifth tab
        self.tab5.masterlayout = QVBoxLayout()
        self.tab5.layout1 = QGridLayout()
        self.tab5.legend1 = QLabel("Spacing")
        self.tab5.legend2 = QLabel("Type")
        self.tab5.legend3 = QLabel("Param1")
        self.tab5.legend4 = QLabel("Param2")
        self.tab5.legend5 = QLabel("Param3")
        
        self.tab5.legend1.setFont(self.fontss)
        self.tab5.legend2.setFont(self.fontss)
        self.tab5.legend3.setFont(self.fontss)
        self.tab5.legend4.setFont(self.fontss)
        self.tab5.legend5.setFont(self.fontss)
        
        self.tab5.layout1.addWidget(self.tab5.legend1, 0, 0, QtCore.Qt.AlignCenter)
        self.tab5.layout1.addWidget(self.tab5.legend2, 0, 1, QtCore.Qt.AlignCenter)
        self.tab5.layout1.addWidget(self.tab5.legend3, 0, 2, QtCore.Qt.AlignCenter)
        self.tab5.layout1.addWidget(self.tab5.legend4, 0, 3, QtCore.Qt.AlignCenter)
        self.tab5.layout1.addWidget(self.tab5.legend5, 0, 4, QtCore.Qt.AlignCenter)
    
        self.tab5.layout2 = QGridLayout()
        tmp_arr1 = np.empty(shape=(self.regionbox.value(), 5), dtype=object)
        for i in range(self.regionbox.value()):  # create default number of tables...too
            tmp_arr1[i, 0] = QtWidgets.QLineEdit("0.0", self)
            tmp_arr1[i, 0].setValidator(QtGui.QDoubleValidator())
            self.tab5.layout2.addWidget(tmp_arr1[i, 0], i+1, 0)
            tmp_arr1[i, 1] = QtWidgets.QComboBox()
            tmp_arr1[i, 1].addItems(self.il7info[:])
            self.tab5.layout2.addWidget(tmp_arr1[i, 1], i+1, 1)
            for j in range(3):
                tmp_arr1[i, j+2] = QtWidgets.QLineEdit("0.0", self)
                tmp_arr1[i, j+2].setValidator(QtGui.QDoubleValidator())
                self.tab5.layout2.addWidget(tmp_arr1[i, j+2], i+1, j+2)
        self.il['Line8'] = tmp_arr1   # creates the Scan portion of the dictionary. only required for shock tube
        self.tab5.masterlayout.addLayout(self.tab5.layout1)
        self.tab5.masterlayout.addLayout(self.tab5.layout2)
        self.tab5.layout1.setSpacing(0)
        self.tab5.setLayout(self.tab5.masterlayout)
        print("created Scan")

        # ---- Creates sixth tab
        self.tab6.masterlayout = QVBoxLayout()
        self.tab6.layout1 = QGridLayout()
        self.tab6.legend11 = QLabel("Slit Profile")
        self.tab6.legend12= QLabel("Base1")
        self.tab6.legend13 = QLabel("Base2 (Trapezoid)")
        self.tab6.legend11.setFont(self.fontss)
        self.tab6.legend12.setFont(self.fontss)
        self.tab6.legend13.setFont(self.fontss)
        self.tab6.layout1.addWidget(self.tab6.legend11, 0, 0, QtCore.Qt.AlignCenter)
        self.tab6.layout1.addWidget(self.tab6.legend12, 0, 1, QtCore.Qt.AlignCenter)
        self.tab6.layout1.addWidget(self.tab6.legend13, 0, 2, QtCore.Qt.AlignCenter)
        
        self.tab6.layout2 = QGridLayout()
        tmp_arr1 = np.empty(shape=(self.regionbox.value(), 3), dtype=object)

        tmp_arr1[0, 0] = QtWidgets.QComboBox()
        tmp_arr1[0, 0].addItem('triangle')
        tmp_arr1[0, 0].addItem('trapezoid')
        self.tab6.layout2.addWidget(tmp_arr1[0, 0], 0, 0)
        tmp_arr1[0, 1] = QtWidgets.QLineEdit("0.0", self)
        tmp_arr1[0, 1].setValidator(QtGui.QDoubleValidator())
        self.tab6.layout2.addWidget(tmp_arr1[0, 1], 0, 1)
        tmp_arr1[0, 2] = QtWidgets.QLineEdit("0.0", self)
        tmp_arr1[0, 2].setValidator(QtGui.QDoubleValidator())
        self.tab6.layout2.addWidget(tmp_arr1[0, 2], 0, 2)
        
        self.tab6.layout3 = QGridLayout()
        self.tab6.legend31 = QLabel("Line Type")
        self.tab6.legend32 = QLabel("Param1")
        self.tab6.legend33 = QLabel("Param2")
        self.tab6.legend31.setFont(self.fontss)
        self.tab6.legend32.setFont(self.fontss)
        self.tab6.legend33.setFont(self.fontss)
        self.tab6.layout3.addWidget(self.tab6.legend31, 0, 0, QtCore.Qt.AlignCenter)
        self.tab6.layout3.addWidget(self.tab6.legend32, 0, 1, QtCore.Qt.AlignCenter)
        self.tab6.layout3.addWidget(self.tab6.legend33, 0, 2, QtCore.Qt.AlignCenter)
        
        self.tab6.layout4 = QGridLayout()
        tmp_arr1[1, 0] = QtWidgets.QComboBox()
        tmp_arr1[1, 0].addItems(self.il7info[:])
        self.tab6.layout4.addWidget(tmp_arr1[1, 0], 1, 0)
        tmp_arr1[1, 1] = QtWidgets.QLineEdit("0.0", self)
        tmp_arr1[1, 1].setValidator(QtGui.QDoubleValidator())
        self.tab6.layout4.addWidget(tmp_arr1[1, 1], 1, 1)
        tmp_arr1[1, 2] = QtWidgets.QLineEdit("0.0", self)
        tmp_arr1[1, 2].setValidator(QtGui.QDoubleValidator())
        self.tab6.layout4.addWidget(tmp_arr1[1, 2], 1, 2)
        
        self.tab6.layout5 = QGridLayout()
        self.tab6.legend51 = QLabel("Temporal Width")
        self.tab6.legend51.setFont(self.fontss)
        self.tab6.layout5.addWidget(self.tab6.legend51, 0, 0, QtCore.Qt.AlignCenter)
        
        self.tab6.layout6 = QGridLayout()
        tmp_arr1[2, 0] = QtWidgets.QLineEdit("0.0", self)
        tmp_arr1[2, 0].setValidator(QtGui.QDoubleValidator())
        self.tab6.layout6.addWidget(tmp_arr1[2, 0], 2, 0)
        self.il['Line9'] = tmp_arr1   # creates the Scan portion of the dictionary. only required for shock tube
        
        self.tab6.masterlayout.addLayout(self.tab6.layout1)
        self.tab6.masterlayout.addLayout(self.tab6.layout2)
        self.tab6.masterlayout.addLayout(self.tab6.layout3)
        self.tab6.masterlayout.addLayout(self.tab6.layout4)
        self.tab6.masterlayout.addLayout(self.tab6.layout5)
        self.tab6.masterlayout.addLayout(self.tab6.layout6)
        self.tab6.setLayout(self.tab6.masterlayout)
        print("created Spatial Scan")

        # Add tabs to widget
        self.layout3.addWidget(self.tabs)
        self.stack3.setLayout(self.layout3)
        del tmp_arr, tmp_arr1

        # FUNCTIONS-------------------------------------------------
    def readplot(self):  # OPENING AND READING FIGURE IN
        self.figure.clf()
        self.colchange1.clear()  # clear the previous plot datas entires
        self.colchange2.clear()  # clear the previous plot datas entires
        datafile, __ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files(*)")
        if datafile:
            datafile = str(datafile)
            self.plotfile =np.genfromtxt(datafile, dtype=float, comments="(", skip_header=1, names=True, unpack=True)
            sax = self.figure.add_subplot(111)  # adds figure as a subplot. might be nice to use this to allow user to plot multiple things.
            sax.plot(self.plotfile[self.plotfile.dtype.names[0]], self.plotfile[self.plotfile.dtype.names[1]], '*-')  # need controls for one vs. another
            self.colchange1.addItems(self.plotfile.dtype.names[:])
            self.colchange2.addItems(self.plotfile.dtype.names[:])
            self.canvas.draw()

    def newplot(self):
        self.figure.clf()
        sax = self.figure.add_subplot(111)  # adds figure as a subplot. might be nice to use this to allow user to plot multiple things.
        i1 = self.colchange1.currentIndex()
        i2 = self.colchange2.currentIndex()
        sax.plot(self.plotfile[self.plotfile.dtype.names[i1]], self.plotfile[self.plotfile.dtype.names[i2]], '*-')
        self.canvas.draw()
        
        
        
    def ReadLOS(self):  # OPENING LOS.DAT FILE TO READ COLUMN HEADERS
        self.aband = ["bb", "bf", "ff"]
        self.n2band = ["1+", "2+", "BH2", "LBH", "BH1", "WJ", "CY"]
        self.o2band = ["SR"]
        self.noband = ["beta", "gam", "del", "eps", "bp", "gp", "IR"]
        datafile, __ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files(*)")
        if datafile:
            print("Opening LOS File:", datafile)
            datafile = str(datafile)
            spectrum =np.genfromtxt(datafile, dtype=None, skip_header=21, names=True)
            self.spec = spectrum.dtype.names[7:-1]  # omitting all of the n, n_total stuff
            self.spec = [w.replace('_1', '+') for w in self.spec]  # erasing the nasty characters and replacing with user-identifiables
            self.spec.sort()  # sort the list

            # This next little piece of code is dumb and inefficient, should replace with something more elegant
            xcount = 0
            for i in range(len(self.spec)):
                if "+" not in self.spec[i]:
                    xcount += 1
            self.speclist = [None]*xcount
            k = 0
            for i in range(len(self.spec)):
                if "+" not in self.spec[i]:
                    self.speclist[k] = self.spec[i]
                    k += 1
            # End bad section
            self.allcheck = QtWidgets.QCheckBox()
            self.allcheck.clicked.connect(self.checkemalll)
            self.tab2.layout3.addWidget(self.allcheck, 0, 1)
            self.tab2.layout3.addWidget(QLabel("Check All Bands"), 0, 2, 1, 7, QtCore.Qt.AlignLeft)

            tmp_arrb = [None]*len(self.speclist)
            tmp_arrcb = np.empty(shape=(xcount, len(self.n2band)), dtype=object)
            for i in range(len(self.speclist)):
                    tmp_arrb[i] = QtWidgets.QPushButton(self.speclist[i], self)
                    tmp_arrb[i].setCheckable(True)
                    self.tab2.layout3.addWidget(tmp_arrb[i], i+1, 0)

                    if len(self.speclist[i]) == 1:
                        for j in range(3):  # making specific bands for atoms(bf, bb, ff)
                            tmp_arrcb[i, j] = QtWidgets.QCheckBox(self.aband[j])
                            self.tab2.layout3.addWidget(tmp_arrcb[i, j], i+1, j*2+1)
                    if "N2" in self.speclist[i] and len(self.speclist[i]) == 2:
                        for j in range(len(self.n2band)):
                            tmp_arrcb[i, j] = QtWidgets.QCheckBox(self.n2band[j])
                            self.tab2.layout3.addWidget(tmp_arrcb[i, j], i+1, j*2+1)
                    if "O2" in self.speclist[i] and len(self.speclist[i]) == 2:
                        for j in range(len(self.o2band)):
                            tmp_arrcb[i, j] = QtWidgets.QCheckBox(self.o2band[j])
                            self.tab2.layout3.addWidget(tmp_arrcb[i, j], i+1, j*2+1)
                    if "NO" in self.speclist[i] and len(self.speclist[i]) == 2:
                        for j in range(len(self.noband)):
                            tmp_arrcb[i, j] = QtWidgets.QCheckBox(self.noband[j])
                            self.tab2.layout3.addWidget(tmp_arrcb[i, j], i+1, j*2+1)
                    xcount += 1
            self.il['Line6'] = tmp_arrb  # The press buttons for each species
            self.il['Line6CB'] = tmp_arrcb  # the check buttons for each species

    def regionchange(self):
        count = self.regionbox.value()  # tables want
        clayout = int((self.tab4.layout4.count())/6)  # tables have(includes spinbox)
        print("count is: ", count, "clayout is: ", clayout)
        if count < clayout:
            for k in range(6):
                self.il['Line7'][clayout-1, k] = None  # the spacing is offset from that array loc by 1
                regionToRemove = self.tab4.layout4.itemAtPosition(clayout, k).widget()
                regionToRemove.setParent(None)
                self.tab4.layout4.removeWidget(regionToRemove)
            for kk in range(5):
                self.il['Line8'][clayout-1, kk] = None
                lineToRemove = self.tab5.layout2.itemAtPosition(clayout, kk).widget()
                lineToRemove.setParent(None)
                self.tab5.layout2.removeWidget(lineToRemove)
        elif count > clayout:
            self.il['Line7'] = np.resize(self.il['Line7'], [count, len(self.il6info)-1])  # resize the array to the count size with corresponding list length
            for j in range(6):
                if j<2 or j == 3 or j == 5:
                    self.il['Line7'][count-1, j] = QtWidgets.QLineEdit("0.0", self)
                    self.il['Line7'][count-1, j].setValidator(QtGui.QDoubleValidator())
                    self.tab4.layout4.addWidget(self.il['Line7'][count-1, j], count, j)
                if j == 2:
                    self.il['Line7'][count-1, j] = QtWidgets.QComboBox()
                    self.il['Line7'][count-1, j].addItems(self.il6info[2:4])
                    self.tab4.layout4.addWidget(self.il['Line7'][count-1, j], count, j)
                if j == 4:
                    self.il['Line7'][count-1, j] = QtWidgets.QCheckBox("R", self)
                    self.tab4.layout4.addWidget(self.il['Line7'][count-1, j], count, j)
            self.tab4.setLayout(self.tab4.masterlayout)

            self.il['Line8'] = np.resize(self.il['Line8'], [count, 5])
            self.il['Line8'][count-1, 0] = QtWidgets.QLineEdit("0.0", self)
            self.il['Line8'][count-1, 0].setValidator(QtGui.QDoubleValidator())
            self.tab5.layout2.addWidget(self.il['Line8'][count-1, 0], count, 0)
            self.il['Line8'][count-1, 0] = QtWidgets.QComboBox()
            self.il['Line8'][count-1, 0].addItems(self.il7info[:])
            self.tab5.layout2.addWidget(self.il['Line8'][count-1, 0], count, 1)
            for j in range(3):
                self.il['Line8'][count-1, j+2] = QtWidgets.QLineEdit("0.0", self)
                self.il['Line8'][count-1, j+2].setValidator(QtGui.QDoubleValidator())
                self.tab5.layout2.addWidget(self.il['Line8'][count-1, j+2], count, j+2)
            self.tab5.setLayout(self.tab5.masterlayout)

    def checkemalll(self):
        if self.allcheck.isChecked():
            for i in range(len(self.speclist)):
                self.il['Line6'][i].setChecked(True)
                for j in range(len(self.n2band)):
                    if hasattr(self.il['Line6CB'][i, j], 'setChecked'):
                        self.il['Line6CB'][i, j].setChecked(True)

    def clearplot(self):
        self.figure.close()
        self.canvas.draw()

    def display(self, i):
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