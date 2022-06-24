import os
from fbprophet import Prophet
import pickle


def create_models(aq_df,sensor_name):
    options = ['pm25', 'pm1', 'pm10']
    options.remove(sensor_name)
    # use pm1, pm10 to predict pm25
    df_final = aq_df[['TimeStamp', 'pm25', 'pm1', 'pm10']].rename({'TimeStamp': 'ds', sensor_name: 'y'}, axis='columns')

    print(df_final.head())

    eighty_percent = int(80 / 100 * len(df_final))

    train_df = df_final[:eighty_percent]
    test_df = df_final[eighty_percent:]

    model = Prophet(interval_width=0.9)
    model.add_regressor(options[0], standardize=False)
    model.add_regressor(options[1], standardize=False)
    model.fit(train_df)

    pickle.dump(model, open(os.path.join('pages_dir','models','fb_prophet_model_' + str(sensor_name) + '.pkl'), 'wb'))
