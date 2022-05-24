from pytictoc import TicToc
import numpy
from numpy import mod
t = TicToc()

import qwiic_tca9548a
import PyNAU7802
import smbus2
import pandas as pd

#from plotly.subplots import make_subplots
#import plotly.graph_objects as go

def enable_port(mux: qwiic_tca9548a.QwiicTCA9548A, port):
    mux.enable_channels(port)


def disable_port(mux: qwiic_tca9548a.QwiicTCA9548A, port):
    mux.disable_channels(port)

def create_bus():
    bus = smbus2.SMBus(1)
    return bus

def get_scale(mux, port):
    
    enable_port(mux, port)
    result=adc.getReading()
    disable_port(mux, port)
    return result
    
#Antal_samplestr= input("Ange antalet samples:")
Antal_samples = 100 #int(Antal_samplestr)
port = int(input('Ange input: '))

mux = qwiic_tca9548a.QwiicTCA9548A(address=0x70)

bus = smbus2.SMBus(1)



enable_port(mux, port)
adc = PyNAU7802.NAU7802()
adc.begin(bus)
disable_port(mux, port)

m = 0 
k = 0

totval = 0  
for i in range(Antal_samples):
    totval += get_scale(mux,port)
    m = (totval/Antal_samples)


vikt = float(input('Lägg på en käng vikt:'))


totval_k = 0  
for a in range(Antal_samples):
    totval_k += get_scale(mux,port)
    k = (vikt/ ((totval_k/Antal_samples) - m))

#df = pd.DataFrame({'k_värden': k, 'm_värden': m})
#df.to_csv('klb.csv', index=False)

print(m)
print(k)

#För att nu beräkna en ny vikt:

