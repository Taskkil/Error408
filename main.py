import part1
import part2
import part3
import part4
import part6
from windows import Timer, wait_for_ctrl_c_keypress, msgbox, close_window, MB_YESNO, MB_ICONQUESTION, IDYES, IDNO, resource_path
from screen import SCREEN
import threading
import os
import time
import ctypes
from PyQt5.QtWidgets import QApplication
import simpleaudio as sa

def play2(timer):
    timer.wait_for(25.17)
    part2.play_video(resource_path("resource1.mp4"), 21)

def play5(timer):
    timer.wait_for(81.566)
    part2.play_video(resource_path("resource2.mp4"), 7)


if __name__ == '__main__':
    threading.Thread(target=wait_for_ctrl_c_keypress).start()
    result = ctypes.windll.user32.MessageBoxW(
    0,
    "这是一个演示程序，不是真正的病毒\n但是可能造成电脑卡顿\n是否运行？\n运行中可以按Ctrl+C退出",
    "by Bilibili taskkill-结束进程",
    MB_YESNO | MB_ICONQUESTION
)
    if result != IDYES:
        os._exit(0)


    timer = Timer()
    timer.start_time += 6.5
    audio = sa.WaveObject.from_wave_file(resource_path("audio1.wav"))
    audio.play()
    threading.Thread(target=part1.play, args=(timer,)).start()
    threading.Thread(target=play2, args=(timer,)).start()
    threading.Thread(target=part3.play, args=(timer,)).start()
    threading.Thread(target=part4.play, args=(timer,)).start()
    threading.Thread(target=play5, args=(timer,)).start()
    timer.wait_for(88.622)
    app = QApplication([])
    mainwindow = part6.MainWindow()
    mainwindow.showFullScreen()
    mainwindow.play()
    threading.Thread(target=part6.play, args=(mainwindow,timer)).start()
    app.exec_()