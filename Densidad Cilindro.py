#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 11:57:08 2021

@author: fernandosangerman
"""
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
#Genere una funcion que regresa x,y,z,r y toma como argumento el numero de muestras deseadas
#para esto use la integral de volumen del cilindro la cual use para generar una funcion CDF
#la cual despeje para sacar muestras de radio,theta y z con numeros aleatorios, despues estas las
#pase a coordenadas cartesianas.
def cilindro(N):
    r0=0.5
    h=1
    r=np.zeros(N)
    the=np.zeros(N)
    z=np.zeros(N)
    for n in range(N):
        randr=np.random.uniform(0,1)
        r[n]=r0*np.sqrt(randr)
        randthe=np.random.uniform(0,1)
        the[n]=2*np.pi*randthe
        randz=np.random.uniform(0,1)
        z[n]=h*randz-h/2
    x=r*np.cos(the)
    y=r*np.sin(the)
    Muestras=[x,y,z,r]
    return Muestras
r0=0.5
N=1000
M=cilindro(N)
fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")
ax.scatter3D(M[0], M[1], M[2], color = "green")
plt.show()
#Aqui para obtener la densidad lineal me voy muestra por muestra en un for que adentro de este
#mismo tiene un for que analiza a que rango de r pertenece la muestra, cuando lo encuentra se suma 1
#al numero de muestras en ese rango y se rompe el for para seguir a la siguiente muestra.
Nr=100
dr=r0/Nr
r=M[3]
Ld=np.zeros(Nr)
for m in range(N):
    for l in range(Nr):
        if r[m]>l*dr and r[m]<(l+1)*dr:
            Ld[l]=Ld[l]+1
            break
        else:
            continue
#Aa lo utilice para calcular la densidad pues es uno sobre el area del aillo asu qye solo lo 
#multiplique por Ld
Aa=[1/(np.pi*(t*dr+dr)**2-np.pi*(t*dr)**2) for t in range(Nr)]
Ld=Ld*Aa

plt.title("Densidad Lineal")          
plt.plot(range(Nr),Ld)
plt.show

plt.title("X contra Y") 
plt.scatter(M[0],M[1]) 
plt.show            
plt.title("Z contra r")
plt.scatter(M[2],M[3]) 
plt.show()
        
        
            
    