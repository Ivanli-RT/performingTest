import os
import math
import numpy as np
import pandas as pd
import data_read
import spatial_methods
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt

class circleB_accuracy_repearability():
    def __init__(self, frequency, section, numbers):
        self.frequency = frequency
        self.section = section
        self.numbers = numbers
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
        #理论圆轨迹目录
        for fileName in os.listdir(path):
            if fileName == '理论点大圆.txt':
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
        #计算理论圆心
        #差分
        A = np.array(pd.DataFrame(instruction, index=range(len(instruction))).diff())[1:]
        n = np.cross(A[0],A[1])
        A = np.r_[A,[n]]
        #如果n是0向量，表示三点共线
        if (n == np.zeros(3)).all():
            r = open(self.pathResult, 'a+')
            r.truncate(0)
            r.write('***大圆轨迹准确度和大圆轨迹重复性***\n')
            r.write('理论点位三点共线，不是圆；')
            r.flush()
            r.close()
            ref = open(self.refreshPath, 'a+')
            ref.truncate(0)
            ref.write('1')
            ref.flush()
            ref.close()
            return None
        #根据三点坐标求得三点所在平面的方程
        #外接圆心到各点距离相等，以此建立方程
        B = [sum(np.array(pd.DataFrame(instruction**2, index=range(len(instruction))).diff())[2])/2]
        B.append(n.dot(instruction[0]))
        B.insert(0,0.0)
        cc = np.linalg.lstsq(A, np.array(B), rcond=None)[0]
        #最终结果cc(1)，cc(2)，cc(3)为圆心的x，y，z坐标
        r = np.linalg.norm(cc-instruction[0])
        #求圆弧的夹角
        theta = math.acos(np.dot(instruction[0]-cc, instruction[-1]-cc)/(np.linalg.norm(instruction[0]-cc)*np.linalg.norm(instruction[-1]-cc)))
        thetas = 2*math.pi-theta
        #单位化的向量 
        a = (instruction[0]-cc)/r
        b = (instruction[-1] - cc - r*a*math.cos(thetas))/(r*math.sin(thetas))
        # #等分面的角度从0到thetas
        theta = [thetas*m/(self.section+1) for m in range(self.section+2)]
        #求圆上各点的xyz坐标
        commandArcPoint = np.array([cc+r*a*math.cos(theta[m])+r*b*math.sin(theta[m]) for m in range(self.section+2)])
        commandArcPoint = np.delete(commandArcPoint,[0,-1],axis=0)
        #计算正交平面
        normal_vector1 = np.cross((commandArcPoint[0]-commandArcPoint[2]), (commandArcPoint[1]-cc))
        normal_vector2 = np.array([np.cross(normal_vector1, commandArcPoint[m]-cc) for m in range(self.section)])
        commandArcPlane = [[normal_vector2[m], -np.dot(normal_vector2[m], cc)] for m in range(self.section)]
        #截屏面上的点
        newXYZ = {}
        sampleArcPoint = {}
        for i in range(self.section):
            normN = commandArcPlane[i][0]
            normU = [commandArcPlane[i][0][1], -commandArcPlane[i][0][0], 0]
            normV = np.cross(normN, normU)
            vectorU = normU/np.linalg.norm(normU)
            vectorV = normV/np.linalg.norm(normV)
            normR = 3
            newXYZ[i] = np.array([commandArcPoint[i]+normR*(vectorU*math.cos(m)+vectorV*math.sin(m)) for m in np.arange(0,2*np.pi+np.pi/20,np.pi/20)])
            #正交面
            sampleArcPoint[i] = []    
            for j in range(self.numbers):
                #筛选测试点，若大于半径则在计算中剔除
                points = [ls[j][m] for m in range(len(ls[j])) if np.linalg.norm(ls[j][m]-commandArcPoint[i]) < r]
                #计算与平面的交点
                cal = spatial_methods.spatialMethod(commandArcPlane[i][0], points, commandArcPlane[i][1])
                sampleArcPoint[i].append(cal.points2planeMin())
        #找出等分面与对应点连线的交点作为每组数据的实测点
        #输入：平面法向量和点，实测两点,commandArcPlane\commandLinePoint\sampleArcPoint{i}(p,j)\sampleArcPoint{i}(n_group+p,j)
        #输出：平面与直线的交点。输出量为6*1向量,sampleArcInterP
        sampleArcInterP = {}
        for i in range(self.section):
            sampleArcInterP[i] = []
            for j in range(self.numbers):
                lineVector = sampleArcPoint[i][j][0] - sampleArcPoint[i][j][1]
                #直线向量与平面向量的点积
                vpt = lineVector.dot(commandArcPlane[i][0])
                #求出中间系数
                t = commandArcPlane[i][0].dot(commandArcPoint[i] - sampleArcPoint[i][j][0]) / vpt
                #返回交点位置坐标
                sampleArcInterP[i].append(sampleArcPoint[i][j][0]+lineVector*t)
            sampleArcInterP[i] = np.array(sampleArcInterP[i])
        '''
        根据标准进行轨迹准确度与轨迹重复性的计算
        '''
        #截面上的平均点位
        sampleAve = [sum(sampleArcInterP[m])/self.numbers for m in range(self.section)]
        #计算轨迹位置准确度，ATP
        ATpAll = [np.linalg.norm(sampleAve[m]-commandArcPoint[m]) for m in range(self.section)]
        ATp = max(enumerate(ATpAll), key=lambda x: x[1])
        #计算轨迹位置重复性，RTp
        lSampleData = {}
        lSampleAve = []
        for i in range(self.section):
            lSampleData[i] = [np.linalg.norm(sampleArcInterP[i][m]-sampleAve[i]) for m in range(self.numbers)]
            lSampleAve.append(sum(lSampleData[i])/self.numbers)
        Sl = [math.sqrt(sum((lSampleData[m]-lSampleAve[m])**2)/(self.numbers-1)) for m in range(self.section)]    
        RTpAll = [lSampleAve[m]+3*Sl[m] for m in range(self.section)]
        RTp = max(enumerate(RTpAll), key=lambda x: x[1])
        
        #将结果写入文件
        r = open(self.pathResult, 'a+')
        r.truncate(0)
        r.write('***大圆轨迹准确度和大圆轨迹重复性***\n')
        r.write('大圆轨迹准确度为：%.4fmm，在第%d个平面；\n大圆轨迹重复性为：%.4fmm，在第%d个平面；'
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
        fig.suptitle('大圆轨迹准确度', fontsize=16)
        # 准确度最大处    
        X = newXYZ[ATp[0]][:,0]
        Y = newXYZ[ATp[0]][:,1]
        X, Y = np.meshgrid(X, Y)    # x-y 平面的网格
        Z = (-commandArcPlane[ATp[0]][0][0]*X + -commandArcPlane[ATp[0]][0][1]*Y + commandArcPlane[ATp[0]][0].dot(newXYZ[ATp[0]][0])) / commandArcPlane[ATp[0]][0][2] #+ D
        ax = fig.add_subplot(1, 2, 1, projection='3d')
        ax.plot_surface(X, Y, Z, color='lightyellow', alpha=0.3)
        ax.scatter(commandArcPoint[ATp[0]][0], commandArcPoint[ATp[0]][1], commandArcPoint[ATp[0]][2], s=40, marker='x', color='purple', label='instruction')
        ax.scatter(sampleAve[ATp[0]][0], sampleAve[ATp[0]][1], sampleAve[ATp[0]][2], s=40, marker='o', color='red', label='avePoints')   
        ax.set_title('轨迹准确度最大处')
        #重复性最大处
        ax = fig.add_subplot(1, 2, 2, projection='3d')
        ax.scatter(sampleAve[RTp[0]][0], sampleAve[RTp[0]][1], sampleAve[RTp[0]][2], s=40, marker='o', color='red', label='avePoints')
        ax.scatter(sampleArcInterP[RTp[0]][:, 0], sampleArcInterP[RTp[0]][:, 1], sampleArcInterP[RTp[0]][:, 2], s=20, marker='o', color='cyan', label='Points')
        ax.set_title('轨迹重复性最大处')
        plt.show()