import sys
from math import *

chargerEffeciency = 1
conversionConstant = 1 #don't know @check @sunil
"""
	Some global parameters for speeding up dp

"""
Tmax = -1
a_vec = []
Cel_vec = []
stateOfCharge_vec = []


def a(t):
	if Tmax == -1:
		sys.stderr.write("Tmax not set yet :)")
		sys.exit(-1)
	else:
		return a_vec[T-t]

def  Cel(t):
	if Tmax == -1:
		sys.stderr.write("Tmax not set yet :)")
		sys.exit(-1)
	else:
		return Cel_vec[T-t]
def  stateOfCharge(t):
	if Tmax == -1:
		sys.stderr.write("Tmax not set yet :)")
		sys.exit(-1)
	else:
		return stateOfCharge_vec[T-t]

def Energy(soc):
	"""
	@check sunil update this
	"""
	return 0

def gasolinePrice(t):
	# @sunil @check
	return gasolinePrice[t]


def costfuction_p(t):
	"""
		cost function while car is plugged into charging station
		charger effeciency [0,1]
	"""
	shouldCharge = a(t)
	elecPrice = Cel(t)
	SOC = stateOfCharge(t)
	energySupplied= Energy(SOC)

	return (shouldCharge*elecPrice*energySupplied)/chargerEffeciency

def costfunction_u(t):
	"""
		when moving
	"""
	fuelCost = gasolinePrice(t)
	energyConsume = Edis(t)
	batteryCapacity = Enom(t)
	SOC = stateOfCharge(t)

	return fuelCost*conversionConstant*max(energyConsume-batteryCapacity*SOC,0)


def dicreteSOC(t,B=20):
	return (ceil(B*stateOfCharge(t)) + 0.5)/B

def rewardfunction(t,a):
	plugged = z(t)
	if  plugged == 1 and a==0 :
		return 0
	elif plugged == 1 and a == 1:
		return -1*costfuction_p(t)
	else :
		return costfunction_u(t)

def Qstate(t,a):
	if t==max:
		return dicreteSOC(t)*AvgElecPrice
	else:
		rewardfunction(t,a) + max(Qstate(t+1,0),Qstate(t+1,1))
		 