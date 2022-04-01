import os
import numpy as np
import re
import csv

class dataRead():
    def __init__(self, path):
        self.path = path
        self.data = []
    #读取txt中的点位数据
    def txtRead(self):
        f = open(self.path, 'r')
        dataStr = f.read()
        dataStrList = dataStr.splitlines()
        #去抬头
        for i in range(len(dataStrList)):
            if dataStrList[0][0] == '/':
                dataStrList.pop(0)
            else:
                break
        tempData = []
        #分割
        for i in range(len(dataStrList)):
            tempAll = re.split('\t| |,', dataStrList[i])
            tempDigit = [m for m in tempAll if len(m)>0 and ((ord(m[0])>=48 and ord(m[0])<=57) or ord(m[0])==45) ]
            tempData.append(tempDigit)
        #转换为浮点数数组
        self.data = np.array(tempData, dtype=float)
    #读取csv中的位姿数据
    def csvread(self):
        f = open(self.path, 'r', encoding='utf-16 le', errors='ignore')
        dataInfo = csv.reader(f)
        dataList = []
        for row in dataInfo:
            dataList.append(row)
        del dataList[0]   #去掉首行
        pose = []
        a = []
        b = []
        c = []
        for i in range(len(dataList)):
            temp = dataList[i][0].split('\t')
            pose.append(temp[1:4])
            a.append(temp[4])
            b.append(temp[5])
            c.append(temp[6])
        self.data = {}
        self.data['pose'] = np.array(pose, dtype=float)
        self.data['a'] = np.array(a, dtype=float)
        self.data['b'] = np.array(b, dtype=float)
        self.data['c'] = np.array(c, dtype=float)

# pp = r'C:\Users\李昊\Desktop\性能测试试验文件夹\位姿准确度重复性\Frame export1600.csv'
# ss = dataRead(pp)
# ss.csvread()