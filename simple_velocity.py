from tkinter import *
import os
import math
import mainWindow
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import data_read

class simpleVlocity():
    def __init__(self, frequency):
        self.frequency = frequency
        self.dataPath = r'.\fileSelect.txt'
        self.refreshPath = r'.\refreshd.txt'
        self.pathResult = r'.\result.txt'

    def calculate(self):
        #读取待处理数据
        with open(self.dataPath, 'r') as ff:
            path = ff.read()
        #读取测试数据
        f = open(path, 'r')
        dataStr = f.read()
        dataList = dataStr.splitlines()
        #去掉抬头
        for i in range(len(dataList)):
            if dataList[0][0] == '/':
                del dataList[0]
            else:
                break
        #转换成浮点型数组
        dataListf = [ np.array([float(x.split(' ')[0]), float(x.split(' ')[1]), float(x.split(' ')[2])]) for x in dataList]
        #计算瞬时速度
        velocity = []
        for i in range(len(dataListf)-1):
            velocity.append(np.linalg.norm(dataListf[i+1]-dataListf[i])*self.frequency/1000)
        vMax = max(velocity)
        #位移
        S = [np.linalg.norm(dataListf[m]-dataListf[0]) for m in range(len(dataListf))]
        #将结果写入文件
        r = open(self.pathResult, 'a+')
        r.truncate(0)
        r.write('***最大速度***\n')
        r.write('最大瞬时速度为：%.4fm/s；' % vMax)
        r.flush()
        r.close()
        ref = open(self.refreshPath, 'a+')
        ref.truncate(0)
        ref.write('1')
        ref.flush()
        ref.close()
        #绘制图线
        fig = plt.figure(figsize=(6,3))
        fig.subplots_adjust(hspace=0.5, wspace=0.5)
        fig.suptitle('简单速度测试',fontsize=16)
        x = [i for i in range(len(velocity))]
        y = velocity
        ax = fig.add_subplot(1,2,1)
        ax.plot(x, y, label='linear')
        ax.grid(True)
        ax.set_title('速度曲线')
        x1 = [i for i in range(len(S))]
        y1 = S
        ax = fig.add_subplot(1,2,2)
        ax.plot(x1,y1, label='linear')
        ax.grid(True)
        ax.set_title('位移')
        plt.show()
        



 