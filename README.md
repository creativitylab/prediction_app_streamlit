# About

    This application provides an overview over the pollutants from Brasov, Romania. It provides the ability to inspect the data and to forecast it.
    The data comes from several sensors, like particulate matter, ozone, carbon dioxide, nitrogen dioxide and others. 
    The menu contains:
    - Data 
    - Air quality
    - LSTM
    - Facebook Prophet
    - Choose Dates-Facebook Prophet
    - Metrics
    - Admin
    
# Deployed Application
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/creativitylabb/prediction_app_streamlit/main/main.py)

# Run the App

To run locally, clone the repository, go to the directory and install the requirements.

```
conda env update --file environment.yml --prune
```

Now, go to the terminal, from the main directory and run:

```
streamlit run main.py 
```
*OR*
```
streamlit run main.py --server.maxMessageSize=500
```