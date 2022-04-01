import numpy as np
import math

class spatialMethod():
    def __init__(self, normal_vector, points,planeD):
        self.normal_vector = normal_vector
        self.points = points
        self.planeD = planeD
        
    #求点云轨迹与某一截平面距离最近的两个点
    def points2planeMin(self):
        k = len(self.points)
        D = [abs(self.normal_vector.dot(self.points[m])+self.planeD)/math.sqrt(self.normal_vector.dot(self.normal_vector)) for m in range(k)]
        B = sorted(enumerate(D), key=lambda x: x[1])
        pointsInter = np.array([self.points[B[0][0]-1], self.points[B[0][0]], self.points[B[0][0]+1]])
        #计算距离最小的3个点在面上的投影点
        ptoPlane = (pointsInter.dot(self.normal_vector)+self.planeD)/self.normal_vector.dot(self.normal_vector)
        #计算两向量之间的夹角
        vector = (np.mat(ptoPlane).T*-self.normal_vector).getA()
        cos21 = vector[1].dot(vector[0]) / np.linalg.norm(vector[1]) / np.linalg.norm(vector[0])
        cos23 = vector[1].dot(vector[2]) / np.linalg.norm(vector[1]) / np.linalg.norm(vector[2])
        #如果第二最小夹角余弦等于-1，则符合，否则，判断下一点
        if cos21 <= 0:
            Q2 = pointsInter[0]
        else:
            Q2 = pointsInter[2]
        return [pointsInter[1], Q2]