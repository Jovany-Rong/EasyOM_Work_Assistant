#!/usr/local/bin python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import time

class splashScreen(QtWidgets.QSplashScreen):
    def __init__(self):
        super(splashScreen, self).__init__(QtGui.QPixmap("src/loading.png"))

    def effect(self):
        self.setWindowOpacity(0)
        t = 0
        while t <= 50:
            newOpacity = self.windowOpacity() + 0.02
            if newOpacity > 1:
                break

            self.setWindowOpacity(newOpacity)
            #self.hide()
            self.show()
            t -= 1
            time.sleep(0.02)

        time.sleep(1)
        t = 0
        while t <= 50:
            newOpacity = self.windowOpacity() - 0.02
            if newOpacity < 0:
                break

            self.setWindowOpacity(newOpacity)
            #self.hide()
            self.show()
            t += 1
            time.sleep(0.02)