from tkinter import *
import os
import math
import csv
import data_read
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter

class distance_ar():
    def __init__(self, cycle, pose, angle):
        self.cycle = int(cycle)
        self.pose = int(pose)
        self.angle = angle
        self.dataPath = r'.\fileSelect.txt'
        self.refreshPath = r'.\refreshd.txt'
        self.pathResult = r'.\result.txt'

    def calculate(self):
        #读取待处理数据目录
        with open(self.dataPath, 'r') as ff:
            path = ff.read()
        #判断是否有姿态
        if self.angle == True:    #有姿态
            #确定子图的布局
            figColumn = 4
            figRows = 1
            #画图
            fig = plt.figure(figsize=(12,3))
            fig.subplots_adjust(hspace=0.5, wspace=0.5)
            fig.suptitle('距离准确度重复性(带姿态)', fontsize=16)
            #读取数据
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
            for i in range(2):
                posePoint[i] = np.array([points[m] for m in range(len(points)) if m%self.pose==i ])
                a[i] = np.array([aa[m] for m in range(len(aa)) if m%self.pose==i ])
                b[i] = np.array([ba[m] for m in range(len(ba)) if m%self.pose==i ])
                c[i] = np.array([ca[m] for m in range(len(ca)) if m%self.pose==i ])
            #读取指令点
            filePath = os.path.split(path)
            insPath = filePath[-2] + '\指令点.txt'
            dataIns = data_read.dataRead(insPath)
            dataIns.txtRead()
            insPoints = dataIns.data[:,0:3]
            insA = dataIns.data[:,3]
            insB = dataIns.data[:,4]
            insC = dataIns.data[:,5]
            #计算指令距离
            Dcxyz = np.linalg.norm(insPoints[0]-insPoints[1])
            Dca = abs(insA[0]-insA[1])
            Dcb = abs(insB[0]-insB[1])
            Dcc = abs(insC[0]-insC[1])
            #计算每次测量的距离
            D = [np.linalg.norm(posePoint[0][m]-posePoint[1][m]) for m in range(self.cycle)]
            Da = [np.linalg.norm(a[0][m]-a[1][m]) for m in range(self.cycle)]
            Db = [np.linalg.norm(b[0][m]-b[1][m]) for m in range(self.cycle)]
            Dc = [np.linalg.norm(c[0][m]-c[1][m]) for m in range(self.cycle)]
            #计算平均值
            DAve = sum(D) / self.cycle
            DA = sum(Da) / self.cycle
            DB = sum(Db) / self.cycle
            DC = sum(Dc) / self.cycle
            #准确度
            ADp = DAve - Dcxyz
            Aa = DA - Dca
            Ab = DB - Dcb
            Ac = DC - Dcc
            #重复性
            RD = 3*math.sqrt(sum((D-DAve)**2)/(self.cycle-1))
            RDa = 3*math.sqrt(sum((Da-DA)**2)/(self.cycle-1))
            RDb = 3*math.sqrt(sum((Db-DB)**2)/(self.cycle-1))
            RDc = 3*math.sqrt(sum((Dc-DC)**2)/(self.cycle-1))
            #输出结果
            r = open(self.pathResult, 'a+')
            r.truncate(0)
            r.write('***距离准确度和距离重复性(有姿态)***\n')
            r.write('距离准确度为%.4fmm，%.4f°，%.4f°，%.4f°；\n'
                    '距离重复性为：±%.4fmm，±%.4f°，±%.4f°，±%.4f°；'
                    % (ADp, Aa, Ab, Ac,
                       RD, RDa, RDb, RDc))
            r.flush()
            r.close()
            ref = open(self.refreshPath, 'a+')
            ref.truncate(0)
            ref.write('1')
            ref.flush()
            ref.close()
            #xyz
            ax = fig.add_subplot(figRows, figColumn, 1)
            ax.plot([m for m in range(1,31)], D, c='blue')
            ax.hlines(DAve, 0, 30, colors='red', linestyle="--")
            ax.set_xlabel('测量次数')
            ax.set_ylabel('距离(mm)')
            titlePlot = '点位距离'
            ax.set_title(titlePlot)
            #A
            ax = fig.add_subplot(figRows, figColumn, 2)
            ax.plot([m for m in range(1,31)], Da, c='blue')
            ax.hlines(DA, 0, 30, colors='red', linestyle="--")
            titlePlot = 'A'
            ax.set_title(titlePlot)
            #B
            ax = fig.add_subplot(figRows, figColumn, 3)
            ax.plot([m for m in range(1,31)], Db, c='blue')
            ax.hlines(DB, 0, 30, colors='red', linestyle="--")
            titlePlot = 'B'
            ax.set_title(titlePlot)
            #C
            ax = fig.add_subplot(figRows, figColumn, 4)
            ax.plot([m for m in range(1,31)], Dc, c='blue')
            ax.hlines(DC, 0, 30, colors='red', linestyle="--")
            titlePlot = 'C'
            ax.set_title(titlePlot)
        elif self.angle == False:
            #读取测试数据
            dataTest = data_read.dataRead(path)
            dataTest.txtRead()
            points = dataTest.data
            #按照点位将测量结果分开
            posePoint = {}
            for i in range(self.pose):
                posePoint[i] = np.array([points[m] for m in range(len(points)) if m%self.pose==i ])
            #读取指令点
            filePath = os.path.split(path)
            insPath = filePath[-2] + '\指令点.txt'
            dataIns = data_read.dataRead(insPath)
            dataIns.txtRead()
            insPoints = dataIns.data
            #计算指令距离
            Dcxyz = np.linalg.norm(insPoints[0]-insPoints[1])
            #计算每次测量的距离
            D = [np.linalg.norm(posePoint[0][m]-posePoint[1][m]) for m in range(self.cycle)]
            #计算平均值
            DAve = sum(D) / self.cycle
            #准确度
            ADp = DAve - Dcxyz
            #重复性
            RD = 3*math.sqrt(sum((D-DAve)**2)/(self.cycle-1))
            # 输出结果
            r = open(self.pathResult, 'a+')
            r.truncate(0)
            r.write('***距离准确度和距离重复性***\n')
            r.write('距离准确度为%.4fmm；\n'
                    '距离重复性为：±%.4fmm；'
                    % (ADp, RD))
            r.flush()
            r.close()
            ref = open(self.refreshPath, 'a+')
            ref.truncate(0)
            ref.write('1')
            ref.flush()
            ref.close()
            #确定子图的布局
            #画图
            plt.figure()
            plt.title('距离准确度重复性', fontsize=16)
            plt.plot([m for m in range(1,31)], D, c='blue')
            plt.hlines(DAve, 0, 30, colors='red', linestyle="--")
            plt.xlabel('测量次数')
            plt.ylabel('距离(mm)')
            plt.axis()
            plt.grid()
        plt.show()

