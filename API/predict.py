

import json
import numpy as np
import pickle

# #load json file for column data(needed for locating the location column)
# with open('data_columns.json', 'r') as f:
#     data_columns = json.load(f)
#     data_columns = data_columns['columns']

# #load pickle file
# with open('bengaluru_property_price_prediction_model.pickle', 'rb') as f:
#     model = pickle.load(f)

def predict_price(location,sqft,bath,bhk, model, data_columns):  
    """
    A function to predict the price based on location, square footage, number of bathrooms, number of bedrooms, a model, and data columns.
    """
    #Find the index of location column in data_columns
    #The value at that index in the feature array(referring to that location) will be set to 1 
    try:
        loc_index = data_columns.index(location.lower())
    except:
        loc_index = -1
    print(loc_index) 

    x = np.zeros(len(data_columns)) #feature array
    #setting values in the feature array as they correspond to the features in data_columns
    #'total_sqft', 'bath', 'bhk', '1st block jayanagar', .... etc.
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    #the input to predict function should be a 2D array of shape (1, n) 
    # where 1 is the sample size and n is the number of features
    return model.predict([x])[0]

#print(data_columns[:6])
# predicted_price =  predict_price('1st Phase JP Nagar',1000, 2, 2, model, data_columns)
# predicted_price = predict_price('Indira Nagar',1000, 3, 3, model, data_columns)
# print('predicted price: ', predicted_price, ' lakhs')