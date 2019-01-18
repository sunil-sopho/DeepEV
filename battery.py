import sys
from math import *
from array import *

vmax = 4.2
vmin = 2.5
vcell = 3.6
vnom = 355.2
ns = vnom/vcell

Ibmax = 0.825
Imin  = 0.05
Idh = 0.55
Qcell = 2.75
Qnom = 45
np = Qnom/Qcell

def getTch():
	soc_at_zero =  # dont know please help @check
	vstar = ns*(vmax - vmin)
	Imi = -1
	T1 = -1
	if soc_at_zero < 1 - ( ()/vmax):
		Imi = 0.825
		T1 = 