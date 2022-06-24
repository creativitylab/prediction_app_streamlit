import streamlit as st
import pandas as pd
from plotly import graph_objs as go
from fbprophet import Prophet


def predict_fb(df, time_column):
    columns = df.columns[df.columns != time_column]

    predict_column = st.selectbox(
        'Select column to predict',
        (columns))

    st.write('You selected:', predict_column)

    options = [column for column in df.columns.tolist()]
    options.remove(time_column)

    options.remove(predict_column)
    print('selected to predict ', columns)
    print('the rest of columns', options)

    if st.button("Predict"):
        df.index = df[time_column]
        df.index.sort_values()
        df = df.interpolate(method='linear', axis=0).ffill().bfill()

        df.rename(columns={time_column: 'ds', predict_column: 'y'}, inplace=True)

        print('df is ', df.columns)
        print('df is ', df.head().to_string())

        chosen_percent = 80
        eighty_percent = int(chosen_percent / 100 * len(df))

        train_df = df[:eighty_percent]
        print('train_df ', len(train_df))
        test_df = df[eighty_percent:]
        print('test_df ', len(test_df))

        model = Prophet(interval_width=0.9)
        for option in options:
            model.add_regressor(option, standardize=False)

        model.fit(train_df)

        forecast_initial = model.predict(test_df)
        forecast = forecast_initial[['ds', 'yhat']]

        forecast = forecast.reset_index(drop=True)
        test_df = test_df.reset_index(drop=True)

        result = pd.concat((forecast['yhat'], test_df), axis=1)
        result = result.rename({'yhat': 'predicted ' + str(predict_column), 'y': predict_column, 'ds': 'date'},
                               axis='columns')
        result['date'] = pd.to_datetime(result['date'])
        result['predicted-actual'] = result['predicted ' + str(predict_column)] - result[predict_column]
        st.write("dataframe is \n ")
        st.dataframe(result)

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=result['date'], y=result['predicted ' + str(predict_column)], name='predicted'))
        fig1.add_trace(go.Scatter(x=result['date'], y=result[predict_column], name='actual'))
        fig1.layout.update(title_text='Predictions vs actual', xaxis_rangeslider_visible=False)
        st.plotly_chart(fig1)


def app():
    st.title('Custom Dataset-Facebook Prophet')
    uploaded_file = st.file_uploader("Choose a dataset")
    if uploaded_file is not None:  # read csv …
        print("uploaded")

        df = pd.read_csv(uploaded_file)
        print('df is ', df.head())

        time_column = st.selectbox(
            'Select Time column',
            (df.columns))

        st.write('You selected:', time_column)
        st.write(df)
        predict_fb(df, time_column)

    else:
        print("no csv")
