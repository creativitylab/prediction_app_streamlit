import pandas as pd
import os
from fbprophet import Prophet

from matplotlib import pyplot as plt
import pickle

cur_path = os.path.dirname(__file__)

print(cur_path)

new_path = os.path.relpath('../../process/df_imputed_120422.csv', cur_path)

df = pd.read_csv(new_path, infer_datetime_format=True)
print(df)
df['TimeStamp'] = pd.to_datetime(df['TimeStamp'], format="%Y-%m-%d %H:%M:%S")
print(df)
df.index = df['TimeStamp']
print(df.index)
df.index.sort_values()

aq_df = df

# use pm1, pm10 to predict pm25
df_final = aq_df[['TimeStamp', 'pm25', 'pm1', 'pm10']].rename({'TimeStamp': 'ds', 'pm25': 'y'}, axis='columns')

print(df_final.head())


eighty_percent = int(80 / 100 * len(df_final))

train_df = df_final[:eighty_percent]
test_df = df_final[eighty_percent:]

model = Prophet(interval_width=0.9)
model.add_regressor('pm1', standardize=False)
model.add_regressor('pm10', standardize=False)
model.fit(train_df)

pickle.dump(model, open('fb_prophet_model_pm25.pkl', 'wb'))
# pickle.dump(model,open('fb_prophet_model_pm1.pkl','wb'))
# pickle.dump(model,open('fb_prophet_model_pm10.pkl','wb'))

forecast = model.predict(test_df)
forecast = forecast[['ds', 'yhat']]

resulted = pd.DataFrame()

forecast = forecast.reset_index(drop=True)
test_df = test_df.reset_index(drop=True)

result = pd.concat((forecast['yhat'], test_df), axis=1)

plt.plot(result['ds'], result['y'], color='red', label='actual')
plt.plot(result['ds'], result['yhat'], color='blue', label='predicted')
plt.legend()
plt.show()

train_df = train_df.reset_index(drop=True)

print('train_df ', train_df)
# FUTURE

df_forecast = model.make_future_dataframe(periods=5, freq='D')

df_final.reset_index(inplace=True)
df_forecast['y'] = df_final['y']
df_forecast['pm1'] = df_final['pm1']
df_forecast['pm10'] = df_final['pm10']
print('df_forecast ', df_forecast.tail())
forecast_future = model.predict(df_forecast)

fig1 = model.plot(forecast_future)
fig1.show()

fig2 = model.plot_components(forecast_future)  # yearly and weekly seasonality
fig2.show()

result['difference'] = result['yhat'] - result['y']

print('result', result)
