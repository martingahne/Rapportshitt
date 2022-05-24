

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


################################################################################
#här finns portarna som man vill koppla till på muxen
################################################################################
ports = [0, 1, 5, 6, 7]

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
for i in range(5):
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
    f = [f1, f2, f3, f4, f5, f6]

    t.tic()
    for i in range(samples):
        for i in range(len(ports)):
            enable_port(mux, i)

            f0 = adcs[i].getReading()
            f[i].append(f0)

            disable_port(mux, i)
    tid = samples/t.tocvalue()

    time = numpy.true_divide((numpy.arange(samples)), tid)
    return f, time



##########################################################
#samplar en scale, given
def sample_scale(samples, port):
    enable_port(mux, port)
    y = []
    x = numpy.arange(0, samples)
    for i in range(samples):
        yi = adcs[port].getReading()
        y.append(yi)

    return x, y

#x, y = sample_scale(2000, 1)


#

f, time = get_scales(mux, 10000)



#datum till filnamn
from datetime import datetime
now = datetime.now()
tid = now.strftime("%d/%m/%Y %H:%M:%S")
print(tid)
name = str(input('filnamn'))


#plotgrejjer
import pandas as pd
df = pd.DataFrame({'f1': f[0], 'f2': f[1], 'f3': f[2], 'f4': f[3], 'f5': f[4], 'tid': time})
df.to_csv(name + '.csv', index=False)




# t.tic()
# for i in range(5):
#     sc = get_scale(mux, i)
# t.toc()
