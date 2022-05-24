import numpy as np
import pickle
import plotly.graph_objects as go
import pandas as pd
from numpy.linalg import norm
from numpy.linalg import inv as inverse
from numpy import matmul as multiply
from numpy import add, subtract
from numpy import diagflat as diag

from math import pi

#########################################################################################
#measurements from cad(mm)
###########################################################################################



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

p_ous = np.array([
    [0, 0, 319.755],
    [0, 0, 319.755],
    [0, 0, 319.755],
    [0, 0, 319.755],
    [0, 0, 319.755],
    [0, 0, 319.755]]).transpose()

# ##########################################################
# Define transfer matrix
# See README.md
# ##########################################################
# Force coefficients
#n = lambda i : self.legs[i].direction
n =[]
nhatt = []
for i in range(6):
    riktning =  p1[:,i] - p0[:, i]
    n.append(riktning)
    riktning_norm = riktning/norm(riktning)
    nhatt.append(riktning_norm)

Atop = np.concatenate([ [n[i]] for i in range(6)], 0).T
print(Atop)

#beräkna ri(vektor)

r_v = []
for i in range(6):
    r = p1[:,i] - p_ous[:, i]
    r_v.append(r)
print('r_v')
print(r_v)

#kryssprodukt r x nhatt
Tao = []
for i in range(6):
    tao = np.cross(r_v[i], nhatt[i])
    Tao.append(tao)

print('Tao')
print(Tao)

Abottom = np.concatenate([ [Tao[i]] for i in range(6)], 0).T

A = np.concatenate([Atop, Abottom])

print('A')
print(A)
# Torque coefficients
#pous = np.sum( np.concatenate( [[self.legs[i].position] for i in range(6)], 0).T, 1) / 6.0 # Assume object is centered on plate



# q = lambda i : self.legs[i].position
# tei = lambda i : np.cross(q(i) - pous, n(i))*1e-3  # stored as mm
# Abottom = np.concatenate([ [tei(i)] for i in range(6)], 0).T

# # Combine into larger matrix
# self.A = np.concatenate([Atop, Abottom])