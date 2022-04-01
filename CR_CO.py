from tkinter import *
import win32api
import win32con
import os
import math
import mainWindow
import numpy as np
import pandas as pd
import data_read
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class CR_COs():
    def __init__(self, numbers):
        self.numbers = numbers
        self.dataPath = r'.\fileSelect.txt'
        self.refreshPath = r'.\refreshd.txt'
        self.pathResult = r'.\result.txt'
    def calculate(self):
        #读取数据所在的目录
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
                elif fileName == '指令点.txt':
                    absPath[0] = os.path.join(path, fileName)
        #读取指令点
        dataIns = data_read.dataRead(absPath[0])
        dataIns.txtRead()
        instruction = dataIns.data
        #读取测试点
        ls = {}
        #将测量结果存入字典
        for i in range(self.numbers):
            dataTest = data_read.dataRead(absPath[i+1])
            dataTest.txtRead()
            ls[i] = dataTest.data
        '''计算圆角误差'''
        RD1 = {}
        RD2 = {}
        RD3 = {}
        RD4 = {}
        for i in range(self.numbers):   #按照测量组数计算圆角误差
            #第一个角的圆角误差
            RD1[i] = [np.linalg.norm(m-instruction[0]) for m in ls[i]]
            #第二个角的圆角误差
            RD2[i] = [np.linalg.norm(m-instruction[1]) for m in ls[i]]
            #第三个角的圆角误差
            RD3[i] = [np.linalg.norm(m-instruction[2]) for m in ls[i]]
            #第四个角的圆角误差
            RD4[i] = [np.linalg.norm(m-instruction[3]) for m in ls[i]]
        # 选出每组数据中相对于每个角误差的最小值
        CR = {}
        CR[5] = max([min(RD1[m]) for m in range(self.numbers)])
        CR[4] = max([min(RD2[m]) for m in range(self.numbers)])
        CR[3] = max([min(RD3[m]) for m in range(self.numbers)])
        CR[2] = max([min(RD4[m]) for m in range(self.numbers)])
        '''计算拐角超调'''
        #计算实测点到轨迹直线的投影点，每个角单独计算
        #5
        P0 = instruction[-1]
        P1 = instruction[0]   #拐角点
        P2 = instruction[1]   #末端点
        Pn = {}                #投影点
        for i in range(self.numbers):
            Pn[i] = np.array([np.dot(m-P1, P2-P1)/(np.linalg.norm(P2-P1)**2)*(P2-P1)+P1 for m in ls[i]])
        #实测点减去投影点形成向量
        vectorN = {}
        for i in range(self.numbers):
            vectorN[i] = ls[i] - Pn[i]
        #每个向量与第一个向量比较判断是否存在反向，若存在反向，证明存在拐角超调
        cosN = {}
        over = []
        OV = []
        for i in range(self.numbers):
            cosN[i] = []
            for j in range(len(ls[i])):
                if np.dot(vectorN[i][j], P0-P1) < 0:
                    over.append(np.linalg.norm(vectorN[i][j]))
        if over == []:
            OV.append('没有超调')
        else:
            OV.append(max(over))
        #4
        P0 = instruction[0]
        P1 = instruction[1]   #拐角点
        P2 = instruction[2]   #末端点
        Pn = {}               #投影点
        for i in range(self.numbers):
            Pn[i] = np.array([np.dot(m-P1, P2-P1)/(np.linalg.norm(P2-P1)**2)*(P2-P1)+P1 for m in ls[i]])
        #实测点减去投影点形成向量
        vectorN = {}
        for i in range(self.numbers):
            vectorN[i] = ls[i] - Pn[i]
        #每个向量与第一个向量比较判断是否存在反向，若存在反向，证明存在拐角超调
        cosN = {}
        over = []
        for i in range(self.numbers):
            cosN[i] = []
            for j in range(len(ls[i])):
                if np.dot(vectorN[i][j], P0-P1) < 0:
                    over.append(np.linalg.norm(vectorN[i][j]))
        if over == []:
            OV.insert(0, '没有超调')
        else:
            OV.insert(0, max(over))
        #3
        P0 = instruction[1]
        P1 = instruction[2]   #拐角点
        P2 = instruction[3]   #末端点
        Pn = {}               #投影点
        for i in range(self.numbers):
            Pn[i] = np.array([np.dot(m-P1, P2-P1)/(np.linalg.norm(P2-P1)**2)*(P2-P1)+P1 for m in ls[i]])
        #实测点减去投影点形成向量
        vectorN = {}
        for i in range(self.numbers):
            vectorN[i] = ls[i] - Pn[i]
        #每个向量与第一个向量比较判断是否存在反向，若存在反向，证明存在拐角超调
        cosN = {}
        over = []
        for i in range(self.numbers):
            cosN[i] = []
            for j in range(len(ls[i])):
                if np.dot(vectorN[i][j], P0-P1) < 0:
                    over.append(np.linalg.norm(vectorN[i][j]))
        if over == []:
            OV.insert(0, '没有超调')
        else:
            OV.insert(0, max(over))
        #2
        P0 = instruction[2]
        P1 = instruction[3]   #拐角点
        P2 = instruction[0]   #末端点
        Pn = {}               #投影点
        for i in range(self.numbers):
            Pn[i] = np.array([np.dot(m-P1, P2-P1)/(np.linalg.norm(P2-P1)**2)*(P2-P1)+P1 for m in ls[i]])
        #实测点减去投影点形成向量
        vectorN = {}
        for i in range(self.numbers):
            vectorN[i] = ls[i] - Pn[i]
        #每个向量与第一个向量比较判断是否存在反向，若存在反向，证明存在拐角超调
        cosN = {}
        over = []
        for i in range(self.numbers):
            cosN[i] = []
            for j in range(len(ls[i])):
                if np.dot(vectorN[i][j], P0-P1) < 0:
                    over.append(np.linalg.norm(vectorN[i][j]))
        if over == []:
            OV.insert(0, '没有超调')
        else:
            OV.insert(0, max(over))
        #将结果写入文件
        r = open(self.pathResult, 'a+')
        r.truncate(0)
        r.write('***圆角误差与拐角超调***\n')
        for i in range(4):
            r.write('拐角P%d的圆角误差为：%.4fmm; ' % (i+2, CR[i+2]))
            if OV[i] == '没有超调':
                r.write(OV[i]+';\n')
            else:
                r.write('拐角超调为%.4fmm;\n' % OV[i])
        r.flush()
        r.close()
        ref = open(self.refreshPath, 'a+')
        ref.truncate(0)
        ref.write('1')
        ref.flush()
        ref.close()