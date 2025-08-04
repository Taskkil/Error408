import ctypes
import win32gui
import win32con
import threading
import uuid
import time
import keyboard
import os
import win32api
import win32process
from ctypes import wintypes
import comtypes
import logging
from typing import Union
#有一些(大部分)是AI写的,我会标注

logger = logging.getLogger(__name__)

class Task:
    def __init__(self):
        self.manager:Union[WindowsManager, SyncMover] = WindowsManager()
        # self.manager.create_parant_window()
        # set_window_z_order(self.manager.parant_hwnd, "topmost")
    
    def sync_move(self, x = 0, y = 0, speed_x = 0, speed_y = 0, acceleration_x = 0, acceleration_y = 0, fps = 60, tick=0.01):
        if not isinstance(self.manager, WindowsManager):
            raise Exception("manager is not WindowsManager")
        if not isinstance(self.manager, SyncMover):
            self.manager = SyncMover(self.manager)
            self.manager.x = x
            self.manager.y = y
            self.manager.speed_x = speed_x
            self.manager.speed_y = speed_y
            self.manager.acceleration_x = acceleration_x
            self.manager.acceleration_y = acceleration_y
            self.manager.fps = fps
            self.manager.tick = tick
        self.manager.start_move()


class Timer:
    def __init__(self):
        self.start_time = time.perf_counter()
    
    def wait_for(self, t):
        delay = t - (time.perf_counter() - self.start_time)
        if delay > 0:
            time.sleep(delay)
        else:
            logger.debug("超时")

def wait_for_ctrl_c_keypress():#qwen
    """
    持续监听键盘，当检测到按下 Ctrl+C 组合键时退出程序。
    """

    def on_key_event(e):
        if e.event_type == keyboard.KEY_DOWN:
            if keyboard.is_pressed('ctrl') and keyboard.is_pressed('c'):
                os._exit(0)

    # 监听所有按键事件
    keyboard.hook(on_key_event)

    try:
        while True:
            time.sleep(0.1)  # 防止占用过多CPU
    except KeyboardInterrupt:
        exit(0)

def wait_for_win_d_keypress():
    def on_key_event(e):
        if e.event_type == keyboard.KEY_DOWN:
            if keyboard.is_pressed('ctrl') and keyboard.is_pressed('windows'):
                return

    # 监听所有按键事件
    keyboard.hook(on_key_event)

    try:
        while True:
            time.sleep(0.1)  # 防止占用过多CPU
    except KeyboardInterrupt:
        return

def msgbox(x, y, message, title, icon=None, button=win32con.MB_OK, timeout=3, wait_close = False):#deepseek
    """
    创建自定义消息框并返回其句柄
    
    参数:
        x, y: 窗口位置坐标
        message: 消息内容
        title: 窗口标题
        icon: 图标类型 (可选: win32con.MB_ICONWARNING等)
        timeout: 等待窗口出现的超时时间(秒)
    
    返回:
        成功: 消息框窗口句柄
        失败: None
    """
    # 生成唯一ID作为初始窗口标题
    x = int(x)
    y = int(y)
    flags = button
    if icon:
        flags |= icon

    if wait_close:
        return ctypes.windll.user32.MessageBoxW(0, message, title, flags)

    unique_id = str(uuid.uuid4())
    
    # 在后台线程中创建消息框
    def create_msgbox():
            
        # 使用win32api创建消息框
        ctypes.windll.user32.MessageBoxW(0, message, unique_id, flags)
    
    thread = threading.Thread(target=create_msgbox)
    thread.daemon = True
    thread.start()
    
    # 等待窗口出现
    hwnd = None
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        # 尝试通过唯一ID查找窗口
        hwnd = win32gui.FindWindow(None, unique_id)
        if hwnd:
            # 设置实际标题
            win32gui.SetWindowText(hwnd, title)
            
            # 获取窗口尺寸
            rect = win32gui.GetWindowRect(hwnd)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]
            
            # 移动窗口到指定位置
            win32gui.MoveWindow(hwnd, x, y, width, height, True)
            return hwnd
        
        time.sleep(0.01)
    
    return None

def move_window(hwnd, x=None, y=None, width=None, height=None, repaint=True):#deepseek
    """
    移动窗口到指定位置并调整大小
    
    参数:
        hwnd: 窗口句柄
        x, y: 窗口左上角新坐标（屏幕坐标系）
        width, height: 窗口新尺寸（宽度和高度）
        repaint: 是否立即重绘窗口（默认为True）
    
    返回:
        bool: 操作是否成功
        
    注意:
        1. 如果只提供位置参数，保持原大小
        2. 如果只提供尺寸参数，保持原位置
        3. 如果都不提供，返回False
    """
    x = int(x)
    y = int(y)
    if x is None and y is None and width is None and height is None:
        return False
    
    # 获取当前窗口位置和尺寸
    try:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        current_width = right - left
        current_height = bottom - top
    except:
        # 无效句柄或其他错误
        return False
    
    # 确定新位置参数（未提供则使用当前位置）
    new_x = left if x is None else x
    new_y = top if y is None else y
    new_width = current_width if width is None else width
    new_height = current_height if height is None else height
    
    # 执行窗口移动/调整大小
    try:
        # 使用MoveWindow函数
        win32gui.MoveWindow(
            hwnd, 
            new_x, 
            new_y, 
            new_width, 
            new_height, 
            repaint
        )
        return True
    except:
        return False
    

