#!/usr/local/bin python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from UIs.Ui_mainWindow import Ui_MainWindow
from langs import lanpacks as l
import time
import ctypes

class MainWindow(QMainWindow, Ui_MainWindow):
    curLang = 0

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.statusBar().showMessage("Powered by Chenfei Jovany Rong | Site: https://rongchenfei.com")
        self.tabWidget.setCurrentIndex(0)
        self.setWindowIcon(QIcon("src/easyOM2.png"))

        self.timer = QBasicTimer()
        self.timer.start(10, self)

        try:
            langCode = ctypes.windll.kernel32.GetSystemDefaultUILanguage()
            if langCode == 2052:
                self.curLang = 1
        except:
            pass
        
        self.localize(self.curLang)

    #event
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 
                                                "EasyOM",
                                                "Do you want to exit?",
                                                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                                QMessageBox.Cancel)
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.lcdClock.display(time.strftime("%X",time.localtime()))
        else:
            super(WigglyWidget, self).timerEvent(event)

    #localize
    def localize(self, lang):
        self.topLabel.setText(l.softName[lang])
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), l.homeTab[lang])
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), l.queryTab[lang])
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), l.analysisTab[lang])
        self.todayTodoLabel.setText(l.todoToday[lang])
        self.todayDoneLabel.setText(l.doneToday[lang])
        self.emerAddButton.setText(l.emerAdd[lang])
        self.taskListLabel.setText(l.taskList[lang])
