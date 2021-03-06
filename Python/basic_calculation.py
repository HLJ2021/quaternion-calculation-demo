# -*- coding: utf-8 -*-
"""
Demo code for basic quaternion calculation

Created on Wed Jul  4 10:13:01 2018

@author: mahao
"""

import math
import numpy as np
from numpy import linalg as la
from transforms3d import quaternions as quat
from transforms3d import euler

def R2D(rad):
    return rad / math.pi * 180.0

def D2R(deg):
    return deg * math.pi / 180.0

### Quaternion calculation notes ###
     
# Define three coordinate systems (CS):
# A: x - East, y - North, z - Up
# B: x - West, y - South, z - Up   (A rotate around its z axis with 180 degree)
# C: x - Down, y - North, z - East (A rotate around its y axis with 90  degree)
    
# 1. Quaternion construction
# Rotation from A to B:
r1_A = np.array([0.0, 0.0, 1.0])  # rotation axis: z axis of A  
theta1 = D2R(180.0)  # rotation angle (following right-hand rule)

# Rotation from A to C:
r2_A = np.array([0.0, 1.0, 0.0])  # rotaion axis: y axis of A
theta2 = D2R(90.0)  # rotation angle (following right-hand rule)

#q_A_B = np.array([math.cos(theta1/2.0), -math.sin(theta1/2.0)*r1_A[0], -math.sin(theta1/2.0)*r1_A[1], -math.sin(theta1/2.0)*r1_A[2]])
#q_A_C = np.array([math.cos(theta2/2.0), -math.sin(theta2/2.0)*r2_A[0], -math.sin(theta2/2.0)*r2_A[1], -math.sin(theta2/2.0)*r2_A[2]])
q_A_B = quat.axangle2quat(r1_A, -theta1)
q_A_C = quat.axangle2quat(r2_A, -theta2)
print("q_A_B: ")
print(q_A_B)
print("q_A_C: ")
print(q_A_C)

# 2. Vector coordinate transformation
xA_A = np.array([1.0, 0.0, 0.0])    # A's x axis in A
xA_B = quat.rotate_vector(xA_A, q_A_B)  # A's x axis in B
xA_C = quat.rotate_vector(xA_A, q_A_C)  # A's x axis in C
print("xA_B: ")
print(xA_B)
print("xA_C: ")
print(xA_C)

q_B_C = quat.qmult(q_A_C, quat.qinverse(q_A_B))
xB_B = np.array([1.0, 0.0, 0.0])   # B's x axis in B
xB_C = quat.rotate_vector(xB_B, q_B_C)  # B's x axis in C
print("q_B_C: ")
print(q_B_C)
print("xB_C: ")
print(xB_C)

# 3. Quatrenion and rotational matrix conversion
M_A_B_1 = quat.quat2mat(q_A_B)
M_A_B_2 = np.eye(3)
yA_B = np.array([0.0, -1.0, 0.0])
zA_B = np.array([0.0, 0.0, 1.0])
M_A_B_2[:,0] = xA_B
M_A_B_2[:,1] = yA_B
M_A_B_2[:,2] = zA_B
M_A_B = M_A_B_1
print("M_A_B: ")
print(M_A_B_1)
print(M_A_B_2)

M_A_C_1 = quat.quat2mat(q_A_C)
M_A_C_2 = np.eye(3)
yA_C = np.array([0.0, 1.0, 0.0])
zA_C = np.array([-1.0, 0.0, 0.0])
M_A_C_2[:,0] = xA_C
M_A_C_2[:,1] = yA_C
M_A_C_2[:,2] = zA_C
M_A_C = M_A_C_1
print("M_A_C: ")
print(M_A_C_1)
print(M_A_C_2)

M_B_C_1 = M_A_C.dot(M_A_B.T);
M_B_C_2 = np.eye(3)
yB_C = np.array([0.0, -1.0, 0.0]);
zB_C = np.array([-1.0, 0.0, 0.0]);
M_B_C_2[:,0] = xB_C
M_B_C_2[:,1] = yB_C
M_B_C_2[:,2] = zB_C
M_B_C = M_B_C_1
print("M_B_C: ")
print(M_B_C_1)
print(M_B_C_2)

# 4. Quaternion/Rotational matrix and Euler angle conversion
alpha = D2R(0.0)  # rotation angle around x axis
beta = D2R(90.0)  # rotation angle around y axis
gamma = D2R(180.0)  # rotation angle around z axis
M_B_C_3 = np.eye(3)
M_B_C_3 = euler.euler2mat(gamma, beta, alpha, 'szyx')
print("M_B_C: ")
print(M_B_C_3)
euler_angles = euler.mat2euler(M_B_C_3, 'szyx')
print("euler angles in ZYZ order: ")
print(R2D(gamma), R2D(beta), R2D(alpha))
print([R2D(angle) for angle in euler_angles])

