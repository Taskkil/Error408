from windows import Timer, msgbox, resource_path, close_window
import screen
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from typing import *
import threading
import math
import time
import os

class MovableObject():
    def __init__(self, data, track:Iterable[Tuple[float, float, int]]):
        self.data = data
        self.track = track
        self.track_iterator = iter(track)
        self.x, self.y, self.r = self.track_iterator.__next__()

class StaticObject():
    def __init__(self, data, x, y, r = 0):
        self.data = data
        self.x = x
        self.y = y
        self.r = r

def track_arc(x, y, r, l, speed, length = -1):
    while length != 0:
        X = l * math.cos(math.radians(-r + 90)) + x
        Y = l * math.sin(math.radians(-r + 90)) + y
        r += speed
        length -= 1
        yield (X, Y, int(r))

def link(mainwindow, layer, x1, y1, x2, y2, r, data, step, delay = 0.):
    timer = Timer()
    t = 0
    for i in range(step):
        X = x1 * (step - i) / step + x2 * i / step
        Y = y1 * (step - i) / step + y2 * i / step
        mainwindow.add(layer, StaticObject(data, X, Y, r))
        t += delay
        timer.wait_for(t)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.layers:List[List[MovableObject | StaticObject]] = []
        self.movable = set()
        self.playing = False
        self.freezed = False
        self.bgcolor = Qt.black
        self.fps = 60
        self.ratio = 1.
        self.x_shift = 0.
        self.y_shift = 0.
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
    
    def add(self, layer, obj):
        if self.freezed: return
        layer.append(obj)
        if isinstance(obj, MovableObject):
            self.movable.add(obj)
    
    def insert(self, layer, index, obj):
        if self.freezed: return
        layer.insert(index, obj)
        if isinstance(obj, MovableObject):
            self.movable.add(obj)
    
    def remove(self, layer, obj):
        if self.freezed: return
        layer.remove(obj)
        if isinstance(obj, MovableObject):
            self.movable.remove(obj)
    
    def pop(self, layer, index):
        if self.freezed: return
        obj = layer.pop(index)
        if isinstance(obj, MovableObject):
            self.movable.remove(obj)
    
    def play(self):
        if self.playing: return
        self.playing = True
        threading.Thread(target=self._play_).start()
        threading.Thread(target=self._update_).start()
    
    def _play_(self):
        timer = Timer()
        t = 0
        while self.playing:
            self.update_pos()
            t += 1/self.fps
            timer.wait_for(t)
    
    def _update_(self):
        timer = Timer()
        t = 0
        while self.playing:
            self.update()
            t += 1/self.fps
            timer.wait_for(t)
    
    def stop(self):
        self.playing = False
    
    def freeze(self):
        self.freezed = True
        self.playing = False
    
    def update_pos(self):
        stoped = []
        for obj in self.movable:
            if isinstance(obj, MovableObject):
                try:
                    obj.x, obj.y, obj.r = obj.track_iterator.__next__()
                except StopIteration:
                    stoped.append(obj)
                    continue
            elif isinstance(obj, StaticObject):
                continue
        for st in stoped:
            self.movable.remove(st)
    

    def paintEvent(self, a0): #*deepseek
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), self.bgcolor)
        
        # 获取画布尺寸
        canvas_width = self.width()
        canvas_height = self.height()
        
        # 确定较小的轴并计算单位长度
        min_axis = min(canvas_width, canvas_height)
        unit_length = min_axis / 2  # 从中心到边缘的距离为1个单位
        
        # 计算中心点
        center_x = canvas_width / 2
        center_y = canvas_height / 2
        
        draw_methods = {
            QPixmap: painter.drawPixmap,
            QImage: painter.drawImage
        }
        
        for layer in self.layers:
            for obj in layer:
                data = obj.data
                # 获取原始图像尺寸
                orig_width = data.width()
                orig_height = data.height()
                
                # 1. 应用比例坐标 (obj.x, obj.y)
                # 2. 应用偏移 (x_shift, y_shift)
                # 3. 应用缩放 (ratio)
                scaled_x = (obj.x + self.x_shift) * self.ratio
                scaled_y = (obj.y + self.y_shift) * self.ratio
                
                # 将比例坐标转换为像素坐标，并确保为整数
                pixel_x = int(center_x + scaled_x * unit_length)
                pixel_y = int(center_y - scaled_y * unit_length)  # 注意：Qt的y轴向下，所以用减号
                
                # 应用ratio缩放图像尺寸，并确保为整数
                scaled_width = int(orig_width * self.ratio)
                scaled_height = int(orig_height * self.ratio)
                
                # 缩放图像
                scaled_data = data.scaled(scaled_width, scaled_height)
                
                # 获取旋转角度
                rotation = getattr(obj, 'r', 0)
                
                if rotation != 0:
                    painter.save()
                    
                    # 计算旋转中心（图像中心）
                    center_img_x = pixel_x
                    center_img_y = pixel_y
                    
                    # 平移到中心点，旋转，然后平移回原点
                    painter.translate(center_img_x, center_img_y)
                    painter.rotate(rotation)
                    painter.translate(-scaled_width / 2, -scaled_height / 2)
                    
                    draw_method = draw_methods.get(type(data))
                    if draw_method is not None:
                        draw_method(0, 0, scaled_data)
                    
                    painter.restore()
                else:
                    draw_method = draw_methods.get(type(data))
                    if draw_method is not None:
                        # 绘制时调整位置使图像中心位于指定坐标，并确保为整数
                        draw_x = int(pixel_x - scaled_width / 2)
                        draw_y = int(pixel_y - scaled_height / 2)
                        draw_method(draw_x, draw_y, scaled_data)