def close_window(hwnd):#deepseek
    """
    通过发送 WM_CLOSE 消息优雅关闭窗口
    (类似于点击窗口的关闭按钮)
    """
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

def move_window_z_order(hwnd, target_hwnd, position):#deepseek
    """
    将指定窗口移动到目标窗口的上方或下方
    
    参数:
        hwnd: 要移动的窗口句柄
        target_hwnd: 目标窗口句柄
        position: "top" 表示移到目标窗口之上，"bottom" 表示之下
    
    返回:
        bool: 操作是否成功
    """
    if not win32gui.IsWindow(hwnd) or not win32gui.IsWindow(target_hwnd):
        logger.error("无效的窗口句柄")
        return False

    try:
        if position == "top":
            # 移动到目标窗口之上
            win32gui.SetWindowPos(
                hwnd,
                target_hwnd,
                0, 0, 0, 0,
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE
            )
        elif position == "bottom":
            # 获取目标窗口的下一个兄弟窗口
            next_hwnd = win32gui.GetWindow(target_hwnd, win32con.GW_HWNDNEXT)
            if next_hwnd:
                # 插入到目标窗口的下一个兄弟窗口之前（即目标窗口之下）
                win32gui.SetWindowPos(
                    hwnd,
                    next_hwnd,
                    0, 0, 0, 0,
                    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE
                )
            else:
                # 没有兄弟窗口，就放到最底部
                win32gui.SetWindowPos(
                    hwnd,
                    win32con.HWND_BOTTOM,
                    0, 0, 0, 0,
                    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE
                )
        else:
            logger.error("position 参数必须是 'top' 或 'bottom'")
            return False

        return True

    except Exception as e:
        logger.error(f"设置窗口层级失败: {e}")
        return False

def set_window_z_order(hwnd, position):#deepseek
    """
    设置窗口的 Z 序位置（置顶或置底）
    
    参数:
        hwnd: 窗口句柄 (int)
        position: 位置设置，可选值:
            'top' - 置顶（最顶层）
            'bottom' - 置底（最底层）
            'topmost' - 永久置顶（即使窗口非活动状态）
            'notopmost' - 取消永久置顶
    """
    # 验证输入参数
    if position not in ['top', 'bottom', 'topmost', 'notopmost']:
        raise ValueError("无效的位置参数。请使用 'top', 'bottom', 'topmost' 或 'notopmost'")
    
    # 设置窗口位置标志
    flags = win32con.SWP_NOSIZE | win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE
    
    if position == 'top':
        # 将窗口置于 Z 序顶部（当前活动窗口栈的顶部）
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, 0, 0, flags)
    
    elif position == 'bottom':
        # 将窗口置于 Z 序底部（桌面之上）
        win32gui.SetWindowPos(hwnd, win32con.HWND_BOTTOM, 0, 0, 0, 0, flags)
    
    elif position == 'topmost':
        # 设置窗口为永久置顶（在所有窗口之上）
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, flags)
    
    elif position == 'notopmost':
        # 取消窗口的永久置顶状态
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, flags)
    
    # 强制刷新窗口
    win32gui.UpdateWindow(hwnd)

def update_window(hwnd, new_title=None, new_content=None):#deepseek
    """
    更改窗口标题和/或内容
    
    参数:
        hwnd: 窗口句柄
        new_title: 新标题文本 (可选)
        new_content: 新内容文本 (可选)
    
    返回:
        bool: 操作是否成功
        
    功能:
        1. 修改窗口标题
        2. 查找内容区域控件并更新文本
    """
    try:
        # 更新标题
        if new_title is not None:
            win32gui.SetWindowText(hwnd, new_title)
        
        # 更新内容
        if new_content is not None:
            # 更可靠地查找内容控件
            # 方法1：尝试查找包含消息文本的控件
            content_hwnd = None
            def find_text_control(hwnd_child, _):
                nonlocal content_hwnd
                class_name = win32gui.GetClassName(hwnd_child)
                if class_name == "Static":
                    # 检查文本长度是否匹配消息内容
                    text = win32gui.GetWindowText(hwnd_child)
                    if len(text) > 10:  # 假设消息文本通常较长
                        content_hwnd = hwnd_child
                return True
            
            # 枚举所有子窗口
            win32gui.EnumChildWindows(hwnd, find_text_control, None)
            
            # 方法2：如果方法1失败，尝试通过控件ID查找
            if not content_hwnd:
                try:
                    # 消息文本的控件ID通常是65535
                    content_hwnd = win32gui.GetDlgItem(hwnd, 65535)
                except:
                    pass
            
            # 方法3：作为最后手段，尝试第一个Static控件
            if not content_hwnd:
                content_hwnd = win32gui.FindWindowEx(hwnd, 0, "Static", None)
            
            if content_hwnd:
                # 设置新文本
                win32gui.SetWindowText(content_hwnd, new_content)
                return True
            return False
        return True
    except:
        return False

