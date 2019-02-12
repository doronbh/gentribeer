
import csv
import time
from datetime import datetime
from operator import itemgetter, attrgetter, methodcaller
from sklearn import linear_model
from scipy import stats
from numpy import float64, mean,  var, random, sign, sqrt, arange
from urllib import request
from matplotlib import pyplot
import json 
import requests

mainList=[]

def month(num1):
    if num1<9:
        return('0'+str(num1+1))
    else:
        return(str(num1+1))
    
with open('Zip_PctOfHomesDecreasingInValues_AllHomes.csv') as csvfile:
    file1 = csv.reader(csvfile, delimiter=',')
    headers = next(file1)
    fields = len(headers)

    yearCols = [0]*33

    for j in range(0,fields):
        if headers[j] == 'RegionName':
            zipCol = j
        if headers[j] == 'City':
            CityCol = j
        if headers[j] == 'Metro':
            metroCol = j
        for k in range(0,33):
            if headers[j] == str((k//12)+2016)+'-'+month(k % 12):
                yearCols[k] = j
    j=0

    for row in file1:

        block=[int(row[zipCol]),row[CityCol]]
        for k in range(0,33):
            block.append(row[yearCols[k]])
        mainList.append(block)
            
        j +=1

for i in range(0,len(mainList)):
    forMean = []
    for j in range(0,33):
        if mainList[i][j+2] != '':
            mainList[i][j+2] = float(mainList[i][j+2])
            forMean.append(round(mainList[i][j+2]*100))
    if forMean != []:
        mainList[i].append(mean(forMean)/100)
    else:
        mainList[i].append('No Data')
    
print('bob')

listOfBreweris = []

for i in range(1,170):
    print('page ',i)
    url = 'https://api.openbrewerydb.org/breweries?page='+str(i)+'&per_page=50'
    response = requests.get(url)
    response_json = json.loads(response.text)
    for j in range(0,len(response_json)):
        if not (response_json[j]['postal_code'] == None or response_json[j]['postal_code'] == 'Jose' or response_json[j]['postal_code'] == 'TBD'):
            listOfBreweris.append([response_json[j]['name'],response_json[j]['brewery_type'],response_json[j]['city'],int(response_json[j]['postal_code'][0:5])])

microList=[brewery for brewery in listOfBreweris if brewery[1]=='micro']

zipList = [brewery[3] for brewery in microList]
zipList = list(set(zipList))
zipIndex = [[x,'',0] for x in zipList]

for i in range(0,len(microList)):
    zipPlace = zipList.index(microList[i][3])
    zipIndex[zipPlace][2] += 1
  
for i in range(0,len(mainList)):
    if mainList[i][0] in zipList:
        zipPlace = zipList.index(mainList[i][0])
        mainList[i].append(zipIndex[zipPlace][2])
    else:
        mainList[i].append(0)

microNum = sorted(list(set([ent[36] for ent in mainList])))

forGraph = []
for i in microNum:
    forMean = []
    for j in range(0,len(mainList)):
        if mainList[j][36] == i and mainList[j][35] != 'No Data':
            forMean.append(mainList[j][35])
    forGraph.append([i,mean(forMean)])
    
print(forGraph)

objects = [ent[0] for ent in forGraph]
y_pos = arange(len(objects))
performance = [ent[1] for ent in forGraph]
            
 
pyplot.bar(y_pos, performance, align='center', alpha=0.5)
pyplot.xticks(y_pos, objects)
pyplot.ylabel('average percentage of homes with decreasing values')
pyplot.xlabel('Number of microbreweries in zip code')
    
pyplot.show()

regression=stats.linregress([i[0] for i in forGraph],[i[1] for i in forGraph])
print(regression)
