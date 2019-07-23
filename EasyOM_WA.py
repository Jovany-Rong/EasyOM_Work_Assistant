#!/usr/local/bin python
# -*- coding: utf-8 -*-

import sys
import ctypes
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from main.mainFunc import MainWindow
from main import splashScreen

#app start
if __name__ == '__main__':
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("easyOMWAAppId")
    except:
        pass

    app = QApplication(sys.argv)

    splash = splashScreen.splashScreen()
    splash.effect()

    app.processEvents()

    mainWin = MainWindow()
    mainWin.show()

    splash.finish(mainWin)

    sys.exit(app.exec_())