#!/usr/local/bin python
# -*- coding: utf-8 -*-

import time
import os
from langs import lanpacks as l

def readTasksConf():
    path = "conf/tasks.conf"

    ddList = list()

    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        
        partList = text.split("----")

        taskList = list()

        for part in partList:
            if "task_name" in part:
                taskList.append(part)
            
        for task in taskList:
            rowList = task.split("\n")
            
            dd = dict()

            for row in rowList:
                if " : " in row:
                    tList = row.split(" : ")
                    dd[tList[0]] = tList[1]

            if "task_name" in dd.keys() and "task_freq" in dd.keys() and "task_date" in dd.keys() and "task_time" in dd.keys() and "task_solution" in dd.keys() and "task_type" in dd.keys() and "task_deli_need" in dd.keys():
                ddList.append(dd)
        
    except:
        pass

    return ddList

def readEmerConf():
    path = "conf/emergency.conf"

    ddList = list()

    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        
        partList = text.split("----")

        taskList = list()

        for part in partList:
            if "task_name" in part:
                taskList.append(part)
            
        for task in taskList:
            rowList = task.split("\n")
            
            dd = dict()

            for row in rowList:
                if " : " in row:
                    tList = row.split(" : ")
                    dd[tList[0]] = tList[1]
            
            dd["task_type"] = l.tempoTask[1]
            dd["task_deli_need"] = "no"

            if "task_name" in dd.keys() and "task_freq" in dd.keys() and "task_date" in dd.keys() and "task_time" in dd.keys() and "task_solution" in dd.keys():
                ddList.append(dd)
        
    except:
        pass

    return ddList

def readDoneLogToday():
    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))

    path = "log/done_%s.done" % today

    ddList = list()

    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        
        partList = text.split("----")

        taskList = list()

        for part in partList:
            if "task_name" in part:
                taskList.append(part)
            
        for task in taskList:
            rowList = task.split("\n")

            dd = dict()

            for row in rowList:
                if " : " in row:
                    tList = row.split(" : ")
                    dd[tList[0]] = tList[1]
            
            if "task_name" in dd.keys() and "due_date" in dd.keys() and "done_time" in dd.keys() and "task_type" in dd.keys() and "task_deli" in dd.keys():
                ddList.append(dd)

    except:
        pass

    return ddList

def readDoneLog(ddate):

    path = "log/done_%s.done" % ddate

    ddList = list()

    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        
        partList = text.split("----")

        taskList = list()

        for part in partList:
            if "task_name" in part:
                taskList.append(part)
            
        for task in taskList:
            rowList = task.split("\n")

            dd = dict()

            for row in rowList:
                if " : " in row:
                    tList = row.split(" : ")
                    dd[tList[0]] = tList[1]
            
            if "task_name" in dd.keys() and "due_date" in dd.keys() and "done_time" in dd.keys() and "task_type" in dd.keys() and "task_deli" in dd.keys():
                ddList.append(dd)

    except:
        pass

    return ddList

def readLeftLogToday():
    #today = time.strftime('%Y-%m-%d',time.localtime(time.time()))

    path = "log/left_tasks.left"

    ddList = list()

    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        
        partList = text.split("----")

        taskList = list()

        for part in partList:
            if "task_name" in part:
                taskList.append(part)
            
        for task in taskList:
            rowList = task.split("\n")

            dd = dict()

            for row in rowList:
                if " : " in row:
                    tList = row.split(" : ")
                    dd[tList[0]] = tList[1]
            
            if "task_name" in dd.keys() and "due_date" in dd.keys():
                ddList.append(dd)

    except:
        pass

    return ddList

def readLoginLog():
    path = "log/login.lin"

    ddList = list()

    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        
        partList = text.split("----")

        taskList = list()

        for part in partList:
            if "login_date" in part:
                taskList.append(part)
            
        for task in taskList:
            rowList = task.split("\n")

            dd = dict()

            for row in rowList:
                if " : " in row:
                    tList = row.split(" : ")
                    dd[tList[0]] = tList[1]
            
            if "login_date" in dd.keys() and "login_time" in dd.keys():
                ddList.append(dd)

    except:
        pass

    return ddList

def walkDir(path, suf):
    pathList = []
    for root, dirs, files in os.walk(path):
        del dirs
        if not (root.endswith("/") or root.endswith("\\")):
            root = root + "/"
        for file in files:
            if file.endswith(".%s" % suf):
                #print((root + file).replace("\\", "/"))
                pathList.append((root + file).replace("\\", "/"))
    
    return pathList

def getDoneFileDate(file):
    text = file[-15:-5]

    return text