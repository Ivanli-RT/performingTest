import os
import math
import csv
import numpy as np
import matplotlib.pyplot as plt
import data_read

class stable_overshoot():
    def __init__(self, frequency, band, numbers):
        self.frequency = frequency
        self.band = band
        self.numbers = numbers
        self.dataPath = r'.\fileSelect.txt'
        self.refreshPath = r'.\refreshd.txt'
        self.pathResult = r'.\result.txt'

    def calculate(self):
        #读取数据所在的目录
        with open(self.dataPath, 'r') as dic:
            path = dic.read()
        absPath = {}
        absPathStop = {}
        #读取目录下的所有需要文件
        #寻找测试数据的目录
        for i in range(self.numbers):
            filename = str(i+1)+'.txt'
            stopPiont = '实到位置' + str(i+1) + '.txt'
            for fileName in os.listdir(path):
                if fileName == filename:
                    absPath[i+1] = os.path.join(path, fileName)
                elif fileName == stopPiont:
                    absPathStop[i+1] = os.path.join(path, fileName)
        #读取测试数据
        ls = {}
        es = {}
        for i in range(self.numbers):
            dataTest = data_read.dataRead(absPath[i+1])
            dataTest.txtRead()
            ls[i+1] = dataTest.data
            dataTest = data_read.dataRead(absPathStop[i+1])
            dataTest.txtRead()
            es[i+1] = dataTest.data
        
        #计算到实到位置的距离
        distances = {}
        for i in range(self.numbers):
            distances[i] = [np.linalg.norm(m-es[i+1]) for m in ls[i+1]]
        
        #找出第一次进入门限带和最后一次抖出门限带的点
        firstIn = []
        lastOut = []
        for i in range(self.numbers):
            for j in range(len(distances[i])):
                if distances[i][j] <= self.band:
                    firstIn.append(j)
                    break
                if j == len(distances[i])-1 and distances[i][j] > self.band:
                    firstIn.append(j)
            for j in range(len(distances[i])-1, 0, -1):
                if distances[i][j] >= self.band:
                    lastOut.append(j)
                    break
        
        #计算位置稳定时间
        stableList = []
        for i in range(self.numbers):
            if firstIn[i] <= lastOut[i]:
                stableList.append(lastOut[i]-firstIn[i])
            else:
                stableList.append(0)
        stableTime = sum(stableList)/3/self.frequency
        
        #计算超调量
        overShootList = []
        for i in range(self.numbers):
            if stableList[i] == 0:
                overShootList.append(0)
            else:
                overShootList.append(max(distances[i][firstIn[i]:]))
        overShoot = max(overShootList)

        r = open(self.pathResult, 'a+')
        r.truncate(0)
        r.write('***位置稳定时间和位置超调量***\n')
        r.write('位置稳定时间为：%.4fs；\n位置超调量为：%.4fmm；'
                 % (stableTime, overShoot))
        r.flush()
        r.close()
        ref = open(self.refreshPath, 'a+')
        ref.truncate(0)
        ref.write('1')
        ref.flush()
        ref.close()

        #示意图
        layouts = self.numbers*10+1
        plt.figure(layouts)
        for i in range(self.numbers):
            ly = layouts*10+i+1
            plt.subplot(ly)
            x = [m for m in range(firstIn[i]-10, len(distances[i]))]
            plt.plot(x, distances[i][firstIn[i]-10:])
            plt.plot(firstIn[i], distances[i][firstIn[i]], 'm', marker='*')
            plt.plot(lastOut[i], distances[i][lastOut[i]], 'm', marker='+')
            plt.hlines(self.band, firstIn[i]-10, len(distances[i]), colors='r', linestyle="--")
            plt.text(firstIn[i], self.band, str(self.band))
            plt.grid()
        plt.show()