def get_window_position(hwnd):#deepseek
    """
    获取指定窗口的屏幕坐标 (x, y)
    
    参数:
        hwnd: 窗口句柄
        
    返回:
        (x, y) 窗口左上角坐标，失败返回 None
    """
    if not win32gui.IsWindow(hwnd):
        logger.error("无效的窗口句柄")
        return None

    try:
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]  # 左边 X 坐标
        y = rect[1]  # 上边 Y 坐标
        return (x, y)
    except Exception as e:
        logger.error(f"获取窗口位置失败: {e}")
        return None

def set_window_alpha(hwnd, alpha):
    """设置窗口整体透明度 (0-255)"""
    # 设置分层样式
    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, 
                          ex_style | win32con.WS_EX_LAYERED)
    
    # 设置透明度
    win32gui.SetLayeredWindowAttributes(hwnd, 0, alpha, win32con.LWA_ALPHA)



# 定义必要的GUID和接口
class IMMDeviceEnumerator(comtypes.IUnknown):
    _iid_ = comtypes.GUID('{A95664D2-9614-4F35-A746-DE8DB63617E6}')
    
class IAudioEndpointVolume(comtypes.IUnknown):
    _iid_ = comtypes.GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')

# 初始化COM
comtypes.CoInitialize()

def set_system_volume(volume: int):#deepseek
    #用不了
    """
    设置Windows系统主音量（全局音量）
    
    参数:
        volume_level: 音量级别，范围0.0~1.0（0=静音，1=最大音量）
        
    异常:
        OSError: 如果API调用失败
        ValueError: 如果音量超出范围
    """
    volume_level = volume / 100
    if not 0.0 <= volume_level <= 1.0:
        raise ValueError("音量必须在0.0到1.0之间")
    
    # 定义必要的CLSID和IID
    CLSID_MMDeviceEnumerator = comtypes.GUID('{BCDE0395-E52F-467C-8E3D-C4579291692E}')
    IID_IMMDeviceEnumerator = comtypes.GUID('{A95664D2-9614-4F35-A746-DE8DB63617E6}')
    
    try:
        # 创建设备枚举器
        device_enumerator = comtypes.CoCreateInstance(
            CLSID_MMDeviceEnumerator,
            IMMDeviceEnumerator,
            comtypes.CLSCTX_INPROC_SERVER
        )
        
        # 获取默认音频端点
        endpoint = ctypes.POINTER(comtypes.IUnknown)()
        device_enumerator.GetDefaultAudioEndpoint(0, 1, ctypes.byref(endpoint))  # 0=渲染设备, 1=控制台
        
        # 获取音频端点音量接口
        audio_endpoint = endpoint.QueryInterface(IAudioEndpointVolume)
        
        # 设置音量
        hr = audio_endpoint.SetMasterVolumeLevelScalar(volume_level, None)
        if hr != 0:
            raise OSError(f"设置音量失败 (HRESULT: {hr:#x})")
            
    except comtypes.COMError as e:
        raise OSError(f"COM错误: {e}") from e
    finally:
        # 释放COM对象
        if 'audio_endpoint' in locals():
            audio_endpoint.Release()
        if 'endpoint' in locals():
            endpoint.Release()
        if 'device_enumerator' in locals():
            device_enumerator.Release()

def find_hwnds_by_pid(pid):#qwen
    def callback(hwnd, hwnds):
        # 获取窗口的线程和进程 ID
        _, process_id = win32process.GetWindowThreadProcessId(hwnd)
        if process_id == pid:
            # 获取窗口标题（可选）
            if win32gui.IsWindowVisible(hwnd):  # 可以加上可见性判断
                try:
                    title = win32gui.GetWindowText(hwnd)
                    print(f"Found HWND: {hwnd}, Title: {title}")
                except:
                    pass
            hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds


