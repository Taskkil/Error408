from screen import *
from windows import *
import threading
import random
import math
import os
import json

fps = 60
task7_fps = 20
task7_window = 8
task10_fps = 30
if os.path.exists("config.json"):
    try:
        with open("config.json", "r", encoding="utf8") as f:
            config = json.load(f)
        config = config["part1"]
        fps = config.get("fps", fps)
        task7_fps = config.get("task7_fps", task7_fps)
        task7_window = config.get("task7_window", task7_window)
        task10_fps = config.get("task10_fps", task10_fps)
    except:
        pass


class Task1(Task):
    def start(self):
        x = SCREEN.width * 0.3312
        y = SCREEN.height * 0.3763
        timer = Timer()
        t = 0
        for i in range(12):
            self.manager.create(x, y, "Windows was not install correctly. Please reinstall Windows.\nError4 (Windows Error 096)", "Microsoft Windows", 16, block=False)
            x += 20
            y += 20
            t += 0.1
            timer.wait_for(t)

class Task2(Task):
    def start(self):
        x = SCREEN.width * 0.5395
        y = SCREEN.height * 0.2210
        timer = Timer()
        t = 0
        for i in range(4):
            self.manager.create(x, y, "Windows was not install correctly. Please reinstall Windows.\nError4 (Windows Error 096)", "Microsoft Windows", 16, block=False)
            x += 20
            y += 20
            t += 0.288
            timer.wait_for(t)

string1 = "Windows has encountered 1,500,000\n" \
            "errors and counting.\n" \
            "Since Windows is a problem with a solution,\n" \
            "please tell Microsoft and shutdown your PC\n" \
            "for good.\n" \
            "-> Beat Microsoft to death"
string1_f = "Windows has encountered {}\n" \
            "errors and counting.\n" \
            "Since Windows is a problem with a solution,\n" \
            "please tell Microsoft and shutdown your PC\n" \
            "for good.\n" \
            "-> Beat Microsoft to death"

string2 = "Are you sure want to exit?" + " "*78
string3 = "Are you sure want to exit?Are you sure want to exit?"

class Task3(Task):
    @classmethod
    def counting(cls, hwnd, count):
        x = 1500000
        timer = Timer()
        t = 0
        for _ in range(count):
            update_window(hwnd, "Mircosoft Windows", string1_f.format(format(int(x) + random.randint(0,int(200000 / fps)), ',')))
            x += 200000 / fps
            t += 1 / fps
            timer.wait_for(t)
    

    def create(self, x, y, i):
        hwnd = self.manager.create(x, y, string1, "Microsoft Windows", 64, button=0)
        Task3.counting(hwnd,int(fps / 10) if i < 22 else int(fps * 5))
    def start(self):
        x = -108
        y = 30
        timer = Timer()
        t = 0
        for i in range(23):
            threading.Thread(target=self.create, args=(x, y, i)).start()
            x += 20
            y += 20
            t += 0.094
            timer.wait_for(t)

class Task4(Task):

    def create(self, x, y, i):
        hwnd = self.manager.create(x, y, string1, "Microsoft Windows", 64)
        Task3.counting(hwnd,int(fps / 10) if i < 23 else int(fps * 2))

    def start(self):
        x = SCREEN.width * 0.79
        y = SCREEN.height * 0.56
        timer = Timer()
        t = 0
        for i in range(23):
            threading.Thread(target=self.create, args=(x, y, i)).start()
            x += -20
            y += -20
            t += 0.094
            timer.wait_for(t)

class Task5(Task):
    def start(self):
        x = SCREEN.width / 2 - 150
        y = SCREEN.height / 2 - 150
        timer = Timer()
        t = 0
        strings = [
            string2 + "\n\n",
            string2 + "\n" + string2 + "\n",
            (string2 + "\n") * 2 + string2,
            (string3 + "\n") * 2 + string2 * 2,
            (string2 + "\n") * 2 + string2,
        ]
        for i in range(5):
            self.manager.create(x, y, strings[i], "Microsoft Windows", 48)
            x += 20
            y += 20
            t += 0.2
            timer.wait_for(t)
        for i in range(5):
            self.manager.destroy(i)
            t += 0.1
            timer.wait_for(t)

def close(tasks:list[Task]):
    l = []
    for t in tasks:
        l.extend(t.manager.hwnds)
    l = [h for h in l if h is not None]
    random.shuffle(l)
    timer = Timer()
    t = 0
    for h in l:
        close_window(h)
        t += 0.011
        timer.wait_for(t)

class Task6(Task):
    def start(self):
        x = SCREEN.width - 350
        y = SCREEN.height - 250
        timer = Timer()
        t = 0
        d = 0.4
        self.manager.create(x, y, "\u202derror", "\u202dMicrosoft Windows", 0)
        for i in range(4):
            self.manager.update(0, "\u202eMicrosoft Windows", "\u202eerror")
            t += d
            timer.wait_for(t)
            self.manager.update(0, "\u202dMicrosoft Windows", "\u202derror")
            t += d
            d -= 0.1
            timer.wait_for(t)
        self.manager.close()

