import pandas as pd
from datetime import datetime

df = pd.read_csv('air_dataset.csv')

df.drop('Unnamed: 0', axis=1, inplace=True)

for sensor_name in df['Sensor'].unique():
    df[sensor_name] = df['Value'][df['Sensor'] == sensor_name]

df = df.drop(['index', 'type', 'Sensor', 'Value', 'id', 'score'], axis=1)

df['TimeStamp'] = df['TimeStamp'].apply(lambda x: datetime.utcfromtimestamp(x / 1000).strftime('%Y-%m-%d %H:%M:%S'))


gk = df.groupby('TimeStamp')

print(gk.first())
gk.first().to_csv('last_step_pagination_110422.csv')



# df.to_csv('air_quality_final.csv')
#TODO RUN THIS AFTER PAGINATION
#step 2


#TODO THIS IS THE GOOD SECOND STEP!!!!!!!!!