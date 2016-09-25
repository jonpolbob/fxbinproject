#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'cagibi'

from selenium import webdriver

driver = webdriver.Ie()

URL = "http://www.histdata.com/download-free-forex-historical-data/?/ninjatrader/tick-bid-quotes/eurusd/2016/9/"


driver.get(URL)

toclic = driver.find_element_by_link_text("HISTDATA_COM_NT_EURUSD_T_BID_201609.zip")



import win32gui
import re

class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""
    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name = None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        '''Pass to win32gui.EnumWindows() to check all the opened windows'''
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) != None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)

#import win32com.client
#shell = win32com.client.Dispatch("WScript.Shell")

#w = WindowMgr()
#x=w.find_window_wildcard(".*Enreg*")

toclic.click()
#x.set_foreground()

#shell.SendKeys("{ENTER}")