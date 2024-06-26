# Bengaluru House Price Prediction

<details>
<summary> <b>Training Linear Regression Model</b> </summary>

<br>
We get the data on Bengaluru house prices from Kaggle. The data contains about 13k rows and 9 columns about property prices. The columns are: 

*area_type,	availability,	location,	size,	society,	total_sqft,	bath, and	balcony	price*

The **price**(in lakhs or *100000 rupees*) is the **target variable** here. 

## Data Processing

The code for data cleaning is in [this notebook](https://github.com/rukshar69/bengaluru-house-prices/blob/main/training_model/bengaluru_property_dataprocessing.ipynb)
The aim is to create a simplified version of the data for linear regression.

- 5 columns: *'location', 'size', 'total_sqft', 'bath', 'price'* are kept
- Any row with *nan* values is dropped
- The *size* column, referring to the number of bedrooms, is processed to construct a new column *bhk*. The *size* column contains string values like `2 BHK`. We take only the number value and insert it in the *bhk* column. The *size* column is then dropped.
- Values in *total_sqft* were found to have range values like `1133 - 1384`. So, the column is modified to have only float values. For the previously mentioned range values, the average is taken and the range value is replaced with the average float value. Cases like `34.46Sq. Meter` are dropped to keep things simple.
- A new feature *price_per_sqft*(in rupees) is created through dividing the *price* column by *total_sqft*

### Dimensionality Reduction in the Location Column

- There are 1287 unique locations mentioned in the *location* column. The distribution of location values is very skewed

<div style="text-align:center;">
    <img src="https://github.com/rukshar69/bengaluru-house-prices/blob/main/training_model/location_density.png" alt="skewed dist" width="300" height="200">
</div>


- Given a large number of locations don't have much datapoints, we need to apply a dimensionality reduction technique here to reduce the number of locations. locations having less than 10 rows are tagged as **other** locations. So, the number of categories is reduced by a lot. When using one-hot encoding, it will help having fewer dummy columns. Now, the number of unique locations is *241*.

### Outlier Removal

- We consider that a normal bedroom size is 300 sqft. We remove properties where per bhk size is less than 300 sqft. We now have about *12.5k* rows.
- The **price per sqft** data reveals a significant price disparity, ranging from a minimum of 267 rupees to a maximum of around 175,000 rupees. To address this variation, **we identify and remove outliers within each location using the mean and standard deviation.** We keep properties for a particular location if the price per square foot is **within 1 standard deviation of the mean** for that location. We now have about *10.2k* rows.
- Let's consider another condition. **For the same location, the price of n bed apt should be greater than the mean of n-1 bed apt**. The datapoints failing to meet the condition are the outliers and will be removed. So for a given location, we build a dictionary of stats of price per sqft per bhk, i.e.
```
{
    
    '1' : {
        'mean': 4000,
        'std: 2000,
        'count': 34
    },

    '2' : {
        'mean': 4300,
        'std: 2300,
        'count': 22
    },    
}
```

- *Now we remove those n BHK apartments whose price_per_sqft is less than the mean price_per_sqft of n-1 BHK apartment*. We now have about *7.3k* rows.

![outlier removal](https://github.com/rukshar69/bengaluru-house-prices/blob/main/training_model/outlier_removal.jpg)

- We can see for **Rajaji Nagar and  Hebbal**, some of the 3 BHK properties with per sqft price less than the mean per sqft price of 2 BHK properties have been removed.

- We now consider a condition where an apartment with n bhk should have no more than n+2 bathrooms. It would be quite *absurd* or *erroneous* to have apartments where for n bhks there are more than n+2 baths. Such apartments are thus considered outliers and are removed from the dataset.

After such thorough cleaning, we move on to training a **Linear Regression** model using this clean and slimmed-down dataset.


## Training 

The code for training is in [this notebook](https://github.com/rukshar69/bengaluru-house-prices/blob/main/training_model/bengaluru_property_training.ipynb)

- There are 4 features: location,	total_sqft,	bath, and	bhk
    - The **price** column is the target variable.
- **One-hot Encoding** is performed for **location**, a string categorical feature. For each location, we get a new binary column. Its value is 1 if the datapoint belongs to that location otherwise it's 0. However, we drop the *other* location column since any datapoint belonging to the *other* category will have 0s in all other location columns.
- The test set is 20% of all datapoints.
- The **coefficient of determination**/**R^2 value** for the trained model is about **86%** on the test set, pretty good for a simplified dataset.

</details>

<details>
<summary> <b>FastAPI API and Streamlit Frontend</b> </summary>

![app structure](https://github.com/rukshar69/bengaluru-house-prices/blob/main/streamlit-app/house_price_predictor.jpg)

- The code for the FastAPI API is in [fastapi_app.py](https://github.com/rukshar69/bengaluru-house-prices/blob/main/API/fastapi_app.py)
- The code for the Streamlit frontend is in [streamlit_app.py](https://github.com/rukshar69/bengaluru-house-prices/blob/main/streamlit_app.py)

### FastAPI 

- The FastAPI API to call the property price prediction function(that uses the Linear Regression model) is **http://127.0.0.1:8000/predict_price**
- **PropertyInput** class (extends from pydantic BaseModel) is used to accept the input data from the user in the form of JSON. **PropertyOutput** class (extends from PropertyInput) is used to return the predicted price in the form of JSON.
- **PropertyInput** has 4 fields: location(str), area(float), bathrooms(integer), and bedrooms(integer).
- **PropertyOutput** has an additional field: predicted_price(float).
- The API calls a method `predict` that extracts the input data, passes it to the Linear Regression model, and returns the predicted price.
- To start the backend run the command: `uvicorn fastapi_app:app --reload`

### Streamlit App

- The frontend provides the 4 input fields: location, area, bathrooms, and bedrooms.
- The frontend calls the `predict_price` method after clicking the button. This method uses the `requests` library to call the `http://127.0.0.1:8000/predict_price` API and send the input data in the form of JSON.
    - The API returns the predicted price in the form of JSON. The frontend displays the predicted price.
- To start the frontend run the command: `streamlit run streamlit_app.py`
- The frontend can be viewed and used at the address `http://127.0.0.1:8501/`

<div style="text-align:center;">
    <img src="https://github.com/rukshar69/bengaluru-house-prices/blob/main/streamlit-app/bengaluru_streamlit.png" alt="streamlit app" width="500" height="500">
</div>

A gif of the using the frontend...

<div style="text-align:center;">
    <img src="https://github.com/rukshar69/bengaluru-house-prices/blob/main/streamlit-app/fastapi_streamlit_bengaluru_house_price.gif" alt="streamlit app" width="500" height="500">
</div>

</details>

# LinkedIn Articles
- [Classical ML with Classical Data: Linear Regression on Real Estate Price Prediction in Bengaluru](https://www.linkedin.com/pulse/classical-ml-data-linear-regression-real-estate-price-rukshar-alam-1omqc/?trackingId=O6pkfCjcSiS8oTMHghc%2FUA%3D%3D)
- [Deploying House Price Predictor using FastAPI](https://www.linkedin.com/pulse/deploying-house-price-predictor-using-fastapi-streamlit-rukshar-alam-nmbrc/)

# Reference

- [House Price Dataset](https://www.kaggle.com/datasets/amitabhajoy/bengaluru-house-price-data/data)
- [Linear Regression Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)
- [FastAPI model dump](https://docs.pydantic.dev/latest/concepts/serialization/#modelmodel_dump)
- [Helper Tutorial](https://github.com/codebasics/py/tree/master/DataScience/BangloreHomePrices)
