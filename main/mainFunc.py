#!/usr/local/bin python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
#from PyQt5.QtMultimedia import QSound
from UIs.Ui_mainWindow import Ui_MainWindow
from UIs.Ui_addEmer import Ui_addEmer
from UIs.Ui_deliCommit import Ui_DeliCommit
from langs import lanpacks as l
from basifuns import timeFuncs as t
from basifuns import configFuncs as c
import time
import ctypes
import re
from os import path, makedirs
import os.path
import qtawesome
import base64

class MainWindow(QMainWindow, Ui_MainWindow):
    curLang = 1
    taskList = list()
    todoList = list()
    alertList = list()
    curSkin = ""
    curWin = 1

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.statusBar().showMessage("Powered by Chenfei Jovany Rong | Site: https://rongchenfei.com")
        self.tabWidget.setCurrentIndex(0)
        self.setWindowIcon(QIcon("src/easyOM2.png"))
        #self.alertSound = QSound("src/alert.wav", self)

        self.timer = QBasicTimer()
        self.timer.start(10, self)

        try:
            langCode = ctypes.windll.kernel32.GetSystemDefaultUILanguage()
            if langCode == 2052:
                self.curLang = 1
        except:
            pass
        
        self.localize(self.curLang)
        self.dateInit()
        self.showTaskList()
        self.showTodoToday()
        self.showDoneToday()
        self.emerAddButton.clicked.connect(self.addEmergency)
        self.pageRefreshButton.clicked.connect(self.refresh)
        self.queryButton.clicked.connect(self.query)
        self.analysisButton.clicked.connect(self.analysis)
        self.stop.clicked.connect(self.close)
        self.min.clicked.connect(self.showMinimized)
        self.max.clicked.connect(self.windowMax)
        self.skin.clicked.connect(self.changeSkin)
        self.beautify()
        self.skinBlack()

    def windowMax(self):
        if self.curWin == 1:
            self.showMaximized()
            self.curWin = 2
        else:
            self.showNormal()
            self.curWin = 1


    def beautify(self):
        self.setWindowOpacity(0.9)
        self.setWindowFlag(Qt.FramelessWindowHint)
        
        self.stop.setStyleSheet('''QPushButton{background:#F76677;border-radius:11px;}
QPushButton:hover{background:red;}''')
        self.min.setStyleSheet('''QPushButton{background:#F7D674;border-radius:11px;}
QPushButton:hover{background:yellow;}''')
        self.max.setStyleSheet('''QPushButton{background:#6DDF6D;border-radius:11px;}
QPushButton:hover{background:green;}''')
        
        self.skin.setStyleSheet(
            """
        QPushButton{border:0px;
        border-radius:5px;
        color:lightGray;
        background:gray;}
        QPushButton:hover{color:white;
                    border:1px solid #F3F3F5;
                    border-radius:5px;
                    background:darkGray;}
            """
        )
        self.buttonQss = """
        QPushButton{border:2px solid #F3F3F5;
        border-radius:7px;
        color:lightGray;
        background:darkGray;}
        QPushButton:hover{color:white;
                    border:2px solid #F3F3F5;
                    border-radius:7px;
                    background:darkGray;}
        """
        try:
            self.emerAddButton.setIcon(qtawesome.icon('fa5s.file-alt', color='white'))
            self.pageRefreshButton.setIcon(qtawesome.icon('fa5s.play-circle', color='white'))
            self.skin.setIcon(qtawesome.icon('fa5s.sun', color='yellow'))
            self.taskListTable.horizontalHeader().setStretchLastSection(True)
            self.todayTodoTable.horizontalHeader().setStretchLastSection(True)
            self.todayDoneTable.horizontalHeader().setStretchLastSection(True)
            self.queryTable.horizontalHeader().setStretchLastSection(True)
            #self.taskListTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        except:
            pass
        

        scrollBarQss = """
QScrollBar:vertical
{
    width:8px;
    background:rgba(0,0,0,0%);
    margin:0px,0px,0px,0px;
    padding-top:9px;   
    padding-bottom:9px;
}
QScrollBar::handle:vertical
{
    width:8px;
    background:rgba(0,0,0,25%);
    border-radius:4px;  
    min-height:20;
}
QScrollBar::handle:vertical:hover
{
    width:8px;
    background:rgba(0,0,0,50%);   
    border-radius:4px;
    min-height:20;
}
QScrollBar::add-line:vertical   
{
    height:9px;width:8px;
    border-image:url(:/images/a/3.png);
    subcontrol-position:bottom;
}
QScrollBar::sub-line:vertical 
{
    height:9px;width:8px;
    border-image:url(:/images/a/1.png);
    subcontrol-position:top;
}
QScrollBar::add-line:vertical:hover 
{
    height:9px;width:8px;
    border-image:url(:/images/a/4.png);
    subcontrol-position:bottom;
}
QScrollBar::sub-line:vertical:hover 
{
    height:9px;width:8px;
    border-image:url(:/images/a/2.png);
    subcontrol-position:top;
}
QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical 
{
    background:rgba(0,0,0,10%);
    border-radius:4px;
}
QScrollBar:horizontal
{
    height:8px;
    background:rgba(0,0,0,0%);
    margin:0px,0px,0px,0px;
    padding-left:9px; 
    padding-right:9px;
}
QScrollBar::handle:horizontal
{
    height:8px;
    background:rgba(0,0,0,25%);
    border-radius:4px;  
    min-width:20;
}
QScrollBar::handle:horizontal:hover
{
    height:8px;
    background:rgba(0,0,0,50%);  
    border-radius:4px;
    min-width:20;
}
QScrollBar::add-line:horizontal  
{
    width:9px;height:8px;
    border-image:url(:/images/a/3.png);
    subcontrol-position:bottom;
}
QScrollBar::sub-line:horizontal  
{
    width:9px;height:8px;
    border-image:url(:/images/a/1.png);
    subcontrol-position:top;
}
QScrollBar::add-line:horizontal:hover  
{
    width:9px;height:8px;
    border-image:url(:/images/a/4.png);
    subcontrol-position:bottom;
}
QScrollBar::sub-line:horizontal:hover  
{
    width:9px;height:8px;
    border-image:url(:/images/a/2.png);
    subcontrol-position:top;
}
QScrollBar::add-page:horizontal,QScrollBar::sub-page:horizontal  
{
    background:rgba(0,0,0,10%);
    border-radius:4px;
}
        """

        self.taskListTable.setStyleSheet(scrollBarQss)
        self.todayTodoTable.setStyleSheet(scrollBarQss)
        self.todayDoneTable.setStyleSheet(scrollBarQss)
        

    def skinBlack(self):
        pe = QPalette()
        self.setAutoFillBackground(True)
        pe.setColor(QPalette.Window,Qt.lightGray)
        self.setPalette(pe)

        self.emerAddButton.setStyleSheet('''QPushButton{border:none;
        color:lightGray;}
        QPushButton:hover{color:white;
                    border:2px solid #F3F3F5;
                    border-radius:7px;
                    background:darkGray;}''')
        self.pageRefreshButton.setStyleSheet('''QPushButton{border:none;
        color:lightGray;}
        QPushButton:hover{color:white;
                    border:2px solid #F3F3F5;
                    border-radius:7px;
                    background:darkGray;}''')
        self.queryButton.setStyleSheet("""
        QPushButton{border:2px solid #F3F3F5;
        border-radius:7px;
        color:lightGray;
        background:darkGray;}
        QPushButton:hover{color:white;
                    border:2px solid #F3F3F5;
                    border-radius:7px;
                    background:darkGray;}
        """)
        self.analysisButton.setStyleSheet("""
        QPushButton{border:2px solid #F3F3F5;
        border-radius:7px;
        color:lightGray;
        background:darkGray;}
        QPushButton:hover{color:white;
                    border:2px solid #F3F3F5;
                    border-radius:7px;
                    background:darkGray;}
        """)

        self.setStyleSheet("""
        QMessageBox{
            background-color:lightGray;
        }
        QTableView , QTableWidget{
        selection-background-color:#44c767;
        background-color:lightGray;
        border:1px solid #E0DDDC;
        gridline-color:white;
        }
        QHeaderView::section{
        background-color: #00CCCC;
        border:0px solid #E0DDDC;
        border-bottom:1px solid #E0DDDC;
        height:20px;
        font-size:14px;
        font-weight:bold;
        }
        QTabWidget::pane{
border:none;
}

QTabWidget::tab-bar {
     left: 5px;
     font-weight:bold;
     font-family:FangSong;
}

QTabBar::tab {
     background: lightgray;
     /*border: 2px solid #C4C4C3;*/
     border-bottom-color: #C2C7CB;
     border-top-left-radius: 4px;
     border-top-right-radius: 4px;
     min-width: 60px;
     padding: 2px;
     font-weight:bold;
     font-family:Song;
 }

QTabBar::tab:selected{
    background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #626262,stop:1 #545454);
    color:white;
}

QTabBar::tab:!selected{
    margin-top:5px;
}
#tab,#tab_2,#tab_3{
    background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #626262,stop:1 #545454);
    border-radius:6px;
}
        """)

        self.curSkin = "black"

    def skinPink(self):
        pe = QPalette()
        self.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, QColor(242,227,242,1))
        self.setPalette(pe)

        self.emerAddButton.setStyleSheet('''QPushButton{border:none;
        color:#f4d6f5;}
        QPushButton:hover{color:white;
                    border:2px solid #F3F3F5;
                    border-radius:7px;
                    background:#e49ee5;}''')
        self.pageRefreshButton.setStyleSheet('''QPushButton{border:none;
        color:#f4d6f5;}
        QPushButton:hover{color:white;
                    border:2px solid #F3F3F5;
                    border-radius:7px;
                    background:#e49ee5;}''')
        self.queryButton.setStyleSheet("""
        QPushButton{border:2px solid #F3F3F5;
        border-radius:7px;
        color:#f4d6f5;
        background:#e49ee5;}
        QPushButton:hover{color:white;
                    border:2px solid #F3F3F5;
                    border-radius:7px;
                    background:#e49ee5;}
        """)
        self.analysisButton.setStyleSheet("""
        QPushButton{border:2px solid #F3F3F5;
        border-radius:7px;
        color:#f4d6f5;
        background:#e49ee5;}
        QPushButton:hover{color:white;
                    border:2px solid #F3F3F5;
                    border-radius:7px;
                    background:#e49ee5;}
        """)

        self.setStyleSheet("""
        QMessageBox{
            background-color:#f4d6f5;
        }
        QTableView , QTableWidget{
        selection-background-color:#44c767;
        background-color:#f4d6f5;
        border:1px solid #E0DDDC;
        gridline-color:white;
        }
        QHeaderView::section{
        background-color: #00CCCC;
        border:0px solid #E0DDDC;
        border-bottom:1px solid #E0DDDC;
        height:20px;
        font-size:14px;
        font-weight:bold;
        }
        QTabWidget::pane{
border:none;
}

QTabWidget::tab-bar {
     left: 5px;
     font-weight:bold;
     font-family:FangSong;
}

QTabBar::tab {
     background: #f4d6f5;
     /*border: 2px solid #C4C4C3;*/
     border-bottom-color: #C2C7CB;
     border-top-left-radius: 4px;
     border-top-right-radius: 4px;
     min-width: 60px;
     padding: 2px;
     font-weight:bold;
     font-family:Song;
 }

QTabBar::tab:selected{
    background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #f38af4,stop:1 #f569f7);
    color:white;
}

QTabBar::tab:!selected{
    margin-top:5px;
}
#tab,#tab_2,#tab_3{
    background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #f38af4,stop:1 #f569f7);
    border-radius:6px;
}
        """)

        self.curSkin = "pink"

    def changeSkin(self):
        if self.curSkin == "black":
            self.skinPink()
        else:
            self.skinBlack()

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
        
        self.dateLable.setText(t.whatDateToday() + " " + t.whatDayToday(self.curLang))
        self.checkAlert()

    def checkAlert(self):
        now = t.getTimeHm()
        #now = time.strftime("%",time.localtime())
        rowNum = 0
        flag = True
        while flag:
            try:
                taskName = self.todayTodoTable.model.item(rowNum, 0).text()
                taskTime = self.todayTodoTable.model.item(rowNum, 4).text()
                rowNum += 1
                if (taskTime == now) and (taskName not in self.alertList):
                    #self.alertSound.play()
                    QMessageBox.question(self, 
                                                "EasyOM",
                                                "%s\n\n【%s】任务时间到了！" % (now, taskName),
                                                QMessageBox.Ok)
                    self.alertList.append(taskName)
            except:
                flag = False

    def dateInit(self):
        today = time.strftime("%Y-%m-%d", time.localtime())
        self.begDate.setDate(QDate.fromString(today, 'yyyy-MM-dd'))
        self.begDate_2.setDate(QDate.fromString(today, 'yyyy-MM-dd'))
        self.endDate.setDate(QDate.fromString(today, 'yyyy-MM-dd'))
        self.endDate_2.setDate(QDate.fromString(today, 'yyyy-MM-dd'))

    #localize
    def localize(self, lang):
        self.topLabel.setText(l.softName[lang])
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), l.homeTab[lang])
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), l.queryTab[lang])
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), l.analysisTab[lang])
        self.todayTodoLabel.setText(l.todoToday[lang])
        self.todayDoneLabel.setText(l.doneToday[lang])
        self.emerAddButton.setText(l.emerAdd[lang])
        self.pageRefreshButton.setText(l.pageRefresh[lang])
        self.taskListLabel.setText(l.taskList[lang])
        self.begDateLabel.setText(l.begDate[lang])
        self.begDateLabel_2.setText(l.begDate[lang])
        self.endDateLabel.setText(l.endDate[lang])
        self.endDateLabel_2.setText(l.endDate[lang])
        self.queryButton.setText(l.query[lang])
        self.analysisButton.setText(l.query[lang])
        self.totalDoneLabel.setText(l.totalDone[lang])
        self.workLabel.setText(l.duringTotalWork[lang])
        self.workLabel_2.setText(l.duringTotalVacation[lang])
        self.workLabel_3.setText(l.duringDays[lang])

    #taskShow
    def showTaskList(self):
        self.taskList = c.readTasksConf()

        insInfo = [l.taskName[self.curLang], l.taskType[self.curLang], l.taskFreq[self.curLang], l.taskDate[self.curLang], l.taskTime[self.curLang], l.taskDeli[self.curLang]]
        insList = ["task_name", "task_type", "task_freq", "task_date", "task_time", "task_deli_need"]

        self.taskListTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.taskListTable.model = QStandardItemModel(0, 0, self.taskListTable)
        self.taskListTable.model.setHorizontalHeaderLabels(insInfo)

        ctRow = 0

        for task in self.taskList:
            self.taskStandardize(task)

            ctCol = 0

            for ins in insList:
                item = QStandardItem(task[ins])
                self.taskListTable.model.setItem(ctRow, ctCol, item)
                ctCol += 1
            
            ctRow += 1
        
        self.taskListTable.setModel(self.taskListTable.model)
        self.taskListTable.setContextMenuPolicy(Qt.CustomContextMenu)
        self.taskListTable.customContextMenuRequested.connect(self.showListMenu)

    def showTodoToday(self):
        self.logLogin()
        taskList4Todo = c.readTasksConf()
        taskList4Emer = c.readEmerConf()

        insInfo = [l.taskName[self.curLang], l.taskType[self.curLang], l.taskFreq[self.curLang], l.taskDate[self.curLang], l.taskTime[self.curLang], l.taskDeli[self.curLang]]
        insList = ["task_name", "task_type", "task_freq", "task_date", "task_time", "task_deli_need"]

        self.todayTodoTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.todayTodoTable.model = QStandardItemModel(0, 0, self.todayTodoTable)
        self.todayTodoTable.model.setHorizontalHeaderLabels(insInfo)

        ctRow = 0

        for task in taskList4Emer:
            if self.emerIsTodo(task):
                self.taskStandardize(task)

                ctCol = 0

                for ins in insList:
                    item = QStandardItem(task[ins])
                    self.todayTodoTable.model.setItem(ctRow, ctCol, item)

                    ctCol += 1

                ctRow += 1

        for task in taskList4Todo:
            if self.taskIsTodo(task):
                self.taskStandardize(task)

                ctCol = 0

                for ins in insList:
                    item = QStandardItem(task[ins])
                    self.todayTodoTable.model.setItem(ctRow, ctCol, item)

                    ctCol += 1

                ctRow += 1

        self.todayTodoTable.setModel(self.todayTodoTable.model)

        self.todayTodoTable.doubleClicked.connect(self.todoAct)

        if ctRow == 0:
            QMessageBox.information(self, "Information", l.noTodo[self.curLang])
        
        self.moveTodo2Left()

        self.todayTodoTable.setContextMenuPolicy(Qt.CustomContextMenu)
        self.todayTodoTable.customContextMenuRequested.connect(self.showTodoMenu)
        
    def showDoneToday(self):
        taskList4Done = c.readDoneLogToday()

        insInfo = [l.taskName[self.curLang], l.taskType[self.curLang], l.doneTime[self.curLang], l.taskDeli[self.curLang]]
        insList = ["task_name", "task_type", "done_time", "task_deli"]

        self.todayDoneTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.todayDoneTable.model = QStandardItemModel(0, 0, self.todayDoneTable)
        self.todayDoneTable.model.setHorizontalHeaderLabels(insInfo)

        ctRow = 0

        for task in taskList4Done:
            if 1 == 1:
                #self.taskStandardize(task)

                ctCol = 0

                for ins in insList:
                    item = QStandardItem(task[ins])
                    self.todayDoneTable.model.setItem(ctRow, ctCol, item)

                    ctCol += 1

                ctRow += 1

        self.todayDoneTable.setModel(self.todayDoneTable.model)
    
    #standardize
    def taskStandardize(self, task):
        if ("month" in task["task_freq"]) or ("season" in task["task_freq"]):           
            pattern = re.compile(r'^[0-9]+$')
            match = pattern.match(task["task_date"])

            if match:
                task["task_date"] = task["task_date"] + l.ri[self.curLang]
            else:
                task["task_date"] = l.unknown[self.curLang]
        elif "emergency" in task["task_freq"]:
            try:
                num = task["task_date"].split("_")
                year = num[0]
                month = num[1]
                day = num[2]
                pattern = re.compile(r'^[0-9]+$')
                match0 = pattern.match(year)
                match1 = pattern.match(month)
                match2 = pattern.match(day)

                if match0 and match1 and match2:
                    task["task_date"] = year + l.nian[self.curLang] + month + l.yue[self.curLang] + day + l.ri[self.curLang]
                else:
                    task["task_date"] = l.unknown[self.curLang]
            except:
                task["task_date"] = l.unknown[self.curLang]
        elif "annual" in task["task_freq"]:
            try:
                num = task["task_date"].split("_")
                month = num[0]
                day = num[1]
                pattern = re.compile(r'^[0-9]+$')
                match1 = pattern.match(month)
                match2 = pattern.match(day)

                if match1 and match2:
                    task["task_date"] = month + l.yue[self.curLang] + day + l.ri[self.curLang]
                else:
                    task["task_date"] = l.unknown[self.curLang]
            except:
                task["task_date"] = l.unknown[self.curLang]
        elif "/" in task["task_date"]:
            task["task_date"] = "-"
        else:
            task["task_date"] = l.unknown[self.curLang]
        
        if task["task_freq"] == "daily_weekday":
            task["task_freq"] = l.dailyWeekday[self.curLang]
        elif task["task_freq"] == "daily_weekend":
            task["task_freq"] = l.dailyWeekend[self.curLang]
        elif task["task_freq"] == "weekly_sunday":
            task["task_freq"] = l.weeklySunday[self.curLang]
        elif task["task_freq"] == "weekly_monday":
            task["task_freq"] = l.weeklyMonday[self.curLang]
        elif task["task_freq"] == "weekly_tuesday":
            task["task_freq"] = l.weeklyTuesday[self.curLang]
        elif task["task_freq"] == "weekly_wednesday":
            task["task_freq"] = l.weeklyWednesday[self.curLang]
        elif task["task_freq"] == "weekly_thursday":
            task["task_freq"] = l.weeklyThursday[self.curLang]
        elif task["task_freq"] == "weekly_friday":
            task["task_freq"] = l.weeklyFriday[self.curLang]
        elif task["task_freq"] == "weekly_saturday":
            task["task_freq"] = l.weeklySaturday[self.curLang]
        elif task["task_freq"] == "monthly":
            task["task_freq"] = l.monthly[self.curLang]
        elif task["task_freq"] == "double_monthly":
            task["task_freq"] = l.doubleMonth[self.curLang]
        elif task["task_freq"] == "seasonly":
            task["task_freq"] = l.seasonly[self.curLang]
        elif task["task_freq"] == "annually":
            task["task_freq"] = l.annually[self.curLang]
        elif task["task_freq"] == "emergency":
            task["task_freq"] = l.emergency[self.curLang]
        else:
            task["task_freq"] = l.unknown[self.curLang]

        try:        
            num = task["task_time"].split("_")
            hour = num[0]
            minute = num[1]
            pattern = re.compile(r'[0-9][0-9]')
            match1 = pattern.match(hour)
            match2 = pattern.match(minute)
            if match1 and match2:
                task["task_time"] = hour + ":" + minute
            else:
                task["task_time"] = l.unknown[self.curLang]
        except:
            task["task_time"] = l.unknown[self.curLang]

        try:
            og = task["task_deli_need"]
            if og == "yes":
                task["task_deli_need"] = l.yes[self.curLang]
            else:
                task["task_deli_need"] = l.no[self.curLang]
        except:
            pass

    def emerIsTodo(self, task):
        doneList = c.readDoneLogToday()
        leftList = c.readLeftLogToday()

        for done in doneList:
            if task["task_name"] == done["task_name"]:
                return False

        for left in leftList:
            if task["task_name"] == left["task_name"]:
                return True

        today = t.whatDateToday()

        todayL = today.split("-")

        dueDay = task["task_date"]
        dueL = dueDay.split("_")

        if (int(todayL[0]) == int(dueL[0])) and (int(todayL[1]) == int(dueL[1])) and (int(todayL[2]) == int(dueL[2])):
            return True

        return False

    def taskIsTodo(self, task):
        doneList = c.readDoneLogToday()
        leftList = c.readLeftLogToday()
        loginList = c.readLoginLog()

        loginDays = list()
        for login in loginList:
            if login["login_date"] not in loginDays:
                loginDays.append(login["login_date"])

        #print(loginDays[0])

        #today = time.strftime('%Y-%m-%d',time.localtime(time.time()))

        for done in doneList:
            if task["task_name"] == done["task_name"]:
                return False

        for left in leftList:
            if task["task_name"] == left["task_name"]:
                return True

        if task["task_freq"] == "daily_weekday":
            if (t.whatDayToday(self.curLang) in l.monday) or (t.whatDayToday(self.curLang) in l.tuesday) or (t.whatDayToday(self.curLang) in l.wednesday) or (t.whatDayToday(self.curLang) in l.thursday) or (t.whatDayToday(self.curLang) in l.friday):
                return True
            else:
                lastFriday = t.getLastDay(5)
                doneL = c.readDoneLog(lastFriday)
                dones = list()
                for done in doneL:
                    dones.append(done["task_name"])
                
                if (task["task_name"] not in dones) and t.strDateGreater(lastFriday, loginDays[0]):
                    return True
                else:
                    return False
                return False
        elif task["task_freq"] == "daily_weekend":
            if (t.whatDayToday(self.curLang) in l.saturday) or (t.whatDayToday(self.curLang) in l.sunday):
                return True
            else:
                lastSunday = t.getLastDay(0)
                doneL = c.readDoneLog(lastSunday)
                dones = list()
                for done in doneL:
                    dones.append(done["task_name"])
                
                if (task["task_name"] not in dones) and t.strDateGreater(lastSunday, loginDays[0]):
                    return True
                else:
                    return False
                return False
        elif task["task_freq"] == "weekly_sunday":
            if (t.whatDayToday(self.curLang) in l.sunday):
                return True
            else:
                lastDay = t.getLastDay(0)
                doneL = c.readDoneLog(lastDay)
                dones = list()
                for done in doneL:
                    dones.append(done["task_name"])
                
                if (task["task_name"] not in dones) and t.strDateGreater(lastDay, loginDays[0]):
                    return True
                else:
                    return False
                return False
        elif task["task_freq"] == "weekly_monday":
            if (t.whatDayToday(self.curLang) in l.monday):
                return True
            else:
                lastDay = t.getLastDay(1)
                doneL = c.readDoneLog(lastDay)
                dones = list()
                for done in doneL:
                    dones.append(done["task_name"])
                
                if (task["task_name"] not in dones) and t.strDateGreater(lastDay, loginDays[0]):
                    return True
                else:
                    return False
                return False
        elif task["task_freq"] == "weekly_tuesday":
            if (t.whatDayToday(self.curLang) in l.tuesday):
                return True
            else:
                lastDay = t.getLastDay(2)
                doneL = c.readDoneLog(lastDay)
                dones = list()
                for done in doneL:
                    dones.append(done["task_name"])
                
                if (task["task_name"] not in dones) and t.strDateGreater(lastDay, loginDays[0]):
                    return True
                else:
                    return False
                return False
        elif task["task_freq"] == "weekly_wednesday":
            if (t.whatDayToday(self.curLang) in l.wednesday):
                return True
            else:
                lastDay = t.getLastDay(3)
                doneL = c.readDoneLog(lastDay)
                dones = list()
                for done in doneL:
                    dones.append(done["task_name"])
                
                if (task["task_name"] not in dones) and t.strDateGreater(lastDay, loginDays[0]):
                    return True
                else:
                    return False
                return False
        elif task["task_freq"] == "weekly_thursday":
            if (t.whatDayToday(self.curLang) in l.thursday):
                return True
            else:
                lastDay = t.getLastDay(4)
                doneL = c.readDoneLog(lastDay)
                dones = list()
                for done in doneL:
                    dones.append(done["task_name"])
                
                if (task["task_name"] not in dones) and t.strDateGreater(lastDay, loginDays[0]):
                    return True
                else:
                    return False
                return False
        elif task["task_freq"] == "weekly_friday":
            if (t.whatDayToday(self.curLang) in l.friday):
                return True
            else:
                lastDay = t.getLastDay(5)
                #print(lastDay)
                doneL = c.readDoneLog(lastDay)
                dones = list()
                for done in doneL:
                    dones.append(done["task_name"])
                #print("%s %s" % (lastDay, loginDays[0]))
                if (task["task_name"] not in dones) and t.strDateGreater(lastDay, loginDays[0]):
                    #print("lastDay: %s loginDays[0]: %s gt: %s" % (lastDay, loginDays[0], t.strDateGreater(lastDay, loginDays[0])))
                    return True
                else:
                    return False
                return False
        elif task["task_freq"] == "weekly_saturday":
            if (t.whatDayToday(self.curLang) in l.saturday):
                return True
            else:
                lastDay = t.getLastDay(6)
                doneL = c.readDoneLog(lastDay)
                dones = list()
                for done in doneL:
                    dones.append(done["task_name"])
                
                if (task["task_name"] not in dones) and t.strDateGreater(lastDay, loginDays[0]):
                    return True
                else:
                    return False
                return False
        elif task["task_freq"] == "monthly":
            if task["task_date"] == time.strftime("%d",time.localtime(time.time())):
                return True
            else:
                lastDay = t.getLastMonthDay(int(task["task_date"]))
                doneL = c.readDoneLog(lastDay)
                dones = list()
                for done in doneL:
                    dones.append(done["task_name"])
                
                if (task["task_name"] not in dones) and t.strDateGreater(lastDay, loginDays[0]):
                    return True
                else:
                    return False
                return False
        elif task["task_freq"] == "double_monthly":
            #print("taskDate: %s" % int(task["task_date"]))
            if (task["task_date"] == time.strftime("%d",time.localtime(time.time()))) and (int(time.strftime("%m",time.localtime(time.time()))) % 2 == 0):
                #print(1)
                return True
            else:
                #print(2)
                lastDay = t.getLast2MonthDay(int(task["task_date"]))
                #print(lastDay)
                doneL = c.readDoneLog(lastDay)
                dones = list()
                for done in doneL:
                    dones.append(done["task_name"])
                
                #print(dones)
                #print(task["task_name"])
                
                if (task["task_name"] not in dones) and (t.strDateGreater(lastDay, loginDays[0])):
                    return True
                else:
                    return False
                return False
        elif task["task_freq"] == "seasonly":
            if (task["task_date"] == time.strftime("%d",time.localtime(time.time()))) and (int(time.strftime("%m",time.localtime(time.time()))) % 3 == 0):
                return True
            else:
                lastDay = t.getLast3MonthDay(int(task["task_date"]))
                doneL = c.readDoneLog(lastDay)
                dones = list()
                for done in doneL:
                    dones.append(done["task_name"])
                
                if (task["task_name"] not in dones) and t.strDateGreater(lastDay, loginDays[0]):
                    return True
                else:
                    return False
                return False
        elif task["task_freq"] == "annually":
            num = task["task_date"].split("_")
            if (num[0] == time.strftime("%m",time.localtime(time.time()))) and (num[1] == time.strftime("%d",time.localtime(time.time()))):
                return True
            else:
                lastDay = t.getLastYearDay(int(num[0]), int(num[1]))
                
                doneL = c.readDoneLog(lastDay)
                dones = list()
                for done in doneL:
                    dones.append(done["task_name"])
                
                if (task["task_name"] not in dones) and t.strDateGreater(lastDay, loginDays[0]):
                    return True
                else:
                    return False
                return False
        else:
            return False
    
    def isOverTime(self, task, fileDate):
        if task["task_type"] == "临时任务":
            return False

        missionList = c.readTasksConf()

        target = None

        for mission in missionList:
            if mission["task_name"] == task["task_name"]:
                target = mission
                break
        
        if target == None:
            return False

        fileRi = fileDate.split("-")[2]
        fileDay = t.whatDay(self.curLang, fileDate)

        if target["task_freq"] == "daily_weekday" or target["task_freq"] == "daily_weekend":
            return False
        elif target["task_freq"] == "weekly_sunday":
            if fileDay in l.sunday:
                return False
            else:
                return True
        elif target["task_freq"] == "weekly_monday":
            if fileDay in l.monday:
                return False
            else:
                return True
        elif target["task_freq"] == "weekly_tuesday":
            if fileDay in l.tuesday:
                return False
            else:
                return True
        elif target["task_freq"] == "weekly_wednesday":
            if (fileDay in l.wednesday):
                return False
            else:
                return True
        elif target["task_freq"] == "weekly_thursday":
            if (fileDay in l.thursday):
                return False
            else:
                return True
        elif target["task_freq"] == "weekly_friday":
            if (fileDay in l.friday):
                return False
            else:
                return True
        elif target["task_freq"] == "weekly_saturday":
            if (fileDay in l.saturday):
                return False
            else:
                return True
        else:
            targetDay = target["task_date"].split("_")[-1].strip()
            if fileRi == targetDay:
                return False
            else:
                return True

    #button for table
    def todoAct(self):
        index =  self.todayTodoTable.currentIndex()
        rowNum = index.row()
        try:
            taskName = self.todayTodoTable.model.item(rowNum, 0).text()
            taskFreq = self.todayTodoTable.model.item(rowNum, 2).text()
            taskDate = self.todayTodoTable.model.item(rowNum, 3).text()
            taskType = self.todayTodoTable.model.item(rowNum, 1).text()
            taskDeliNeed = self.todayTodoTable.model.item(rowNum, 5).text()
            taskDeli = "/"

            if taskDeliNeed in l.yes:
                isDeli = True
            else:
                isDeli = False
        
            reply = QMessageBox.question(self, 
                                                "EasyOM",
                                                l.confirmFinish[self.curLang] + taskName + l.questionMark[self.curLang],
                                                QMessageBox.Yes | QMessageBox.No,
                                                QMessageBox.No)
        
            if reply == QMessageBox.Yes:
                if isDeli:
                    self.DeliComm = DeliCommit()
                    self.DeliComm.cancelButton.clicked.connect(self.DeliComm.close)
                    self.DeliComm.okButton.clicked.connect(lambda: self.doDeliCommit(taskName, taskType))
                    self.DeliComm.show()
                else:
                    self.todo2Done(taskName, taskType, taskDeli)
            else:
                pass
        except:
            pass

    def doDeliCommit(self, taskName, taskType):
        if self.DeliComm.deli.text().strip() != "":
            taskDeli = self.DeliComm.deli.text().strip()
            self.DeliComm.close()
            self.todo2Done(taskName, taskType, taskDeli)
        else:
            QMessageBox.question(self, 
                                                "Info",
                                                "可交付成果必须提交！",
                                                QMessageBox.Ok)

    #todo2Done
    def todo2Done(self, taskName, taskType, taskDeli):
        if not path.isdir("log"):
            makedirs("log")
        
        today = time.strftime('%Y-%m-%d',time.localtime(time.time()))

        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        doneFileName = "done_%s.done" % today

        #missionList = self.taskList

        text = ""

        #for mission in missionList:
            #if mission["task_name"] == taskName:
                #task = mission
        
        try:
            text = text + ("----\ntask_name : %s\ntask_type : %s\ntask_deli : %s\ndue_date : %s\ndone_time : %s\n" % (taskName, taskType, taskDeli, "", now))
        except Exception as E:
            print(E)

        with open("log/%s" % doneFileName, "a+", encoding="utf-8") as fa:
            fa.write(text + "\n")
        
        self.showDoneToday()
        self.showTodoToday()
    
    def moveTodo2Left(self):
        rowNum = 0
        text = ""

        while True:
            try:
                text = text + ("----\ntask_name : %s\ntask_type : %s\ndue_date : %s\n" % (self.todayTodoTable.model.item(rowNum, 0).text(), self.todayTodoTable.model.item(rowNum, 1).text(), ""))
                rowNum += 1
            except:
                break
        
        #print(text)

        if not path.isdir("log"):
            makedirs("log")

        leftFileName = "left_tasks.left"

        with open("log/%s" % leftFileName, "w+", encoding="utf-8") as fw:
            fw.write(text)

    def logLogin(self):
        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        today = time.strftime('%Y-%m-%d',time.localtime(time.time()))

        loginFileName = "login.lin"

        text = "----\nlogin_date : %s\nlogin_time : %s\n" % (today, now)

        if not path.isdir("log"):
            makedirs("log")

        with open("log/%s" % loginFileName, "a+", encoding="utf-8") as fa:
            fa.write(text + "\n")
    
    def addEmergency(self):
        self.addEmer = AddEmer()
        self.addEmer.show()

    def refresh(self):
        self.showTaskList()
        self.showTodoToday()
        self.showDoneToday()

    def query(self):
        begDate = self.begDate.date().toString("yyyy-MM-dd")
        endDate = self.endDate.date().toString("yyyy-MM-dd")
        pathList = c.walkDir("log", "done")

        insInfo = [l.taskName[self.curLang], l.taskType[self.curLang], l.doneTime[self.curLang], l.taskDeli[self.curLang]]
        insList = ["task_name", "task_type", "done_time", "task_deli"]

        self.queryTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.queryTable.model = QStandardItemModel(0, 0, self.queryTable)
        self.queryTable.model.setHorizontalHeaderLabels(insInfo)

        ctRow = 0

        doneList = []

        for path in pathList:
            fileDate = c.getDoneFileDate(path)
            if t.strDateGreater(fileDate, begDate) and t.strDateGreater(endDate, fileDate):
                doneList.extend(c.readDoneLog(fileDate))
        
        for task in doneList:
            if 1 == 1:
                #self.taskStandardize(task)

                ctCol = 0

                for ins in insList:
                    item = QStandardItem(task[ins])
                    self.queryTable.model.setItem(ctRow, ctCol, item)

                    ctCol += 1

                ctRow += 1

        self.queryTable.setModel(self.queryTable.model)

    def analysis(self):
        begDate = self.begDate_2.date().toString("yyyy-MM-dd")
        endDate = self.endDate_2.date().toString("yyyy-MM-dd")

        score = 0
        scoreTemp = 0
        weight = 0
        scoreSysChk = 0
        scoreSysChkTemp = 0
        weightSysChk = 0
        scoreDataEdit = 0
        scoreDataEditTemp = 0
        weightDataEdit = 0
        scoreReqTrck = 0
        scoreReqTrckTemp = 0
        weightReqTrck = 0
        scorePrjManChg = 0
        scorePrjManChgTemp = 0
        weightPrjManChg = 0
        scoreOtherWork = 0
        scoreOtherWorkTemp = 0
        weightOtherWork = 0
        scoreTempoWork = 0
        scoreTempoWorkTemp = 0
        weightTempoWork = 0

        pathList = c.walkDir("log", "done")

        leftList = c.readLeftLogToday()

        ctSysChkLeft = 0
        ctDataEditLeft = 0
        ctReqTrckLeft = 0
        ctPrjManChgLeft = 0
        ctOtherWorkLeft = 0

        for left in leftList:
            if left["task_type"] == "系统例行检查":
                ctSysChkLeft += 1
            elif left["task_type"] == "日常数据修改":
                ctDataEditLeft += 1
            elif left["task_type"] == "需求跟踪反馈":
                ctReqTrckLeft += 1
            elif left["task_type"] == "项目管理变更":
                ctPrjManChgLeft += 1
            elif left["task_type"] == "其他维护事务":
                ctOtherWorkLeft += 1

        ctDone = 0
        ctWork = 0

        taskAll = []

        ctOT = dict()
        ctOT["系统例行检查"] = 0
        ctOT["日常数据修改"] = 0
        ctOT["需求跟踪反馈"] = 0
        ctOT["项目管理变更"] = 0
        ctOT["其他维护事务"] = 0

        for path in pathList:
            fileDate = c.getDoneFileDate(path)
            if t.strDateGreater(fileDate, begDate) and t.strDateGreater(endDate, fileDate):
                doneList = c.readDoneLog(fileDate)
                ctDone += len(doneList)
                taskAll = taskAll + doneList
                ctWork += 1

                for done in doneList:
                    if self.isOverTime(done, fileDate):
                        try:
                            ctOT[done["task_type"]] += 1
                        except:
                            ctOT["其他维护事务"] += 1

        typeDict = dict()

        typeDict["系统例行检查"] = 0
        typeDict["日常数据修改"] = 0
        typeDict["需求跟踪反馈"] = 0
        typeDict["项目管理变更"] = 0
        typeDict["其他维护事务"] = 0
        typeDict["临时任务"] = 0
        typeDict["Temporary Task"] = 0

        for task in taskAll:
            if task["task_type"] not in typeDict:
                typeDict[task["task_type"]] = 1
            else:
                typeDict[task["task_type"]] += 1

        text = ""

        for typee in typeDict:
            text = text + "%s : %s\n\n" % (typee, str(typeDict[typee]))

        text = text.strip()

        ctTotal = t.strDateDiff(begDate, endDate) + 1
        ctVac = ctTotal - ctWork

        self.totalDone.setText(str(ctDone))
        self.workDays.setText(str(ctWork))
        self.holiDays.setText(str(ctVac))
        self.typeNo.setText(text)

        if ctSysChkLeft >= 40:
            wt = 5
            scoreTemp += 0 * wt
            weight += wt
            scoreSysChkTemp += 0 * wt
            weightSysChk += wt
        else:
            wt = 5
            scoreTemp += 100 * (1 - (40 - ctSysChkLeft) / 40) * wt
            weight += wt
            scoreSysChkTemp += 100 * (1 - (40 - ctSysChkLeft) / 40) * wt
            weightSysChk += wt

        if ctOT["系统例行检查"] >= 40:
            wt = 3
            scoreTemp += 0 * wt
            weight += wt
            scoreSysChkTemp += 0 * wt
            weightSysChk += wt
        else:
            wt = 3
            scoreTemp += 100 * (1 - (40 - ctOT["系统例行检查"]) / 40) * wt
            weight += wt
            scoreSysChkTemp += 100 * (1 - (40 - ctOT["系统例行检查"]) / 40) * wt
            weightSysChk += wt

        if typeDict["系统例行检查"] >= 48:
            wt = 2
            scoreTemp += 100 * wt
            weight += wt
            scoreSysChkTemp += 100 * wt
            weightSysChk += wt
        else:
            wt = 2
            scoreTemp += 100 * (typeDict["系统例行检查"] / 48) * wt
            weight += wt
            scoreSysChkTemp += 100 * (typeDict["系统例行检查"] / 48) * wt
            weightSysChk += wt

        if ctDataEditLeft >= 20:
            wt = 5
            scoreTemp += 0 * wt
            weight += wt
            scoreDataEditTemp += 0 * wt
            weightDataEdit += wt
        else:
            wt = 5
            scoreTemp += 100 * (1 - (20 - ctDataEditLeft) / 20) * wt
            weight += wt
            scoreDataEditTemp += 100 * (1 - (20 - ctDataEditLeft) / 20) * wt
            weightDataEdit += wt

        if ctOT["日常数据修改"] >= 16:
            wt = 3
            scoreTemp += 0 * wt
            weight += wt
            scoreDataEditTemp += 0 * wt
            weightDataEdit += wt
        else:
            wt = 3
            scoreTemp += 100 * (1 - (16 - ctOT["日常数据修改"]) / 16) * wt
            weight += wt
            scoreDataEditTemp += 100 * (1 - (16 - ctOT["日常数据修改"]) / 16) * wt
            weightDataEdit += wt

        if typeDict["日常数据修改"] >= 40:
            wt = 2
            scoreTemp += 100 * wt
            weight += wt
            scoreDataEditTemp += 100 * wt
            weightDataEdit += wt
        else:
            wt = 2
            scoreTemp += 100 * (typeDict["日常数据修改"] / 40) * wt
            weight += wt
            scoreDataEditTemp += 100 * (typeDict["日常数据修改"] / 40) * wt
            weightDataEdit += wt

        if ctReqTrckLeft >= 20:
            wt = 5
            scoreTemp += 0 * wt
            weight += wt
            scoreReqTrckTemp += 0 * wt
            weightReqTrck += wt
        else:
            wt = 5
            scoreTemp += 100 * (1 - (20 - ctReqTrckLeft) / 20) * wt
            weight += wt
            scoreReqTrckTemp += 100 * (1 - (20 - ctReqTrckLeft) / 20) * wt
            weightReqTrck += wt

        if ctOT["需求跟踪反馈"] >= 8:
            wt = 3
            scoreTemp += 0 * wt
            weight += wt
            scoreReqTrckTemp += 0 * wt
            weightReqTrck += wt
        else:
            wt = 3
            scoreTemp += 100 * (1 - (8 - ctOT["需求跟踪反馈"]) / 8) * wt
            weight += wt
            scoreReqTrckTemp += 100 * (1 - (8 - ctOT["需求跟踪反馈"]) / 8) * wt
            weightReqTrck += wt

        if typeDict["需求跟踪反馈"] >= 20:
            wt = 2
            scoreTemp += 100 * wt
            weight += wt
            scoreReqTrckTemp += 100 * wt
            weightReqTrck += wt
        else:
            wt = 2
            scoreTemp += 100 * (typeDict["需求跟踪反馈"] / 20) * wt
            weight += wt
            scoreReqTrckTemp += 100 * (typeDict["需求跟踪反馈"] / 20) * wt
            weightReqTrck += wt

        if ctPrjManChgLeft >= 20:
            wt = 5
            scoreTemp += 0 * wt
            weight += wt
            scorePrjManChgTemp += 0 * wt
            weightPrjManChg += wt
        else:
            wt = 5
            scoreTemp += 100 * (1 - (20 - ctPrjManChgLeft) / 20) * wt
            weight += wt
            scorePrjManChgTemp += 100 * (1 - (20 - ctPrjManChgLeft) / 20) * wt
            weightPrjManChg += wt

        if ctOT["项目管理变更"] >= 8:
            wt = 3
            scoreTemp += 0 * wt
            weight += wt
            scorePrjManChgTemp += 0 * wt
            weightPrjManChg += wt
        else:
            wt = 3
            scoreTemp += 100 * (1 - (8 - ctOT["项目管理变更"]) / 8) * wt
            weight += wt
            scorePrjManChgTemp += 100 * (1 - (8 - ctOT["项目管理变更"]) / 8) * wt
            weightPrjManChg += wt

        if typeDict["项目管理变更"] >= 28:
            wt = 2
            scoreTemp += 100 * wt
            weight += wt
            scorePrjManChgTemp += 100 * wt
            weightPrjManChg += wt
        else:
            wt = 2
            scoreTemp += 100 * (typeDict["项目管理变更"] / 28) * wt
            weight += wt
            scorePrjManChgTemp += 100 * (typeDict["项目管理变更"] / 28) * wt
            weightPrjManChg += wt

        if ctOtherWorkLeft >= 20:
            wt = 5
            scoreTemp += 0 * wt
            weight += wt
            scoreOtherWorkTemp += 0 * wt
            weightOtherWork += wt
        else:
            wt = 5
            scoreTemp += 100 * (1 - (20 - ctOtherWorkLeft) / 20) * wt
            weight += wt
            scoreOtherWorkTemp += 100 * (1 - (20 - ctOtherWorkLeft) / 20) * wt
            weightOtherWork += wt

        if ctOT["其他维护事务"] >= 8:
            wt = 3
            scoreTemp += 0 * wt
            weight += wt
            scoreOtherWorkTemp += 0 * wt
            weightOtherWork += wt
        else:
            wt = 3
            scoreTemp += 100 * (1 - (8 - ctOT["其他维护事务"]) / 8) * wt
            weight += wt
            scoreOtherWorkTemp += 100 * (1 - (8 - ctOT["其他维护事务"]) / 8) * wt
            weightOtherWork += wt

        if typeDict["其他维护事务"] >= 20:
            wt = 2
            scoreTemp += 100 * wt
            weight += wt
            scoreOtherWorkTemp += 100 * wt
            weightOtherWork += wt
        else:
            wt = 2
            scoreTemp += 100 * (typeDict["其他维护事务"] / 20) * wt
            weight += wt
            scoreOtherWorkTemp += 100 * (typeDict["其他维护事务"] / 20) * wt
            weightOtherWork += wt

        ctTW = typeDict["临时任务"] + typeDict["Temporary Task"]

        if ctTW >= 80:
            wt = 3
            scoreTemp += 100 * wt
            weight += wt
            scoreTempoWorkTemp += 100 * wt
            weightTempoWork += wt
        else:
            wt = 3
            scoreTemp += 100 * (ctTW / 80) * wt
            weight += wt
            scoreTempoWorkTemp += 100 * (ctTW / 80) * wt
            weightTempoWork += wt

        if weight > 0:
            score = int(scoreTemp / weight)
        if weightSysChk > 0:
            scoreSysChk = int(scoreSysChkTemp / weightSysChk)
        if weightDataEdit > 0:
            scoreDataEdit = int(scoreDataEditTemp / weightDataEdit)
        if weightReqTrck > 0:
            scoreReqTrck = int(scoreReqTrckTemp / weightReqTrck)
        if weightPrjManChg > 0:
            scorePrjManChg = int(scorePrjManChgTemp / weightPrjManChg)
        if weightOtherWork > 0:
            scoreOtherWork = int(scoreOtherWorkTemp / weightOtherWork)
        if weightTempoWork > 0:
            scoreTempoWork = int(scoreTempoWorkTemp / weightTempoWork)

        conf = c.readConfigConf()

        organ = "未知部门"
        team = "未知项目组"
        name = "未知人员"

        try:
            organ = conf["organ"]
            team = conf["team"]
            name = conf["name"]
        except:
            pass
        
        outText = ""

        month = time.strftime('%Y-%m',time.localtime(time.time()))

        outText = """
        month : %s
        organ : %s
        team : %s
        name : %s
        score : %s
        syschk_score : %s
        dataedit_score : %s
        reqtrck_score : %s
        prjmanchg_score : %s
        otherwork_score : %s
        tempowork_score : %s
        ========
        """ % (month, organ, team, name, score, scoreSysChk, scoreDataEdit, scoreReqTrck, scorePrjManChg, scoreOtherWork, scoreTempoWork)

        for task in taskAll:
            outText = outText + """
        task_name : %s
        task_type : %s
        task_deli : %s
        done_time : %s
        ----
        """ % (task["task_name"], task["task_type"], task["task_deli"], task["done_time"])

        encTemp = base64.b64encode(outText.encode("utf-8")).decode("utf-8")

        if not os.path.isdir("Output"):
            makedirs("Output")

        fileName = "%s_%s_%s_%s.omy" % (organ, team, name, month)

        with open("Output/" + fileName, "w+", encoding='utf-8') as f:
            f.write(encTemp)
        
        #print(outText)
        
    def showListMenu(self):
        self.taskListTable.contextMenu = QMenu(self)
        self.actionViewSolution = self.taskListTable.contextMenu.addAction('Detail')
        self.taskListTable.contextMenu.popup(QCursor.pos())
        self.actionViewSolution.triggered.connect(self.viewSolution4List)
        self.taskListTable.contextMenu.show()

    def showTodoMenu(self):
        self.todayTodoTable.contextMenu = QMenu(self)
        self.actionViewSolutionTodo = self.todayTodoTable.contextMenu.addAction('Detail')
        self.actionFinishTodo = self.todayTodoTable.contextMenu.addAction('Finish')
        self.todayTodoTable.contextMenu.popup(QCursor.pos())
        self.actionViewSolutionTodo.triggered.connect(self.viewSolution4Todo)
        self.actionFinishTodo.triggered.connect(self.todoAct)
        self.todayTodoTable.contextMenu.show()
    
    def viewSolution4Todo(self):
        index =  self.todayTodoTable.currentIndex()
        rowNum = index.row()
        try:
            taskName = self.todayTodoTable.model.item(rowNum, 0).text()
            taskType = self.todayTodoTable.model.item(rowNum, 1).text()
            taskFreq = self.todayTodoTable.model.item(rowNum, 2).text()
            taskDate = self.todayTodoTable.model.item(rowNum, 3).text()
            taskTime = self.todayTodoTable.model.item(rowNum, 4).text()
            taskDeliNeed = self.todayTodoTable.model.item(rowNum, 5).text()
            taskSolution = "/"
            emerList = c.readEmerConf()
            for i in self.taskList:
                if i["task_name"] == taskName:
                    taskSolution = i["task_solution"].replace("\\", "\n")
                else:
                    for emer in emerList:
                        if taskName == emer["task_name"]:
                            taskSolution = emer["task_solution"].replace("\\", "\n")
            

            QMessageBox.question(self, 
                                                "EasyOM",
                                                l.taskName[self.curLang] + ": " + taskName + "\n" 
                                                + l.taskType[self.curLang] + ": " + taskType + "\n"
                                                + l.taskFreq[self.curLang] + ": " + taskFreq + "\n"
                                                + l.taskDate[self.curLang] + ": " + taskDate + "\n"
                                                + l.taskTime[self.curLang] + ": " + taskTime + "\n"
                                                + l.taskDeli[self.curLang] + ": " + taskDeliNeed + "\n"
                                                + l.taskSolution[self.curLang] + ": \n" + taskSolution + "\n",
                                                QMessageBox.Ok)
        except:
            pass

    def viewSolution4List(self):
        index =  self.taskListTable.currentIndex()
        rowNum = index.row()
        try:
            taskName = self.taskListTable.model.item(rowNum, 0).text()
            taskType = self.taskListTable.model.item(rowNum, 1).text()
            taskFreq = self.taskListTable.model.item(rowNum, 2).text()
            taskDate = self.taskListTable.model.item(rowNum, 3).text()
            taskTime = self.taskListTable.model.item(rowNum, 4).text()
            taskDeliNeed = self.taskListTable.model.item(rowNum, 5).text()
            taskSolution = "/"
            emerList = c.readEmerConf()
            for i in self.taskList:
                if i["task_name"] == taskName:
                    taskSolution = i["task_solution"].replace("\\", "\n")
                else:
                    for emer in emerList:
                        if i["task_name"] == emer["task_name"]:
                            taskSolution = emer["task_solution"].replace("\\", "\n")

            QMessageBox.question(self, 
                                                "EasyOM",
                                                l.taskName[self.curLang] + ": " + taskName + "\n" 
                                                + l.taskType[self.curLang] + ": " + taskType + "\n"
                                                + l.taskFreq[self.curLang] + ": " + taskFreq + "\n"
                                                + l.taskDate[self.curLang] + ": " + taskDate + "\n"
                                                + l.taskTime[self.curLang] + ": " + taskTime + "\n"
                                                + l.taskDeli[self.curLang] + ": " + taskDeliNeed + "\n"
                                                + l.taskSolution[self.curLang] + ": \n" + taskSolution + "\n",
                                                QMessageBox.Ok)
        except:
            pass


