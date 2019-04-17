import sys
from math import *
from array import *
from battery import *
from data_handler import *

import random

chargerEffeciency = 1
conversionConstant = 1 #don't know @check @sunil
"""
	Some global parameters for speeding up dp

"""
Tmax = -1
a_vec = []
stateOfCharge_vec = []
gasolinePrice_vec = []
Cel_vec = []
Edis = []

def a(t):
	"""
		Is being charged or not when not moving
		|-(1) charged
		|-(0) not charging
		needs to be figured out
	"""
	if Tmax == -1:
		sys.stderr.write("Tmax not set yet :)")
		sys.exit(-1)
	else:
		return a_vec[(Tmax-t-1)]

def  Cel(t):
	"""
		cost of electricity at time t
		|- needs to be setted by a setter
	"""
	return Cel_vec[int(t/3600)]



def  stateOfCharge(t):
	"""
	 @check needs apendix knowledge
	"""
	if Tmax == -1:
		sys.stderr.write("Tmax not set yet :)")
		sys.exit(-1)
	else:
		return stateOfCharge_vec[Tmax-t-1]

def Energy(soc):
	"""
	@check sunil update this
	"""
	return 10

def gasolinePrice(t):
	"""
	 price of gasoline at an time t
	 |- needs pre setting using setter
	# @sunil @check
	"""
	return gasolinePrice_vec[t]

def Edis(t):
	"""
		returns energy consuption at time t
		need pre set by setter
	"""
	return Edis[t]

def getAvgElecPrice():
	sum = 0
	for i in range(len(Cel)):
		sum += Cel[i]
	return sum/len(Cel)

# ===========================================================================
# ----------------- Main function here -------------------------------------- 
# ===========================================================================


def costfuction_p(t):
	"""
		cost function while car is plugged into charging station
		charger effeciency [0,1]
		@check for energy and soc
	"""
	shouldCharge = a(t)
	elecPrice = Cel(t)
	SOC = stateOfCharge(t)
	energySupplied= Energy(SOC)

	return (shouldCharge*elecPrice*energySupplied)/chargerEffeciency

def costfunction_u(t):
	"""
		when moving
		@check for edis and enom
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
	"""
		Not meant to use due to exponetial nature
		-- will help to check recursive condition
	"""
	if t==Tmax:
		AvgElecPrice =  getAvgElecPrice()
		return dicreteSOC(t)*AvgElecPrice
	else:
		rewardfunction(t,a) + max(Qstate(t+1,0),Qstate(t+1,1))

def getAstar(tmax):
	"""
	 gives array a-star best decision to be taken
	 1) calculate qstate for tmax and a=0,a=1
	 2) back iterate to have value for all points
	 3) infer a-star from all this 
	"""
	Qstates = []
	AvgElecPrice =  getAvgElecPrice()
	value = dicreteSOC(t)*AvgElecPrice
	Qstates.insert(0, [value,value])

	for i in range(Tmax-1):
		maxOld = max(Qstates[0,0],Qstate[0,1])
		Qstate0 = rewardfunction(Tmax-1-i,0) + maxOld
		Qstate1 = rewardfunction(Tmax-1-i,1) + maxOld
		Qstates.insert(0,[Qstate0,Qstate1])

	#Qstate Eval Complete
	#Get Astar Values

	astar = []
	for i  in range(len(Qstates)):
		if Qstates[i][0] >= Qstates[i][1]:
			astar.insert(0)
		else:
			astar.insert(1)

	#process finish here for now
	return astar


def fillData(mode):
	dsize = 10
	if mode == "p":

		dat = get_data("4");
		# @sunil later sync dates too for now just take data
		# print(float(dat[0][['HOEP']].iloc[0]))
		# Electicity price set
		for i in range(dsize):
			Cel_vec.append(float(dat[0][2].iloc[i+1]))
		global Tmax
		Tmax = 3600*dsize

		for i in range(Tmax):
			a_vec.append(random.randint(1,101)%2);
			stateOfCharge_vec.append(random.randint(1,101)/3);

	elif mode== "u":
		dat = get_data("6")
		print(dat[0].iloc[[0]])

		for i in range(int(dsize/24) +1):
			# gasolinePrice_vec.append(float(dat[0]['Ontario Average/Moyenne provinciale'].iloc[i]))
			gasolinePrice_vec.append(float(dat[0][11].iloc[i+1]))

		dat = sync_power_usage("7","2")
		print(dat)
		# print()
	else:
		print()

if __name__ == '__main__':
	fillData("p")
	# print(Tmax)
	# for i in range(Tmax):
	# 	print(costfuction_p(i))

	# fill data for u equation too
	fillData("u")

