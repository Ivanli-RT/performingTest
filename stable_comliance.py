from tkinter import *
import win32api
import win32con
import os
import math
import mainWindow
import numpy as np
import pandas as pd
import data_read

class stableCompliance():
    def __init__(self, load, numbers):
        self.load = load
        self.numbers = numbers
        self.dataPath = r'.\fileSelect.txt'
        self.refreshPath = r'.\refreshd.txt'
        self.pathResult = r'.\result.txt'
    def calculate(self):
        #读取待处理数据
        with open(self.dataPath, 'r') as ff:
            path = ff.read()
        #读取测试数据
        dataTest = data_read.dataRead(path)
        dataTest.txtRead()
        dataArray = dataTest.data
        #计算每次测试的位移
        distance = [np.linalg.norm(dataArray[m+1]-dataArray[m]) for m in range(0, len(dataArray), 2)]
        # #计算每个方向的平均值 x+ x- y+ y- z+ z-
        xp = distance[0:self.numbers]
        xm = distance[self.numbers:self.numbers*2]
        yp = distance[self.numbers*2:self.numbers*3]
        ym = distance[self.numbers*3:self.numbers*4]
        zp = distance[self.numbers*4:self.numbers*5]
        zm = distance[self.numbers*5:self.numbers*6]
        
        xpAve = sum(xp) / self.numbers / self.load / 10
        xmAve = sum(xm) / self.numbers / self.load / 10
        ypAve = sum(yp) / self.numbers / self.load / 10
        ymAve = sum(ym) / self.numbers / self.load / 10
        zpAve = sum(zp) / self.numbers / self.load / 10
        zmAve = sum(zm) / self.numbers / self.load / 10

        r = open(self.pathResult, 'a+')
        r.truncate(0)
        r.write('***静态柔顺性***\n')
        r.write('各方向的静态柔顺性为：\nx+：%.4fmm/N；x-：%.4fmm/N；\ny+：%.4fmm/N；y-：%.4fmm/N；\nz+：%.4fmm/N；z-：%.4fmm/N；'
                % (xpAve, xmAve, ypAve, ymAve, zpAve, zmAve))
        r.flush()
        r.close()
        ref = open(self.refreshPath, 'a+')
        ref.truncate(0)
        ref.write('1')
        ref.flush()
        ref.close()