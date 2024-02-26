import csv
from itertools import count
from urllib import robotparser
import pandas as pd
import numpy as np
from collections import Counter

# CSV Input and output paths. Change these.
IN_CSV_PATH = "D:/rowan/cs02570information visualization/final project/2017MC1Data/Lekagul Sensor Data.csv"
OUT_CSV_PATH3 = "D:/rowan/cs02570information visualization/final project/all.csv"

def main():
    
    # Read in data
    df = pd.read_csv(IN_CSV_PATH)

    # Find routes
    ranger_cars_in_park = []
    routes = {}

    for index, row in df.iterrows():
            if row["car-id"] not in ranger_cars_in_park:
                ranger_cars_in_park.append(row["car-id"])
                routes[row["car-id"]] = [row["gate-name"]]
            elif row["car-id"] in ranger_cars_in_park:
                routes[row["car-id"]].append(row["gate-name"])

            

    
    # Find only unique routes
    unique_routes = []
    same_routes = []
    routess=[]
    count = 0
    count1 = 0
    for idx, route in routes.items():
        routess.append(route)
        if route not in unique_routes:
            unique_routes.append(route)
            count = count + 1
        else : 
            same_routes.append(route)
            count1 = count1 + 1
    print("router number:")
    print(count)
    print("router same number:")
    print(count1)
    
    
    
    # Output to CSV
    with open(OUT_CSV_PATH3, 'w', newline='') as csvfile:
        csvreader = csv.writer(csvfile, delimiter=',')
        for route in routess:
            csvreader.writerow(route)
            
'''
    df = pd.read_csv(OUT_CSV_PATH3,encoding="utf_8")
    
    
    df.fillna(value='Na').groupby(df.columns.tolist(),as_index=False).size().to_csv("./allcountroute.csv", encoding="utf_8_sig") 
            '''

if __name__ == "__main__":
    main()
