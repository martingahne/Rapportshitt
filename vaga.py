



#library för hårdvara
import qwiic_tca9548a
import PyNAU7802
import smbus2


#library för tidtagning och sparande av data.
from pytictoc import TicToc
import numpy
import pandas
import plotly.express as px
import math
import csv
from pandas import *
 


################################################################################
#här finns portarna som man vill koppla till på muxen
################################################################################
ports = [6, 2, 1, 0, 7, 5]

#skapar mux med address 0x70
mux = qwiic_tca9548a.QwiicTCA9548A(address=0x70)

#skapar bus för i2c kommunikation
bus = smbus2.SMBus(1)

#tidtagare för prestandatest
t = TicToc()

#öppnar/stänger portar på muxen
def enable_port(mux: qwiic_tca9548a.QwiicTCA9548A, port):
    mux.enable_channels(ports[port])

def disable_port(mux: qwiic_tca9548a.QwiicTCA9548A, port):
    mux.disable_channels(ports[port])

##########################################################################
#öppnar en port på muxen, skapar ett adc objekt för den porten och lägger till i listan adcs. stänger sedan porten.
##########################################################################
adcs = list()
for i in range(6):
    enable_port(mux, i)
    adc = PyNAU7802.NAU7802()
    adc.begin(bus)
    adcs += [adc]
    disable_port(mux, i)

################################################################
#hämtar getReading från samtliga adc i ports
#################################################################
def get_scales(mux, samples):

    f = [[], [], [], [], [], []]
    t.tic()
    for i in range(samples):
        for i in range(len(ports)):
            enable_port(mux, i)

            f0 = adcs[i].getReading()
            f[i].append(f0)

            disable_port(mux, i)

    samples_div_tid = samples/t.tocvalue()

    time = numpy.true_divide((numpy.arange(samples)), samples_div_tid)
    return f, time

raw_f, time = get_scales(mux,1)

##############################################################
#ladar kalibrering
##############################################################

kalibrering = str(input('ange filnamn för kalibrering: '))
# reading CSV file
data = read_csv(kalibrering + '.csv')

m_vals = data['m_vals'].tolist()
k_vals = data['k_vals'].tolist()

##############################################################
#använder värden från kalibrering
##############################################################
def kalibrera(raw_f, m_vals, k_vals):
#tar bort m värde m_vals[i] från varje element i listan raw_f[i] 
    for i in range(len(ports)):
        raw_minus_m = [[], [], [], [], [], []]
        raw_f[i] = [x - m_vals[i] for x in raw_f[i]]

#multiplicerar varje värde med k värdet.
    f = [[], [], [], [], [], []]
    for i in range(len(ports)):
        f[i] = [x * k_vals[i] for x in raw_f[i]]
    return f

f = kalibrera(raw_f, m_vals, k_vals)

f_tot = 0
for i in range(len(ports)):
    f_tot += (f[i])[0]



print(f)
print('vikt')
print(f_tot)