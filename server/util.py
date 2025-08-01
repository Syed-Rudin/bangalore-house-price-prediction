import json
import pickle
import numpy as np 
import pandas as pd

__locations = None
__data_columns = None 
__model = None

def get_estimated_price(location, sqft, bhk, bath):

    input_df = pd.DataFrame(0, index=[0], columns=__data_columns)

    # Find the column index for the given location (e.g., '1st Phase JP Nagar')
    if location.lower() in __data_columns:
        input_df[location.lower()] = 1
    # Set the one-hot encoded location column to 1, if it's not an 'other' location
    # If loc_index is -1 (meaning it's an 'other' location), then all location dummy variables remain 0,
    # which correctly represents the 'other' category due to the dummy variable trap handling.

    # Set the 'sqft', 'bath', and 'bhk' values
    input_df['total_sqft'] = sqft
    input_df['bath'] = bath
    input_df['bhk'] = bhk

    return round(__model.predict(input_df)[0], 2)

def get_location_names():
    return __locations

def load_saved_artifacts():
    print("Loading saved artifacts...")
    global __data_columns 
    global __locations 

    with open("./artifacts/columns.json", 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]
    
    global __model
    with open("./artifacts/bangalore_home_prices_model.pickle", 'rb') as f:
        __model = pickle.load(f)
    
    print("Saved artifacts loaded!")

if __name__ == "__main__":
    load_saved_artifacts()
    # print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('testing', 1000, 2, 2))
    print(get_estimated_price('attibele', 1000, 2, 2))