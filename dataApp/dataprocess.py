###################
#
# File handling the processing of cvs and calculations for
# the Naive Bayes probability
#
# NOTES:
#    1- Need to loop for looking for the historical files
#    2- Need to create accessible function from outside to get:
#        a- begin and end lon/lats
#        b- sigmoid and 1-5 mapping
#        c- Count events in state
#
####################


import pandas as pd
import numpy as np
import math as mt
import os

from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn import metrics

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

#predictor
global mnb
#mnb = MultinomialNB()
mnb = GaussianNB()

# empty death and injury dataframe
global di_data
di_data = pd.DataFrame(columns=['STATE','COUNT','NUM_EVENTS', 'MONTH_NAME', 'CLASS'])

# empty location dataframe
global loc_data
loc_data = pd.DataFrame(columns=['STATE','MONTH_NAME','INJURIES_DIRECT','INJURIES_INDIRECT','DEATHS_DIRECT','DEATHS_INDIRECT','BEGIN_LAT','BEGIN_LON','END_LAT','END_LON'])

global state_events
state_events = {}

global total_inj
total_inj = {}

global total_evn
total_evn = {}

global state_names
state_names={'ALABAMA':0,
'ALASKA':1,
'ARIZONA':2,
'ARKANSAS':3,
'CALIFORNIA':4,
'COLORADO':5,
'CONNECTICUT':6,
'DELAWARE':7,
'FLORIDA':8,
'GEORGIA':9,
'HAWAII':10,
'IDAHO':11,
'ILLINOIS':12,
'INDIANA':13,
'IOWA':14,
'KANSAS':15,
'KENTUCKY':16,
'LOUISIANA':17,
'MAINE':18,
'MARYLAND':19,
'MASSACHUSETTS':20,
'MICHIGAN':21,
'MINNESOTA':22,
'MISSISSIPPI':23,
'MISSOURI':24,
'MONTANA':25,
'MONTANA':26,
'NEBRASKA':27,
'NEVADA':28,
'NEW HAMPSHIRE':29,
'NEW JERSEY':30,
'NEW MEXICO':31,
'NEW YORK':32,
'NORTH CAROLINA':33,
'NORTH DAKOTA':34,
'OHIO':35,
'OKLAHOMA':36,
'OREGON':37,
'PENNSYLVANIA':38,
'RHODE ISLAND':39,
'SOUTH CAROLINA':40,
'SOUTH DAKOTA':41,
'TENNESSEE':42,
'TEXAS':43,
'UTAH':44,
'VERMONT':45,
'VIRGINIA':46,
'WASHINGTON':47,
'WEST VIRGINIA':48,
'WISCONSIN':49,
'WYOMING':50,
'DISTRICT OF COLUMBIA':51,
'PUERTO RICO':52,}

