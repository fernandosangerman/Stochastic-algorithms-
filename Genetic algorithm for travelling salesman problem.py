#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 19:54:11 2021

@author: fernandosangerman
"""

import numpy as np
import matplotlib.pyplot as plt




def _gencities(Ncities,xy):
    '''
    

    Parameters
    ----------
    Ncities : Int
        Number of cities .
    xy : Array
        Coordinates of the cities.

    Returns
    -------
    D : Array
        Squared matrix containing the distance between every city.

    '''
    
    D=np.zeros([Ncities,Ncities])
    for i in range(Ncities):
        for ii in range(Ncities):
            D[i,ii]=np.sqrt((xy[i,0]-xy[ii,0])**2+(xy[i,1]-xy[ii,1])**2)

    return D
    

def _genpop(Npop,Ncities):
    '''
    

    Parameters
    ----------
    Npop : Int
        Size of the population.
    Ncities : Int
        Number of cities.

    Returns
    -------
    pop : Array
        Entire population with coefficients as the order in which cities are visited.

    '''
    base=np.arange(1,Ncities)
    pop=np.zeros([Npop,Ncities+1])
    for j in range(Npop):
        np.random.shuffle(base) 
        base1=base
        base1=np.append(base1,0)
        base1=np.append(0,base1)
        pop[j]=base1
    
    return pop

def distance(N,Ncities,pop,D):
    '''
    

    Parameters
    ----------
    N : Int
        Size of the population.
    Ncities : Int
        Number of cities.
    pop : Array
        Entire population with coefficients as the order in which cities are visited.
    D : Array
        Squared matrix containing the distance between every city.

    Returns
    -------
    Ds : Array
        Total distance of every individual.

    '''
    Ds=np.zeros(N)
    pop = pop.astype(int)
    for k in range(N):
        for kk in range(Ncities):
            Ds[k]+=D[pop[k,kk],pop[k,kk+1]]
    return Ds

def _selection(Ds):
    '''

    Parameters
    ----------
    Ds : Array
        Total distance of every individual.

    Returns
    -------
    il : Array
        Parents.

    '''
    A=sum(1/Ds)
    il=[0,0]
    for parents in range(2):
        S=np.random.uniform(0,1)
        s=0
        while s<S:
            s+=(1/Ds[il[parents]])/A
            il[parents]+=1
        il[parents]+=-1
    return il

def crossover(Ds,pop,Nnewgen,Ncities):
    '''
    

    Parameters
    ----------
     Ds : Array
        Total distance of every individual.
    pop : Array
        Entire population with coefficients as the order in which cities are visited.
    Nnewgen : Int
        Number of new individuals that will be added to the population.
    Ncities : Int
        Number of cities.

    Returns
    -------
    kids : Array
        Duplicates of the selected parents.

    '''
    kids=np.zeros([Nnewgen,Ncities+1])
    for ij in range(Nnewgen):
        pt=_selection(Ds)
        kids[ij]=pop[pt[0]]
      
    return kids
        
def mutation(kids,Nnewgen,Nmuts):
    '''
    Parameters
    ----------
    kkids : Array
        Duplicates of the selected parents.
    Nnewgen : Int
        Number of new individuals that will be added to the population.
    Nmuts : Int
        Number of coefficients exchanged in every new individual.

    Returns
    -------
    kids : Array
        Duplicates of the selected parents but with Nmuts exchanges in their coefficients.

    '''
    for muts in range(Nnewgen):
        for imut in range(Nmuts):     
            imut=np.random.randint(1,Ncities,[1,2])
            [kids[muts,imut[0,0]],kids[muts,imut[0,1]]]=[kids[muts,imut[0,1]],kids[muts,imut[0,0]]]        
    return kids

def _genocide(pop,Ds,Nnewgen):
    '''
    

    Parameters
    ----------
    pop : Array
        Entire population with coefficients as the order in which cities are visited.
    Ds : Array
        Total distance of every individual.
    Nnewgen : Int
        Number of new individuals that will be added to the population.

    Returns
    -------
    pop : Array
        Best part of the population with coefficients as the order in which cities are visited .
    Ds : Array
        Total distance of the best individuals.

    '''
    for gone in range(Nnewgen):
        q=np.argmax(Ds)
        Ds=np.delete(Ds,q,0)
        pop=np.delete(pop,q,0)
    return pop, Ds

def Main(N,Ncities,Nnewgen,Ngens,Nmuts,xy):
    '''
    

    Parameters
    ----------
    N : Int
        Size of the population.
    Ncities : Int
        Number of cities.
    Nnewgen : Int
        Number of new individuals that will be added to the population.
    Ngens : Int
        Number of generations.
    Nmuts : Int
        Number of coefficients exchanged in every new individual.
    xy : Array
        Coordinates of the cities.

    Returns
    -------
    pop : Array
        Entire population with coefficients as the order in which cities are visited.
    Ds : Array
        Total distance of every individual.
    bestfits : Array
        Best distance in every generation.
    bestpath : Array
        Best individual of the last population.

    '''
    D=_gencities(Ncities,xy)
    pop=_genpop(N,Ncities)
    Ds=distance(N,Ncities,pop,D)
    bestfits=np.zeros(Ngens)
    for jk in range(Ngens):
        kid=crossover(Ds, pop, Nnewgen, Ncities)
        kid=mutation(kid, Nnewgen,Nmuts)
        [pop,Ds]=_genocide(pop, Ds, Nnewgen)
        newDs=distance(Nnewgen,Ncities,kid,D)
        pop=np.concatenate((pop,kid))
        Ds=np.concatenate((Ds,newDs))
        bestfits[jk]=np.min(Ds)
    bestarg=np.argmin(Ds)
    bestpath=pop[bestarg]
    bestpath = bestpath.astype(int)
    return pop, Ds, bestfits,bestpath

def pathgraph(xy,bestpath,Ncities):
    '''
    

    Parameters
    ----------
    xy : Array
        Coordinates of the cities.
    bestpath : Array
        Best individual of the last population.
    Ncities : Int
        Number of cities.

    Returns
    -------
    None.

    '''
    path=np.zeros([Ncities+1,2])
    for ki in range(Ncities+1):
        path[ki]=xy[bestpath[ki]]
        
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax1.set_ylabel('Y')
    ax1.set_xlabel('X')
    ax1.set_title('Map of cities and trajectory travelled.')
    line1, = ax1.plot(path[:,0],path[:,1],'b',label='Tour')
    line2, = ax1.plot(xy[:,0],xy[:,1],'r.',markersize=20,label='Cities')
    line3, = ax1.plot(xy[0,0],xy[0,1],'g.',markersize=20)
    plt.legend()
    plt.show()    
    print(bestpath)

def distancegraph(bestfits):
    '''
    

    Parameters
    ----------
    bestfits : Array
        Best distance in every generation.

    Returns
    -------
    None.

    '''
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax1.set_ylabel('Distance')
    ax1.set_xlabel('Generation')
    ax1.set_title('Best distance of every generation')
    line1, = ax1.plot(bestfits,'b',label='Trayectoria')
    plt.plot(bestfits)
    plt.show()
    print(bestfits[-1])
        
xy=np.loadtxt('15Cities.txt')
#xy=np.random.uniform(0,1,[20,2])

N=100
Ncities=len(xy)
Nnewgen=10
Ngens=10**3
Nmuts=3

[population,Ds,bestfits,bestpath]=Main(N,Ncities,Nnewgen,Ngens,Nmuts,xy)

pathgraph(xy,bestpath,Ncities)
distancegraph(bestfits)









