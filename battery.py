import sys
from math import *
from array import *

vmax = 4.2
vmin = 2.5
vcell = 3.6
vnom = 355.2
ns = vnom/vcell

Rb = 0.1 # for now but need to updated @sunil 
Ibmax = 0.825
Ibmin  = 0.05
Idh = 0.55
Qcell = 2.75
Qnom = 45
np = Qnom/Qcell

def getTch():
	soc_at_zero =  # dont know please help @check
	vstar = ns*(vmax - vmin)
	Imi = -1
	T1 = -1
	Condition = (1- soc_at_zero - (Rb*Ibmax)/vmax );
	if Condition > 0:
		Imi = Ibmax
		T1 = Qnom/Ibmax
		T1 *= Condition;
	else:
		Imi = (1 - soc_at_zero)*vstar
		Imi /= Rb
		T1 = 0

	# Calculate t2
	t2  = (Rb*Qnom)/vstar
	t2 *= -1
	t2 *= log(Ibmin/Imi)

	tch  = t1+t2

	return {tch,t1,Imi}

def Soc_at_t(deltaT):
	tch,t1,Imi = getTch;
	soc_at_t = -1
	if t1 == 0:
		soc_at_t = soc_at_zero + (Imi*min(tch,deltaT))/Qnom
	elif t1 > 0 and t1 < deltaT:
		w1 = (Imi*t1)/Qnom
		w2 = (Imi*min(deltaT - t1, tch-t1 ))/Qnom

		soc_at_t = soc_at_zero + w1 + w2
	elif t1 >= deltaT:
		soc_at_t = soc_at_zero + (Imi*deltaT)/Qnom

	return soc_at_t

def ElecticDrivingRange():
	MPGe = 0.0470
	Enom = 16.5 *1000 #Wh
	return (me*MPGe*Soc_at_t()*Enom)/dischargingEffeciency