def move(hwnd, track_x, track_y, delay=1 / fps, close=True):
    timer = Timer()
    t = 0
    for x,y in zip(track_x, track_y):
        move_window(hwnd, x, y)
        t += delay
        timer.wait_for(t)
    if close: close_window(hwnd)

class Task7(Task):
    fps = task7_fps
    window = task7_window


    def start(self):
        track_x = []
        track_y = []
        x = -300
        y = DESKTOP.height - 300
        speed_x = 400
        speed_y = 50
        g = 100
        r = 0.8
        bottom = DESKTOP.height - 200
        while x < SCREEN.width:
            x += speed_x / Task7.fps
            y += speed_y / Task7.fps
            speed_y += g / Task7.fps
            if y > bottom:
                y = bottom
                speed_y = -speed_y * r
            track_x.append(x)
            track_y.append(y)
        timer = Timer()
        t = 0
        last_hwnd = None
        for _ in range(Task7.window):
            hwnd = self.manager.create(-300, DESKTOP.height - 300, "Task failed successfully.", "Microsoft Windows", 64)
            if last_hwnd is not None:
                move_window_z_order(hwnd, last_hwnd, "bottom")
            last_hwnd = hwnd
            threading.Thread(target=move, args=(hwnd, track_x, track_y, 1/Task7.fps)).start()
            t += 1.5 / Task7.window
            timer.wait_for(t)

class Task8(Task):
    def start(self):
        timer = Timer()
        t = 0
        for i in range(16):
            self.manager.create(random.randint(0, DESKTOP.width - 300), random.randint(0, DESKTOP.height - 200), "Windows hardware update\n" \
            "Windows has detected that you have moved\n" \
            "your mouse. Please restart your computer.", "Microsoft Windows", 64)
            t += 0.1
            timer.wait_for(t)
        self.manager.close()

class Task9(Task):
    def start(self):
        def error_window(x, y, timer):
            t = 0
            hwnd = self.manager.create(x, y, "\u202derror", "\u202dMicrosoft Windows", 0)
            for i in range(8):
                update_window(hwnd, "\u202eMicrosoft Windows", "\u202eerror")
                t += 0.1
                timer.wait_for(t)
                update_window(hwnd, "\u202dMicrosoft Windows", "\u202derror")
                t += 0.1
                timer.wait_for(t)
        timer = Timer()
        t1 = threading.Thread(target=error_window, args=(30, DESKTOP.height - 430, timer))
        t2 = threading.Thread(target=error_window, args=(30, DESKTOP.height - 250, timer))
        t1.start();t2.start()
        t1.join();t2.join()
        self.manager.close()





class Task10(Task):
    fps = 10
    def fail(self, hwnd, x, y, fps):
        touched = False
        desplay_y = y
        speed_x = 0
        speed_y = 0
        g = 600
        timer = Timer()
        t = 0
        while y < SCREEN.height:
            move_window(hwnd, x, desplay_y)
            x += speed_x / fps
            y += speed_y / fps
            desplay_y = y
            speed_y += g / fps
            if y >= DESKTOP.height - 230 and not touched:
                desplay_y = DESKTOP.height - 200
                touched = True
                speed_y = -speed_y
            t += 1/fps
            timer.wait_for(t)
        close_window(hwnd)

    def start(self):
        x = SCREEN.width / 2 - 250
        y = SCREEN.height / 2
        times = [
            0.330,
            0.556,
            0.765,
            0.832,
            1.232,
            1.300,
            1.400,
            1.500,
        ]
        timer = Timer()
        for t in times:
            timer.wait_for(t)
            self.manager.create(x, y, "Windows hardware update\n" \
            "Windows has detected that you have moved\n" \
            "your mouse. Please restart your computer.", "Microsoft Windows", 64)
            x += 20
            y -= 20
        timer = Timer()
        t = 0
        for hwnd in self.manager.hwnds:
            pos = get_window_position(hwnd)
            if not pos:
                print("failed to get window position")
                close_window(hwnd)
            else:
                threading.Thread(target=self.fail, args=(hwnd, pos[0], pos[1], Task10.fps)).start()
            t += 0.4
            timer.wait_for(t)

class Task11():
    def start(self):
        timer = Timer()
        volumes = [
            60,
            55,
            45,
            70,
            45,
            20,
            60,
            45,
            30,
            60,
            45,
            30,
            70,
            45,
            75,
            55,
            20,
            60,
            45,
            90,
            10,
            40,
            60,
            80,
            45,
            60,
            80,
            95,
            70,
            90,
            100,
        ]
        times = [
            0,
            0.030,
            0.170,
            0.230,
            0.330,
            0.430,
            0.530,
            0.600,
            0.700,
            0.800,
            0.900,
            0.966,
            1.067,
            1.167,
            1.200,
            1.430,
            1.530,
            1.600,
            1.700,
            1.800,
            1.866,
            1.966,
            2.033,
            2.131,
            2.266,
            2.333,
            2.433,
            2.533,
            2.633,
            2.700,
            2.800,
        ]
        for v,t in zip(volumes, times):
            print(f"设置音量:{v}")
            timer.wait_for(t)
            set_system_volume(v)

