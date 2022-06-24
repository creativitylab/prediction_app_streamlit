from plotly import graph_objs as go
import streamlit as st


def plot_fb_data(result, y, yhat, ds):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=result[ds], y=result[y], name=y))
    fig.add_trace(go.Scatter(x=result[ds], y=result[yhat], name=yhat))
    fig.layout.update(title_text='Predicted vs Actual Observations', xaxis_rangeslider_visible=False)
    st.plotly_chart(fig)


@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')
