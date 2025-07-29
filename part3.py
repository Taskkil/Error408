import os
import time
from windows import *
import win32gui
import subprocess

os.system("start part3.exe")
c = 0
while c < 30:
    hwnd = win32gui.FindWindow(None, "part3.exe")
    if hwnd:
        print(2)
        break
    else:
        time.sleep(0.1)
        print(1)
        c += 1
move_window(hwnd, 0, 0)