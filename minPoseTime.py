import os
import math
import mainWindow
import numpy as np
import pandas as pd
import data_read

class mptime():
    def __init__(self, frequency, poseNum, numbers, threshold):
        self.frequency = frequency
        self.poseNum = poseNum
        self.numbers = numbers
        self.threshold = threshold
        self.dataPath = r'.\fileSelect.txt'
        self.refreshPath = r'.\refreshd.txt'
        self.pathResult = r'.\result.txt'
    def calculate(self):
        with open(self.dataPath, 'r') as dic:
            path = dic.read()
        absPath = {}
        #读取目录下的所有需要文件
        #寻找测试数据的目录
        for i in range(self.numbers):
            filename = str(i+1)+'.txt'
            for fileName in os.listdir(path):
                if fileName == filename:
                    absPath[i] = os.path.join(path, fileName)   
        ls = {}
        #将测量结果存入字典
        for i in range(self.numbers):
            dataTest = data_read.dataRead(absPath[i])
            dataTest.txtRead()
            ls[i] = dataTest.data
        #计算速度
        velocity = {}
        for i in range(self.numbers):
            velocity[i] = []
            for j in range(len(ls[i])-1):
                velocity[i].append(np.linalg.norm(ls[i][j+1]-ls[i][j])*self.frequency/1000)
        #计算加速度
        acceleration = {}
        for i in range(self.numbers):
            acceleration[i] = []
            for j in range(len(velocity[i])-5):
                acceleration[i].append((velocity[i][j+5] - velocity[i][j])*self.frequency)
        
        #根据速度和加速度将点位分割
        poses = []
        for i in range(self.numbers):
            pStart = 0
            pStop = 0
            posei = {}
            for j in range(self.poseNum):
                signStart = 0    #标志位
                signStop = 0
                for k in range(pStop, len(velocity[i])):
                    if velocity[i][k] > 0.04 and acceleration[i][k+1]+acceleration[i][k] > 0 and signStart == 0:
                        pStart = k
                        signStart = 1
                    if signStop == 0 and signStart == 1 and velocity[i][k] < 0.04:
                        pStop = k+1000
                        signStop = 1
                posei[j] = [pStart, pStop]
            poses.append(posei)
        #分别计算位置稳定时间
        pTime = []
        for i in range(self.numbers):
            pTimei = []
            for j in range(self.poseNum): 
                for k in range(poses[i][j][1], poses[i][j][0], -1):
                   if np.linalg.norm(ls[i][k]-ls[i][poses[i][j][1]]) > self.threshold:
                       tm = (k - poses[i][j][0]  + 1) / self.frequency
                       pTimei.append(tm)
                       break
            pTime.append(pTimei)
        pTimeAve = []
        for i in range(self.poseNum):
            tmm = 0
            for j in range(self.numbers):
                tmm += pTime[j][i]    
            pTimeAve.append(tmm/self.numbers)
        #将结果写入文件
        r = open(self.pathResult, 'a+')
        r.truncate(0)
        r.write('***最小定位时间***\n')
        for i in range(self.poseNum):
            r.write('点位：P1+%d的最小定位时间为：%.4fs；\n'
                    % (i+1, pTimeAve[i]))
        r.flush()
        r.close()
        ref = open(self.refreshPath, 'a+')
        ref.truncate(0)
        ref.write('1')
        ref.flush()
        ref.close()

