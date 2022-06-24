import os
import plotly.express as px
import streamlit as st
from elasticsearch import Elasticsearch
import pandas as pd
from pandas import json_normalize
import plotly.graph_objects as go
from datetime import datetime
import json

json_file = open(os.path.join('pages_dir', 'resources', 'credentials.json'))
json_data = json.load(json_file)


# @st.experimental_memo(ttl=600)
def get_es_result(username=json_data['username'], password=json_data['password'], sensor_name='pm10'):
    df = pd.DataFrame()
    es = Elasticsearch(['https://8f9677360fc34e2eb943d737b2597c7b.us-east-1.aws.found.io:9243/'],
                       http_auth=(username, password))

    # get last 24h pm25 data
    # TODO check for 24h: gte:now-24h
    query = {
        "range": {"TimeStamp": {"gte": "now-100h", "lte": "now", "format": "epoch_millis"}}
    }
    result = es.search(index="brasov-dev", q=sensor_name, body=
    {
        "query": query
    }
                       )

    df = df.append(json_normalize(result['hits']['hits']))
    return df


def create_plot(df):
    df = df.rename(columns={'_source.LocationLat': 'Latitude', '_source.LocationLong': 'Longitude',
                            '_source.Value': 'Sensor Value'})

    fig = px.density_mapbox(df, lat='Latitude', lon='Longitude', z='Sensor Value', radius=10, opacity=1,
                            center=dict(lat=45.657974, lon=25.601198), zoom=9.5,
                            # color_continuous_scale=color_codes,
                            mapbox_style="stamen-terrain")

    fig.update_layout(
        title='Heatmap'
    )
    return fig


def app():
    """homepage of the app: plot and table"""
    st.title('Air quality')
    st.markdown(
        '''This page shows the `values recorded` by the 
        `sensors` based on **longitude** and **latitude**, 
        in the last `24 hours`.''')

    sensor_name = st.sidebar.selectbox(
        'Choose sensor:',
        ('pm10', 'pm25', 'pm1', 'co2', 'cho2', 'o3', 'no2', 'so2'))
    # co2,cho2,o3,no2,so2
    st.write('You selected:', sensor_name)

    df = get_es_result(username=json_data['username'], password=json_data['password'], sensor_name=sensor_name)

    fig = create_plot(df)

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df[['_source.Source', '_source.Sensor', '_source.Value', '_source.LocationLat', '_source.LocationLong',
                     '_source.TimeStamp']])
