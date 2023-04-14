from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QComboBox
import threading
import sys
import re
import numpy as np
import os
from pathlib import Path
from sys import platform
import shlex
from subprocess import run,PIPE


def clearOutput():
    if platform == "linux" or platform == "linux2":
        os.system('clear')
    elif platform == "win32":
        os.system('cls')

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def setupUi(self):
        colNum = 0
        ColData = ["Clock", "VA", "TransID", "PA", "Core", "Req State", "Resp State", "Req Type", "Resp Type", "Probe Type", "C2X", "CL", "IL", "PF", "PacketPtr",
                   "BA", "PackID", "Tag", "Index", "Bank", "Way", "ReqPort", "IssuePort", "RCS", "MCS", "LUS", "ReqT", "DecT", "IssT", "FwtT", "MissRT", "RespT", "EvictT", "WBT", "Drop", "VictimPkt", "Message"]
        self.setObjectName("MainWindow")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 100, 1850, 800))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.combobox = QComboBox(self.centralwidget)
        self.combobox.setGeometry(QtCore.QRect(10, 10, 250, 35))
        self.combobox.addItems(ColData)
        self.textbox = QLineEdit('', self.centralwidget)
        self.textbox.setGeometry(QtCore.QRect(260, 10, 100, 35))
        self.button = QPushButton('Filter', self.centralwidget)
        self.button.setGeometry(QtCore.QRect(400, 10, 100, 35))
        self.button.clicked.connect(self.Filter)

        self.buttonColumn = QPushButton('Hide', self.centralwidget)
        self.buttonColumn.setGeometry(QtCore.QRect(600, 10, 100, 35))
        self.buttonColumn.clicked.connect(self.hideColumn)

        numCols = len(ColData)
        self.tableWidget.setColumnCount(numCols)
        for col in ColData:
            item = QtWidgets.QTableWidgetItem()
            item.setText(QtCore.QCoreApplication.translate(
                "MainWindow", ColData[colNum]))
            self.tableWidget.setVerticalHeaderItem(colNum, item)
            colNum += 1
        self.tableWidget.setHorizontalHeaderLabels(ColData)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.setWindowTitle(QtCore.QCoreApplication.translate(
            "MainWindow", "LogViewer"))
        QtCore.QMetaObject.connectSlotsByName(self)

    def hideColumn(self):
        self.tableWidget.setColumnHidden(self.combobox.currentIndex(), True)

    def Filter(self):
        textBoxValue = self.textbox.text()
        self.textbox.setText("")
        row = 0
        inputRow = 0
        self.filteredRecord = []
        for logRecordItem in self.logRecord:
            if logRecordItem[self.combobox.currentIndex()] == textBoxValue:
                self.filteredRecord.append(self.logRecord[inputRow])
                row = row + 1
            inputRow = inputRow + 1
        self.viewData()

    def loadData(self):

        path = Path('logrecord.npy')

        if path.is_file():
            print("Loading already existing file")
            self.logRecord = np.load('logrecord.npy', allow_pickle = True)
            print("Loaded")
            return self.logRecord

        print("Started loading log data")
        logFile = f = open("assets/files/log", "r")
        print("Loaded log data")

        row = 0
        self.logRecord = []
        while(True):

            print("Row number: ", row)
            line = logFile.readline()
            if not line:
                break
            logLine = line.split("M:")
            transDetails = logLine[0].split("\t")
            del transDetails[-1]
            if len(logLine) == 3:
                pktDetails = logLine[1].split("\t")
                del pktDetails[-1]
                message = logLine[2]
            else:
                pktDetails = ["", "", "", "", "", "", "", "", "",
                              "", "", "", "", "", "", "", "", "", "", "", ""]
                message = logLine[1]
            colData = np.concatenate(
                (transDetails, pktDetails, message), axis=None)

            self.logRecord.append(colData)
            row += 1
            clearOutput()
        print("Data loaded")
        self.filteredRecord = self.logRecord
        logFile.close()

        np.save('logrecord.npy', self.logRecord)

        return self.logRecord

    def applyFilter(self, objName, pkt_id, logRecord):
        colNum = int(objName.split(' ')[1])
        setattr(self, self.sender().text(),
                displayPacket(colNum, pkt_id, logRecord))
        getattr(self, self.sender().text()).showMaximized()
        getattr(self, self.sender().text()).show()

    def viewData(self):
        row = 0
        self.tableWidget.setRowCount(0)
        btns = {}
        for logRecordItem in self.filteredRecord:
            self.tableWidget.insertRow(row)
            __sortingEnabled = self.tableWidget.isSortingEnabled()
            self.tableWidget.setSortingEnabled(False)
            colNums = 0
            colData = self.filteredRecord[row]
            for col in colData:
                button_name = str(row) + " " + str(colNums) + " " + col
                btns[button_name] = QPushButton(button_name, self.tableWidget)
                btns[button_name].setText(col)
                btns[button_name].setObjectName(button_name)
                btns[button_name].setEnabled(True)
                btns[button_name].clicked.connect(lambda: self.applyFilter(
                    self.sender().objectName(), self.sender().text(), self.logRecord))
                item = self.tableWidget.setCellWidget(
                    row, colNums, btns[button_name])
                colNums += 1
            self.tableWidget.setSortingEnabled(__sortingEnabled)
            row = row + 1

        self.tableWidget.resizeColumnsToContents()


def displayPacket(colNum, pkt_id, logRecord=None):  
    ui = Ui_MainWindow()
    ui.setupUi()

    def FilterWithPktId(pkt_id):
        file_path = "assets/files/testLog"
        temp_file = open("assets/files/temp", "w")
        p = "PID:"+ pkt_id
        cmd = "grep %s %s" % (str(p), file_path)
        args = shlex.split(cmd)
        if platform == "win32":
            cmd = "findstr %s %s" % (str(p), "assets\\files\\testLog")
            args = cmd
        process = run(args, shell=True, stdout=temp_file, stderr=PIPE, text=True)
        
        temp_file.close()

        try: 
            temp_file = open("assets/files/temp", "r")
            line = temp_file.readline()
            transDetails = line.split("\t")
            tx_id = transDetails[2]
            cmd = "grep %s %s" % (str(tx_id), "assets/files/testLog")
            args = shlex.split(cmd)
            if platform == "win32":
                cmd = "findstr %s %s" % (str(tx_id), "assets\\files\\testLog")
                args = cmd
            with open("assets/files/txRecord", "w") as filteredPktFile:
                process = run(args, shell=True, stdout=filteredPktFile, stderr=filteredPktFile, text=True)
                print("executed")

            temp_file.close()

            if os.path.exists("assets\\files\\temp"):
                os.remove("assets/files/temp")
            else: 
                print("error")
        except:
            print("Some error in ")

    
    FilterWithPktId(pkt_id)

    print("setupUi")

    if logRecord is None:
        logRecord = ui.loadData()
    else:
        ui.logRecord = logRecord

    print("logRecord Loaded")

    ui.combobox.setCurrentIndex(colNum)
    ui.textbox.setText(str(pkt_id))
    ui.Filter()

    return ui


if __name__ == "__main__":
    ui = displayPacket(16, 10000)
