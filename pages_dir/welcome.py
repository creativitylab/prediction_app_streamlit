import streamlit as st
import os
from PIL import Image


def app():
    st.title('Introduction')
    image = Image.open(os.path.join('pages_dir', 'resources', 'welcome.jpg'))
    st.image(image, caption='Air pollution')

    st.subheader('About')

    st.write("""
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
    
    """)

    st.subheader('Data')
    st.write(
        "The Data section provides the possibility to inspect the almost raw data and the clean data, for the several air quality sensors.")

    st.subheader('Custom Data-Explore')
    st.write('This section allows the inspection of a custom dataset, uploaded by the user.')

    st.subheader('Air quality')
    st.write(
        "The air quality section provides the values recorded by the sensors in the last couple of hours, in different latitude and longitude values, considered of interest.")

    st.subheader('LSTM')
    st.write(
        "LSTM provides the possibility to predict the values recorded by PM2.5, PM1 or PM10, over a set period of time."
        "\n The model was trained before, using 80% of data as train.")

    st.subheader('Facebook Prophet')
    st.write(
        "Facebook Prophet provides the possibility to predict the values recorded by the air sensors and to choose the train percentage."
        "\n When choosing *All* as an option, the algorithm takes into consideration the whole period of time since values were recorded.")

    st.write(
        "LSTM and Facebook Prophet provide the possibility to predict 5 days into the future, based on the previous recorded values.")
    st.write(
        "LSTM and Facebook Prophet provide the possibility to one sensor's values based on the other ones, being multivariate forecasts.")

    st.subheader('Choose Dates-Facebook Prophet')
    st.write(
        'This section allows the user to choose a certain period when the predictions are made. Also, the user can choose what sensors to be included in the multivariate forecast.')

    st.subheader('Custom Dataset-Facebook Prophet')
    st.write('This section allows the user to test the Facebook Prophet algorithm on his own dataset.')

    st.subheader('XGBoost')
    st.write(
        'This section allows the user to train the data using XGBoost algorithm and inspect the prediction results.')

    st.subheader('Metrics')
    st.write('Description of the used metrics to establish the performance of the used models.')

    st.subheader('Admin')
    st.write(
        'Section used to trigger some background processes, like updating the data, running the models. Requires authorization.')
