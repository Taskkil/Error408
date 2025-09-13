from windows import *
from screen import *

fps = 60

class Task1(Task):
    def start(self, timer:Timer):
        timer.wait_for(64.165)
        self.sync_move(speed_y=200)
        self.manager.create(75, SCREEN.height - 200, "?????????????????????????????", "-----------------", 16)
        self.manager.create(55, -170, "?????????????????????????????\n?????????????????????????????", "---------------", 16)
        self.manager.create(75, -150, "?????????????????????????????\n?????????????????????????????", "---------------", 16)
        timer.wait_for(64.466)
        x = 125
        y = -100
        t = 64.466
        for _ in range(3):
            self.manager.create(x, y, "???????????????????????????", "Error", 0)
            x += 20
            y += 20
            t += 0.1
            timer.wait_for(t)
        timer.wait_for(64.766)
        self.manager.create(SCREEN.width / 2 + 100, -100, "???? ???????? ???????? ???????? ????? ????? ????????? ??????? ???????\n??????? ????? ??? ??????? ????? ????????? ????? ??????? ?????? ??????\n??????? ???? ???????? ????? ???????? ????????? ?????? ???? ???????", "???????? ????????", 48)
        timer.wait_for(64.966)
        x = SCREEN.width / 2 + 80
        y = -200
        t = 64.966
        for _ in range(3):
            self.manager.create(x, y, "?????? ??????? ????????? ?????? ???????? ?????? ?????\n????? ??????? ??????", "Microsoft ?????", 16)
            x += 40
            y += 30
            t += 0.1
            timer.wait_for(t)
        timer.wait_for(65.267)
        x = SCREEN.width / 2
        y = -400
        t = 65.267
        for _ in range(3):
            self.manager.create(x, y, "-------------------", "----------------", 48)
            x += 20
            y += 20
            t += 0.1
            timer.wait_for(t)
        timer.wait_for(65.599)
        x = SCREEN.width / 2 + 100
        y = -350
        t = 65.599
        for _ in range(2):
            self.manager.create(x, y, "????????????????????????????????????????????\n?????????????????????", "?????? ?????? ??????", 48)
            x += 20
            y += 20
            t += 0.1
            timer.wait_for(t)
        timer.wait_for(65.932)
        self.manager.create(30, -400, "???????????????????????????????????????????????????????????????\n??????????????????????????", "?????????????????????????? ??????????? ??????????????????????", 48)
        timer.wait_for(65.999)
        self.manager.create(10, -420, "???????????????????????????????????????????????????????????????\n??????????????????????????", "?????????????????????????? ??????????? ??????????????????????", 48)
        timer.wait_for(66.099)
        self.manager.create(200, -370, "?????????????????????????????????????????????????????????????\n????????????????????????????????????????", "??????????????????????????????????????", 16)
        timer.wait_for(66.433)
        self.manager.create(SCREEN.width / 2 - 350, -450, "????????????????????????????????\n????????????????????????\n\n????????????????????????????????????????????\n???????????????????????", "????????? ????????????", 16, button=win32con.MB_YESNO)
        timer.wait_for(66.499)
        self.manager.create(100, -500, "?????????????????????????????????????????????????????????\n?????????????????????????????????????????????????????????\n?????????????????????????????????????????????????????????", "Warning", 48)
        timer.wait_for(69.498)
        self.manager.close()


class Task2(Task):
    def start(self, timer:Timer):
        threading.Thread(target=os.system, args=("control",)).start()
        timer.wait_for(69.432)
        x = 0
        y = 100
        t = 69.432
        for _ in range(20):
            hwnd = self.manager.create(x, y, "Unexpected error: 21", "Cannot Run Program", 48)
            set_window_z_order(hwnd, "topmost")
            x += 20
            y += 20
            t += 0.1
            timer.wait_for(t)
        timer.wait_for(71.932)
        self.manager.close()
        os.system("taskkill /t /im explorer.exe")

