import pandas as pd
from fbprophet import Prophet
import streamlit as st
import pickle
import os
from plotly import graph_objs as go

# Plot raw data
from pages_dir.data import clean_df_fb as clean_df

from pages_dir.helper_plot import convert_df, plot_fb_data
from pages_dir.home import create_metrics

df_final = clean_df.copy()


# @st.cache
def predict_future_fb(selected_sensor='pm25'):
    # predict pm25 using 80% training data
    if selected_sensor == 'pm25':
        fb_prophet_model = pickle.load(
            open(os.path.join('pages_dir', 'models', 'fb_prophet_model_pm25.pkl'), 'rb'))  # predicts pm25
    elif selected_sensor == 'pm1':
        fb_prophet_model = pickle.load(
            open(os.path.join('pages_dir', 'models', 'fb_prophet_model_pm1.pkl'), 'rb'))  # predicts pm1
    elif selected_sensor == 'pm10':
        fb_prophet_model = pickle.load(
            open(os.path.join('pages_dir', 'models', 'fb_prophet_model_pm10.pkl'), 'rb'))  # predicts pm10
    else:
        fb_prophet_model = pickle.load(
            open(os.path.join('pages_dir', 'models', 'fb_prophet_model_pm25.pkl'), 'rb'))  # predicts pm25

    # future
    eighty_percent = int(80 / 100 * len(df_final))
    # selected_sensor = 'pm25'
    df_final_renamed = df_final[['TimeStamp', 'pm25', 'pm1', 'pm10']].rename({'TimeStamp': 'ds', selected_sensor: 'y'},
                                                                             axis='columns')
    test_df = df_final_renamed[eighty_percent:]

    # predict for next 5 days
    test_length = len(test_df) + 5

    df_forecast = fb_prophet_model.make_future_dataframe(periods=test_length, freq='D', include_history=True)
    test_df.reset_index(inplace=True)

    df_forecast["y"] = df_final_renamed['y']

    if 'pm25' not in df_final_renamed.columns:
        df_forecast['pm1'] = df_final_renamed['pm1']
        df_forecast['pm10'] = df_final_renamed['pm10']

        df_forecast['pm1'][-5:] = df_final_renamed['pm1'][-5:]  # 0
        df_forecast['pm10'][-5:] = df_final_renamed['pm10'][-5:]  # 0

    if 'pm1' not in df_final_renamed.columns:
        df_forecast['pm25'] = df_final_renamed['pm25']
        df_forecast['pm10'] = df_final_renamed['pm10']

        df_forecast['pm25'][-5:] = df_final_renamed['pm25'][-5:]  # 0
        df_forecast['pm10'][-5:] = df_final_renamed['pm10'][-5:]  # 0

    if 'pm10' not in df_final_renamed.columns:
        df_forecast['pm1'] = df_final_renamed['pm1']
        df_forecast['pm25'] = df_final_renamed['pm25']

        df_forecast['pm1'][-5:] = df_final_renamed['pm1'][-5:]  # 0
        df_forecast['pm25'][-5:] = df_final_renamed['pm25'][-5:]  # 0

    df_forecast['y'][-5:] = df_final_renamed['y'][-5:]  # 0
    df_test = df_forecast[-5:]
    print('df_forecast for next 5 days \n', df_test)  # get only test data

    print('test_df\n', test_df)

    # predict on test data
    forecast_data = fb_prophet_model.predict(df_test)

    return forecast_data


def all_data(selected_sensor):
    """make predictions for all given data-fb prophet"""
    options = ['pm25', 'pm1', 'pm10']
    options.remove(selected_sensor)
    print('not_selected', options)
    print('selected', selected_sensor)

    chosen_percent = st.sidebar.slider(
        'Train percentage?',
        75, 85, value=80)
    st.sidebar.write('Chosen train percentage:', chosen_percent)

    aq_df = clean_df

    if st.sidebar.button('Predict'):
        with st.spinner('Loading the predictions...'):
            aq_df['TimeStamp'] = pd.to_datetime(aq_df['TimeStamp'], format="%Y-%m-%d %H:%M:%S")

            aq_df.index = aq_df['TimeStamp']

            aq_df.index.sort_values()

            # # use pm1, pm10 to predict pm25
            df_final = aq_df[['TimeStamp', 'pm25', 'pm1', 'pm10']].rename({'TimeStamp': 'ds', selected_sensor: 'y'},
                                                                          axis='columns')

            df_final.set_index('ds')[['y', options[0], options[1]]].plot()  # pm25,pm1,pm10

            eighty_percent = int(chosen_percent / 100 * len(df_final))

            train_df = df_final[:eighty_percent]
            test_df = df_final[eighty_percent:]

            model = Prophet(interval_width=0.9)
            model.add_regressor(options[0], standardize=False)
            model.add_regressor(options[1], standardize=False)
            model.fit(train_df)

            forecast_initial = model.predict(test_df)
            forecast = forecast_initial[['ds', 'yhat']]

            forecast = forecast.reset_index(drop=True)
            test_df = test_df.reset_index(drop=True)

            result = pd.concat((forecast['yhat'], test_df), axis=1)
            result = result.rename({'yhat': 'predicted ' + str(selected_sensor), 'y': selected_sensor, 'ds': 'date'},
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

            with st.expander("See more plots"):
                fig2 = model.plot_components(forecast_initial)
                st.write(fig2)
                create_metrics(result, selected_sensor)
        st.success('Done!')


def app():
    """homepage of the app: plot and table"""
    st.title('Facebook Prophet')

    selected_sensor = st.sidebar.selectbox(
        'What sensor to predict?',
        ('pm25', 'pm1', 'pm10')
    )
    st.sidebar.write('Chosen sensor: ', selected_sensor)

    opt = st.sidebar.selectbox(
        'What data you want to predict?',
        ('All', '5 days in the future'))

    if opt == 'All':
        all_data(selected_sensor)

    if opt == "5 days in the future":
        if st.sidebar.button('Predict'):
            with st.spinner('Loading the predictions...'):
                future_fb_df = predict_future_fb(selected_sensor=selected_sensor)

                fmt = "%Y-%m-%d"
                result = future_fb_df.copy()
                result = result.rename({'yhat': 'predicted', 'ds': 'date'},
                                       axis='columns')

                styler = result[['predicted', 'date']][-5:].style.format(
                    {
                        "ds": lambda t: t.strftime(fmt)
                    }
                )

                st.dataframe(styler)

                fig1 = go.Figure()
                fig1.add_trace(go.Scatter(x=result['date'][-5:], y=result['predicted'][-5:], name='pm25'))
                fig1.layout.update(title_text='Prediction for 5 days into the future', xaxis_rangeslider_visible=False)
                st.plotly_chart(fig1)
