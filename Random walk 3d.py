#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 15:24:15 2021

@author: fernandosangerman
"""

import numpy as np
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
def caminataA(N,L):
    Estado=np.zeros(N)
    Px=np.zeros(N)
    Py=np.zeros(N)
    Pz=np.zeros(N)
    Px[0]=np.random.uniform(-1,1)*L
    Py[0]=np.random.uniform(-1,1)*L
    Pz[0]=np.random.uniform(-1,1)*L
    for steps in range(1,N):
        rn=np.random.uniform(0,1)
        if rn>0 and rn<1/6:
            Px[steps]=Px[steps-1]+L
            Py[steps]=Py[steps-1]
            Pz[steps]=Pz[steps-1]
            Estado[steps-1]=0
        elif rn>1/6 and rn<2/6:
            Py[steps]=Py[steps-1]+L
            Px[steps]=Px[steps-1]
            Pz[steps]=Pz[steps-1]
            Estado[steps-1]=1
        elif rn>2/6 and rn<3/6:
            Px[steps]=Px[steps-1]-L
            Py[steps]=Py[steps-1]
            Pz[steps]=Pz[steps-1]
            Estado[steps-1]=2
        elif rn>3/6 and rn<4/6:
            Py[steps]=Py[steps-1]-L 
            Px[steps]=Px[steps-1]
            Pz[steps]=Pz[steps-1]
            Estado[steps-1]=3
        elif rn>4/6 and rn<5/6:
             Pz[steps]=Pz[steps-1]+L 
             Py[steps]=Py[steps-1]
             Px[steps]=Px[steps-1]
             
             Estado[steps-1]=4
        else:
            Pz[steps]=Pz[steps-1]-L
            Py[steps]=Py[steps-1]
            Px[steps]=Px[steps-1]
        
            Estado[steps-1]=5
                
        
    P=[Px,Py,Pz,Estado]
    
    return P

N=100
L=2
Posiciones=caminataA(N,L)
ax.plot(Posiciones[0],Posiciones[1],Posiciones[2])
ax.show