class AddEmer(QDialog, Ui_addEmer):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        Qt.WA_DeleteOnClose = True
        self.setWindowIcon(QIcon("src/icon.png"))
        now = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
        self.taskTime.setDateTime(QDateTime.fromString(now, "yyyy-MM-dd HH:mm"))
        self.localize()
        self.cancelButton.clicked.connect(self.close)
        self.okButton.clicked.connect(self.add)

    def localize(self):
        self.taskNameLabel.setText("突发事件名称")
        self.taskTimeLabel.setText("突发事件时间")
        self.taskSolutionLabel.setText("突发事件明细")

    def add(self):
        emerName = self.taskName.text()
        emerDate = self.taskTime.dateTime().toString("yyyy_MM_dd")
        emerTime = self.taskTime.dateTime().toString("HH_mm")
        emerSolution = self.taskSolution.toPlainText()

        if emerSolution.strip() == "":
            emerSolution = "/"
        
        emerSolution = emerSolution.replace("\n", "\\")

        emerName = emerName.strip()

        if (emerName == "") or (emerName == None):
            QMessageBox.question(self, 
                                                "Info",
                                                "突发事件描述不能为空！",
                                                QMessageBox.Ok)
        
        else:
            text = "----\ntask_name : %s\ntask_type : 临时任务\ntask_freq : emergency\ntask_date : %s\ntask_time : %s\ntask_solution : %s\ntask_deli_need : no\n" % (emerName, emerDate, emerTime, emerSolution)

            if not path.isdir("conf"):
                makedirs("conf")

            with open("conf/%s" % "emergency.conf", "a+", encoding="utf-8") as fa:
                fa.write(text + "\n")
            
            self.close()

class DeliCommit(QDialog, Ui_DeliCommit):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        Qt.WA_DeleteOnClose = True
        self.setWindowIcon(QIcon("src/icon.png"))