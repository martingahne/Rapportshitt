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

###########################################################
#öppnar en port(port), läser av adc på den porten, stänger porten och returnerar result.
#################################################################

def get_scale(mux, port):
    enable_port(mux, port)

    result = adcs[port].getReading()
    print(result)

    disable_port(mux, port)
    return result

################################################################
#samma som get_scale fast den hämtar från samtliga adc in range
#################################################################
def get_scales(mux, samples):
    f1 = []
    f2 = []
    f3 = []
    f4 = []
    f5 = []
    f6 = []
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

raw_f, time = get_scales(mux,10)







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

#tar bort m värde m_vals[i] från varje element i listan raw_f[i] 
for i in range(len(ports)):
    raw_f[i] = [x - m_vals[i] for x in raw_f[i]]

#multiplicerar varje värde med k värdet.
fk = [[], [], [], [], [], []]
for i in range(len(ports)):
    fk[i] = [x * k_vals[i] for x in raw_f[i]]



#############################################################
#sparar till fil
#############################################################

#datum till filnamn
from datetime import datetime
now = datetime.now()
tid = now.strftime("%d/%m/%Y %H:%M:%S")
print(tid)
name = str(input('filnamn'))

#sparar alla f och en tidsaxel till csv
import pandas as pd
df = pd.DataFrame({'f1': fk[0], 'f2': fk[1], 'f3': fk[2], 'f4': fk[3], 'f5': fk[4], 'f6': fk[5], 'time': time})
df.to_csv(name + '.csv', index=False)
