import pynmea2
import pandas as pd
import numpy as np
import math

def getGPSData():
	#Declaracion variables
	fileSensorReadings = 'sensor_readings_output.csv'
	countCheck = 0
	countParse = 0
	tim = []
	lat = []
	lon = []
	alt = []
	#Se abre archivo
	with open("NMEA.TXT") as f:
	    for line in f:
	    	content = line.split(',')
	    	if (content[0] == '$GPGGA' and content[2] != '' ):

	    		try:
	    			msg = pynmea2.parse(line)
	    			if msg.altitude >=2000:
						tim.append((msg.timestamp))
						lat.append(msg.latitude)
						lon.append(msg.longitude)
						alt.append(str(msg.altitude))

	                except pynmea2.nmea.ChecksumError:
	    			     countCheck = countCheck + 1
	    			     pass
	                except pynmea2.nmea.ParseError:
	                     countParse = countParse + 1
	                     pass

	data_degrees = { #almacena todos los datos en una matriz
		'time':tim,
		'lat':lat,
		'lng':lon,
		'alt':alt
	}
	matrix = pd.DataFrame(data_degrees)
	matrix.to_csv(fileSensorReadings)
	#print("Numero de errores ChecksumError: " + str(countCheck))
	#print("Numero de errores ParseError: " + str(countParse))
	return matrix
