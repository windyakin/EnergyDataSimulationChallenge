# -*- coding: utf-8 -*-
"""
Created on Mon Sep 01 11:19:10 2014

@author: Dan
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pylab as pl
import csv

df = pd.read_csv("C:/Users/Dan/Documents/GitHub/EnergyDataSimulationChallenge/challenge1/data/training_dataset_500.csv", header = 0)  #read in the data as a pandas dataset

#setup a function to plot graphs of the means of the three available variables for some visualisation
def meanvariable(month, variable):#(month, variable) month can be either 'Label' or 'Month' and variable can be either of the 3 variables
    listofmonth = list((df.apply(set)[month]))#get all the unique months (this will be either 12 or 227
    averages = []#create an empty list for the averages to go into
    for i in listofmonth:
        dd = df[df[month] == i]  #create a new dataset that only has the data for each individual month in
        averages.append(np.mean(dd[variable])) #graphs look the same using meadian or mean, no real outliers anyway
    x = pl.int_(listofmonth)    
    plt.scatter(x, averages)  #plot the mean against the month
    plt.xlabel('Months beginning July 2011')
    plt.ylabel(variable)
    plt.xlim(0,22)
    plt.show()
meanvariable('Label', 'Temperature')  #call the funcion with the 3 variables
meanvariable('Label', 'Daylight')  
meanvariable('Label', 'EnergyProduction')
#from these we can see a very clear pattern in temperature but not in energy production and daylight
#it might be expected that combining daylight and temperature and plotting on a 3d graph may help to see a pattern

df = df.drop(['ID'], axis = 1)  #drop ID from dataset (useless identifier)
cols = df.columns.tolist() #put the columns of the dataset into a list called cols
cols = cols[-1:] + cols[:-1] #move energy production to the front of the list
df = df[cols] #relabel the dataset columns
df['Daylight*Temp'] = df.Daylight * df.Temperature  #create a new column with the variable that combines daylight and temp
train_data = df.values #store the dataset values into train data 

de = pd.read_csv("C:/Users/Dan/Documents/GitHub/EnergyDataSimulationChallenge/challenge1/data/test_dataset_500.csv", header = 0)
de = de.drop(['ID', 'EnergyProduction'], axis = 1)  #drop ID and EnergyProduction (as we are predicting energy production)
de['Daylight*Temp'] = de.Daylight * de.Temperature 
test_data = de.values  #store dataset as test data


# Import the random forest package
from sklearn.ensemble import RandomForestClassifier 

# Create the random forest object which will include all the parameters
# for the fit
forest = RandomForestClassifier(n_estimators = 300)  #300 estimators gives required accuracy without taking too long

# Fit the training data to the Survived labels and create the decision trees
forest = forest.fit(train_data[0::,1::],train_data[0::,0])


# Take the same decision trees and run it on the test data
output = forest.predict(test_data)
#need to be integers for kaggle to work

#need to convert array to a list to add the titles back in
output = output.tolist()
output = ['EnergyProduction']+output #add column title back in
energy = output  #rename as energy for clarity
Housenumber = ['House'] + range(1,500)  #match with housenumbers

##Now turn back into CSV file

# open a file for writing.
csv_out = open("C:/Users/Dan/Documents/GitHub/EnergyDataSimulationChallenge/challenge1/analysis/danjones/myresults.csv", 'wb')

# create the csv writer object.
mywriter = csv.writer(csv_out)

# writerow - one row of data at a time.
for row in zip(Housenumber,energy):
    mywriter.writerow(row)

#colse the newly created csv file to avoid data loss
csv_out.close()
#end of predictor code







#code below is code to find the MAPE value
dataset = pd.read_csv("C:/Users/Dan/Documents/GitHub/EnergyDataSimulationChallenge/challenge1/analysis/danjones/myresults.csv", header = 0) #read in he results to a pandas dataset
dg = pd.read_csv("C:/Users/Dan/Documents/GitHub/EnergyDataSimulationChallenge/challenge1/data/test_dataset_500.csv", header = 0)


results = []  #create an empty results list
for row in dataset['EnergyProduction']:  #for each row in the price column
    results.append(float(row))  #append that row to the resulst list

zipped = []  #create an empty zipped list
for elem in zip(dg['EnergyProduction'], results):   #for each element in prices and results (dependently) add it to a list
    zipped.extend(elem)

percentages = []  #create an empty list to store the percentage errors
for e,f in zip(zipped,zipped[1:])[::2]:  #for each item pairwise in the zipped list (prices then results)
    percentages.append(abs(((e-f)/e)))  #append the error 

MAPE =  np.mean(percentages)  #print the median percentage error
print MAPE


#code to write MAPE value to txt file automatically
csv_out = open("C:/Users/Dan/Documents/GitHub/EnergyDataSimulationChallenge/challenge1/analysis/danjones/MAPE.txt", 'wb')
mywriter = csv.writer(csv_out)
mywriter.writerow(['MAPE'])
mywriter.writerow([MAPE])
csv_out.close()
