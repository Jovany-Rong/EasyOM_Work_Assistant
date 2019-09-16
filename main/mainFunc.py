#!/usr/local/bin python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from UIs.Ui_mainWindow import Ui_MainWindow
from langs import lanpacks as l
from basifuns import timeFuncs as t
from basifuns import configFuncs as c
import time
import ctypes
import re
from os import path, makedirs

class MainWindow(QMainWindow, Ui_MainWindow):
    curLang = 0
    taskList = list()
    todoList = list()

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
        self.showTaskList()
        self.showTodoToday()
        self.showDoneToday()

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

    #taskShow
    def showTaskList(self):
        self.taskList = c.readTasksConf()

        insInfo = [l.taskName[self.curLang], l.taskFreq[self.curLang], l.taskDate[self.curLang], l.taskTime[self.curLang]]
        insList = ["task_name", "task_freq", "task_date", "task_time"]

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

    def showTodoToday(self):
        taskList4Todo = c.readTasksConf()

        insInfo = [l.taskName[self.curLang], l.taskFreq[self.curLang], l.taskDate[self.curLang], l.taskTime[self.curLang]]
        insList = ["task_name", "task_freq", "task_date", "task_time"]

        self.todayTodoTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.todayTodoTable.model = QStandardItemModel(0, 0, self.todayTodoTable)
        self.todayTodoTable.model.setHorizontalHeaderLabels(insInfo)

        ctRow = 0

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
        
    def showDoneToday(self):
        taskList4Done = c.readDoneLogToday()

        insInfo = [l.taskName[self.curLang], l.doneTime[self.curLang]]
        insList = ["task_name", "done_time"]

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
    
    def taskIsTodo(self, task):
        doneList = c.readDoneLogToday()

        for done in doneList:
            if task["task_name"] == done["task_name"]:
                return False

        if task["task_freq"] == "daily_weekday":
            if (t.whatDayToday(self.curLang) in l.monday) or (t.whatDayToday(self.curLang) in l.tuesday) or (t.whatDayToday(self.curLang) in l.wednesday) or (t.whatDayToday(self.curLang) in l.thursday) or (t.whatDayToday(self.curLang) in l.friday):
                return True
            else:
                return False
        elif task["task_freq"] == "daily_weekend":
            if (t.whatDayToday(self.curLang) in l.saturday) or (t.whatDayToday(self.curLang) in l.sunday):
                return True
            else:
                return False
        elif task["task_freq"] == "weekly_sunday":
            if (t.whatDayToday(self.curLang) in l.sunday):
                return True
            else:
                return False
        elif task["task_freq"] == "weekly_monday":
            if (t.whatDayToday(self.curLang) in l.monday):
                return True
            else:
                return False
        elif task["task_freq"] == "weekly_tuesday":
            if (t.whatDayToday(self.curLang) in l.tuesday):
                return True
            else:
                return False
        elif task["task_freq"] == "weekly_wednesday":
            if (t.whatDayToday(self.curLang) in l.wednesday):
                return True
            else:
                return False
        elif task["task_freq"] == "weekly_thursday":
            if (t.whatDayToday(self.curLang) in l.thursday):
                return True
            else:
                return False
        elif task["task_freq"] == "weekly_friday":
            if (t.whatDayToday(self.curLang) in l.friday):
                return True
            else:
                return False
        elif task["task_freq"] == "weekly_saturday":
            if (t.whatDayToday(self.curLang) in l.saturday):
                return True
            else:
                return False
        elif task["task_freq"] == "monthly":
            if task["task_date"] == time.strftime("%d",time.localtime(time.time())):
                return True
            else:
                return False
        elif task["task_freq"] == "double_monthly":
            if (task["task_date"] == time.strftime("%d",time.localtime(time.time()))) and (int(time.strftime("%m",time.localtime(time.time()))) % 2 == 0):
                return True
            else:
                return False
        elif task["task_freq"] == "seasonly":
            if (task["task_date"] == time.strftime("%d",time.localtime(time.time()))) and (int(time.strftime("%m",time.localtime(time.time()))) % 3 == 0):
                return True
            else:
                return False
        elif task["task_freq"] == "annually":
            num = task["task_date"].split("_")
            if (num[0] == time.strftime("%m",time.localtime(time.time()))) and (num[1] == time.strftime("%d",time.localtime(time.time()))):
                return True
            else:
                return False
        else:
            return False
    
    #button for table
    def todoAct(self):
        index =  self.todayTodoTable.currentIndex()
        rowNum = index.row()
        try:
            taskName = self.todayTodoTable.model.item(rowNum, 0).text()
            taskFreq = self.todayTodoTable.model.item(rowNum, 1).text()
            taskDate = self.todayTodoTable.model.item(rowNum, 2).text()
        
            reply = QMessageBox.question(self, 
                                                "EasyOM",
                                                l.confirmFinish[self.curLang] + taskName + l.questionMark[self.curLang],
                                                QMessageBox.Yes | QMessageBox.No,
                                                QMessageBox.No)
        
            if reply == QMessageBox.Yes:
                self.todo2Done(taskName)
            else:
                pass
        except:
            pass

    #todo2Done
    def todo2Done(self, taskName):
        if not path.isdir("log"):
            makedirs("log")
        
        today = time.strftime('%Y-%m-%d',time.localtime(time.time()))

        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        doneFileName = "done_%s.done" % today

        missionList = self.taskList

        text = ""

        for mission in missionList:
            if mission["task_name"] == taskName:
                task = mission
        
        try:
            text = text + ("----\ntask_name : %s\ndue_date : %s\ndone_time : %s\n" % (task["task_name"], "", now))
        except Exception as E:
            print(E)

        with open("log/%s" % doneFileName, "a+", encoding="utf-8") as fa:
            fa.write(text + "\n")
        
        self.showDoneToday()
        self.showTodoToday()
    
    def moveTodo2Left(self):
        rowNum = 0

        while True:
            try:
                print(self.todayTodoTable.model.item(rowNum, 0).text())
                rowNum += 1
            except:
                break
