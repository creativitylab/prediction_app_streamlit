# from fbprophet import Prophet
# import pandas as pd
# import numpy as np
# df=pd.read_csv('../../process/df_imputed_120422.csv')
# model = Prophet(interval_width=0.9)
#
# # df_copy=df.copy()
# df['ds']=df['TimeStamp']
# df['y']=df['pm25']
# model.fit(df)
#
#
# # df_forecast = model.make_future_dataframe(periods=5, freq='D', include_history=True)
# # print(df_forecast)
#
# last_date = df['TimeStamp'].max()
#
# dates=pd.date_range(last_date, periods=5)
# dates = dates[dates > last_date]  # Drop start if equals last_date
#
# df2=dates.to_frame(index=False, name='TimeStamp')
#
# df2['ds']=df2['TimeStamp']
# df2['y']=''#df['pm25']
# print(df2)
#
#
# df_final=pd.concat([df, df2])
# df_final=df_final.reset_index(drop=True)
#
#
# # df2= pd.DataFrame({'ds': dates2})
# print('df2 ',df_final)
# pred=model.predict(df2)
# print('pred ',pred)