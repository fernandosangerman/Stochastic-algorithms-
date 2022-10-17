#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 09:14:33 2021

@author: fernandosangerman
"""

import numpy as np
import matplotlib.pyplot as plt

with  open("/Users/fernandosangerman/Documents/Septimo/Fiscomp2/Tarea 4/mock_data.txt", "r") as f:
   
    data=f.readlines()

#Cada elemento separado por tab (\t) en una lista
R=np.array([]); vc=np.array([]); v_error=np.array([])
for line in data[1:]: #El primer elemento son los encabezados, los quitamos
    line=line.replace("\n","") #Quitamos los string enter (\n)
    lineinlist=line.split(" ") #Convierte str en una lista
    #Convertimos todo a float, originalmente tenemos los numeros en string
    fvals=[float(x) for x in lineinlist]
    R=np.append(R, [fvals[0]]); 
    vc=np.append(vc, [fvals[1]])
    v_error=np.append(v_error, [fvals[2]])
    
#Funcion que calcula chi^2
def chi2(R,vc,v_error,P):
    #Inputs:
    #R(Array) Datos de la distancia del centro hasta el gas
    #vc(Array) Datos de la velocidad de rotación del gas
    #v_error(Array) Datos del error estandar
    #P(Array) Predicciones de V0 y Rc
    #Outputs:
    #chi^2 de las V0 y Rc de la iteración
    n=len(R)
    x=0
    for i in range(n):
        #Este if lo puse para evitar las divisiones entre cero pues el 
        #primer termino del array R es cero y aveces en las N iteraciones
        #P[1] llega a ser cero asi que lo cambio por un valor cercano a cero
        if P[1]**2<0.01:
            P[1]=0.01
        m=P[0]*R[i]/np.sqrt(P[1]**2+R[i]**2)            
        x=x+((vc[i]-m)/v_error[i])**2        
    return x
#Función de optimización
def mle(R,v_error,vc,N):
    #Inputs:
    #R(Array) Datos de la distancia del centro hasta el gas
    #vc(Array) Datos de la velocidad de rotación del gas
    #v_error(Array) Datos del error estandar
    #P(Array) Predicciones de V0 y Rc
    #N(int) Numero de iteraciones
    #Outputs:
    #x1(Array) Chi^2 de cada iteración
    #Rechazos(int) Numero de veces que no se cumplio el criterio de aceptación
    #P(array) P[:,0] Prediccion de V0 de cada iteracion, P[:,1] Prediccion de Rc de cada iteración
    PE=np.zeros([N,2]) # [V0,Rc]
    
    PE[0,:]=[200,2] #Valores iniciales de V0 y Rc                  
    P=np.array(PE) #convierto la lista en array
    
    x1=np.ones(N) #genero el vector donde guardare las chi^2
    
    x1[0]=chi2(R,vc,v_error,P[0,:]) #Calculo la primera chi^2
    
    rechazos=0
    for j in range(N-1):
        #copio los puntos de la iteracion para poder alterarlos
        #solo cambio un factor por operacion, cv significa
        #changing value
        Pi=np.copy(P[j,:]) 
        cv=np.random.randint(0,2)
        #Aqui creo que tmb se podria multiplicar la distribucion de gauss por
        #un paso 
        Pi[cv]=Pi[cv]+np.random.normal(0,0.5)
        #Aqui saco la chi^2 del que podra ser el nuevo set de puntos
        #con puntos me refiero a v0 y Rc
        x2=chi2(R,vc,v_error,Pi)
        
        #condicionales para saber si si escogeremos este nuevo set de puntos
        if x2<x1[j]:
            x1[j+1]=x2
            P[j+1,:]=np.copy(Pi)
        else:
            rn=np.random.uniform(0,1)
            rg=np.exp(-0.5*(x2-x1[j]))
            if rn<rg:
                x1[j+1]=x2
                P[j+1,:]=np.copy(Pi)
            else:
                x1[j+1]=x1[j]
                P[j+1,:]=np.copy(P[j,:])
                
                rechazos+=1
    return x1,rechazos,P
N=10**5
t=mle(R,v_error,vc,N)
chis=t[0]

print(t[1]/N*100,'%Rechazos')   
print(chis[-1],'chi^2')  
val=t[2]
        
#plt.plot(range(N),chis)
#plt.show
print(val[-1,:], 'V0 y Rc Finales')
vc0r=val[-1,0]
Rr=val[-1,1]
#lo de abajo lo deje comentado porque sale raro 
#plt.scatter(val[0],val[1])
#plt.show
vcr=np.zeros(len(R))
for k in range(len(R)):
    vcr[k]=vc0r*R[k]/np.sqrt(Rr**2+R[k]**2)
    
plt.plot(R,vcr)   
plt.plot(R,vc)
plt.show
    