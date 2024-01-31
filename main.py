#!/usr/bin/python
from ui.main_ui import MainUI
import ctypes

myappid = "com.miajio.guess"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if __name__ == "__main__":
    m = MainUI()
    m.run()