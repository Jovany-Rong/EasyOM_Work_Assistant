#!/usr/local/bin python
#coding: utf-8

import sys
sys.path.append("..")
import time
import datetime
from langs import lanpacks as l

def whatDayToday(lang):
    """
    Return what day it is today, based on the set language.
"""
    today = time.strftime("%Y-%m-%d",time.localtime(time.time()))

    whatDay= datetime.datetime.strptime(today,'%Y-%m-%d').strftime("%w")

    weekList = [l.sunday, l.monday, l.tuesday, l.wednesday, l.thursday, l.friday, l.saturday]

    return weekList[int(whatDay)][lang]

def whatDateToday():
    """
    Return what date it is today.
"""
    today = time.strftime("%Y-%m-%d",time.localtime(time.time()))

    return today