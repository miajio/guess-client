import tkinter as tk
import tkinter.filedialog as tkfd
from utils.window import *
import json
import csv

encodings = ['utf-8', 'gbk', 'gb18030', 'gb2312']

def file_read(file:str, encodingIndex:int):
    """
    读取文件
    """
    if len(encodings) > encodingIndex:
        try:
            with open(file,'r', encoding=encodings[encodingIndex]) as f:
                text = f.read()
            return text
        except:
            return file_read(file, encodingIndex + 1)
    return open(file,'r', errors='replace')

class MainUI:
    """
    主界面
    """

    def __init__(self):
        # 是否已经读取json文件
        self.has_json = False

        self.win = tk.Tk()
        self.win.title("guess-client")
        self.win.iconbitmap('resources/logo/favicon.ico')
        self.win.wm_iconbitmap('resources/logo/favicon.ico')
        # 窗口设置全局默认字体
        self.win.option_add("*Font", ("微软雅黑", 9))

        # 面板加一个宽高依据窗口大小加一个文本框,文本框宽高依据窗口动态变换
        self.panel = tk.Frame(self.win, width=1000, height=600)
        self.panel.pack()
        self.text = tk.Text(self.panel, width=1000, height=600)
        self.text.pack()

        # 创建菜单,菜单中有文件选项,下级有导入文件选项
        self.menu = tk.Menu(self.win)
        self.fileMenu = tk.Menu(self.menu, tearoff=False)
        self.fileMenu.add_command(label="打开文件", command=lambda: self.read_file_method())
        # 默认内置的文件导出菜单,该菜单由导入json文件后才显示
        self.fileMenu.add_command(label="导出", command=lambda: self.write_file_method())

        self.menu.add_cascade(label="文件", menu=self.fileMenu)

        self.win.config(menu=self.menu)
        center_window(self.win, 1000, 600)

    def run(self):
        """
        运行主界面
        """
        self.win.mainloop()
    
    def read_file_method(self):
        """
        读取json文件
        """
        file = tkfd.askopenfilename(title='文件选择', filetypes=[("txt", "*.txt"), ("json", "*.json")])
        if file is None or file == '':
            return
        # 读取文件
        text = file_read(file, 0)
        
        data = text
        # 如果不是json文件,则将文件内容直接显示
        try:    
            # 对文本json文件进行解析
            data = json.loads(text)
            data = json.dumps(data, sort_keys=True, indent=4, separators=(',', ':'))
        # except:
            # self.is_json = False
        finally:
            # if self.is_json:
            #     self.fileMenu.add_command(label="导出", command=lambda: self.write_file_method())
            #     self.has_json = True
            # else:
                # if self.has_json:
                #     self.fileMenu.delete("导出")
                # self.has_json = False
            self.text.delete('0.0', 'end')
            self.text.insert('0.0', data)

    def write_file_method(self):
        """
        导出文件
        """
        file = tkfd.asksaveasfilename(title='文件选择', initialfile='out', defaultextension=".txt", filetypes=[("txt", "*.txt"), ("json", "*.json"), ("csv", "*.csv")])
        if file is None or file == '':
            return
        msg = self.text.get('0.0', 'end').replace('\n', '').replace('\t', '')
        # 判断导出的文件类型
        match file.split('.')[1]:
            case 'txt'| 'json':
                with open(file=file, mode='w') as f:
                    f.write(msg)
            case 'csv':
                try:
                    isArray = False
                    data = json.loads(msg)
                    keys = []
                    if isinstance(data, list):
                        isArray = True
                        for key in data[0]:
                            keys.append(key)
                    else:
                        for key in data:
                            keys.append(key)
                    with open(file=file, mode='w', newline='', encoding='utf-8') as f:
                        csvwriter = csv.writer(f)
                        csvwriter.writerow(keys)
                        if isArray:
                            for val in data:
                                values = []
                                for key in keys:
                                    values.append(val[key])
                                csvwriter.writerow(values)
                        else:
                            values = []
                            for key in keys:
                                values.append(data[key])
                            csvwriter.writerow(values)
                except:
                    print("非json文件,无法导出csv文件")
                    with open(file=file.split('.')[0]+".txt", mode='w') as f:
                        f.write(msg)

                print("导出csv文件")
            case _:
                print("未知文件类型")