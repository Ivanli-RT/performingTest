from tkinter import *
import os
import math
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import numpy as np
import data_read

class pose_accuracy_repeatability():
    def __init__(self, cycle, pose, accuracy):
        self.cycle = cycle
        self.pose = pose
        self.accuracy = accuracy
        self.dataPath = r'.\fileSelect.txt'
        self.refreshPath = r'.\refreshd.txt'
        self.pathResult = r'.\result.txt'

    def calculate(self):
        #读取待处理数据目录
        with open(self.dataPath, 'r') as ff:
            path = ff.read()
        #读取测试数据
        dataTest = data_read.dataRead(path)
        dataTest.txtRead()
        points = dataTest.data
        #按照点位将测量结果分开
        posePoint = {}
        for i in range(self.pose):
            posePoint[i] = np.array([points[m] for m in range(len(points)) if m%self.pose==i ])
        if self.accuracy == True:
            #读取指令点
            filePath = os.path.split(path)
            insPath = filePath[-2]+'\指令点.txt'
            dataIns = data_read.dataRead(insPath)
            dataIns.txtRead()
            instruction = dataIns.data
            #计算各点位的平均点
            pointsAve = [sum(posePoint[m])/self.cycle for m in range(self.pose)]
            #计算该点位位置准确度
            Ap = [np.linalg.norm(instruction[m]-pointsAve[m]) for m in range(self.pose)]
            print(sum(Ap)/self.pose)
            li = {}
            lAve = []          
            for i in range(self.pose):
                #计算各点到平均点的偏差
                li[i] = np.array([np.linalg.norm(m-pointsAve[i]) for m in posePoint[i]])
                lAve.append(np.mean(li[i]))
            #计算方差
            St = [math.sqrt(sum((li[m]-lAve[m])**2)/(self.cycle-1)) for m in range(self.pose)]
            #计算重复性
            Rp = [lAve[m]+3*St[m] for m in range(self.pose)]
            print(sum(Rp)/self.pose)
            #输出结果
            r = open(self.pathResult, 'a+')
            r.truncate(0)
            r.write('***位置准确度与位置重复性***\n')
            for i in range(self.pose):
                r.write('点位P%d的位置准确度为：%.4fmm；重复性为：%.4fmm；\n'
                        % (i+1, Ap[i], Rp[i]))
            r.flush()
            r.close()
            ref = open(self.refreshPath, 'a+')
            ref.truncate(0)
            ref.write('1')
            ref.flush()
            ref.close()
        else:
            #计算各点位的平均点
            pointsAve = [sum(posePoint[m])/self.cycle for m in range(self.pose)]
            li = {}
            lAve = []           
            for i in range(self.pose):
                #计算各点到平均点的偏差
                li[i] = np.array([np.linalg.norm(m-pointsAve[i]) for m in posePoint[i]])
                lAve.append(np.mean(li[i]))
            #计算方差
            St = [math.sqrt(sum((li[m]-lAve[m])**2)/(self.cycle-1)) for m in range(self.pose)]
            #计算重复性
            Rp = [lAve[m]+3*St[m] for m in range(self.pose)]
            print(sum(Rp)/self.pose)
            #输出结果
            r = open(self.pathResult, 'a+')
            r.truncate(0)
            r.write('***位置准确度与位置重复性***\n')
            for i in range(self.pose):
                r.write('点位P%d的位置重复性为：%.4fmm；\n'
                        % (i+1, Rp[i]))
            r.flush()
            r.close()
            ref = open(self.refreshPath, 'a+')
            ref.truncate(0)
            ref.write('1')
            ref.flush()
            ref.close()
        #绘制图像
        #确定子图的布局
        if self.pose <= 5:
            figColumn = self.pose
            figRows = 1
        elif self.pose % 5 != 0:
            figColumn = 5
            figRows = self.pose / 5 + 1
        else:
            figColumn = 5
            figRows = self.pose / 5
        #画图
        fig = plt.figure(figsize=(15,3))
        fig.subplots_adjust(hspace=0.5, wspace=0.5)
        fig.suptitle('位置重复性点位分布',fontsize=16)
        for i in range(self.pose):
            ax = fig.add_subplot(figRows, figColumn, i+1, projection='3d')
            ax.scatter(posePoint[i][:,0], posePoint[i][:,1], posePoint[i][:,2], s=20, marker='o', color='cyan', label='points')
            ax.scatter(pointsAve[i][0], pointsAve[i][1], pointsAve[i][2], s=40, marker='x', color='purple', label='avePoints')
            titlePlot = 'P' + str(i+1)
            ax.set_title(titlePlot)
        plt.show()