class Task1:
    def start(self, timer:Timer, mainwindow:MainWindow, layer0, layers):
        t = timer.time()
        window_X = mainwindow.width()
        window_Y = mainwindow.height()
        ratio = min(window_X, window_Y)
        image_r = 0.2
        empty_window = QPixmap(resource_path("empty_window.bmp"))
        scale_raito = ratio / 5 / empty_window.width()
        w, h = empty_window.width(), empty_window.height()
        empty_window = empty_window.scaled(int(w * scale_raito), int(h * scale_raito))

        r = 0
        for _ in range(6):
            layer0.insert(0, StaticObject(
                empty_window,
                x = 0,
                y = 0,
                r = r
            ))
            t += 0.1
            r -= 15
            timer.wait_for(t)
        t += 0.2
        timer.wait_for(t)
        x_l = [0.] * 6
        y_l = [0.] * 6
        c = 50
        for i in range(c + 6):
            for idx, layer in enumerate(layers):
                if i >= idx and i - idx < c - 6:
                    layer.insert(0, StaticObject(
                        empty_window,
                        x = x_l[idx],
                        y = y_l[idx],
                        r = 60 * idx
                    ))
                    x_l[idx] += math.sin(idx / 3 * math.pi) * image_r / 1.5
                    y_l[idx] += math.cos(idx / 3 * math.pi) * image_r / 1.5
            t += 0.1
            timer.wait_for(t)
    
class Task2:
    def start(self, timer:Timer, mainwindow:MainWindow):
        t = timer.time()
        while mainwindow.playing:
            mainwindow.ratio *= 0.992
            t += 0.05
            timer.wait_for(t)



class Task3:
    def start(self, timer:Timer, mainwindow:MainWindow, layer):
        window_X = mainwindow.width()
        window_Y = mainwindow.height()
        ratio = min(window_X, window_Y)
        empty_window = QPixmap(resource_path("empty_window.bmp"))
        scale_raito = ratio / 5 / empty_window.width()
        w, h = empty_window.width(), empty_window.height()
        empty_window = empty_window.scaled(int(w * scale_raito), int(h * scale_raito))
        t = timer.time()
        for r in range(32):
            mainwindow.add(layer,
                MovableObject(
                    data = empty_window,
                    track = track_arc(0, 0, r * 16 + 60, 1, 0.8),
                )
            )
            t += 0.1
            timer.wait_for(t)
        empty_window1 = empty_window.scaled(int(empty_window.width() * 1.3), int(empty_window.height() * 1.3))
        for r in range(32):
            mainwindow.add(layer,
                MovableObject(
                    data = empty_window1,
                    track = track_arc(0, 0, r * 16 + 90, 1.8, 0.8),
                )
            )
            t += 0.1
            timer.wait_for(t)


