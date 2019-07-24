#!/usr/local/bin python
# -*- coding: utf-8 -*-

class Task(object):
    name = ""
    freq = ""
    date = "/"
    time = "00_00"
    
    def setName(self, name):
        self.name = name

    def setFreq(self, freq):
        self.freq = freq
    
    def setDate(self, date):
        self.date = date

    def setTime(self, time):
        self.time = time