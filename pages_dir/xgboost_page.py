from xgboost import XGBRegressor
import streamlit as st
from pages_dir.data import clean_df
import plotly.graph_objects as go
import numpy as np
import math
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from scipy.stats.stats import pearsonr


def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


def cv_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return (np.sqrt(np.sum(np.square(y_pred - y_true)) / (len(y_true) - 1)) / np.mean(y_true)) * 100


def smape(A, F):
    return 100 / len(A) * np.sum(2 * np.abs(F - A) / (np.abs(A) + np.abs(F)))


df_final = clean_df.copy()


def show_metrics(test_df, label, y_test):
    rmse_score_test = round(math.sqrt(mean_squared_error(test_df[label], test_df['predictions'])), 2)

    mape_score_test = round(mean_absolute_percentage_error(test_df[label], test_df['predictions']), 2)

    cv_score_test = round(cv_error(test_df[label], test_df['predictions']), 2)

    smape_score_test = round(smape(test_df[label], test_df['predictions']), 2)

    pearson_score_test = round(pearsonr(test_df[label], y_test)[0], 3)

    r_squared_score_test = round(r2_score(test_df[label], test_df['predictions']), 2)

    mse_score_test = round(np.mean((test_df[label] - test_df['predictions']) ** 2), 2)

    st.write('Test Score: %.2f RMSE' % (rmse_score_test))
    st.write('Test Score: %.2f MAPE' % (mape_score_test))
    st.write('Test Score: %.2f CV' % (cv_score_test))
    st.write('Test Score: %.2f SMAPE' % (smape_score_test))
    st.write('Test Score: %.2f R-Squared' % (r_squared_score_test))
    st.write('Test Score: %.2f MSE' % (mse_score_test))
    st.write('Pearson Score: %.3f' % (pearson_score_test))


def app():
    st.title("XGBoost")
    time_column = 'TimeStamp'
    df = df_final.drop(columns=['LocationLat', 'LocationLong'])

    columns = df.columns[df.columns != time_column]
    predict_column = st.selectbox(
        'Select column to predict',
        (columns))

    st.write('You selected:', predict_column)

    if st.button("Predict"):
        st.write("Start predicitons")

        df_corr = df.corr(method="pearson")

        df_corrH = df_corr[df_corr[predict_column] > 0.75]  # print correlation with wchich pm25 has greater than 0.5
        st.header('Correlation matrix to the selected sensor')
        st.write(df_corrH)

        df3 = df[df_corrH.index]

        df.index = df[time_column]
        st.header('Most correlated sensors to the selected one; values > 0.75')

        st.write(df3)
        print(df3.columns.to_list())

        test_df = df[int(80 / 100 * len(df)):]

        train_df = df[:int(80 / 100 * len(df))]

        features = df3.columns.to_list()  # ['pm10', 'pm25']
        target_column = predict_column  # 'pm10'

        X_train, y_train = train_df[features], train_df[target_column]
        X_test, y_test = test_df[features], test_df[target_column]

        reg = XGBRegressor(n_estimators=500, learning_rate=0.01)
        reg.fit(X_train,
                y_train,
                eval_set=[(X_train, y_train), (X_test, y_test)],
                eval_metric='mae')

        predictions = reg.predict(X_test)
        test_df['predictions'] = (predictions)
        test_df['actual-predicted'] = test_df[target_column] - test_df['predictions']

        st.header("Prediction plot")

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=test_df[time_column], y=test_df[target_column], name='Actual ' + str(target_column)))
        fig.add_trace(
            go.Scatter(x=test_df[time_column], y=test_df['predictions'], name='Predicted ' + str(target_column)))
        fig.layout.update(title_text='Predicted vs Actual Observations', xaxis_rangeslider_visible=False)
        st.plotly_chart(fig)

        with st.expander("See metrics"):
            show_metrics(test_df, target_column, y_test)

        with st.expander("See actual values vs predicitons"):
            st.dataframe(test_df[['actual-predicted', 'predictions', target_column]])
