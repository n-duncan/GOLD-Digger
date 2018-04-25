from bs4 import BeautifulSoup
import os
import csv
import time
import datetime

dataFolder = "./Data"
if (os.environ.get('cronFlag') == "True"):
	dataFolder = "./DataCrontab"

#returns list of files in the directory
def getAllFiles(dir):
	files = []
	listing = os.listdir(dir)
	for infile in listing:
		fileName = './Output/' + infile
		files.append(fileName)
	return files


#get start time
start = time.time()

#directory containing html files to parse ***EDIT THIS PATH IF USED ON A DIFFERENT MACHINE***
rootDirectory = './Output'
filesToParse = getAllFiles(rootDirectory)

#list for cleaned data
cleanedData = []
for file in filesToParse:
	#create bs object
	soup = BeautifulSoup(open(file), "html.parser")

	#find all table bodies and store them in list
	rows = soup.find_all('tr', {'class':'CourseInfoRow'})

	#iterate over list and create our raw results
	data = []
	for row in rows:
		colData = []

		cols = row.find_all('td')
		for col in cols:
			for string in col.stripped_strings:
				colData.append(string)
		data.append(colData)

	#getting significant information
	for course in data:
		cleanedDataTemp = []
		#append filename for information about Quarter and Year
		cleanedDataTemp.append(str(file))
		cleanedDataTemp.append(course[0])
		cleanedDataTemp.append(course[course.index('College:') + 1])
		cleanedDataTemp.append(course[course.index('Units:') + 1])
		cleanedDataTemp.append(course[course.index('Grading:') + 1])
		#grab last 5 indices containing important information
		for index in range(len(course) - 4, len(course)):
			cleanedDataTemp.append(course[index])
		#add the cleaned course data to cleanedData
		if cleanedDataTemp[len(cleanedDataTemp) - 2] == 'T B A':
			cleanedDataTemp[len(cleanedDataTemp) - 2] = 'N/A'
		if cleanedDataTemp[len(cleanedDataTemp) - 3] == 'T B A':
			cleanedDataTemp[len(cleanedDataTemp) - 3] = 'N/A'
			cleanedDataTemp[len(cleanedDataTemp) - 4] = 'N/A'
		elif ('am' not in cleanedDataTemp[len(cleanedDataTemp) - 3] and 'pm' not in cleanedDataTemp[len(cleanedDataTemp) - 3]):
			cleanedDataTemp = []

		cleanedData.append(cleanedDataTemp)
	data = []
	print('parsed: ' + file)

#output to CSV file:
now = datetime.datetime.now()
with open(dataFolder + "/data_" + str(now.month) + "_" + str(now.day) + "_" + str(now.hour) + ".csv", "w+", newline="") as f:
	writer = csv.writer(f)
	writer.writerows(cleanedData)

end = time.time()
#print elapsed time
print('Time to parse: ' + str(end - start))

#print out CSV file (testing purposes)
#os.system('column -s, -t < ./Data/data.csv | less -#2 -N -S')

#Print out raw results:
"""
for course in data:
	i = 0
	for x in course:
		print(str(i) + ": ")
		print(x)
		i+=1
	print('\n')
"""