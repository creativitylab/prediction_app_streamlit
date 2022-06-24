import streamlit as st
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


@st.cache
def plot_histogram(data, x, height, width):
    """used to display histogram in the data visualization page"""
    # USED
    fig = px.histogram(data, x=x)
    fig.update_layout(bargap=0.2, height=height, width=width)

    return fig


@st.cache(allow_output_mutation=True)
def plot_line(data, x, y, height, width):
    # USED
    fig = px.line(data, x=x, y=y)

    fig.update_layout(bargap=0.05, height=height, width=width)

    return fig


@st.cache
def plot_scatter(data, x, y, height, width, margin, title_text):
    fig = px.scatter(
        data, x=x, y=y,
        trendline='ols',
        opacity=.5
    )

    fig.update_layout(bargap=0.05, height=height, width=width, title_text=title_text, margin=dict(t=margin,
                                                                                                  b=margin
                                                                                                  )
                      )
    return fig


@st.cache
def plot_heatmap(corr_matrix):
    fig = ff.create_annotated_heatmap(
        z=np.round(corr_matrix.values, 2),
        x=corr_matrix.index.tolist(),
        y=corr_matrix.columns.values.tolist(),
        hoverinfo="text",
        hovertext=np.round(corr_matrix.values, 2),
        showscale=True,
    )
    fig.update_layout(bargap=0.05, height=550, width=700)

    return fig