class Task12(Task):
    string1 = "windows7.exe has stopped working\nWindows is collecting more information about this problem.\nThis might take several decades...\n{}"
    def collecting(self, hwnd, max, time=20, delay=1/fps):
        timer = Timer()
        t = 0
        i = 0
        while i < max:
            string = f"[{' '*(int(i)%20) * 5}-{' '*(19-(int(i)%20)) * 5}]"
            update_window(hwnd, new_content=Task12.string1.format(string))
            t += delay
            timer.wait_for(t)
            i += 1

    def start(self):
        x,y = SCREEN.width / 2 - 150, DESKTOP.height - 250
        r = (SCREEN.width - 300) * 0.375
        pos = []
        for i in range(46):
            pos.append((x + math.sin(math.pi * i / 45 + math.pi / 2) * r, y + math.cos(math.pi * i / 45 + math.pi / 2) * r))
        t1 = pos[:15]
        h1_l = []
        t2 = pos[15:30]
        h2_l = []
        t3 = pos[30:]
        h3_l = []
        h4_l = []
        timer = Timer()
        t = 0
        for i in t1:#arch part1
            hwnd = self.manager.create(i[0], i[1], "Something happend.", "Microsoft Windows", 32)
            h1_l.append(hwnd)
            t += 1.266 / 14
            timer.wait_for(t)
        t = 1.377
        timer.wait_for(t)
        h1 = None
        for i in t3:#arch path3
            hwnd = self.manager.create(i[0], i[1], "Something happend.", "Microsoft Windows", 32)
            h3_l.append(hwnd)
            if h1 is None:
                h1 = hwnd
            t += 1.456 / 15
            timer.wait_for(t)
        t = 3.062
        timer.wait_for(t)
        last_hwnd = None
        x = SCREEN.width / 2 - 300
        y = DESKTOP.height / 2 - 50
        h2 = None
        for i in range(8):#line
            hwnd = self.manager.create(x, y, Task12.string1.format("[-                    ]"), "Microsoft Windows", 0)
            h4_l.append(hwnd)
            if h2 is None:
                h2 = hwnd
            last_hwnd = hwnd
            if last_hwnd is not None:
                move_window_z_order(hwnd, last_hwnd, "top")
            move_window_z_order(hwnd, h1, "bottom")
            threading.Thread(target=self.collecting, args=(hwnd, 100 if i < 7 else 200, 20, 1/fps)).start()
            t += 0.3532
            x += 20
            y += 20
            timer.wait_for(t)
        last_hwnd = None
        for i in t2:#arch part3
            hwnd = self.manager.create(i[0], i[1], "Something happend.", "Microsoft Windows", 32)
            h2_l.append(hwnd)
            if last_hwnd is not None:
                move_window_z_order(hwnd, last_hwnd, "top")
            last_hwnd = hwnd
            move_window_z_order(hwnd, h2, "bottom")
            t += 1.266 / 14
            timer.wait_for(t)
        d = 0.833 / 45
        arc_hwnd = h1_l + h2_l + h3_l
        for i in range(46):#close
            
            close_window(arc_hwnd[i])
            if 8 > (i - 30) >= 0:
                close_window(h4_l[i - 30])
            t += d
            timer.wait_for(t)





def play(timer = None):
    task1 = Task1()
    task2 = Task2()
    task3 = Task3()
    task4 = Task4()
    task5 = Task5()
    task6 = Task6()
    task7 = Task7()
    task8 = Task8()
    task9 = Task9()
    task10 = Task10()
    task11 = Task11()
    task12 = Task12()
    timer = Timer() if timer is None else timer
    timer.wait_for(0.566)
    threading.Thread(target=task1.start).start()
    timer.wait_for(1.032)
    threading.Thread(target=task2.start).start()
    timer.wait_for(2)
    threading.Thread(target=task3.start).start()
    timer.wait_for(4.966)
    threading.Thread(target=task4.start).start()
    timer.wait_for(7.312)
    threading.Thread(target=close, args=([task1, task2, task3, task4],)).start()
    threading.Thread(target=task5.start).start()
    timer.wait_for(7.799)
    threading.Thread(target=task6.start).start()
    threading.Thread(target=task7.start).start()
    timer.wait_for(9.232)
    threading.Thread(target=task8.start).start()
    timer.wait_for(10.766)
    threading.Thread(target=task9.start).start()
    timer.wait_for(12)
    threading.Thread(target=task10.start).start()
    timer.wait_for(16.6)
    # threading.Thread(target=task11.start).start()
    last_task = threading.Thread(target=task12.start)
    last_task.start()
    last_task.join()









if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()], format='[%(levelname)s - %(name)s - %(asctime)s]: %(message)s')
    threading.Thread(target=wait_for_ctrl_c_keypress).start()
    timer = Timer()
    play(timer)
    time.sleep(5)
    os._exit(0)



# manager = WindowsManager()
# hwnd = manager.create(0, 0, "hello", "hello", 16)
# print(update_window(hwnd, "Hello", "Hello"))
# input()