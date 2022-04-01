from tkinter import *
import os
import math
import mainWindow
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import numpy as np
import data_read
import spatial_methods

class line_accuracy_repearability():
    def __init__(self, frequency, section, numbers):
        self.frequency = frequency
        self.section = section
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
        #理论直线轨迹目录
        for fileName in os.listdir(path):
            if fileName == '理论直线轨迹.txt':
                absPath[0] = os.path.join(path, fileName)
        #读取理论点
        dataTest = data_read.dataRead(absPath[0])
        dataTest.txtRead()
        instruction = dataTest.data        
        #读取测试数据并且存成字典
        ls = {}
        for i in range(self.numbers):
            dataTest = data_read.dataRead(absPath[i+1])
            dataTest.txtRead()
            ls[i] = dataTest.data
        '''
        计算理论等分点，画出垂直于理论直线的等分面
        '''
        #计算理论直线正交平面
        normal_vector = np.array(instruction[1]-instruction[0])
        
        #等分点坐标
        sectionP = {}
        commandLinePlane4 = []
        for i in range(self.section):
            t1 = instruction[0] + normal_vector / (self.section+1) * (i+1)
            sectionP[i] = t1
            commandLinePlane4.append(-normal_vector.dot(t1))
        '''
        暂不测姿态
        '''
        #截平面上的点
        newXYZ = {}
        for i in range(self.section):
            normN = normal_vector
            normU =  [normal_vector[1], -normal_vector[0], 0]
            normV = np.cross(normN, normU)
            vectorU = normU / np.linalg.norm(normU)
            vectorV = normV / np.linalg.norm(normV)
            normR = 3
            newXYZ[i] = np.array([sectionP[i]+normR*(vectorU*math.cos(m)+vectorV*math.sin(m)) for m in np.arange(0,2*np.pi+np.pi/20,np.pi/20)])
        #找出离切面距离最小点的对应点
        sampleLinePoint = {}       
        for i in range(self.section):     #正交面方程
            sampleLinePoint[i] = []
            for j in range(self.numbers):
                cal = spatial_methods.spatialMethod(normal_vector, ls[j], commandLinePlane4[i])
                sampleLinePoint[i].append(cal.points2planeMin())

        #找出等分面与对应点连线的交点作为每组数据的实测点
        #输入：平面法向量和点，实测两点,commandLinePlane4\normal_vector\sectionP\sampleLinePoint
        #输出：平面与直线的交点。输出量为6*1向量,sampleLineInterP
        sampleLineInterP = {}
        for i in range(self.section):
            sampleLineInterP[i] = []
            for j in range(self.numbers):
                lineVector = sampleLinePoint[i][j][0] - sampleLinePoint[i][j][1]
                #直线向量与平面向量的点积
                vpt = lineVector.dot(normal_vector)
                #求出中间系数
                t = normal_vector.dot(sectionP[i] - sampleLinePoint[i][j][0]) / vpt
                #返回交点位置坐标
                sampleLineInterP[i].append(sampleLinePoint[i][j][0]+lineVector*t)
            sampleLineInterP[i] = np.array(sampleLineInterP[i])
        # print(sampleLineInterP[0])
        '''
        暂不测姿态
        '''
        '''
        根据标准进行轨迹准确度与轨迹重复性的计算
        '''
        #截面上的平均点位
        sampleAve = [sum(sampleLineInterP[m])/self.numbers for m in range(self.section)]
        #计算轨迹位置准确度，ATp
        ATpAll = [np.linalg.norm(sampleAve[m]-sectionP[m]) for m in range(self.section)]
        ATp = max(enumerate(ATpAll), key=lambda x: x[1])
        #计算轨迹位置重复性，RTp
        lSampleData = {}
        lSampleAve = []
        for i in range(self.section):
            lSampleData[i] = [np.linalg.norm(sampleLineInterP[i][m]-sampleAve[i]) for m in range(self.numbers)]
            lSampleAve.append(sum(lSampleData[i])/self.numbers)
        Sl = [math.sqrt(sum((lSampleData[m]-lSampleAve[m])**2)/(self.numbers-1)) for m in range(self.section)]    
        RTpAll = [lSampleAve[m]+3*Sl[m] for m in range(self.section)]
        RTp = max(enumerate(RTpAll), key=lambda x: x[1])

        #将结果写入文件
        r = open(self.pathResult, 'a+')
        r.truncate(0)
        r.write('***直线轨迹准确度和直线轨迹重复性***\n')
        r.write('直线轨迹准确度为：%.4fmm，在第%d个平面；\n直线轨迹重复性为：%.4fmm，在第%d个平面；'
                 % (ATp[1], ATp[0]+1, RTp[1], RTp[0]+1))
        r.flush()
        r.close()
        ref = open(self.refreshPath, 'a+')
        ref.truncate(0)
        ref.write('1')
        ref.flush()
        ref.close()
        '''
        画图
        '''
        fig = plt.figure(figsize=(5,3))
        fig.subplots_adjust(hspace=0.5, wspace=0.5)
        fig.suptitle('直线轨迹准确度', fontsize=16)
        #准确度最大处    
        X = newXYZ[ATp[0]][:,0]
        Y = newXYZ[ATp[0]][:,1]
        X, Y = np.meshgrid(X, Y)    # x-y 平面的网格
        Z = (-normal_vector[0]*X + -normal_vector[1]*Y + normal_vector.dot(newXYZ[ATp[0]][0])) / normal_vector[2] #+ D
        ax = fig.add_subplot(1, 2, 1, projection='3d')
        ax.plot_surface(X, Y, Z, color='lightyellow', alpha=0.3)
        ax.scatter(sectionP[ATp[0]][0], sectionP[ATp[0]][1], sectionP[ATp[0]][2], s=40, marker='x', color='purple', label='instruction')
        ax.scatter(sampleAve[ATp[0]][0], sampleAve[ATp[0]][1], sampleAve[ATp[0]][2], s=40, marker='o', color='red', label='avePoints')   
        ax.set_title('轨迹准确度最大处')
        #重复性最大处
        ax = fig.add_subplot(1, 2, 2, projection='3d')
        ax.scatter(sampleAve[RTp[0]][0], sampleAve[RTp[0]][1], sampleAve[RTp[0]][2], s=40, marker='o', color='red', label='avePoints')
        ax.scatter(sampleLineInterP[RTp[0]][:, 0], sampleLineInterP[RTp[0]][:, 1], sampleLineInterP[RTp[0]][:, 2], s=20, marker='o', color='cyan', label='Points')
        ax.set_title('轨迹重复性最大处')
        plt.show()



