import time

import streamlit as st
import pandas as pd
from fbprophet import Prophet
from datetime import datetime

from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

from pages_dir import graphs
from pages_dir.data import clean_df

from pages_dir.helper_plot import plot_fb_data, convert_df

df_final = clean_df.copy()


def opt(sensor_name):
    """get options for second selection-multiple selection, except the sensor selected to be predicted"""
    predict_options_sel = ['pm25', 'pm1', 'pm10', 'co2', 'o3', 'cho2', 'no2', 'so2']
    predict_options_sel2 = predict_options_sel.copy()
    predict_options_sel2.remove(sensor_name)
    return predict_options_sel2


def create_metrics(result, selected_sensor):
    st.write('Maximum difference between predicted and actual values ', max(result['predicted-actual']))
    st.write('Miniumum difference between predicted and actual values ', min(result['predicted-actual']))
    mse = mean_squared_error(result[selected_sensor], result['predicted ' + str(selected_sensor)])  # not future
    r2 = r2_score(result[selected_sensor], result['predicted ' + str(selected_sensor)])
    mae = mean_absolute_error(result[selected_sensor], result['predicted ' + str(selected_sensor)])
    rmse = mean_squared_error(result[selected_sensor], result['predicted ' + str(selected_sensor)], squared=False)

    st.write("MSE ", mse)
    st.write("RMSE ", rmse)
    st.write("R2 ", r2)
    st.write("MAE ", mae)


def predict_based_on_selection(train_df, test_df, options, selected_sensor):
    if st.sidebar.button("Predict"):
        with st.spinner('Loading the predictions...'):

            train_df = train_df.rename({'TimeStamp': 'ds', selected_sensor: 'y'},
                                       axis='columns')
            test_df = test_df.rename({'TimeStamp': 'ds', selected_sensor: 'y'},
                                     axis='columns')
            train_df = train_df[['ds', 'y', *options]]

            test_df = test_df[['ds', 'y', *options]]

            model = Prophet(interval_width=0.9)
            for option in options:
                model.add_regressor(option, standardize=False)
            model.fit(train_df)

            forecast_initial = model.predict(test_df)
            forecast = forecast_initial[['ds', 'yhat']]

            forecast = forecast.reset_index(drop=True)
            test_df = test_df.reset_index(drop=True)

            result = pd.concat((forecast['yhat'], test_df), axis=1)
            result = result.rename(
                {'yhat': 'predicted ' + str(selected_sensor), 'y': selected_sensor, 'ds': 'date'},
                axis='columns')
            result['date'] = pd.to_datetime(result['date'])
            result['predicted-actual'] = result['predicted ' + str(selected_sensor)] - result[selected_sensor]

            csv = convert_df(result)

            fmt = "%Y-%m-%d"
            styler = result.style.format(
                {
                    "date": lambda t: t.strftime(fmt)
                }
            )

            st.dataframe(styler)

            st.download_button(
                "Download results",
                csv,
                "file.csv",
                "text/csv",
                key='download-csv'
            )
            plot_fb_data(result, selected_sensor, 'predicted ' + str(selected_sensor), 'date')

            with st.expander("See further analysis of the resulted predictions"):
                create_metrics(result, selected_sensor)
                fig = graphs.plot_scatter(data=result, x='predicted ' + str(selected_sensor),
                                          y=selected_sensor,
                                          height=500,
                                          width=600, margin=20, title_text='Predicted vs Actual')
                st.plotly_chart(fig)

        st.success('Done!')


def app():
    """homepage of the app: plot and table"""
    st.title('Choose Dates-Facebook Prophet')

    start_date = st.sidebar.date_input('start date', datetime(2022, 3, 12))
    end_date = st.sidebar.date_input('end date', datetime(2022, 4, 11))

    df_final['TimeStamp'] = pd.to_datetime(df_final['TimeStamp'])
    print('hello', type(time.strftime("%Y-%m-%d", time.strptime(str(df_final['TimeStamp'][0]), "%Y-%m-%d %H:%M:%S"))))
    print('hello', time.strftime("%Y-%m-%d", time.strptime(str(df_final['TimeStamp'][0]), "%Y-%m-%d %H:%M:%S")))
    # todo check here
    if pd.Timestamp(start_date) < df_final['TimeStamp'][0]:
        print('less, no data record')
        st.error(
            "Please choose another interval. There is no data recorded at the chosen period. \n Start date must be more recent than " + str(
                time.strftime("%Y-%m-%d", time.strptime(str(df_final['TimeStamp'][0]), "%Y-%m-%d %H:%M:%S"))))

    elif pd.Timestamp(end_date) > df_final['TimeStamp'][len(df_final) - 1]:
        print('more, no data record')
        st.error(
            "Please choose another interval. There is no data recorded at the chosen period. \n End date must be less than " + str(
                time.strftime("%Y-%m-%d", time.strptime(str(df_final['TimeStamp'][0]), "%Y-%m-%d %H:%M:%S"))))

    else:
        test_df = df_final[
            (df_final['TimeStamp'] >= pd.Timestamp(start_date)) & (df_final['TimeStamp'] <= pd.Timestamp(end_date))]
        train_df = df_final[(df_final['TimeStamp'] < pd.Timestamp(start_date))]

        predict_options_sel = ['pm25', 'pm1', 'pm10', 'co2', 'o3', 'cho2', 'no2', 'so2']

        selected_sensor = st.sidebar.selectbox(
            'Choose sensor',
            predict_options_sel)

        predict_options = opt(selected_sensor)

        st.sidebar.write('Chosen sensor: ', selected_sensor)

        options = st.sidebar.multiselect(
            'Choose what sensors to include in the multivariate',
            predict_options)

        st.sidebar.write('You selected:', options)
        if options == []:
            print('nothing here')
            st.error("Please choose at least a sensor to include in the multivariate predictions.")

        else:
            print('we can predict now')
            predict_based_on_selection(train_df, test_df, options, selected_sensor)
