import part1
from windows import Timer, wait_for_ctrl_c_keypress, msgbox, close_window, MB_YESNO, MB_ICONQUESTION, IDYES, IDNO
from screen import SCREEN
import threading
import os
import time
import ctypes



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
    last_task = threading.Thread(target=part1.play, args=(timer,))
    last_task.start()
    last_task.join()
    time.sleep(5)
    os._exit(0)