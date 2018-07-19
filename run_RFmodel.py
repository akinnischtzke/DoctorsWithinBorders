

import pandas as pd
import numpy as np
import random

import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import sklearn.metrics
import sklearn.datasets

import pickle

def load_data(dir):

	# Load data from file
	
	data = pd.read_csv(dir)
	print("Model data size: ", data.shape)

	data.rename(columns={'Unnamed: 0':'county_fips'}, inplace=True)
	data.set_index(keys = 'county_fips', inplace=True)
	data.drop(labels=['State','County'], axis=1, inplace=True) # keeping all features for now

	return data


def split_data(data, test_perc):

	#Split into features and labels
	labels = data['HPSA Score'].values
	labels_list = ['HPSA Score']

	features = data.drop(labels=['HPSA Score'], axis=1) # keeping all features for now
	feature_list = list(features.columns) # Saving feature names for later use
	features = features.values # Convert to numpy array
	#print(feature_list)

	# Using Scikit-learn to split data into training and testing sets
	train_features, test_features, train_labels, test_labels = train_test_split(features, 
		labels, test_size = test_perc, random_state = 42)

	return train_features, test_features, train_labels, test_labels

def run_model(x_train, x_test, y_train, y_test):

	# Running a random forest model
	rf = RandomForestRegressor()
	rf.fit(x_train, y_train); 
	predictions = rf.predict(x_test) 
	errors_MAE = abs(predictions - y_test) # Calculate the absolute errors

	#Run k_fold cross-validation
	k_fold = sklearn.model_selection.KFold(5)
	scores = sklearn.model_selection.cross_val_score(rf, train_features, train_labels,cv=k_fold,scoring='neg_mean_absolute_error')
	print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

	pickle.dump(rf, open('finalized_model.sav', 'wb')) # save model for later use

	return predictions, errors_MAE

########

# Read in the (mostly) cleaned data for the model
basedir = 'https://raw.githubusercontent.com/akinnischtzke/DoctorsWithinBorders/master/hpsacounties_modeldata_cleaned.csv'
model_data = load_data(basedir)

# Split into training/test data
test_perc = 0.2
train_features, test_features, train_labels, test_labels = split_data(
	model_data, test_perc)

# Run RF regression model, return predicted HPSA values
predictions, errors_RF = run_model(train_features, test_features, 
	train_labels, test_labels)

#Save results
results = pd.DataFrame({'actual': test_labels,
	                       'predicted': predictions,
	                       'MAE': errors_RF,
	                       })

# Save model predictions & error to file
results.to_csv('model_results.csv')












