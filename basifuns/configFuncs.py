#!/usr/local/bin python
# -*- coding: utf-8 -*-

import time

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

            if "task_name" in dd.keys() and "task_freq" in dd.keys() and "task_date" in dd.keys() and "task_time" in dd.keys():
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
            
            if "task_name" in dd.keys() and "due_date" in dd.keys() and "done_time" in dd.keys():
                ddList.append(dd)

    except:
        pass

    return ddList