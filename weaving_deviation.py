from tkinter import *
import win32api
import win32con
import os
import math
import mainWindow
import numpy as np
import pandas as pd

class weavingsf():
    def __init__(self, frequency, SC, FC, numbers, FD):
        self.frequency = float(frequency)
        self.Sc = float(SC)
        self.Fc = float(FC)
        self.numbers = int(numbers)
        self.FD = float(FD)
        self.dataPath = r'.\fileSelect.txt'
        self.refreshPath = r'.\refreshd.txt'
        self.pathResult = r'.\result.txt'
    def calculate(self):
        #读取数据所在目录的数据
        with open(self.dataPath, 'r') as dic:
            path = dic.read()
        absPath = {}
        #读取目录下的所有需要文件
        #寻找测试数据的目录
        for i in range(self.numbers):
            filename = str(i+1)+'.txt'
            for fileName in os.listdir(path):
                if fileName == filename:
                    absPath[i+1] = os.path.join(path, fileName)
        #读取指令点
        for fileName in os.listdir(path):
            if fileName == '指令点.txt':
                absPath[0] = os.path.join(path, fileName)
        ls = {}
        #将测量结果存入字典
        with open(absPath[0], 'r') as ins:
            insStr = ins.read()
            instruction = insStr.splitlines()
        insPoints = []
        for i in range(3):
            temp = instruction.split(' ')
            insPoints.append(np.array([float(temp[0]), float(temp[1]), float(temp[2])]))
        # print()
        # print(instruction)
        for i in range(self.numbers):
            with open(absPath[i+1], 'r') as l:
                lStr = l.read()
                ls[i+1] = lStr.splitlines()  
        #去除抬头
        for i in range(self.numbers):
            for j in range(len(ls[i+1])):
                if ls[i+1][0][0] == "/":
                    del ls[i+1][0]
                else:
                    break
        #将测量数据转换为浮点数
        for i in range(self.numbers):
            for j in range(len(ls[i+1])):
                lsm = ls[i+1][j].split(' ')
                ls[i+1][j] = np.array([float(lsm[0]), float(lsm[1]), float(lsm[2])])

        #去掉头尾没有运动的部分
        #计算速度
        velocity = {}
        for i in range(self.numbers):
            velocity[i] = []
            for j in range(len(ls[i+1])-1):
                velocity[i].append(np.linalg.norm(ls[i+1][j+1]-ls[i+1][j])*self.frequency/1000)
        #掐头去尾
        for i in range(self.numbers):
            for j in range(len(velocity[i])):
                if velocity[i][j] < 0.04:
                    ls[i+1].pop(0)
                else:
                    break
            for j in range(len(velocity[i]), 0, -1):
                if velocity[i][j] < 0.04:
                    ls[i+1].pop(-1)

        #创建P1到测量点的向量，以及P2P3的向量
        P2P3 = insPoints[2]-insPoints[1]
        P1P = {}
        disPTempOne = {}
        for i in range(self.numbers):
            disPTempOne[i] = []
            P1P[i] = []
            for j in range(len(ls[i+1])):
                P1P[i].append(ls[i+1][j]-insPoints[0])
                disPTempOne[i].append(np.cross(P1P[i][j], P2P3)/np.linalg.norm(P2P3))
        
        #找到所有极值点，并去除某一顶点的极值点
        localMax = {}
        localMin = {}
        for i in range(self.numbers):
            localMax[i] = []
            localMin[i] = []
            temp1 = 0
            temp2 = 0
            for j in range(self.frequency/10, len(disPTempOne[i])-self.frequency/10, 1):
                #极大值
                if disPTempOne[i][j] > disPTempOne[i][j-self.frequency/10] and disPTempOne[i][j] > disPTempOne[i][j+self.frequency/10]:
                    if temp1 == 0:
                        temp1 = disPTempOne[i][j] 
                    elif np.linalg.norm(ls[i+1][j]-ls[i+1][j-1]) < self.FD:
                        if disPTempOne[i][j] > disPTempOne[i][j-1]:
                            temp1 = disPTempOne[i][j]
                    else:
                        localMax[i].append(temp1)
                        temp1 = disPTempOne[i][j]
                localMax[i].append(temp1)
                #极小值    
                if disPTempOne[i][j] < disPTempOne[i][j-self.frequency/10] and disPTempOne[i][j] < disPTempOne[i][j+self.frequency/10]:
                    if temp2 == 0:
                        temp2 = disPTempOne[i][j] 
                    elif np.linalg.norm(ls[i+1][j]-ls[i+1][j-1]) < self.FD:
                        if disPTempOne[i][j] < disPTempOne[i][j-1]:
                            temp2 = disPTempOne[i][j]
                    else:
                        localMin[i].append(temp2)
                        temp2 = disPTempOne[i][j]
                localMin[i].append(temp2)
        #计算摆幅误差
        Sa = (sum(localMax)-sum(localMin))/self.numbers
        WS = (Sa - self.Sc) / self.Sc *100

        #计算摆频误差
        tSum = 0
        for i in range(self.numbers):
            tSum += len(ls[i+1])
        WT = tSum / self.numbers / self.frequency
        Fa = 1 / WT
        WF = (Fa - self.Fc) / self.Fc * 100
        
        r = open(self.pathResult, 'a+')
        r.truncate(0)
        r.write('***摆动偏差***\n')
        r.write('摆幅误差为：%.4f%%；\n摆频误差为：%.4f%%；'
                % (WS, WF))
        r.flush()
        r.close()
        ref = open(self.refreshPath, 'a+')
        ref.truncate(0)
        ref.write('1')
        ref.flush()
        ref.close()