class Task3(Task):
    def start(self, timer:Timer):
        timer.wait_for(70)
        x = SCREEN.width / 2 - 150
        y = SCREEN.height / 2 - 100
        t = 70
        for _ in range(20):
            hwnd = self.manager.create(x, y, "Insufficient memory or disk space", "Setup Initialization Error", 16)
            set_window_z_order(hwnd, "topmost")
            x += 20
            y += 20
            t += 0.05
            timer.wait_for(t)
        timer.wait_for(71.932)
        self.manager.close()

class Task4(Task):
    def start(self, timer:Timer):
        timer.wait_for(73.399)
        t = 73.399
        x = SCREEN.width / 2 - 150
        y = SCREEN.height / 2 - 100
        for _ in range(13):
            hwnd = self.manager.create(x, y, "", "", 0)#空
            set_window_z_order(hwnd, "topmost")
            x += 20
            y += 20
            t += 0.1
            timer.wait_for(t)
        timer.wait_for(75.166)
        self.manager.close()

class Task5(Task):
    def move_down(self, hwnd, x, y, speed, delay=1 / fps, distance=20):
        timer = Timer()
        t = 0
        for _ in range(distance // int(speed * delay)):
            move_window(hwnd, x, y)
            y += speed * delay
            t += delay
            timer.wait_for(t)
    def start(self, timer:Timer):
        timer.wait_for(75.531)
        
        t = 75.531
        x1 = SCREEN.width / 2 - 150
        y1 = SCREEN.height / 2 -100
        x2 = SCREEN.width / 2 + 50
        y2 = 100
        t = 75.531
        for i in "02200111102211":
            if i != "1":
                hwnd = self.manager.create(x1, y1, "You not have permission to view or edit the current permission\nsetting for Documents, but you can take ownership or change\naudting settings.", "Security", 48)
                x1 += 20
                y1 += 20
                set_window_z_order(hwnd, "topmost")
            if i != "0":
                hwnd = self.manager.create(x2, y2, "An error has occurred, See the log File\nE:\\Developer\\.metadacal\\.log", "Eclipse", 0)
                x2 += 20
                y2 += 20
                set_window_z_order(hwnd, "topmost")
            t += 0.1
            timer.wait_for(t)
        timer.wait_for(77.566)
        x = SCREEN.width / 3
        y = SCREEN.height / 3
        t = 77.566
        for _ in range(3):
            hwnd = self.manager.create(x, y, "Unable to install or run the application. The application\nrequires that assembly System.Data SqlServerCe Version\n3.5.1.0 be installed in the Global Assembly Cache(GAC) first.\n\nPlease contact your system administrator.", "System Update Required", win32con.MB_ICONQUESTION)
            set_window_z_order(hwnd, "topmost")
            x += 20
            y += 20
            t += 0.1
            timer.wait_for(t)
        t += 0.2
        timer.wait_for(t)
        self.manager.close()


        timer.wait_for(78.332)
        hwnd = self.manager.create(SCREEN.width / 2 - 150, SCREEN.height / 2 - 100, '"Totally Legit Software, Not Evil Malware" is an\napplication downloaded from the Internet. Are you\nsure you want to open it?\nGoogle Chrome.app downloaded this file today at 3:02 PM', "", win32con.MB_ICONWARNING, win32con.MB_YESNO)
        set_window_z_order(hwnd, "topmost")
        self.move_down(hwnd, SCREEN.width / 2 - 150, SCREEN.height / 2 - 100, 200)
        timer.wait_for(78.498)
        hwnd = self.manager.create(200, 200, 'Save changes to the Adobe Photoshop\nDocument "Untitled-1" befor closing?', '', win32con.MB_ICONQUESTION, win32con.MB_YESNOCANCEL)
        set_window_z_order(hwnd, "topmost")
        self.move_down(hwnd, 200, 200, 200)
        timer.wait_for(78.631)
        hwnd = self.manager.create(SCREEN.width / 2 + 150, SCREEN.height / 2 + 100, 'You are opening the application "OmniGraffle\nProfessional" for the first time. Are you sure you\nwant to open this application?\n\nThe application is in a folder named "Applications". To see the\napplication in the Finder without opening it, click Show\nApplications.', '', win32con.MB_ICONWARNING, win32con.MB_YESNOCANCEL)
        set_window_z_order(hwnd, "topmost")
        self.move_down(hwnd, SCREEN.width / 2 + 200, SCREEN.height / 2 + 100, 200)
        timer.wait_for(78.866)
        hwnd = self.manager.create(SCREEN.width / 2 + 100, 200, 'Can not join "RedSky".\nA connetion timeout occurred.', '', win32con.MB_ICONWARNING)
        set_window_z_order(hwnd, "topmost")
        self.move_down(hwnd, SCREEN.width / 2 + 100, 200, 200)
        timer.wait_for(78.933)
        hwnd = self.manager.create(SCREEN.width / 2 + 120, 220, 'Error\n\nUnexpected error occurred. You can help us to solve\nthe problem by posting the contents of the log file\non the Factorio forums.', '', win32con.MB_ICONWARNING)
        set_window_z_order(hwnd, "topmost")
        self.move_down(hwnd, SCREEN.width / 2 + 120, 220, 200)
        timer.wait_for(79.099)
        hwnd = self.manager.create(200, 400, 'guiminer Error', '', win32con.MB_ICONERROR, win32con.MB_OKCANCEL)
        set_window_z_order(hwnd, "topmost")
        self.move_down(hwnd, 200, 400, 200)
        timer.wait_for(79.266)
        hwnd = self.manager.create(SCREEN.width / 2 - 300, SCREEN.height / 2 - 50, "https://www.btopenzone.com:8443\nJavaScript error detected!\n\nError: TypeError: 'null' is not an object\nLine: 0\nURL: undefined\nBowser: Mozilla/5.0 (Macintosh; Intel Mac OS X\n10_7_3)AppleWebKit/534.53.11 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10", '', win32con.MB_ICONERROR)
        set_window_z_order(hwnd, "topmost")
        self.move_down(hwnd, SCREEN.width / 2 - 300, SCREEN.height / 2 - 50, 200)
        timer.wait_for(79.437)
        hwnd = self.manager.create(SCREEN.width / 2 - 150, 30, "Partition failed\n\nPartition failed with the error:\n\nThe partition cannot be resized. Try reducing the\namount of change in the size of the partition.", "", 16)
        set_window_z_order(hwnd, "topmost")
        self.move_down(hwnd, SCREEN.width / 2 - 150, 30, 200)
        timer.wait_for(79.598)
        hwnd = self.manager.create(SCREEN.width / 2 + 100, 250, '"Sibelius 7 Installer.mpkg" can'  + "'t be\nopened because it is from an unidentified\ndeveloper.\n\nYour security preferences allow installations of only\napp from the Mac App Store and identified developers.\n\n" + '"Sibelius 7 Installer.mpkg" is on the disk image\n"Sibelius 7 Allt_ang.dmg". Firefox downloaded this disk\nimage today at 14:46.', "", 16)
        set_window_z_order(hwnd, 'topmost')
        self.move_down(hwnd, SCREEN.width / 2 + 100, 250, 200)
        timer.wait_for(79.667)
        hwnd = self.manager.create(
            SCREEN.width / 2 - 200, SCREEN.height / 2 - 200,
            "Your computer was restarted because of a problem.\n" \
            "This report will be send to Apple automatically.\n" \
            "Comments\n" \
            "Problem Details and System Configuration\n" \
            "Interval Scince Last Panic Report: 10078 sec\n" \
            "Panic Scince Last Report:          4\n" \
            "Anonymous UUID:\n" \
            "***\n" \
            "\n" \
            "Wed Aug 15 11:34:03 2012\n" \
            "***\n" \
            "***\n" \
            "\n" \
            "Backtrace (CPU 5), Frame : Return Address:\n" \
            "0xffffff80c50abbb0 : 0xffffff800e21d5f6\n" \
            "0xffffff80c50abc20 : 0xffffff7f90000f1f\n" \
            "0xffffff80c50abc30 : 0xffffff800e5f9fae\n" \
            "0xffffff80c50abc90 : 0xffffff800e5f809d\n" \
            "0xffffff80c50abce0 : 0xffffff800e5f6f7d\n" \
            "0xffffff80c50abd40 : 0xffffff800e5f694d\n" \
            "0xffffff80c50abdb0 : 0xffffff800e607c33",
            "Problem Report for OS X",
            16,
            win32con.MB_OKCANCEL
        )
        set_window_z_order(hwnd, 'topmost')
        self.move_down(hwnd, SCREEN.width / 2 - 200, SCREEN.height / 2 - 200, 200)
        timer.wait_for(79.732)
        t = 79.732
        x = 50
        y = SCREEN.height / 3 * 2
        windows = [
            ("Your computer was restarted because of a\nproblem.\nClick Report to see more detailed information and\nsend a report to Apple.", "", 48, win32con.MB_OKCANCEL),
            ("Steam requires that /Applications/Steam.app/\nContents/MacOS be created on a case insensitive\nfile system, with read-write access.", "", win32con.MB_ICONINFORMATION),
            ("Unsupported File Format\nThe PICT file format is not supported in 64-bit\nmode. Try selecting " '"Open in 32-bit Mode" in the\nFinder ' "'s info window for Preview.", "", 48),
            ("Site Manager - Invalid data\nFileZilla is running in kiosk mode.\n'Normal' and 'Account' logontypes are not avaliable in this\nmode.", "", 48),
            ("The application FileSyncAgent quit\nunexpectedly.\n\nMac OS X and other applications are not affected.\n\nClick Retaunch to launch the application again. Click\nReport to see more details of send a report to Apple.", "", 48, win32con.MB_YESNOCANCEL),
            ("Connection failed\n\nThe server " '"Meredith" may not exist or it is\nunavaliable at this time. Check the server name or IP\naddress, check your network connection. and then\ntry again.', "", 48),
            ('"MacDefender.mpkg" will damage your computer.\nYou should move it to the Trash.\nSarfar downloaded this file today at 2:24 PM from\n 169.254.77.133. It contains the "OSX.MacDefender.A" malware.', "", 16, win32con.MB_YESNOCANCEL),
            ('"10019117.pdf" is damaged and can' "'t be\nopened. You should move it to the Trash.", "", 48, win32con.MB_OKCANCEL),
            ("Application Moved\nThe application was been moved, and it's path has\nchanged. To update the product congfiguration, Clickn\nUpdate.", "", 16, win32con.MB_YESNO),
            ("The application FileSyncAgent quit\nunexpectedly.\n\nMac OS X and other applications are not affected.\n\nClick Retaunch to launch the application again. Click\nReport to see more details of send a report to Apple.", "", 48, win32con.MB_YESNOCANCEL),
            ("Your computer was restarted because of a\nproblem.\nClick Report to see more detailed information and\nsend a report to Apple.", "", 48, win32con.MB_OKCANCEL),
            ("Connection failed\n\nThe server " '"Meredith" may not exist or it is\nunavaliable at this time. Check the server name or IP\naddress, check your network connection. and then\ntry again.', "", 48),
        ]
        for window in windows:
            try:
                hwnd = self.manager.create(x, y, *window)
            except Exception:
                print(window)
                raise
            set_window_z_order(hwnd, 'topmost')
            self.move_down(hwnd, x, y, 200)
            t += 0.0909
            timer.wait_for(t)
            x += 50
            y -= 45













def play(timer):
    timer = Timer() if timer is None else timer
    task1 = Task1()
    task2 = Task2()
    task3 = Task3()
    task4 = Task4()
    task5 = Task5()
    timer.wait_for(64.165)
    threading.Thread(target=task1.start, args=(timer,)).start()
    timer.wait_for(69.432)
    threading.Thread(target=task2.start, args=(timer,)).start()
    timer.wait_for(70)
    threading.Thread(target=task3.start, args=(timer,)).start()
    timer.wait_for(73.399)
    threading.Thread(target=task4.start, args=(timer,)).start()
    timer.wait_for(75.531)
    threading.Thread(target=task5.start, args=(timer,)).start()
    


if __name__ == "__main__":
    timer = Timer()
    timer.start_time -= 64.165
    play(timer)