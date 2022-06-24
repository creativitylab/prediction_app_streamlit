import streamlit as st
from pages_dir.data import clean_df
import os
import pandas as pd

from keras.preprocessing.sequence import TimeseriesGenerator
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import load_model

from pages_dir.helper_plot import plot_fb_data
from pages_dir.home import create_metrics

df_clean = clean_df.copy()


def model_lstm(selected_sensor='pm25'):
    print("LSTM")

    if st.sidebar.button('Predict'):
        with st.spinner('Loading the predictions...'):

            # todo change name
            model = load_model(os.path.join('pages_dir', 'models', 'lstm_model_' + str(selected_sensor) + '.h5'))

            df = df_clean.copy()
            df.index = df['TimeStamp']

            last_date = df['TimeStamp'].max()

            dates = pd.date_range(last_date, periods=7)
            dates = dates[dates > last_date]  # Drop start if equals last_date

            df2 = dates.to_frame(index=False, name='TimeStamp')

            df2 = pd.concat([df, df2])
            df2 = df2.reset_index(drop=True)
            df2.index = df2['TimeStamp']
            print('df22 ', df2)
            df2['pm25'][-5:] = df['pm25'][-5:]  # 0
            df2['pm1'][-5:] = df['pm1'][-5:]  # 0
            df2['pm10'][-5:] = df['pm10'][-5:]  # 0

            df = df2

            df = df[['pm25', 'pm1', 'pm10']]

            scaler = MinMaxScaler()
            data_scaled = scaler.fit_transform(df)

            features = data_scaled  # pm1	pm10
            if selected_sensor == 'pm25':
                target = data_scaled[:, 0]  # pm25 #todo change!
            elif selected_sensor == 'pm1':
                target = data_scaled[:, 1]  # pm1 #todo change!
            elif selected_sensor == 'pm10':
                target = data_scaled[:, 2]  # pm10 #todo change!

            x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=123,
                                                                shuffle=False)  # just pass features, not time
            win_length = 2  # random
            batch_size = 128  # 32  #training to be faster
            test_generator = TimeseriesGenerator(x_test, y_test, length=win_length, sampling_rate=1,
                                                 batch_size=batch_size)

            predictions = model.predict_generator(test_generator)

            df_pred = pd.concat([pd.DataFrame(predictions), pd.DataFrame(x_test[:, 1:][win_length:])], axis=1)
            df_pred.head()  # df with scaled values

            rev_trans = scaler.inverse_transform(df_pred)

            df_final = df[predictions.shape[0] * -1:]

            df_final['predicted ' + str(selected_sensor)] = rev_trans[:,
                                                            0]  # get only first column, pm10 predicted column
            print('df_final ', df_final)
            df_final['TimeStamp'] = df_final.index

            print("DF FINAL ", df_final)

            plot_fb_data(df_final, selected_sensor, 'predicted ' + str(selected_sensor), 'TimeStamp')

            df_final['predicted-actual'] = df_final['predicted ' + str(selected_sensor)] - df_final[selected_sensor]

            with st.expander("See metrics"):
                create_metrics(df_final, selected_sensor)


def app():
    """homepage of the app: plot and table"""
    st.title('LSTM')
    selected_sensor_lstm = st.sidebar.selectbox(
        'Choose sensor:',
        ('pm25', 'pm1', 'pm10')
    )
    st.sidebar.write('Chosen sensor: ', selected_sensor_lstm)
    model_lstm(selected_sensor=selected_sensor_lstm)
