import os
import math
import numpy as np
import pandas as pd
import data_read
from matplotlib import pyplot as plt

class pathVelocityCharacteristics():
    def __init__(self, frequency, speed, numbers):
        self.frequency = float(frequency)
        self.speed = float(speed)
        self.numbers = int(numbers)
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
                    absPath[i] = os.path.join(path, fileName)
        ls = {}
        #将测量结果存入字典
        for i in range(self.numbers):
            dataTest = data_read.dataRead(absPath[i])
            dataTest.txtRead()
            ls[i] = dataTest.data  
        '''
        取整段距离的中间50%段
        '''
        #首末点距离
        totalDistance = [np.linalg.norm(ls[m][-1]-ls[m][0]) for m in range(self.numbers)]
        distanceFirstRef = {}
        distanceLastRef = {}
        #计算每点到起点和端点的距离
        for i in range(self.numbers):
            distanceFirstRef[i] = [np.linalg.norm(ls[i][m] - ls[i][0]) for m in range(len(ls[i]))]
            distanceLastRef[i] = [np.linalg.norm(ls[i][m] - ls[i][-1]) for m in range(len(ls[i]))]
        points50 = {}
        velocity= {}
        #取中间50%段并计算速度
        for i in range(self.numbers):
            points50[i] = []
            velocity[i] = []
            for j in range(len(ls[i])-1):
                if distanceFirstRef[i][j] > totalDistance[i]/4 and distanceLastRef[i][j] > totalDistance[i]/4:
                    points50[i].append(ls[i][j])
                    velocity[i].append(np.linalg.norm(ls[i][j+1]-ls[i][j])*self.frequency)
        #求平均速度
        tempSpeed = {}
        aveSpeed = []
        maxSpeed = []
        minSpeed = []
        for i in range(self.numbers):
            tempSpeed[i] = []
            sumSpeed = 0
            num = 0
            for j in range(len(velocity[i])):
                if velocity[i][j] != 0:
                    tempSpeed[i].append(velocity[i][j])
                    sumSpeed += velocity[i][j]
                    num += 1
            aveSpeed.append(sumSpeed/num)
            maxSpeed.append(max(tempSpeed[i]))
            minSpeed.append(min(tempSpeed[i]))
        #总的平均速度
        tempV = 0
        for i in range(self.numbers):
            tempV += aveSpeed[i]
        totalAveSpeed = tempV/self.numbers
       
        #速度准确度
        AV = (totalAveSpeed - self.speed)/self.speed*100
        
        #计算速度重复性
        tempSv = 0
        for i in range(self.numbers):
            tempSv += (aveSpeed[i] - totalAveSpeed)**2
        Sv = math.sqrt(tempSv/(self.numbers-1))
        RV = Sv*3/self.speed*100
        
        #计算轨迹速度波动
        FVTemp = []
        for i in range(self.numbers):
            FVTemp.append(maxSpeed[i]-minSpeed[i])
        FV = max(FVTemp)
        
        #将结果写入到文件
        r = open(self.pathResult, 'a+')
        r.truncate(0)
        r.write('***轨迹速度特性***\n')
        r.write('轨迹速度准确度为：%.4f%%；\n轨迹速度重复性为：%.4f%%;\n轨迹速度波动为：%.4fmm/s；'
                 % (AV, RV, FV))
        r.flush()
        r.close()
        ref = open(self.refreshPath, 'a+')
        ref.truncate(0)
        ref.write('1')
        ref.flush()
        ref.close()

        for i in range(self.numbers):
            x = [m for m in range(len(tempSpeed[i]))]
            plt.plot(x, tempSpeed[i], label='linear')
            plt.hlines(self.speed, 0, len(tempSpeed[i]), colors='r', linestyle="--")
            plt.hlines(maxSpeed[i], 0, len(tempSpeed[i]), linestyle="-.")
            plt.hlines(minSpeed[i], 0, len(tempSpeed[i]), linestyle="-.")
        plt.show()