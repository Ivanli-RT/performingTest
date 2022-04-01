from tkinter import *
from tkinter import ttk
import os
from setWindows import *
import csv
from multiprocessing import Process
import threading
import winreg
import result_save_delete

class mainWindows(Frame):
    def __init__(self, win, width, height):
        self.win = win
        self.width = int(int(width)/15)
        self.height = int(int(height)/15)
        self.set = setWindows()
        self.rsd = result_save_delete.dataSavesDel()
        self.pathData = r'.\data.txt'
        self.pathResult = r'.\result.txt'
        def get_desktop():
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
            return winreg.QueryValueEx(key, "Desktop")[0]
        self.pathDesktop = get_desktop()
        self.itemPath = r'E:\上电科\委托项目'
        self.refreshPath = r'.\refreshd.txt'
        self.fileSelect = r'.\fileSelect.txt'
        self.lock = threading.Lock()

    def func(self):
        self.contents()

    def contents(self):
        #显示目录（树状图）
        self.dicLabel = Label(self.win, text='文件目录')
        self.dicLabel.grid(row=0, column=0, sticky=W)
        bre = Button(self.win, text='刷新目录', command=self.func)
        bre.grid(row=0, column=2, sticky=E)
        self.tree = ttk.Treeview(self.win)
        self.tree.grid(row=1, column=0,
                       sticky=(N, S, E, W),
                       rowspan=27,
                       columnspan=3)#
        #遍历桌面并显示
        root = self.tree.insert('', 'end', text=self.getLastPath(self.pathDesktop), open=True, values=(self.pathDesktop,))
        self.loadTree(root, self.pathDesktop)

        #创建关联滚动条
        self.scrollc1 = Scrollbar()
        self.scrollc1.grid(row=1, column=3, rowspan=26, sticky=N+S)
        #关联
        self.scrollc1.config(command=self.tree.yview)
        self.tree.config(yscrollcommand=self.scrollc1.set)
        #绑定事件
        self.tree.bind('<<TreeviewSelect>>', self.readData)

    def getLastPath(self, path):
        pathList = os.path.split(path)
        return pathList[-1]

    def loadTree(self, parent, parentPath):
        for fileName in os.listdir(parentPath):
            absPath = os.path.join(parentPath, fileName)
            # 插入树枝
            treey = self.tree.insert(parent, 'end', text=self.getLastPath(absPath), values=(absPath,))
            # 判断是否是目录
            if os.path.isdir(absPath):
                self.loadTree(treey, absPath)

    def readData(self, event):
        self.v = event.widget.selection()
        for sv in self.v:
            file = self.tree.item(sv)['text']
            absPath = self.tree.item(sv)['values'][0]
        f = open(self.fileSelect, 'a+')
        f.truncate(0)
        f.write(absPath)
        f.flush()
        f.close()
        pathList = os.path.split(absPath)
        filename = os.path.splitext(pathList[-1])
        filename,type = filename
        if type == '.txt':
            r = open(absPath, 'r')
            dataStr = r.read()
            dataList = dataStr.splitlines()
            pNum = len(dataList)
            d = open(self.pathData, 'a+')
            d.truncate(0)
            for i in range(pNum):
                d.write(dataList[i]+'\n')
            d.flush()
            d.close()
            ref = open(self.refreshPath, 'a+')
            ref.truncate(0)
            ref.write('1')
            ref.flush()
            ref.close()
        elif type == '.csv':
            dataList = []
            with open(absPath, 'r', encoding='utf-16 le', errors='ignore') as f:
                dataInfo = csv.reader(f)
                for row in dataInfo:
                    dataList.append(row)
            pNum = len(dataList)
            d = open(self.pathData, 'a+')
            d.truncate(0)
            for i in range(pNum):
                med = dataList[i][0].encode(encoding='gbk', errors='ignore')
                d.write(med.decode(encoding='gbk', errors='ignore') + '\n')
            d.flush()
            d.close()
            ref = open(self.refreshPath, 'a+')
            ref.truncate(0)
            ref.write('1')
            ref.flush()
            ref.close()
        elif os.path.isdir(absPath):
            d = open(self.pathData, 'a+')
            d.truncate(0)
            for fileName in os.listdir(absPath):
                d.write(fileName+'\n')
            d.flush()
            d.close()
            ref = open(self.refreshPath, 'a+')
            ref.truncate(0)
            ref.write('1')
            ref.flush()
            ref.close()

    def results(self):
        #创建结果文本框
        with open(self.pathResult, 'r') as r:
            view = r.read()
        self.resLabel = Label(self.win, text='计算\n结果', font=('C71585', 16), fg='SteelBlue')
        self.resLabel.grid(row=28, column=0, rowspan=4, sticky=W+E)
        button_save = Button(self.win, text='保存结果',
                              command=self.rsd.dataSave
                              )
        button_save.grid(row=32, column=0, sticky=W+E)
        button_delete = Button(self.win, text='删除结果',
                              command=self.resultSaves
                              )
        button_delete.grid(row=33, column=0, sticky=W+E)
        self.result = Text(self.win, width=int(self.width/2.5),
                            height=int(self.height/5))
        self.result.grid(row=28, column=1, columnspan=6,
                         rowspan=8, sticky=(N, S, E, W))
        self.result.delete(0.0, END)
        self.result.insert(INSERT, view)
        r.close()
        # 创建关联滚动条
        self.scrollc2 = Scrollbar()
        self.scrollc2.grid(row=28, column=6, rowspan=8, sticky=N + S)
        # 关联
        self.scrollc2.config(command=self.result.yview)
        self.result.config(yscrollcommand=self.scrollc2.set)


    def datas(self):
        #创建数据显示框
        with open(self.pathData, 'r') as d:
            view = d.read()
        self.dataLabel = Label(self.win, text='数据')
        self.dataLabel.grid(row=0, column=5, sticky=W)
        self.data = Text(self.win, width=int(self.width),
                         height=int(self.height/1.3))
        self.data.grid(row=1, column=5, rowspan=26,
                       sticky=(N, S, E, W))
        self.data.delete(0.0, END)
        self.data.insert(INSERT, view)
        d.close()
        # 创建关联滚动条
        self.scrollc3 = Scrollbar()
        self.scrollc3.grid(row=1, column=6, rowspan=27, sticky=N + S)
        # 关联
        self.scrollc3.config(command=self.data.yview)
        self.data.config(yscrollcommand=self.scrollc3.set)


    def commands(self):
        #按钮列
        self.button1 = Button(self.win, text='位置准确度&重复性',
                              command=self.PAPR_Subprocess
                              )
        self.button1.grid(row=0, column=4, sticky=W+E)
        self.button2 = Button(self.win, text='位姿准确度&重复性',
                              command=self.PAPR2_Subprocess
                              )
        self.button2.grid(row=1, column=4, sticky=W+E)
        self.button3 = Button(self.win, text='多方向位姿准确度变动',
                              command=self.MDpose_Subprocess
                              )
        self.button3.grid(row=2, column=4, sticky=W+E)
        self.button4 = Button(self.win, text='距离准确度和重复性',
                              command=self.DAR_Subprocess
                              )
        self.button4.grid(row=3, column=4, sticky=W+E)
        self.button5 = Button(self.win, text='位置稳定时间&超调量',
                              command=self.SO_Subprocess
                              )
        self.button5.grid(row=4, column=4, sticky=W+E)
        self.button6 = Button(self.win, text='位姿特性漂移',
                              command=self.drift_Subprocess
                              )
        self.button6.grid(row=5, column=4, sticky=W+E)
        self.button7 = Button(self.win, text='直线准确度&重复性',
                              command=self.line_Subprocess
                              )
        self.button7.grid(row=6, column=4, sticky=W+E)
        self.button8 = Button(self.win, text='大圆准确度&重复性',
                              command=self.BC_Subprocess
                              )
        self.button8.grid(row=7, column=4, sticky=W + E)
        self.button9 = Button(self.win, text='小圆准确度&重复性',
                              command=self.SC_Subprocess
                              )
        self.button9.grid(row=8, column=4, sticky=W + E)
        self.button10 = Button(self.win, text='重定向轨迹准确度',
                              command=self.Reorientation_Subprocess
                              )
        self.button10.grid(row=9, column=4, sticky=W + E)
        self.button11 = Button(self.win, text='静态柔顺性',
                              command=self.SCOM_Subprocess
                              )
        self.button11.grid(row=10, column=4, sticky=W+E)
        self.button12 = Button(self.win, text='拐角偏差&拐角超调',
                              command=self.COCR_Subprocess
                              )
        self.button12.grid(row=11, column=4, sticky=W+E)
        self.button13 = Button(self.win, text='最小定位时间',
                              command=self.MINPT_Subprocess
                              )
        self.button13.grid(row=12, column=4, sticky=W+E)
        self.button14 = Button(self.win, text='轨迹速度特性',
                              command=self.TarckS_Subprocess
                               )
        self.button14.grid(row=13, column=4, sticky=W+E)
        self.button15 = Button(self.win, text='摆动偏差',
                              command=self.WEAVING_Subprocess
                               )
        self.button15.grid(row=14, column=4, sticky=W+E)
        self.button16 = Button(self.win, text='简单速度测试',
                              command=self.set.simple_v
                               )
        self.button16.grid(row=15, column=4, sticky=W+E)
    '''
    设置窗口进程
    '''
    def PAPR_Subprocess(self):
        p = Process(target=self.set.poseAR, name='ar')
        p.start()
        
    def PAPR2_Subprocess(self):
        p = Process(target=self.set.poseAR2, name='ar2')
        p.start()
        
    def MDpose_Subprocess(self):
        p = Process(target=self.set.MD_Pose, name='mdp')
        p.start()
    
    def DAR_Subprocess(self):
        p = Process(target=self.set.d_AR, name='dar')
        p.start()
    
    def SO_Subprocess(self):
        p = Process(target=self.set.Stable_Overshoot, name='stabletimeover&shoot')
        p.start()
    
    def drift_Subprocess(self):
        p = Process(target=self.set.drift, name='drift')
        p.start()
    
    def line_Subprocess(self):
        p = Process(target=self.set.line_AR, name='linear')
        p.start()

    def BC_Subprocess(self):
        p = Process(target=self.set.bcircle_AR, name='bigcircle')
        p.start()

    def SC_Subprocess(self):
        p = Process(target=self.set.scircle_AR, name='smallcircle')
        p.start()
    
    def Reorientation_Subprocess(self):
        p = Process(target=self.set.reorientation_A, name='reorientation')
        p.start()

    def SCOM_Subprocess(self):
        p = Process(target=self.set.Stable_Compliance, name='stablecomliance')
        p.start()
    
    def COCR_Subprocess(self):
        p = Process(target=self.set.CRCO_AR, name='cocr')
        p.start()
    
    def MINPT_Subprocess(self):
        p = Process(target=self.set.min_time, name='minimumposingtime')
        p.start()
    
    def TarckS_Subprocess(self):
        p = Process(target=self.set.Track_Speed, name='pathvelocitycharacteristic')
        p.start()
    
    def WEAVING_Subprocess(self):
        p = Process(target=self.set.weaving, name='weaving')
        p.start()
    
    def resultSaves(self):
        p = Process(target=self.rsd.dataDelete, name='weaving')
        p.start()