import streamlit as st
import requests; import json 

# Load locations from JSON file and sort alphabetically
with open("location_names.json", "r") as f:
    locations_data = json.load(f)
locations = sorted(locations_data["locations"])

# Function to call the FastAPI API and return the response
def predict_price(location, area, bedrooms, bathrooms):
    """
    A function that sends a POST request to a server to predict the price based on location, area, bedrooms, and bathrooms.

    Parameters:
    - location (str): The location of the property.
    - area (int): The area of the property in square feet.
    - bedrooms (int): The number of bedrooms in the property.
    - bathrooms (int): The number of bathrooms in the property.

    Returns:
    - dict: A JSON response containing the predicted price.
    """
    data = {"location": location, "area": area, "bedrooms": bedrooms, "bathrooms": bathrooms}
    response = requests.post("http://127.0.0.1:8000/predict_price", json=data)
    return response.json()

# Streamlit app
st.title("Bengaluru Property Price Prediction App")

# Input fields for property details
location = st.selectbox("Location", locations)
area = st.number_input("Area (sqft)", min_value=0)
bedrooms = st.number_input("Number of Bedrooms", min_value=0)
bathrooms = st.number_input("Number of Bathrooms", min_value=0)

# Button to trigger prediction
if st.button("Predict Price"):
    # Call the API and get the response
    prediction = predict_price(location, area, bedrooms, bathrooms)

    # Display the prediction results
    st.subheader("Prediction Results")
    st.write(f"**Predicted Price: {prediction['predicted_price']:.2f} Lakhs**")
    st.write(f"Location: {prediction['location']}")
    st.write(f"Area: {prediction['area']:.2f} sqft")
    st.write(f"Bedrooms: {prediction['bedrooms']}")
    st.write(f"Bathrooms: {prediction['bathrooms']}")
    
