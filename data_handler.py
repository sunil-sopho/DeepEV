import sys
import csv
import numpy as np
import pandas as pd

PARENT = "./datasets/"
DIRECTORIES = {"1":"1/trips/","2":"1/power/","3":"2/HOD/","4":"2/HOEP/","5":"3/","6":"4/"}
SUBFILES = {"2":["power_weekday.csv","power_weekend.csv"],"3":["PUB_Demand_2008.csv","PUB_Demand_2008_v1.csv","PUB_Demand_2009.csv","PUB_Demand_2009_v1.csv"],"4":["PUB_PriceHOEPPredispOR_2008.csv","PUB_PriceHOEPPredispOR_2008_v1.csv","PUB_PriceHOEPPredispOR_2009.csv","PUB_PriceHOEPPredispOR_2009_v1.csv"],"5":["2008_weather_station_data.csv","2009_weather_station_data.csv"],"6":["fueltypesall.csv"]}
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
            data = data + [pd.read_csv(DIRECTORIES[arg1]+file,error_bad_lines=False)]
    # print(data)
    return data

# def sync_timeline():
