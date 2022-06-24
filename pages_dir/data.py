import streamlit as st
import pandas as pd
import os
from pages_dir import data_helper
from pages_dir import graphs
import numpy as np

import requests
import pandas as pd
import zipfile

from pages_dir.graphs import plot_heatmap

pd.set_option('precision', 2)

endpoint = "https://gitlab.com/api/v4/projects/35474313/jobs/artifacts/main/download?job=build-job"
# data = {"ip": "1.1.2.3"}
headers = {"Authorization": "Bearer glpat-3jZqLV1_yc-D7bX-v-5z"}


@st.cache
def get_raw_data():
    """
    This function return a pandas DataFrame with the raw data.
    """
    raw_df = pd.read_csv(os.path.join('process', 'last_step_pagination_110422.csv'))
    return raw_df


@st.cache
def get_clean_data():
    """
    This function returns a pandas DataFrame with the clean data.
    """
    clean_df = pd.read_csv(os.path.join('process', 'last_step_pagination_110422.csv'), infer_datetime_format=True)

    clean_df['TimeStamp'] = pd.to_datetime(clean_df['TimeStamp'], format="%Y-%m-%d %H:%M:%S")

    # remove data before 2021
    clean_df = clean_df[clean_df['TimeStamp'] > '2021-01-01']

    # add missing days
    clean_df = clean_df.resample('3h', on='TimeStamp').mean()

    sensor_column_names = ['pm25', 'pm1', 'pm10', 'co2', 'o3', 'cho2', 'no2', 'so2']
    clean_df = clean_df.interpolate(method='linear', axis=0).ffill().bfill()

    clean_df['TimeStamp'] = clean_df.index
    print("CLEAN DF ", clean_df.columns)

    return clean_df


@st.cache(allow_output_mutation=True)
def get_clean_data_fb():
    """
    This function return a pandas DataFrame with the clean data.
    """
    clean_df = pd.read_csv(os.path.join('process', 'last_step_pagination_110422.csv'), infer_datetime_format=True)

    clean_df['TimeStamp'] = pd.to_datetime(clean_df['TimeStamp'], format="%Y-%m-%d %H:%M:%S")

    # remove data before 2021
    clean_df = clean_df[clean_df['TimeStamp'] > '2021-01-01']

    clean_df = clean_df.resample('24h', on='TimeStamp').mean()

    sensor_column_names = ['pm25', 'pm1', 'pm10', 'co2', 'o3', 'cho2', 'no2', 'so2']

    clean_df = clean_df.interpolate(method='linear', axis=0).ffill().bfill()

    clean_df['TimeStamp'] = clean_df.index
    print("CLEAN DF ", clean_df.columns)

    return clean_df


raw_df = get_raw_data()
clean_df = get_clean_data()
clean_df_fb = get_clean_data_fb()


def create_visualization(data):
    """histogram and line plot"""
    sensor_names = list(data.columns)
    try:
        for item in ['TimeStamp', 'LocationLat', 'LocationLong', 'Source', 'Measurement']:
            sensor_names.remove(item)
    except ValueError:
        pass

    select_sensor = st.selectbox(
        'Select a sensor from the list',
        [i for i in sensor_names]
    )

    st.subheader('Histogram')

    fig = graphs.plot_histogram(data=data, x=select_sensor, height=500, width=950)
    st.plotly_chart(fig)

    st.subheader('Line Plot')

    fig = graphs.plot_line(data=data, x=data['TimeStamp'], y=select_sensor, height=500, width=700)

    st.plotly_chart(fig)


def app():
    st.title('Data')

    st.write("The following is the `air pollution` dataset.")

    type_of_data = st.radio(
        "Type of Data",
        ('Raw Data', 'Clean Data'),
        help='Data source that will be used in the analysis'
    )

    if type_of_data == 'Raw Data':
        data = raw_df.copy()
        st.dataframe(data)

    elif type_of_data == 'Clean Data':
        data = clean_df.copy()
        st.dataframe(data)
    else:
        data = raw_df.copy()

    with st.container():
        st.header('Descriptive Statistics\n')

        descriptive_df = data_helper.summary_table(data)
        st.dataframe(descriptive_df.style.format({"E": "{:.2f}"}))

    with st.expander("See further description of data"):
        st.dataframe(data.describe())

    create_visualization(data)

    st.subheader('Correlation Matrix')

    corr_matrix = data[['pm25', 'pm10', 'pm1', 'co2', 'o3', 'cho2', 'no2', 'so2']].corr()

    fig = plot_heatmap(corr_matrix)

    st.plotly_chart(fig)
