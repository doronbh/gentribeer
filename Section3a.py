
import csv
import time
from datetime import datetime
from operator import itemgetter, attrgetter, methodcaller
from numpy import var, sqrt, average
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

with open('Zip_Zri_AllHomes.csv') as csvfile:
    file1 = csv.reader(csvfile, delimiter=',')
    headers = next(file1)
    fields = len(headers)

    for j in range(0,fields):
        if headers[j] == 'RegionName':
            zipCol = j
        if headers[j] == 'City':
            CityCol = j
        if headers[j] == 'Metro':
            metroCol = j
        if headers[j] == '2018-09':
            col2018 = j
        if headers[j] == '2015-09':
            col2015 = j
    j=0
        
    for row in file1:
        if row[col2018] == '' or row[col2015] == '':
            print('No Data on '+row[zipCol])
        else:
            block=[int(row[zipCol]),row[CityCol],int(row[col2018]),int(row[col2015]),int(row[col2018])-int(row[col2015])]
        mainList.append(block)
            
    j +=1
            
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
print(len(microList))

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
    
microNum = sorted(list(set([ent[5] for ent in mainList])))

forGraph = []

for i in range(0,5):
    forMean = []
    for j in range(0,len(mainList)):
        if mainList[j][5] == i:
            forMean.append(mainList[j][4])
    forGraph.append([str(i),mean(forMean)])

forMean = []
for j in range(0,len(mainList)):
    if mainList[j][5] >= 5 and mainList[j][5] <= 7:
        forMean.append(mainList[j][4])
forGraph.append(['5-7',mean(forMean)])

forMean = []
for j in range(0,len(mainList)):
    if mainList[j][5] >= 8:
        forMean.append(mainList[j][4])
forGraph.append(['8+',mean(forMean)])

print(forGraph)

objects = [ent[0] for ent in forGraph]
y_pos = arange(len(objects))
performance = [ent[1] for ent in forGraph]
            
 
pyplot.bar(y_pos, performance, align='center', alpha=0.5)
pyplot.xticks(y_pos, objects)
pyplot.ylabel('Average increase in value per square foot')
pyplot.xlabel('Number of microbreweries in zip code')
    
pyplot.show()
pyplot.savefig('foo.png',  bbox_inches='tight')