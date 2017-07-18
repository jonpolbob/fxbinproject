import msvcrt
import os

from ctypes import *

class COORD(Structure):
    pass

COORD._fields_ = [("X", c_short), ("Y", c_short)]

STD_OUTPUT_HANDLE = -11
h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


def Xprint(*toprint):
    for a in toprint :
        print(a , end='')  #pas de cr lf
    print("")

def setxy(x,y):
    windll.kernel32.SetConsoleCursorPosition(h, COORD(x, y))

def Xkbhit():
    return msvcrt.kbhit()

def Xinput(question):
    return input(question)

def cls():
    os.system('cls')
