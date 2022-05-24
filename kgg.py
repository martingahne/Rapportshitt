
from pytictoc import TicToc
import numpy
from numpy import mod
t = TicToc()

import qwiic_tca9548a
import PyNAU7802
import smbus2
import pandas as pd
#

def enable_port(mux: qwiic_tca9548a.QwiicTCA9548A, port):
    mux.enable_channels(ports[port])


def disable_port(mux: qwiic_tca9548a.QwiicTCA9548A, port):
    mux.disable_channels(ports[port])

def create_bus():
    bus = smbus2.SMBus(1)
    return bus

def get_scale(mux, port):
    
    enable_port(mux, port)
    result=adcs[port].getReading()
    disable_port(mux, port)
    return result
    
Antal_samplestr= input("Ange antalet samples:")
Antal_samples = int(Antal_samplestr) #Lägg 10
ports = [6, 2, 1, 0, 7, 5]

mux = qwiic_tca9548a.QwiicTCA9548A(address=0x70)

bus = smbus2.SMBus(1)
adcs = list()


for i in range(6):
    enable_port(mux, i)
    adc = PyNAU7802.NAU7802()
    adc.begin(bus)
    adcs += [adc]
    disable_port(mux, i)

dct = {}
for i in range(6):
    dct['sensor_%s' % i] = []  


t.tic()
for i in range(Antal_samples * 6):
    dct['sensor_%s' % mod(i,6)].append(get_scale(mux, mod(i,6)))
t.toc()

Samples = numpy.arange(1,(Antal_samples+1))


df = pd.DataFrame({'Samplar': Samples, 'Port6': dct['sensor_0'], 'Port2': dct['sensor_1'], 'Port1': dct['sensor_2'], 'Port0': dct['sensor_3'],'Port7': dct['sensor_4'],'Port5': dct['sensor_5']})
df.to_csv('saker.csv', index=False)

