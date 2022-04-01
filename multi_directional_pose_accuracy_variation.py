from tkinter import *
import os
import math
import csv
import data_read
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt

class md_pose_av():
    def __init__(self, cycle, pose, angle):
        self.cycle = cycle
        self.pose = pose
        self.angle = angle
        self.dataPath = r'.\fileSelect.txt'
        self.refreshPath = r'.\refreshd.txt'
        self.pathResult = r'.\result.txt'

    def calculate(self):
        #读取待处理数据
        with open(self.dataPath, 'r') as ff:
            path = ff.read()
        #判断是否有姿态
        if self.angle == True:    #有姿态
            #确定子图的布局
            figColumn = 4
            figRows = self.pose
            #画图
            fig = plt.figure(figsize=(12,10))
            fig.subplots_adjust(hspace=0.5, wspace=0.5)
            fig.suptitle('多方位位姿准确度点位姿态分布(角度放大1000倍)', fontsize=16)
            #读取测试数据
            dataTest = data_read.dataRead(path)
            dataTest.csvread()
            vAPp = []
            vAPa = []
            vAPb = []
            vAPc = []
            #按照点位将测量结果分开
            for i in range(self.pose):
                #按照点位将测试结果分开
                tempPoints = dataTest.data['pose'][i*self.cycle*3:i*self.cycle*3+self.cycle*3]
                tempA = dataTest.data['a'][i*self.cycle*3:i*self.cycle*3+self.cycle*3]
                tempB = dataTest.data['b'][i*self.cycle*3:i*self.cycle*3+self.cycle*3]
                tempC = dataTest.data['c'][i*self.cycle*3:i*self.cycle*3+self.cycle*3]
                #按照到位方向将测试结果分开
                posePoint = {}
                a = {}
                b = {}
                c = {}
                for key, value in {'x':0, 'y':1, 'z':2}.items():
                    posePoint[key] = np.array([tempPoints[m] for m in range(len(tempPoints)) if m%3==value])
                    a[key] = np.array([tempA[m] for m in range(len(tempA)) if m%3==value])
                    b[key] = np.array([tempB[m] for m in range(len(tempB)) if m%3==value])
                    c[key] = np.array([tempC[m] for m in range(len(tempC)) if m%3==value])
                #计算各方向点位和姿态的平均值
                poseAve = [sum(posePoint[m])/self.cycle for m in 'xyz']
                aAve = [sum(a[m])/self.cycle for m in 'xyz']
                bAve = [sum(b[m])/self.cycle for m in 'xyz']
                cAve = [sum(c[m])/self.cycle for m in 'xyz']
                vAp = [np.linalg.norm(poseAve[m]-poseAve[n]) for m in range(3) for n in range(3)]
                vAa = [np.linalg.norm(aAve[m]-aAve[n]) for m in range(3) for n in range(3)]
                vAb = [np.linalg.norm(bAve[m]-bAve[n]) for m in range(3) for n in range(3)]
                vAc = [np.linalg.norm(cAve[m]-cAve[n]) for m in range(3) for n in range(3)]
                vAPp.append(max(vAp))
                vAPa.append(max(vAa))
                vAPb.append(max(vAb))
                vAPc.append(max(vAc))
                #xyz
                ax = fig.add_subplot(figRows, figColumn, i*4+1, projection='3d')
                ax.scatter(posePoint['x'][:,0], posePoint['x'][:,1], posePoint['x'][:,2], s=20, marker='o', color='springgreen', label='x')
                ax.scatter(posePoint['y'][:,0], posePoint['y'][:,1], posePoint['y'][:,2], s=20, marker='o', color='cyan', label='y')
                ax.scatter(posePoint['z'][:,0], posePoint['z'][:,1], posePoint['z'][:,2], s=20, marker='o', color='pink', label='z')
                ax.scatter(poseAve[0][0], poseAve[0][1], poseAve[0][2], s=40, marker='x', color='forestgreen', label='xAve')
                ax.scatter(poseAve[1][0], poseAve[1][1], poseAve[1][2], s=40, marker='x', color='blue', label='yAve')
                ax.scatter(poseAve[2][0], poseAve[2][1], poseAve[2][2], s=40, marker='x', color='hotpink', label='zAve')
                titlePlot = 'P' + str(i+1)
                ax.set_title(titlePlot)
                #A
                ax = fig.add_subplot(figRows, figColumn, i*4+2, projection='polar')
                ax.set_rlim(0.5, 2.3)           
                thetaMin = min(tempA*1000)-5
                thetaMax = max(tempA*1000)+5
                ax.set_thetamin(thetaMin)
                ax.set_thetamax(thetaMax)  
                ax.scatter(a['x']*1000/180*np.pi, [m*2 for m in np.ones(self.cycle)], c='springgreen', cmap='cool', alpha=0.75)
                ax.scatter(a['y']*1000/180*np.pi, [m*2 for m in np.ones(self.cycle)], c='cyan', cmap='cool', alpha=0.75)
                ax.scatter(a['z']*1000/180*np.pi, [m*2 for m in np.ones(self.cycle)], c='pink', cmap='cool', alpha=0.75)
                titlePlot = 'A'
                ax.set_title(titlePlot)
                #B
                ax = fig.add_subplot(figRows, figColumn, i*4+3, projection='polar')
                ax.set_rlim(0.5, 2.3)           
                thetaMin = min(tempB*1000)-5
                thetaMax = max(tempB*1000)+5
                ax.set_thetamin(thetaMin)
                ax.set_thetamax(thetaMax)  
                ax.scatter(b['x']*1000/180*np.pi, [m*2 for m in np.ones(self.cycle)], c='springgreen', cmap='cool', alpha=0.75)
                ax.scatter(b['y']*1000/180*np.pi, [m*2 for m in np.ones(self.cycle)], c='cyan', cmap='cool', alpha=0.75)
                ax.scatter(b['z']*1000/180*np.pi, [m*2 for m in np.ones(self.cycle)], c='pink', cmap='cool', alpha=0.75)
                titlePlot = 'B'
                ax.set_title(titlePlot)
                #C
                ax = fig.add_subplot(figRows, figColumn, i*4+4, projection='polar')
                ax.set_rlim(0.5, 2.3)           
                thetaMin = min(tempC*1000)-5
                thetaMax = max(tempC*1000)+5
                ax.set_thetamin(thetaMin)
                ax.set_thetamax(thetaMax)  
                ax.scatter(c['x']*1000/180*np.pi, [m*2 for m in np.ones(self.cycle)], c='springgreen', cmap='cool', alpha=0.75)
                ax.scatter(c['y']*1000/180*np.pi, [m*2 for m in np.ones(self.cycle)], c='cyan', cmap='cool', alpha=0.75)
                ax.scatter(c['z']*1000/180*np.pi, [m*2 for m in np.ones(self.cycle)], c='pink', cmap='cool', alpha=0.75)
                titlePlot = 'C'
                ax.set_title(titlePlot)
            #输出结果
            r = open(self.pathResult, 'a+')
            r.truncate(0)
            r.write('***多方位位姿准确度变动***\n')
            for i in range(self.pose):
                r.write('点位%d的多方位位姿准确度变动为：'
                        'xyz:%.4fmm，a:%.4f°，b:%.4f°，c:%.4f°;\n'
                        % (i+1, vAPp[i], vAPa[i], vAPb[i], vAPc[i]))
            r.flush()
            r.close()
            ref = open(self.refreshPath, 'a+')
            ref.truncate(0)
            ref.write('1')
            ref.flush()
            ref.close()
        else:
            #读取测试数据
            dataTest = data_read.dataRead(path)
            dataTest.txtRead()
            vAPp = []
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
            fig = plt.figure(figsize=(12,3))
            fig.subplots_adjust(hspace=0.5, wspace=0.5)
            fig.suptitle('多方位位置准确度点位分布', fontsize=16)
            #按照点位将测量结果分开
            for i in range(self.pose):
                #按照点位将测试结果分开
                tempPoints = dataTest.data[i*self.cycle*3:i*self.cycle*3+self.cycle*3]
                #按照到位方向将测试结果分开
                posePoint = {}
                for key, value in {'x':0, 'y':1, 'z':2}.items():
                    posePoint[key] = np.array([tempPoints[m] for m in range(len(tempPoints)) if m%3==value])
                #计算各方向点位和姿态的平均值
                poseAve = [sum(posePoint[m])/self.cycle for m in 'xyz']
                vAp = [np.linalg.norm(poseAve[m]-poseAve[n]) for m in range(3) for n in range(3)]
                vAPp.append(max(vAp))
                #xyz
                ax = fig.add_subplot(figRows, figColumn, i+1, projection='3d')
                ax.scatter(posePoint['x'][:,0], posePoint['x'][:,1], posePoint['x'][:,2], s=20, marker='o', color='springgreen', label='x')
                ax.scatter(posePoint['y'][:,0], posePoint['y'][:,1], posePoint['y'][:,2], s=20, marker='o', color='cyan', label='y')
                ax.scatter(posePoint['z'][:,0], posePoint['z'][:,1], posePoint['z'][:,2], s=20, marker='o', color='pink', label='z')
                ax.scatter(poseAve[0][0], poseAve[0][1], poseAve[0][2], s=40, marker='x', color='forestgreen', label='xAve')
                ax.scatter(poseAve[1][0], poseAve[1][1], poseAve[1][2], s=40, marker='x', color='blue', label='yAve')
                ax.scatter(poseAve[2][0], poseAve[2][1], poseAve[2][2], s=40, marker='x', color='hotpink', label='zAve')
                titlePlot = 'P' + str(i+1)
                ax.set_title(titlePlot)
            #输出结果
            r = open(self.pathResult, 'a+')
            r.truncate(0)
            r.write('***多方位位姿准确度变动***\n')
            for i in range(self.pose):
                r.write('点位%d的多方位位置准确度变动为：'
                        'xyz:%.4fmm;\n'
                        % (i+1, vAPp[i]))
            r.flush()
            r.close()
            ref = open(self.refreshPath, 'a+')
            ref.truncate(0)
            ref.write('1')
            ref.flush()
            ref.close()

        plt.show()