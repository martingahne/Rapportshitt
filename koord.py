import numpy as np
import pandas as pd
import pickle
from numpy.linalg import norm
from numpy.linalg import inv as inverse
from numpy import matmul as multiply
from numpy import add, subtract


data1 = pd.read_csv('k0.csv')

m_vals = data1['m_vals'].tolist()
k_vals = data1['k_vals'].tolist()

x = pd.read_csv('saker.csv')

Samplar = x['Samplar'].tolist()



p1 = np.array([
    [ 86.873,  67.477,  292.283],
    [ 101.873, 41.496 , 292.283],
    [ 15,     -108.972, 292.283],
    [-15,     -108.972, 292.283],
    [-101.873, 41.496,  292.283],
    [-86.873,  67.477,  292.283]]).transpose()

p0 = np.array([
    [ 15,       181.883,  0],
    [ 165.015, -77.951,   0],
    [ 150.015, -103.932,  0],
    [-150.015, -103.932,  0],
    [-165.015, -77.951,   0],
    [-15,       181.833,  0]]).transpose()

pous = np.array([
    [ 0,  0,  319.755],
    [ 0, 0 , 319.755],
    [ 0,     0, 319.755],
    [0, 0, 319.755],
    [0, 0,  319.755],
    [0,  0,  319.755]]).transpose()

len_ben = list()
riktning_list= list()
riktning_list_norm= list()
r_hatt_list =list()
tei = list()

for i in range(6):  
    len_ben.append(np.sqrt(np.power((p0[0,i]-p1[0,i]),2) + np.power((p0[1,i]-p1[1,i]),2) + np.power((p0[2,i]-p1[2,i]),2)))


for i in range(6):
        riktning =  p1[:,i] - p0[:, i]
        riktning_list.append(riktning)
        riktning_norm = riktning/len_ben[i]
        riktning_list_norm.append(riktning_norm)

for i in range(6):
    r_hatt = p1[:,i] - pous[:,i]
    r_hatt_list.append(r_hatt)

Atop = np.concatenate([ [(riktning_list[i])*1e-3] for i in range(6)], 0).T

for i in range(6):
    tei.append(np.cross(r_hatt_list[i],riktning_list_norm[i])*1e-3)


Abottom = np.concatenate([ [tei[i]] for i in range(6)], 0).T

A = np.concatenate([Atop, Abottom])

y = np.zeros((len(Samplar),6),dtype=float)

for i in range(len(Samplar)):      
    for a in range(6):
        y[i,a] = ((x.iat[i,a+1]) - m_vals[a]) * k_vals[a] 

#Slutligen V = A*y
V =[]
for i in range(len(Samplar)):
    Vi = np.matmul(A,y[i,:])
    V.append(Vi)
print(V)





