from fastapi import FastAPI, Body
from pydantic import BaseModel
import json, pickle
from predict import predict_price

#load json file for column data(needed for locating the location column)
with open('data_columns.json', 'r') as f:
    data_columns = json.load(f)
    data_columns = data_columns['columns']

#load pickle file
with open('bengaluru_property_price_prediction_model.pickle', 'rb') as f:
    model = pickle.load(f)

app = FastAPI()


# Define a model class to hold the input data
class PropertyInput(BaseModel):
    location: str
    area: float
    bedrooms: int
    bathrooms: int

class PropertyOutput(PropertyInput):
    predicted_price: float

@app.post("/predict_price")
def predict(input_data: PropertyInput):
    input_data = input_data.model_dump()
    predicted_price = predict_price(input_data['location'], input_data['area'], input_data['bathrooms'], input_data['bedrooms'],  model, data_columns)
    #create a PropertyOutput object with the predicted price
    output = PropertyOutput(location=input_data['location'], area=input_data['area'], bedrooms=input_data['bedrooms'], bathrooms=input_data['bathrooms'], predicted_price=predicted_price)
    return output

#CLI for running this app
#uvicorn fastapi_app:app --reload
# http://127.0.0.1:8000/docs#/