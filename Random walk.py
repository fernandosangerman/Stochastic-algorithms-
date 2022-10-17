#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 18:54:58 2021

@author: fernandosangerman
"""

import numpy as np
import matplotlib.pyplot as plt 
def caminataAG(N,L,res):
    
    Estado=np.zeros(N)
    Px=np.zeros(N)
    Py=np.zeros(N)
    Px[0]=0
    Py[0]=0
    steps=0
    iteraciones=0
    coincidencias=np.zeros(N)
    while steps<N:
        rn=np.random.uniform(0,1)
        if rn>0 and rn<0.25:
            Px[steps]=Px[steps-1]+L
            Py[steps]=Py[steps-1]
            Estado[steps-1]=0
           
        elif rn>0.25 and rn<0.5:
            Py[steps]=Py[steps-1]+L
            Px[steps]=Px[steps-1]
            Estado[steps-1]=1
            
        elif rn>0.5 and rn<0.75:
            Px[steps]=Px[steps-1]-L
            Py[steps]=Py[steps-1]
            Estado[steps-1]=2
        elif rn>0.75 and rn<1:
            Py[steps]=Py[steps-1]-L 
            Px[steps]=Px[steps-1]
            Estado[steps-1]=3
        
            
        for i in range(steps):
            if np.round(Px[steps],res)==np.round(Px[i],res) and np.round(Py[steps],res)==np.round(Py[i],res): 
                coincidencias[steps]=coincidencias[steps]+1
                steps=steps-1
                
            
            
        steps=steps+1
        iteraciones=iteraciones+1
        if coincidencias[steps]>2000:
            break
         
            
    Px=Px[0:steps+1] 
    Py=Py[0:steps+1]
    coincidencias=coincidencias[0:steps+1]
    P=[Px,Py,coincidencias]
    
    return P

N=10000
L=3
R=5
Posiciones=caminataAG(N,L,R)
Est=Posiciones[2]
plt.plot(Posiciones[0],Posiciones[1])
plt.show