class WindowsManager:
    #使用这个类时关闭窗口后不应再次访问，不在内部做判断
    def __init__(self, original = None):
        if original and isinstance(original, WindowsManager):
            self.hwnds = original.hwnds.copy()
            self.parant_hwnd = original.parant_hwnd
            self.names = original.names.copy()
            self.vaild_hwnd = original.vaild_hwnd.copy()
        else:
            self.hwnds = []
            self.parant_hwnd = None
            #hwnds中hwnd的索引不能改变
            self.names = {}
            self.vaild_hwnd = set()
    
    def create_parant_window(self):
        #用不了
        return
        self.parant_hwnd = msgbox(0, 0,"","")
    
    def create(self, x, y, message, title, icon, button=win32con.MB_OK, name=None, block=True):
        if not block:
            threading.Thread(target=self.create, args=(x, y, message, title, icon, button, name, True)).start()
            return
        hwnd = msgbox(x, y, message, title, icon)
        if hwnd is None:
            raise Exception("Error: Failed to create window")
        self.hwnds.append(hwnd)
        self.vaild_hwnd.add(hwnd)
        if name is not None:
            self.names[name] = hwnd
        if self.parant_hwnd is not None:
            win32gui.SetParent(hwnd, self.parant_hwnd)
        return hwnd
    
    def auto_hwnd(self, window):
        if isinstance(window, str):
            return self.names[window]
        elif isinstance(window, int):
            return self.hwnds[window]
        else:
            raise TypeError("window must be a string or an integer")
    
    def move(self, x, y, window = None):
        move_window(x, y, self.auto_hwnd(window))
    
    def update(self, window = None, title = None, content = None):
        update_window(self.auto_hwnd(window), title, content)
        
    def destroy(self, window = None):
        "destroy a window"
        hwnd = self.auto_hwnd(window)
        close_window(hwnd)
        self.hwnds[self.hwnds.index(hwnd)] = None
        if hwnd in self.vaild_hwnd: self.vaild_hwnd.remove(hwnd)

    def close(self):
        "close all windows"
        if self.parant_hwnd is not None:
            close_window(self.parant_hwnd)
            self.parant_hwnd = None
        for i in range(len(self.hwnds)):
            if self.hwnds[i] is not None:
                close_window(self.hwnds[i])
                if self.hwnds[i] in self.vaild_hwnd: self.vaild_hwnd.remove(self.hwnds[i])
                self.hwnds[i] = None
    
    def __del__(self):
        try:
            self.close()
        except: pass

class SyncMover(WindowsManager):
    def __init__(self, original = None):
        super().__init__(original)
        if isinstance(original, SyncMover):
            self.windows_coordinates = original.windows_coordinates.copy()
            self.x = original.x
            self.y = original.y
            self.speed_x = original.speed_x
            self.speed_y = original.speed_y
            self.acceleration_x = original.acceleration_x
            self.acceleration_y = original.acceleration_y
            self.tick = original.tick
            self.fps = original.fps
            self.moving = threading.Lock()
            if original.moving.locked():
                self.start_move()
        else:
            self.windows_coordinates = {}
            self.x = 0
            self.y = 0
            self.speed_x = 0
            self.speed_y = 0
            self.acceleration_x = 0
            self.acceleration_y = 0
            self.tick = 0.01
            self.fps = 60
            self.moving = threading.Lock()
    
    def _move(self):
        with self.moving:
            st = time.perf_counter()
            t = 0
            while self.moving.locked():
                self.x += self.speed_x * (self.tick - min(0, t))
                self.y += self.speed_y * (self.tick - min(0, t))
                self.speed_x += self.acceleration_x * (self.tick - min(0, t))
                self.speed_y += self.acceleration_y * (self.tick - min(0, t))
                t = self.tick - time.perf_counter() + st
                if t > 0:
                    time.sleep(t)
                st = time.perf_counter()

    
    def updating(self):
        timer = Timer()
        t = 0
        while self.moving.locked():
            for hwnd in reversed(self.hwnds):
                if not hwnd:
                    continue
                move_window(hwnd, self.windows_coordinates[hwnd][0] + self.x, self.windows_coordinates[hwnd][1] + self.y)
            t += 1/self.fps
            timer.wait_for(t)

    
    def start_move(self):
        if self.moving.locked(): return
        threading.Thread(target=self._move).start()
        threading.Thread(target=self.updating).start()
    
    def stop_move(self):
        if self.moving.locked():
            self.moving.release()

    def create(self, x, y, message, title, icon, button=win32con.MB_OK, name=None, block=True):
        if not block:
            threading.Thread(target=self.create, args=(x, y, message, title, icon, button, name, True)).start()
            return
        hwnd = msgbox(x + self.x, y + self.y, message, title, icon)
        if hwnd is None:
            raise Exception("Error: Failed to create window")
        self.hwnds.append(hwnd)
        self.vaild_hwnd.add(hwnd)
        if name is not None:
            self.names[name] = hwnd
        if self.parant_hwnd is not None:
            win32gui.SetParent(hwnd, self.parant_hwnd)
        self.windows_coordinates[hwnd] = [x, y]
        return hwnd