#!/usr/local/bin python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QSound
from UIs.Ui_mainWindow import Ui_MainWindow
from UIs.Ui_addEmer import Ui_addEmer
from langs import lanpacks as l
from basifuns import timeFuncs as t
from basifuns import configFuncs as c
import time
import ctypes
import re
from os import path, makedirs

class MainWindow(QMainWindow, Ui_MainWindow):
    curLang = 1
    taskList = list()
    todoList = list()
    alertList = list()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.statusBar().showMessage("Powered by Chenfei Jovany Rong | Site: https://rongchenfei.com")
        self.tabWidget.setCurrentIndex(0)
        self.setWindowIcon(QIcon("src/easyOM2.png"))
        self.alertSound = QSound("src/alert.wav", self)

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
                taskTime = self.todayTodoTable.model.item(rowNum, 3).text()
                rowNum += 1
                if (taskTime == now) and (taskName not in self.alertList):
                    self.alertSound.play()
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
        self.taskListTable.setContextMenuPolicy(Qt.CustomContextMenu)
        self.taskListTable.customContextMenuRequested.connect(self.showListMenu)

    def showTodoToday(self):
        self.logLogin()
        taskList4Todo = c.readTasksConf()
        taskList4Emer = c.readEmerConf()

        insInfo = [l.taskName[self.curLang], l.taskFreq[self.curLang], l.taskDate[self.curLang], l.taskTime[self.curLang]]
        insList = ["task_name", "task_freq", "task_date", "task_time"]

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

        #missionList = self.taskList

        text = ""

        #for mission in missionList:
            #if mission["task_name"] == taskName:
                #task = mission
        
        try:
            text = text + ("----\ntask_name : %s\ndue_date : %s\ndone_time : %s\n" % (taskName, "", now))
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
                text = text + ("----\ntask_name : %s\ndue_date : %s\n" % (self.todayTodoTable.model.item(rowNum, 0).text(), ""))
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

        insInfo = [l.taskName[self.curLang], l.doneTime[self.curLang]]
        insList = ["task_name", "done_time"]

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

        pathList = c.walkDir("log", "done")

        ctDone = 0
        ctWork = 0

        for path in pathList:
            fileDate = c.getDoneFileDate(path)
            if t.strDateGreater(fileDate, begDate) and t.strDateGreater(endDate, fileDate):
                ctDone += len(c.readDoneLog(fileDate))
                ctWork += 1

        ctTotal = t.strDateDiff(begDate, endDate) + 1
        ctVac = ctTotal - ctWork

        self.totalDone.setText(str(ctWork))
        self.workDays.setText(str(ctWork))
        self.holiDays.setText(str(ctVac))
        
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
            taskFreq = self.todayTodoTable.model.item(rowNum, 1).text()
            taskDate = self.todayTodoTable.model.item(rowNum, 2).text()
            taskTime = self.todayTodoTable.model.item(rowNum, 3).text()
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
                                                + l.taskFreq[self.curLang] + ": " + taskFreq + "\n"
                                                + l.taskDate[self.curLang] + ": " + taskDate + "\n"
                                                + l.taskTime[self.curLang] + ": " + taskTime + "\n"
                                                + l.taskSolution[self.curLang] + ": \n" + taskSolution + "\n",
                                                QMessageBox.Ok)
        except:
            pass

    def viewSolution4List(self):
        index =  self.taskListTable.currentIndex()
        rowNum = index.row()
        try:
            taskName = self.taskListTable.model.item(rowNum, 0).text()
            taskFreq = self.taskListTable.model.item(rowNum, 1).text()
            taskDate = self.taskListTable.model.item(rowNum, 2).text()
            taskTime = self.taskListTable.model.item(rowNum, 3).text()
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
                                                + l.taskFreq[self.curLang] + ": " + taskFreq + "\n"
                                                + l.taskDate[self.curLang] + ": " + taskDate + "\n"
                                                + l.taskTime[self.curLang] + ": " + taskTime + "\n"
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
            text = "----\ntask_name : %s\ntask_freq : emergency\ntask_date : %s\ntask_time : %s\ntask_solution : %s\n" % (emerName, emerDate, emerTime, emerSolution)

            if not path.isdir("conf"):
                makedirs("conf")

            with open("conf/%s" % "emergency.conf", "a+", encoding="utf-8") as fa:
                fa.write(text + "\n")
            
            self.close()