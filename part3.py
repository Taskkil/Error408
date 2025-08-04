import os
import time
from windows import *
from screen import *
import win32gui
import win32process
import subprocess
import threading

fps = 60
exe_delay = 0

def _start_():
    time.sleep(exe_delay)
    process = subprocess.Popen("part3.exe", creationflags=subprocess.CREATE_NEW_CONSOLE)
    pid = process.pid
    time.sleep(5.5 - exe_delay)
    subprocess.run("taskkill /f /t /pid %d"%pid, capture_output=True, shell=True)

class Task1(Task):
    def start(self):
        threading.Thread(target=_start_).start()
        timer = Timer()
        self.sync_move(speed_x=-1500, fps=fps)
        t = 0
        x = SCREEN.width
        y = SCREEN.height * 0.75
        for _ in range(6):
            hwnd = self.manager.create(x, y, "*看不清看不清看不清看不清", "Macrohard Windows", 16)
            set_window_z_order(hwnd, "topmost")
            x += 150
            y -= 50
            t += 0.1
            timer.wait_for(t)
        y = SCREEN.height * 0.25
        for _ in range(7):
            hwnd = self.manager.create(x, y, "*看不清看不清看不清看不清", "Macrohard Windows", 32)
            set_window_z_order(hwnd, "topmost")
            x += 150
            t += 0.1
            timer.wait_for(t)
        y = SCREEN.height * 0.75
        for _ in range(11):
            hwnd = self.manager.create(x, y, "*看不清看不清看不清看不清", "Macrohard Windows", 32)
            set_window_z_order(hwnd, "topmost")
            x += 150
            y -= 40
            t += 0.1
            timer.wait_for(t)
        t += 3
        timer.wait_for(t)
        self.manager.close()

class Task2(Task):
    def start(self, timer):
        self.sync_move(speed_x = -200)
        if not isinstance(self.manager, SyncMover):raise#傻逼pylance
        hwnd = self.manager.create(SCREEN.width * 0.5 - 150, SCREEN.height * 0.5 - 100, "*看不懂日语                                         ", "Microsoft Windows", 16)
        set_window_z_order(hwnd, "topmost")
        timer.wait_for(53.136)
        hwnd = self.manager.create(SCREEN.width * 0.5 + 50, SCREEN.height * 0.5 - 25, "", "", 0)#空
        set_window_z_order(hwnd, "topmost")
        timer.wait_for(53.499)
        hwnd = self.manager.create(SCREEN.width * 0.5, SCREEN.height * 0.5, "Windows Firewall can't change some of your settings.\nError code 0x80070424", "Windows Firewall", 16)
        set_window_z_order(hwnd, "topmost")
        timer.wait_for(54.298)
        subprocess.Popen("control")
        timer.wait_for(54.898)
        subprocess.Popen("cleanmgr")
        timer.wait_for(55.599)
        subprocess.Popen("calc")
        timer.wait_for(56.531)
        # subprocess.Popen("msconfig")
        timer.wait_for(56.832)
        subprocess.Popen("explorer")
        timer.wait_for(58.300)
        x,y = -self.manager.x, -self.manager.y
        hwnd = self.manager.create(SCREEN.width * 0.5 + x, SCREEN.height * 0.5 + y + 50, "你的USB出了点问题,我也不知道是什么\n原视频写的是日语我看不懂", "看不懂", 16)
        set_window_z_order(hwnd, "topmost")
        timer.wait_for(59.8)
        x,y = -self.manager.x, -self.manager.y
        t = 59.8
        for _ in range(3):
            hwnd = self.manager.create(SCREEN.width * 0.5 + x, SCREEN.height * 0.5 + y, "Device driver software was not installed", "Microsoft Windows", 16)
            set_window_z_order(hwnd, "topmost")
            t += 0.1
            x += 20
            y += 20
            timer.wait_for(t)
        timer.wait_for(62.331)
        os.system("shutdown /s /t 99999")
        hwnd = msgbox(SCREEN.width * 0.5 - 100, SCREEN.height * 0.5 - 50, "Start By\tTurn Off\tRestart", "Turn off computer", 0)
        set_window_z_order(hwnd, "topmost")
        timer.wait_for(62.431)
        hwnd = msgbox(SCREEN.width * 0.5 - 50, SCREEN.height * 0.5, "Start By\tTurn Off\tRestart", "Turn off computer", 0)
        set_window_z_order(hwnd, "topmost")
        timer.wait_for(63)
        os.system("shutdown /a")







def play(timer = None):
    task1 = Task1()
    task2 = Task2()
    timer = Timer() if timer is None else timer
    timer.wait_for(46.331)
    task1.start()
    timer.wait_for(52.800)
    task2.start(timer)



if __name__ == "__main__":
    timer = Timer()
    timer.start_time -= 46.331
    play(timer)
