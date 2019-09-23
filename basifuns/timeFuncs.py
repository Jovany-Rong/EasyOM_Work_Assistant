#!/usr/local/bin python
#coding: utf-8

import sys
sys.path.append("..")
import time
import datetime
from langs import lanpacks as l

def getTimeHm():
    now = time.strftime("%H:%M",time.localtime(time.time()))
    return now

def whatDayToday(lang):
    """
    Return what day it is today, based on the set language.
"""
    today = time.strftime("%Y-%m-%d",time.localtime(time.time()))

    whatDay= datetime.datetime.strptime(today,'%Y-%m-%d').strftime("%w")

    weekList = [l.sunday, l.monday, l.tuesday, l.wednesday, l.thursday, l.friday, l.saturday]

    return weekList[int(whatDay)][lang]

def getLastDay(wDay):
    yr = int(time.strftime("%Y",time.localtime(time.time())))
    mo = int(time.strftime("%m",time.localtime(time.time())))
    dy = int(time.strftime("%d",time.localtime(time.time())))
    moDay = {1 : 31, 2 : 28, 3 : 31, 4 : 30, 5 : 31, 6 : 30, 7 : 31, 8 : 31, 9 : 30, 10 : 31, 11 : 30, 12 : 31}

    flag = True

    while flag:
        if dy == 1:
            if mo == 1:
                yr = yr - 1
                mo = 12
                dy = 31
            else:
                mo = mo - 1
                dy = moDay[mo]
                if mo == 2 and isLeapYear(yr):
                    dy = 29

        else:
            dy = dy - 1
        
        if int(datetime.datetime.strptime("%s-%s-%s" % (str(yr), str(mo), str(dy)),'%Y-%m-%d').strftime("%w")) == wDay:
            flag = False
    
    return "%s-%s-%s" % (str(yr), str(mo), str(dy))

def getLastMonthDay(wDay):
    yr = int(time.strftime("%Y",time.localtime(time.time())))
    mo = int(time.strftime("%m",time.localtime(time.time())))
    dy = int(time.strftime("%d",time.localtime(time.time())))
    moDay = {1 : 31, 2 : 28, 3 : 31, 4 : 30, 5 : 31, 6 : 30, 7 : 31, 8 : 31, 9 : 30, 10 : 31, 11 : 30, 12 : 31}

    flag = True

    while flag:
        if mo == 1:
            yr = yr - 1
            mo = 12
        else:
            mo = mo - 1
    
        if wDay <= moDay[mo]:
            flag = False

    return "%s-%s-%s" % (str(yr), str(mo), str(wDay))

def getLast2MonthDay(wDay):
    yr = int(time.strftime("%Y",time.localtime(time.time())))
    mo = int(time.strftime("%m",time.localtime(time.time())))
    dy = int(time.strftime("%d",time.localtime(time.time())))
    moDay = {1 : 31, 2 : 28, 3 : 31, 4 : 30, 5 : 31, 6 : 30, 7 : 31, 8 : 31, 9 : 30, 10 : 31, 11 : 30, 12 : 31}

    flag = True

    while flag:
        if mo <= 2:
            yr = yr - 1
            mo = mo - 2 + 12
        else:
            mo = mo - 2
    
        if wDay <= moDay[mo]:
            flag = False

    return "%s-%s-%s" % (str(yr), str(mo), str(wDay))

def getLast3MonthDay(wDay):
    yr = int(time.strftime("%Y",time.localtime(time.time())))
    mo = int(time.strftime("%m",time.localtime(time.time())))
    dy = int(time.strftime("%d",time.localtime(time.time())))
    moDay = {1 : 31, 2 : 28, 3 : 31, 4 : 30, 5 : 31, 6 : 30, 7 : 31, 8 : 31, 9 : 30, 10 : 31, 11 : 30, 12 : 31}

    flag = True

    while flag:
        if mo <= 3:
            yr = yr - 1
            mo = mo - 3 + 12
        else:
            mo = mo - 3
    
        if wDay <= moDay[mo]:
            flag = False

    return "%s-%s-%s" % (str(yr), str(mo), str(wDay))

def getLastYearDay(wMon, wDay):
    yr = int(time.strftime("%Y",time.localtime(time.time())))

    yr = yr - 1

    return "%s-%s-%s" % (str(yr), str(wMon), str(wDay))

def isLeapYear(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

def whatDateToday():
    """
    Return what date it is today.
"""
    today = time.strftime("%Y-%m-%d",time.localtime(time.time()))

    return today

def whatYearToday():
    year = time.strftime("%Y",time.localtime(time.time()))

    return year

def whatMonthToday():
    month = time.strftime("%m",time.localtime(time.time()))

    return month

def strDateGreater(aDate, bDate):
    if "-" not in bDate:
        return False
    
    aList = aDate.split("-")
    bList = bDate.split("-")

    if int(aList[0]) > int(bList[0]):
        return True
    elif int(aList[0]) < int(bList[0]):
        return False

    if int(aList[1]) > int(bList[1]):
        return True
    elif int(aList[1]) < int(bList[1]):
        return False

    if int(aList[2]) >= int(bList[2]):
        return True
    else:
        return False

def strDateDiff(date1, date2):
    date1=time.strptime(date1,"%Y-%m-%d")
    date2=time.strptime(date2,"%Y-%m-%d")
    date1=datetime.datetime(date1[0],date1[1],date1[2])
    date2=datetime.datetime(date2[0],date2[1],date2[2])

    return (date2 - date1).days