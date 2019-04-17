import sys
import csv
import numpy as np
import pandas as pd

PARENT = "./datasets/"
DIRECTORIES = {"1":"1/trips/","2":"1/power/","3":"2/HOD/","4":"2/HOEP/","5":"3/","6":"4/","7":"1/base/"}
SUBFILES = {"2":["power_weekday.csv","power_weekend.csv"],"3":["PUB_Demand_2008.csv","PUB_Demand_2008_v1.csv","PUB_Demand_2009.csv","PUB_Demand_2009_v1.csv"],"4":["PUB_PriceHOEPPredispOR_2008.csv","PUB_PriceHOEPPredispOR_2008_v1.csv","PUB_PriceHOEPPredispOR_2009.csv","PUB_PriceHOEPPredispOR_2009_v1.csv"],"5":["2008_weather_station_data.csv","2009_weather_station_data.csv"],"6":["fueltypesall.csv"],"7":["Weekday duty cycle_86400 Sec.csv","Weekend duty cycle_86400 Sec.csv"]}
BASEFILES = {"2":["",""]}
# 1 : trips
# 2 : power
# 3 : HOD
# 4 : HOEP
# 5 : Weather
# 6 : Fuel prices

for dir in DIRECTORIES:
    DIRECTORIES[dir] = PARENT + DIRECTORIES[dir]

# def sync_timeline():


def get_data(arguments):
    arg1 = arguments[0]
    if (arg1 == "1"):
        data = [pd.read_csv(DIRECTORIES[arg1]+arguments[1]+".csv",header=None,error_bad_lines=False)]
    else :
        dir = DIRECTORIES[arg1]
        data = []
        for file in SUBFILES[arg1]:
            data = data + [pd.read_csv(DIRECTORIES[arg1]+file,error_bad_lines=False,header=None)]
    # print(data)
    return data

"""
args :-
    @base : "7"
    @to_sync : "2"

output :-
    v -- list of dataframes
    v[0] -- weekday t,speed,power
    v[1] -- weekend t,speed,power

"""

def sync_power_usage(base, to_sync):
    dat1 = get_data(base)
    dat2 = get_data(to_sync)
    synced = []
    deft = [0, 0]

    for i in range(2):
        iterator = 0
        delimiter = 0
        df = pd.DataFrame(0,index=np.arange(dat1[i].size),columns=['Speed','Power'])

        # print ("i = ", i)
        for j in range(dat1[i].size):
            print (j)
            if(dat1[i].iloc[j,0] == 0):
                df.loc[j] = deft
                if(delimiter == 1):
                    delimiter = 0
            else:
                if(delimiter == 0):
                    delimiter = 1

            if(delimiter == 1):
                while(dat2[i].iloc[iterator,1] == 0):
                    iterator = iterator + 1
                df.loc[j] = [dat2[i].iloc[iterator,1],dat2[i].iloc[iterator,2]]
                iterator = iterator + 1

        synced.append(df)

    return synced

def get_synced_usage():
    dat = []
    dat.append(pd.read_csv("datasets/1/weekday_merge.csv",error_bad_lines=False))
    dat.append(pd.read_csv("datasets/1/weekend_merge.csv",error_bad_lines=False))
    return dat
