from tkinter import *
import os
import math
import csv
import data_read
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt

class posture_accuracy_repeatability():
    def __init__(self, cycle, pose, accuracy):
        self.accuracy = {}
        self.repeatability = {}
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
        dataTest.csvread()
        points = dataTest.data['pose']
        aa = dataTest.data['a']
        ba = dataTest.data['b']
        ca = dataTest.data['c']
        #按照点位将测量结果分开
        posePoint = {}
        a = {}
        b = {}
        c = {}
        for i in range(self.pose):
            posePoint[i] = np.array([points[m] for m in range(len(points)) if m%self.pose==i ])
            a[i] = np.array([aa[m] for m in range(len(aa)) if m%self.pose==i ])
            b[i] = np.array([ba[m] for m in range(len(ba)) if m%self.pose==i ])
            c[i] = np.array([ca[m] for m in range(len(ca)) if m%self.pose==i ])
        v1 = posePoint[1] - posePoint[0]
        v1Ave = sum(v1)/self.cycle
        theta1 = [np.arccos(np.dot(v1Ave,m)/np.linalg.norm(m)/np.linalg.norm(v1Ave))/np.pi*180 for m in v1]
        theta1Ave = sum(theta1)/self.cycle
        tr = 3*math.sqrt(sum((theta1-theta1Ave)**2)/(self.cycle-1))
        # print(tr)
        print(tr)
        print(max(theta1-theta1Ave))
        if self.accuracy == True:
            #读取指令点
            filePath = os.path.split(path)
            insPath = filePath[-2]+'\指令点.txt'
            dataIns = data_read.dataRead(insPath)
            dataIns.txtRead()
            insPoints = dataIns.data[:,0:3]
            insA = dataIns.data[:,3]
            insB = dataIns.data[:,4]
            insC = dataIns.data[:,5]
            #计算各点位的平均点和平均姿态
            pointsAve = [sum(posePoint[m])/self.cycle for m in range(self.pose)]
            aAve = [sum(a[m])/self.cycle for m in range(self.pose)]
            bAve = [sum(b[m])/self.cycle for m in range(self.pose)]
            cAve = [sum(c[m])/self.cycle for m in range(self.pose)]
            #计算该点位的位置准确度和姿态准确度
            Ap = [np.linalg.norm(insPoints[m]-pointsAve[m]) for m in range(self.pose)]
            Aa = [aAve[m]-insA[m] for m in range(self.pose)]
            Ab = [bAve[m]-insB[m] for m in range(self.pose)]
            Ac = [cAve[m]-insC[m] for m in range(self.pose)]
            li = {}
            lAve = []
            for i in range(self.pose):
                #计算各点到平均点的偏差
                li[i] = np.array([np.linalg.norm(m-pointsAve[i]) for m in posePoint[i]])
                lAve.append(np.mean(li[i]))
            #计算位置方差
            St = [math.sqrt(sum((li[m]-lAve[m])**2)/(self.cycle-1)) for m in range(self.pose)]
            #计算重复性
            RPl = [lAve[m]+3*St[m] for m in range(self.pose)]
            RPa = [3*math.sqrt(sum((a[m]-aAve[m])**2)/(self.cycle-1)) for m in range(self.pose)]
            RPb = [3*math.sqrt(sum((b[m]-bAve[m])**2)/(self.cycle-1)) for m in range(self.pose)]
            RPc = [3*math.sqrt(sum((c[m]-cAve[m])**2)/(self.cycle-1)) for m in range(self.pose)]
            #输出结果
            r = open(self.pathResult, 'a+')
            r.truncate(0)
            r.write('***位姿准确度和位姿重复性***\n')
            for i in range(self.pose):
                r.write('点位P%d的位姿准确度为：%.4fmm,A:%.4f°,B:%.4f°,C:%.4f°；'
                        '重复性为：%.4fmm,A:%.4f°,B:%.4f°,C:%.4f°；\n'
                        % (i+1, Ap[i], Aa[i], Ab[i], Ac[i], RPl[i], RPa[i], RPb[i], RPc[i]))
            r.flush()
            r.close()
            ref = open(self.refreshPath, 'a+')
            ref.truncate(0)
            ref.write('1')
            ref.flush()
            ref.close()
        else:
            #计算各点位的平均点和平均姿态
            pointsAve = [sum(posePoint[m])/self.cycle for m in range(self.pose)]
            aAve = [sum(a[m])/self.cycle for m in range(self.pose)]
            bAve = [sum(b[m])/self.cycle for m in range(self.pose)]
            cAve = [sum(c[m])/self.cycle for m in range(self.pose)]
            #计算该点位的位置准确度和姿态准确度
            li = {}
            lAve = []
            for i in range(self.pose):
                #计算各点到平均点的偏差
                li[i] = np.array([np.linalg.norm(m-pointsAve[i]) for m in posePoint[i]])
                lAve.append(np.mean(li[i]))
            #计算位置方差
            St = [math.sqrt(sum((li[m]-lAve[m])**2)/(self.cycle-1)) for m in range(self.pose)]
            #计算重复性
            RPl = [lAve[m]+3*St[m] for m in range(self.pose)]
            RPa = [3*math.sqrt(sum((a[m]-aAve[m])**2)/(self.cycle-1)) for m in range(self.pose)]
            RPb = [3*math.sqrt(sum((b[m]-bAve[m])**2)/(self.cycle-1)) for m in range(self.pose)]
            RPc = [3*math.sqrt(sum((c[m]-cAve[m])**2)/(self.cycle-1)) for m in range(self.pose)]
            #输出结果
            r = open(self.pathResult, 'a+')
            r.truncate(0)
            r.write('***位姿准确度和位姿重复性***\n')
            for i in range(self.pose):
                r.write('点位P%d的位姿重复性为：%.4fmm,A:%.4f°,B:%.4f°,C:%.4f°；\n'
                        % (i+1, RPl[i], RPa[i], RPb[i], RPc[i]))
            r.flush()
            r.close()
            ref = open(self.refreshPath, 'a+')
            ref.truncate(0)
            ref.write('1')
            ref.flush()
            ref.close()
        #绘制图像       

        #确定子图的布局
        figColumn = 4
        figRows = self.pose
        #画图
        fig = plt.figure(figsize=(12,10))
        fig.subplots_adjust(hspace=0.5, wspace=0.5)
        fig.suptitle('位姿重复性点位姿态分布(角度放大1000倍)', fontsize=16)
        for i in range(self.pose):
            #xyz
            ax = fig.add_subplot(figRows, figColumn, i*4+1, projection='3d')
            ax.scatter(posePoint[i][:,0], posePoint[i][:,1], posePoint[i][:,2], s=20, marker='o', color='cyan', label='points')
            ax.scatter(pointsAve[i][0], pointsAve[i][1], pointsAve[i][2], s=40, marker='x', color='purple', label='avePoints')
            titlePlot = 'P' + str(i+1)
            ax.set_title(titlePlot)
            #A
            ax = fig.add_subplot(figRows, figColumn, i*4+2, projection='polar')
            ax.set_rlim(0.5, 2.3)
            plotAngle = [m*1000/180*np.pi  for m in a[i]]
            thetaMin = min(a[i]*1000)-5
            thetaMax = max(a[i]*1000)+5
            ax.set_thetamin(thetaMin)
            ax.set_thetamax(thetaMax)  
            color=plotAngle  
            ax.scatter(plotAngle, [m for m in np.arange(1,2.2,1.2/(self.cycle-1))], c=color, cmap='cool', alpha=0.75)
            titlePlot = 'A'
            ax.set_title(titlePlot)
            #B
            ax = fig.add_subplot(figRows, figColumn, i*4+3, projection='polar')
            ax.set_rlim(0.5, 2.3)
            plotAngle = [m*1000/180*np.pi  for m in b[i]]
            thetaMin = min(b[i]*1000)-5
            thetaMax = max(b[i]*1000)+5
            ax.set_thetamin(thetaMin)
            ax.set_thetamax(thetaMax)  
            color=plotAngle  
            ax.scatter(plotAngle, [m for m in np.arange(1,2.2,1.2/(self.cycle-1))], c=color, cmap='cool', alpha=0.75)
            titlePlot = 'B'
            ax.set_title(titlePlot)
            #C
            ax = fig.add_subplot(figRows, figColumn, i*4+4, projection='polar')
            ax.set_rlim(0.5, 2.3)
            plotAngle = [m*1000/180*np.pi  for m in c[i]]
            thetaMin = min(c[i]*1000)-5
            thetaMax = max(c[i]*1000)+5
            ax.set_thetamin(thetaMin)
            ax.set_thetamax(thetaMax)  
            color=plotAngle  
            ax.scatter(plotAngle, [m for m in np.arange(1,2.2,1.2/(self.cycle-1))], c=color, cmap='cool', alpha=0.75)
            titlePlot = 'C'
            ax.set_title(titlePlot)
        plt.show()