#list of month names
global months
months = {"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12}


#################
### FUNCTIONS ###
#################

#squash the output between 0-1
def sigmoid(x):
    g=getGlobalRating()
    #g=1
    #return  g/(mt.exp(1.5-x) + g)
    #return g/(g + mt.exp(-(5*x -3)))
    return g/(g + x )


# get the danger index in our 1-5 range
def dangerrate(x):
    x = sigmoid(x)

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

# Get the global average (sum of averages)
def getGlobalRating():
    #return the number of deaths and incidents over the number of events
    #return loc_data['COUNT'].sum() / loc_data['NUM_EVENTS'].sum()
    return (loc_data['INJURIES_DIRECT'].sum() + loc_data['INJURIES_INDIRECT'].sum() + loc_data['DEATHS_DIRECT'].sum() + loc_data['DEATHS_INDIRECT'].sum())/loc_data.shape[0]

def getStateRating(state):

    state_ave = 0

    # if we have data for that state, grabb it
    if state in di_data['STATE'].unique():
        state_ave = di_data.loc[di_data['STATE'] == state,'COUNT'].values[0] /di_data.loc[di_data['STATE'] == state,'NUM_EVENTS'].values[0]

    else:
        return -1
    return dangerrate(state_ave)

#return the state events with locations in a dictionary
def getStateEvents(state="MD"):
    input1 = states.index(state)
    #check if we have data for the
    if input1 in di_data['STATE'].unique():
        return di_data.loc[di_data['STATE'] == input1].to_dict()

    else:
        return {}

#for some input get prediction
def getPrediction(state, month):
    input1 = [states.index(state),month]
    return mnb.predict([input1])



##############################################################################

print("""

Begining to parse files from Datasets directory.
Please Be Patient while we produce a model.

""")
# Main portion that takes care of data loading and processing from the historical files
#loop between our historical data files
for datafile in os.listdir(os.fsencode("Datasets")):

    print("Reading file: ", datafile.decode('utf-8'))

    # read the current file into datagram
    data = pd.read_csv("Datasets/"+datafile.decode('utf-8'))

    #clean the column names
    data.columns = [x.strip() for x in data.columns]

    #subset the data into our desired working data
    data = data[['STATE','MONTH_NAME','INJURIES_DIRECT','INJURIES_INDIRECT','DEATHS_DIRECT','DEATHS_INDIRECT','BEGIN_LAT','BEGIN_LON','END_LAT','END_LON']]

    #print(data[['INJURIES_DIRECT','INJURIES_INDIRECT','DEATHS_DIRECT','DEATHS_INDIRECT']])


    # grabbing the location data of the file
    loc_data = loc_data.append(data[['STATE','MONTH_NAME','INJURIES_DIRECT','INJURIES_INDIRECT','DEATHS_DIRECT','DEATHS_INDIRECT','BEGIN_LAT','BEGIN_LON','END_LAT','END_LON']],ignore_index=True)
    #print(loc_data[['INJURIES_DIRECT','INJURIES_INDIRECT','DEATHS_DIRECT','DEATHS_INDIRECT']])

    # remove cached file for space reasons
    del data

print("Cleaning up the data.")
#print(loc_data[['INJURIES_DIRECT','INJURIES_INDIRECT','DEATHS_DIRECT','DEATHS_INDIRECT']])

# clean the NaNs
loc_data['END_LON'].fillna(0.000, inplace=True)
loc_data['END_LAT'].fillna(0.000, inplace=True)
loc_data['BEGIN_LON'].fillna(0.000, inplace=True)
loc_data['BEGIN_LAT'].fillna(0.000, inplace=True)


print("Obtaining number of events per state.")


#get the number of events for each state by month
mydict = dict(tuple(loc_data.groupby('STATE')))
for st in mydict.keys():
    df = mydict[st]
    # print(df)
    for mo in df['MONTH_NAME'].unique():
        # print(mo)
        t = df.loc[df['MONTH_NAME'] == mo, ['INJURIES_DIRECT']].sum()[0]
        # print("T",t)
        t += df.loc[df['MONTH_NAME'] == mo, ['INJURIES_INDIRECT']].sum()[0]
        t += df.loc[df['MONTH_NAME'] == mo, ['DEATHS_DIRECT']].sum()[0]
        t += df.loc[df['MONTH_NAME'] == mo, ['DEATHS_INDIRECT']].sum()[0]

        if st not in total_inj.keys():
            total_inj[st]={}

        total_inj[st][mo]=t

        if st not in total_evn.keys():
            total_evn[st] = {}

        total_evn[st][mo] =  df.loc[df['MONTH_NAME'] == mo].shape[0]


print("Manipulating data into our dataframes.")
# grabbing the event data per state
for curr_row in loc_data.iterrows():

    #trick: change to object
    curr_row = curr_row[1]

    total = total_inj[curr_row['STATE']][curr_row['MONTH_NAME']]
    #print("total:", total)

    #number of events in that state
    num_event = total_evn[curr_row['STATE']][curr_row['MONTH_NAME']]

    #print("num_event: ",num_event)

    #get month name
    mon = months[curr_row['MONTH_NAME']]

    #get danger class
    rclass = dangerrate(total/num_event)

    #grab lons and lats
    blat = curr_row['BEGIN_LAT']
    blon = curr_row['BEGIN_LON']
    elat = curr_row['END_LAT']
    elon = curr_row['END_LON']

    st = state_names[curr_row['STATE']]

    # temporary dataframe to hold extracted data
    t = pd.DataFrame([[st, total, num_event, mon, blat, blon, elat, elon, rclass]], columns=['STATE','COUNT','NUM_EVENTS', 'MONTH_NAME','BEGIN_LAT','BEGIN_LON','END_LAT','END_LON', 'CLASS'])

    # adding the data to the main dataframe
    di_data = di_data.append(t,ignore_index=True)


del loc_data

# Now that the data massaging has been done
# we can move on to doing Machine Learning


print("Begining Machine Learning Model Preparations")


print("Splitting data..")
# filter out the data we want to use for training
X = di_data[['STATE', 'MONTH_NAME']]
y = di_data[['CLASS']].values[:,0]

#need to re-type to int from obj
y=y.astype('int')

#split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)



print("Training Model...")
#train model
mnb.fit(X_train, y_train)

y_predicted = mnb.predict(X_test)

print("Model Acuracy:")
print(metrics.accuracy_score(y_test,y_predicted))
