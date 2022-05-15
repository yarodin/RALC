import msgpack
import csv
import os

entites = {'AF': list(), 'AS': list(), 'EU': list(), 'NA': list(), 'OC': list(), 'SA': list(), 'UA': list()}
if os.path.isfile("cty.csv"):
    with open('cty.csv', newline='') as csvfile:
        csvfile = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvfile:
            if row[0][:2] == 'UA':
                entites['UA'].append(row[0].replace('*', ''))
            else:
                entites[row[3]].append(row[0].replace('*',''))
        with open("cty.db", "wb") as outfile:
            packed = msgpack.packb(entites)
            outfile.write(packed)
            outfile.close()