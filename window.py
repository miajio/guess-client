import tkinter as tk

def center_window(win:tk.Tk, win_width: int, win_height: int):
    """
    窗体居中
    参数: win 窗体
    参数: win_width 窗体宽度
    参数: win_height 窗体高度
    """ 
    # 获取屏幕宽高
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # 计算窗口左上角应该放置的x,y坐标
    x = (screen_width - win_width) / 2
    y = (screen_height - win_height) / 2
    # 设置窗口居中
    win.geometry('%dx%d+%d+%d' % (win_width, win_height, x, y))