class Task4:
    def link(self, mainwindow, layer, data):
        pos = [(math.sin((i + 0.5) * math.pi / 3 * 2) * 5.8, math.cos((i + 0.5) * math.pi / 3 * 2) * 5.8) for i in range(3)]
        link(mainwindow, layer, *pos[0], *pos[1], 120, data, 40, 0.1)
        link(mainwindow, layer, *pos[1], *pos[2], 240, data, 40, 0.1)
        link(mainwindow, layer, *pos[2], *pos[0], 0, data, 40, 0.1)
    
    def circle(self, mainwindow, layer, x, y, r, r0, l, r1, delay, data):
        timer = Timer()
        t = 0
        for i in range(math.ceil(360 // r0)):
            mainwindow.add(layer,
                StaticObject(
                    data = data,
                    x = x + math.sin(math.radians(i * r0 + r - 90) * l),
                    y = y + math.cos(math.radians(i * r0 + r - 90) * l),
                    r = r1
                )
            )
            t += delay
            timer.wait_for(t)

    def start(self, timer:Timer, mainwindow:MainWindow, layer0, layer1):
        window_X = mainwindow.width()
        window_Y = mainwindow.height()
        ratio = min(window_X, window_Y)
        empty_window = QPixmap(resource_path("empty_window.bmp"))
        scale_raito = ratio / 5 / empty_window.width()
        w, h = empty_window.width(), empty_window.height()
        empty_window = empty_window.scaled(int(w * scale_raito), int(h * scale_raito))
        empty_window1 = empty_window.scaled(int(empty_window.width() * 1.3), int(empty_window.height() * 1.3))
        threading.Thread(target=self.circle, args=(mainwindow, layer1, 0, 3.2, 0, 11.25, 1, 0, 0.1, empty_window1)).start()
        threading.Thread(target=self.circle, args=(mainwindow, layer1, math.sin(math.pi / 3 * 2) * 3.2, math.cos(math.pi / 3 * 2) * 3.2, 0, 11.25, 1, 0, 0.1, empty_window1)).start()
        threading.Thread(target=self.circle, args=(mainwindow, layer1, math.sin(-math.pi / 3 * 2) * 3.2, math.cos(-math.pi / 3 * 2) * 3.2, 0, 11.25, 1, 0, 0.1, empty_window1)).start()
        self.link(mainwindow, layer0, empty_window)

class Task5:
    def start(self, timer:Timer, mainwindow:MainWindow, layer):
        window_X = mainwindow.width()
        window_Y = mainwindow.height()
        ratio = min(window_X, window_Y)
        empty_window = QPixmap(resource_path("empty_window.bmp"))
        scale_raito = ratio / 5 / empty_window.width()
        w, h = empty_window.width(), empty_window.height()
        empty_window = empty_window.scaled(int(w * scale_raito), int(h * scale_raito))
        t = timer.time()
        count = 160
        for i in range(count):
            mainwindow.add(layer,
                StaticObject(
                    data = empty_window,
                    x = math.sin(math.radians(i * 360 / count)) * 5.8,
                    y = math.cos(math.radians(i * 360 / count)) * 5.8,
                    r = int(i * 360 / count)
                )
            )
            t += 0.1
            timer.wait_for(t)


class Task6:
    def start(self, timer:Timer, mainwindow:MainWindow, layer):
        window_X = mainwindow.width()
        window_Y = mainwindow.height()
        ratio = min(window_X, window_Y)
        empty_window = QPixmap(resource_path("empty_window.bmp"))
        scale_raito = ratio / 5 / empty_window.width()
        w, h = empty_window.width(), empty_window.height()
        empty_window = empty_window.scaled(int(w * scale_raito), int(h * scale_raito))
        t = timer.time()
        count = 96
        for i in range(count):
            mainwindow.add(layer,
                StaticObject(
                    data = empty_window,
                    x = math.sin(math.radians(i * 360 / count)) * 5,
                    y = math.cos(math.radians(i * 360 / count)) * 5,
                    r = int(i * 360 / count)
                )
            )
            t += 0.1
            timer.wait_for(t)

class Task7:
    def start(self, timer:Timer, mainwindow:MainWindow, layer):
        window_X = mainwindow.width()
        window_Y = mainwindow.height()
        ratio = min(window_X, window_Y)
        empty_window = QPixmap(resource_path("empty_window.bmp"))
        scale_raito = ratio / 5 / empty_window.width()
        w, h = empty_window.width(), empty_window.height()
        empty_window = empty_window.scaled(int(w * scale_raito), int(h * scale_raito))
        t = timer.time()
        count = 12
        r = 120
        l = 5.5
        for i in range(3):
            o_x = math.sin(math.radians(60 - i * 120)) * l
            o_y = math.cos(math.radians(60 - i * 120)) * l
            for j in range(count):
                mainwindow.add(layer,
                    StaticObject(
                        data = empty_window,
                        x = o_x - math.sin(math.radians(j * r / count + r / count / 2 - i * 120)) * 2,
                        y = o_y - math.cos(math.radians(j * r / count + r / count / 2 - i * 120)) * 2,
                        r = int(j * r / count + r / count / 2 - i * 120)
                    )
                )
                t += 0.1
                timer.wait_for(t)


class Task8:
    def start(self, timer:Timer, mainwindow:MainWindow, layer):
        window_X = mainwindow.width()
        window_Y = mainwindow.height()
        ratio = min(window_X, window_Y)
        empty_window = QPixmap(resource_path("empty_window.bmp"))
        scale_raito = ratio / 5 / empty_window.width()
        w, h = empty_window.width(), empty_window.height()
        empty_window = empty_window.scaled(int(w * scale_raito), int(h * scale_raito))
        t = timer.time()
        for r in range(140):
            mainwindow.add(layer,
                MovableObject(
                    data = empty_window,
                    track = track_arc(0, 0, r * 15 + 60, 8, 2),
                )
            )
            t += 0.1
            timer.wait_for(t)


def process_pixmap(pixmap, color=Qt.red):
    """
    处理QPixmap的函数，根据mod值应用不同的效果
    
    参数:
    pixmap: 要处理的QPixmap对象
    mod: 处理模式 (0: 正常, 1: 纯黑, 2: 纯白, 3: 中间白四周渐变)
    d: 渐变距离（像素），从边缘向内d个像素是渐变区域
    color: 渐变颜色，默认为红色
    """
    
    # 创建与原图相同大小的临时图像
    result = QPixmap(pixmap.size())
    result.fill(Qt.transparent)  # 透明背景
    
    painter = QPainter(result)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.fillRect(0, 0, pixmap.width(), pixmap.height(), color)
    
    painter.end()
    return result





class Task9:
    def start(self, timer:Timer, mainwindow:MainWindow):
        qpixmaps:Set[QPixmap] = set()
        timer.wait_for(99.9)
        for layer in mainwindow.layers:
            for obj in layer:
                qpixmaps.add(obj.data)
        changed = {id(p):process_pixmap(p, Qt.black) for p in qpixmaps}
        timer.wait_for(100.099)
        mainwindow.freezed = True
        for layer in mainwindow.layers:
            for obj in layer:
                obj.data = changed[id(obj.data)]
        mainwindow.bgcolor = Qt.white
        for layer in mainwindow.layers:
            for obj in layer:
                qpixmaps.add(obj.data)
        changed = {id(p):process_pixmap(p, Qt.white) for p in qpixmaps}
        timer.wait_for(100.399)
        for layer in mainwindow.layers:
            for obj in layer:
                obj.data = changed[id(obj.data)]
        mainwindow.bgcolor = Qt.black
        for layer in mainwindow.layers:
            for obj in layer:
                qpixmaps.add(obj.data)
        changed = {id(p):process_pixmap(p, Qt.black) for p in qpixmaps}
        timer.wait_for(100.666)
        for layer in mainwindow.layers:
            for obj in layer:
                obj.data = changed[id(obj.data)]
        mainwindow.bgcolor = Qt.white
        for layer in mainwindow.layers:
            for obj in layer:
                qpixmaps.add(obj.data)
        changed = {id(p):process_pixmap(p, Qt.white) for p in qpixmaps}
        timer.wait_for(101.033)
        for layer in mainwindow.layers:
            for obj in layer:
                obj.data = changed[id(obj.data)]
        mainwindow.bgcolor = Qt.black
        mainwindow.freeze()
        mainwindow.update()

class Task10:
    def start(self, timer:Timer, mainwindow:MainWindow):
        x = screen.SCREEN.width / 2
        y = screen.SCREEN.height / 2
        timer.wait_for(101.266)
        hwnds = []
        hwnds.append(msgbox(x, y, "bilibili.exe has stopped working\nWindows is collecting more information about the problem.", "Microsoft Windows", icon=0))
        time.sleep(0.2)
        x +=20
        y += 20
        hwnds.append(msgbox(x, y, "ttank.exe has stopped working\nWindows is collecting more information about the problem.", "Microsoft Windows", icon=0))
        time.sleep(0.2)
        x +=20
        y += 20
        hwnds.append(msgbox(x, y, "you.exe has stopped working\nWindows is collecting more information about the problem.", "Microsoft Windows", icon=0))
        time.sleep(0.2)
        x +=20
        y += 20
        hwnds.append(msgbox(x, y, "for.exe has stopped working\nWindows is collecting more information about the problem.", "Microsoft Windows", icon=0))
        time.sleep(0.2)
        x +=20
        y += 20
        hwnds.append(msgbox(x, y, "watching.exe has stopped working\nWindows is collecting more information about the problem.", "Microsoft Windows", icon=0))
        os.system("taskmgr")
        time.sleep(1)
        mainwindow.close()
        for hwnd in hwnds:
            close_window(hwnd)
        time.sleep(3)
        os._exit(0)



def play(mainwindow:MainWindow, timer = None):
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
    timer = Timer() if timer is None else timer
    mainwindow.play()
    mainwindow.layers = [[] for _ in range(12)]
    timer.wait_for(88.622)
    threading.Thread(target=task1.start, args=(timer, mainwindow, mainwindow.layers[7], mainwindow.layers[1:7])).start()
    threading.Thread(target=task2.start, args=(timer, mainwindow)).start()
    threading.Thread(target=task3.start, args=(timer, mainwindow, mainwindow.layers[8])).start()
    threading.Thread(target=task4.start, args=(timer, mainwindow, mainwindow.layers[0], mainwindow.layers[9])).start()
    threading.Thread(target=task5.start, args=(timer, mainwindow, mainwindow.layers[9])).start()
    threading.Thread(target=task6.start, args=(timer, mainwindow, mainwindow.layers[11])).start()
    threading.Thread(target=task8.start, args=(timer, mainwindow, mainwindow.layers[10])).start()
    threading.Thread(target=task9.start, args=(timer, mainwindow)).start()
    time.sleep(3)
    threading.Thread(target=task7.start, args=(timer, mainwindow, mainwindow.layers[10])).start()
    threading.Thread(target=task10.start, args=(timer, mainwindow)).start()


if __name__ == "__main__":
    app = QApplication([])
    mainwindow = MainWindow()
    mainwindow.showFullScreen()
    mainwindow.play()
    timer = Timer()
    timer.start_time -= 88.622
    threading.Thread(target=play, args=(mainwindow,timer)).start()
    app.exec_()