###################
#
# File handling the processing of cvs and calculations for
# the Naive Bayes probability
#
# NOTES:
#	1- Need to loop for looking for the historical files
#	2- Need to create accessible function from outside to get:
#		a- begin and end lon/lats
#		b- sigmoid and 1-5 mapping
#		c- Count events in state
#
####################


import pandas as pd
import numpy as np


def runData(state="MD"):
	# need to do this on a loop for the files in our system
	data = pd.read_csv('Datasets/StormEvents_details-ftp_v1.0_d1950_c20170120.csv')
	data.columns = [x.strip() for x in data.columns]

	data = data[['STATE','YEAR','MONTH_NAME','INJURIES_DIRECT','INJURIES_INDIRECT', 'DEATHS_DIRECT','DEATHS_INDIRECT','BEGIN_LAT','BEGIN_LON','END_LAT','END_LON']]

	data['END_LON'].fillna(0.000, inplace=True)
	data['END_LAT'].fillna(0.000, inplace=True)
	data['BEGIN_LON'].fillna(0.000, inplace=True)
	data['BEGIN_LAT'].fillna(0.000, inplace=True)

	# datagram containing the differet event coordinates
	loc_data = data[['STATE','BEGIN_LAT','BEGIN_LON','END_LAT','END_LON']]

	# empty death and injury dataframe
	di_data = pd.DataFrame(columns=['STATE','COUNT','NUM_EVENTS'])

	# empty death and injury dataframe
	loc_data = pd.DataFrame(columns=['STATE','COUNT','NUM_EVENTS'])

	# Grabbing the data
	for curr_state in data['STATE'].unique():
		total = data.loc[data['STATE'] == curr_state, 'DEATHS_DIRECT'].sum() + data.loc[data['STATE'] == curr_state, 'DEATHS_INDIRECT'].sum() + data.loc[data['STATE'] == curr_state, 'INJURIES_DIRECT'].sum() + data.loc[data['STATE'] == curr_state, 'INJURIES_INDIRECT'].sum()

		num_event = data.loc[data['STATE']== curr_state].shape[0]
		t = pd.DataFrame([[curr_state, total, num_event]], columns=['STATE','COUNT','NUM_EVENTS'])
		di_data = pd.concat([di_data, t])

	return "Test OK"
	# need two csv one with state info and number of events, deaths and injuries, one with the lat and long

	# avergage each col by state for all categories

	# sum col and devide by nmber of rows - this is our score say 30 deaths in 4 events we have 30/4 and then use sigmoid to give a num from 0-1 and map it to range 1 - 5


def getGlobalRating():
	di = 0
	di2 = di_data.loc[di_data['STATE'] == curr_state, 'COUNT'].sum() / di_data.loc[di_data['STATE'] == curr_state, 'NUM_EVENTS'].sum()
	evt = 0
#	for curr_state in data['STATE'].unique():
#		di += di_data.loc[di_data['STATE'] == curr_state, 'COUNT'][0]
#		evt += di_data.loc[di_data['STATE'] == curr_state, 'NUM_EVENTS'][0]
#		di = di_data.loc[di_data['STATE'] == curr_state, 'COUNT'][0] / di_data.loc[di_data['STATE'] == curr_state, 'NUM_EVENTS'][0]


	print(di2,evt)

	return di2#/evt


def getStateRating(state):
	state_ave = di_data.loc[di_data['STATE'] == state, 'COUNT'][0] / di_data.loc[di_data['STATE'] == state, 'NUM_EVENTS'][0]

	print("state ave:", state_ave)

	print ("Global ave:",getGlobalRating())
	return dangerrate(state_ave)


def sigmoid(x):
    #squash the output between 0-1
    #using the sigmoid activation fucntion
	g=getGlobalRating()
	return  g/(x + g)


def dangerrate(x):
	x = sigmoid(x)
	print("SIGMOID:", x)
	if x>=0.8:
		return 1
	elif x<0.8 and x>=0.6:
		return 2
	elif x<0.6 and x>=0.4:
		return 3
	elif x<0.4 and x>=0.2:
		return 4
	elif x<0.2:
		return 5
