import csv
import json
import os.path
from sensor_readings import *
from sensor_insights import *
from pprint import pprint

fileSensorReadings = 'sensor_readings_output.csv'
fileSensorInsights = 'sensor_insights_output.csv'
outputFile = 'results.json'

def executeAlgorithm():

    getGPSData()
    getSpeedTests()

    #creating output file
    jsonfile = open(outputFile, 'w')

    #Reading insights
    csvFileSensorReadings = open(fileSensorReadings, 'r')
    numLinesSensorReadings = sum(1 for line in open(fileSensorReadings))

    fieldnames = ("no","alt","lat","lng","time")
    reader = csv.DictReader( csvFileSensorReadings, fieldnames)

    #opening json file
    jsonfile.write('{"readings":[')
    jsonfile.write('\n')

    i = 0
    for row in reader:
        if i!=0:
            json.dump(row, jsonfile)
            if i != numLinesSensorReadings - 1:
                jsonfile.write(',\n')
            else:
                jsonfile.write('\n')
        i = i + 1

    jsonfile.write('\n')

    #Reading readings
    csvFileSensorInsights = open(fileSensorInsights, 'r')
    numLinesSensorInsights= sum(1 for line in open(fileSensorInsights))


    fieldnames = ("no","delta_height","distance","lat_1","lat_2","lng_1","lng_2","time","type","vkph","vmps")
    reader = csv.DictReader( csvFileSensorInsights, fieldnames)

    jsonfile.write('],"insights":[')
    jsonfile.write('\n')

    i = 0
    for row in reader:
        if i!=0:
            json.dump(row, jsonfile)
            if i != numLinesSensorInsights - 1:
                jsonfile.write(',\n')
            else:
                jsonfile.write('\n')
        i = i + 1

    jsonfile.write('\n')

    #Reading speed results
    jsonfile.write('],"speed_results":')

    resultadoSpeedTests = getSpeedTests()
    jsonfile.write(json.dumps(resultadoSpeedTests))

    #closing json file
    jsonfile.write('}')

def getResults():
    executeAlgorithm()

    if os.path.exists(outputFile):
        with open(outputFile) as data_file:
            data = json.load(data_file)
            dataStr = json.dumps(data)
            pprint("Success")
        return dataStr
    else:
        return False

# getResults()
