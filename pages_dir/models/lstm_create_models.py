import pandas as pd
import os
from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import TimeseriesGenerator
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
from keras.layers.recurrent import LSTM
from keras.layers.core import Dense, Flatten


# plot loss and val_loss
def plot_loss(history, epochs):
    loss_train = history.history['loss']
    loss_val = history.history['val_loss']
    no_epochs = range(epochs)
    plt.plot(no_epochs, loss_train, 'g', label='Training loss')
    plt.plot(no_epochs, loss_val, 'b', label='validation loss')
    plt.title('Training and Validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()


def create_model_lstm(df, column_index, sensor_name, epochs):
    scaler = MinMaxScaler()  # scale data
    data_scaled = scaler.fit_transform(df)

    features = data_scaled  # pm25 pm1	pm10
    target = data_scaled[:, column_index]  # target sensor to be predicted

    # target = data_scaled[:, 0]  # pm25
    # target = data_scaled[:, 1]  # pm1
    # target = data_scaled[:, 2]  # pm10

    x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=123,
                                                        shuffle=False)
    df.index = pd.to_datetime(df.index)

    win_length = 1
    batch_size = 24

    num_features = len(df.columns)  # features used in model

    train_generator = TimeseriesGenerator(x_train, y_train, length=win_length, sampling_rate=1, batch_size=batch_size)
    test_generator = TimeseriesGenerator(x_test, y_test, length=win_length, sampling_rate=1, batch_size=batch_size)

    epoch = 400
    batch_size = 24
    lr = 0.001

    model = Sequential()

    model.add((LSTM(units=32, return_sequences=True, input_shape=(win_length, num_features), activation='relu')))
    model.add((LSTM(units=16, return_sequences=True, activation='relu')))

    model.add(Flatten())
    model.add(Dense(units=1, activation='sigmoid'))

    adam = tf.optimizers.Adam(lr=lr)
    model.compile(loss='mean_squared_error', optimizer=adam)

    history = model.fit(train_generator, validation_data=test_generator, epochs=epoch, batch_size=batch_size, verbose=1,
                        shuffle=False)
    model.summary()

    plot_loss(history, epochs)

    model.evaluate_generator(test_generator, verbose=0)  # evaluate model with test data

    model.save(
        os.path.join('pages_dir', 'models',
                     'lstm_model_' + str(sensor_name) + '.h5'))  # creates a HDF5 file 'my_model.h5'
