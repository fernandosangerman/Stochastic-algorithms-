import numpy as np
import matplotlib.pyplot as plt

def importData(file):
    """
    Imports data divided in columns from a txt file
    """
    with open(file, "r") as f:
        data=f.readlines()
    #The elements are separated b tab (\t) in a
    x=np.array([]); y=np.array([]); s=np.array([])
    for line in data[1:]: #Removal of headers
        line=line.replace("\n","") #Removal of (\n)
        lineinlist=line.split(" ") #Converts str into list
        fvals=[float(x) for x in lineinlist] #String to float
        x=np.append(x, [fvals[0]]); 
        y=np.append(y, [fvals[1]])
        s=np.append(s, [fvals[2]])
    return(x,y,s)

#M is the model function, P is the parameters vector
M=lambda P, R: P[0]*R/np.sqrt(P[1]**2+R**2)

def _chisq(x,y, s, P):
    """
    Chi square function evaluation
    See docstring in Metropolis for variable information
    """
    final=0
    for i in range(len(x)):
        final+=((y[i]-M(P, x[i]))/s[i])**2
    return final

def Metropolis(x, y, s, P, Niters):
    """
    Args:
        x (array): vector with with independent variable data
        y (array): vector with with dependent variable data
        s (array): vector with with error data
        P (array): Vector containing the the initial guess parameters
        Niters (int): Number of iterations
    Returns:
        voLog, Rlog (arrays): Contain de data per iteration of the parameters vo, R
        P (array): Latest values of the parameters [voLog[-1], Rlog[-1]]
        chilog (list): Contains de data per iteration of the parameters of chi square.
        rejects (int): Number of rejections done by the algorithm
    """
    rejects=0
    chi1=_chisq(x, y, s, P)
    RLog=[P[0]]; voLog=[P[1]] #Init the variables log per iteration.
    chiLog=[chi1]
    for _ in range(Niters): #Metropolis algorithm
        #Random adittion to a random parameter
        rnindx=np.random.randint(0, len(P))
        Ptest=np.copy(P)
        Ptest[rnindx]+=np.random.normal(0, 0.75) 
        #New chi square proposal
        chi2=_chisq(x, y, s, Ptest)
        #Evaliatopm
        if chi2<chi1: #Acept new chi
            P=np.copy(Ptest); chi1=chi2
        else:
            Lfactor=np.exp(-0.5*(chi2-chi1)) 
            if Lfactor>=np.random.uniform(0., 1.0):#Acept
                P=np.copy(Ptest); chi1=chi2
            else: #Reject
                rejects+=1
        chiLog.append(chi1) #Saves the new variables in Logs
        voLog.append(P[0]); RLog.append(P[1])

    return(np.array(voLog), np.array(RLog), P, chiLog, rejects)
            

def plotModel(x, y, P):
    """Plots our model and the disperse data"""
    ax=plt.axes()
    ax.plot(x, M(P,x))
    ax.scatter(x, y)
    plt.show()

def plotChi(chilog):
    ax=plt.axes()
    ax.plot(chilog)
    plt.show()


P=np.array([1.0, 1.0]) #Parameters [v0, Rc]
Niters=10**3

(x,y,s)=importData("mock_data.txt")
(voLog, RLog, P, chiLog, rejects)=Metropolis(x,y,s,P, Niters)
plotModel(x, y, P)
plotChi(chiLog)
print("chi2: "+ str(chiLog[-1]))


#L=1/(2*np.pi)**(n/2) #Likelihood function start