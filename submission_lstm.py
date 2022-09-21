# -*- coding: utf-8 -*-
"""Submission LSTM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rg9SGokG2xc6Xtl9Na5dD53j7lRFOH_f

**Nama : Wahyu Bagus Wicaksono**

**Grup : M07**

Import Semua Library yang dibutuhkan
"""

import numpy as np
import pandas as pd
from keras.layers import Dense, LSTM, Bidirectional
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

"""Menampilkan Data dari CSV dan mengubah tipedata dari Date ke datetime dan Volume ke float

Data yang digunakan : https://www.kaggle.com/datasets/varpit94/apple-stock-data-updated-till-22jun2021
"""

data_train = pd.read_csv('AAPL.csv')
# data_train.head(100)
data_train['Date'] =  pd.to_datetime(data_train['Date'])
data_train['Volume'] = data_train['Volume'].astype(float)

df = pd.DataFrame(data_train)
df

print(df.dtypes)

"""Menampilkan plot dari data High dengan sumbu X yaitu date dan Y adalah price"""

dates = data_train['Date'].values
high = data_train['High'].values


plt.figure(figsize=(15,5))
plt.plot(dates, high)
plt.title('All Time High 1980 - 2020',
          fontsize=20)
plt.xlabel('Date')
plt.ylabel('Price')

"""Membuat varibel yang digunakan untuk training data"""

cols = list(df)[1:7]
df_cols = df[cols].astype(float)

"""Menormalisasikan data dengan StandardScaler selain dengan StandardScaler kita juga bisa menggunakan MinMaxScaler"""

scaler = preprocessing.StandardScaler()
scalerData = scaler.fit(df_cols)
df_cols_scale = scalerData.transform(df_cols)

"""Merubah array dates ke tipe data float32 dan array high ke tipe data float32"""

dates = np.asarray(dates).astype('float32')
high = np.asarray(high).astype('float32')

"""Melakukan reshape terhadap array trainX dan trainY"""

trainX = []
trainY = []

n_f = 2 #Jumlah hari yang digunakan untuk memprediksi masa depan dari hari N
n_past = 3 #Jumlah hari kemaren yang digunakan untuk memprediksi masa depan dari hari N

for i in range(n_past, len(df_cols_scale) - n_f+1):
  trainX.append(df_cols_scale[i - n_past:i, 0:df_cols.shape[1]])
  trainY.append(df_cols_scale[i + n_f - 1:i + n_f,0])

trainX, trainY = np.array(trainX), np.array(trainY)

print(trainX.shape, trainY.shape)

"""Membangun model Sequential dengan LSTM"""

model = tf.keras.models.Sequential([
  tf.keras.layers.LSTM(256, activation='relu', return_sequences=True),
  tf.keras.layers.LSTM(128, activation='relu'),
  tf.keras.layers.Dropout(0.4),
  tf.keras.layers.Dense(30, activation="relu"),
  tf.keras.layers.Dense(10, activation="relu"),
  tf.keras.layers.Dropout(0.5),
  tf.keras.layers.Dense(1),
])

"""Membuat callbacks, jika MAE sudah dibawah 10%, maka train model akan berhenti"""

# Berhenti ketika MAE dibawah 10%
class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('mae')< 0.1):
      print("\nMAE kurang dari 10%")
      self.model.stop_training = True

callbacks = myCallback()

"""Latih model dengan mode.fit dan menyimpannya ke dalam variabel history guna memudahkan proses plotting"""

optimizer = tf.keras.optimizers.SGD(learning_rate=1.0000e-04, momentum=0.9)
model.compile(loss=tf.keras.losses.Huber(),
              optimizer=optimizer,
              metrics=["mae"])

history = model.fit(trainX,
                    trainY,
                    epochs=100,
                    validation_split=0.2, # Validation set sebesar 20% dari dataset
                    callbacks=[callbacks],
                    verbose=1)

"""Scatter plot Training dan Validation MAE"""

mae = history.history['mae']
val_mae = history.history['val_mae']
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(len(mae))

plt.plot(epochs, mae, 'r', label='Train MAE ')                
plt.plot(epochs, val_mae, 'b', label='Valid MAE')
plt.title('Train and Valid MAE')
plt.legend(loc=0)
plt.figure()                                                                      
plt.show()

plt.plot(epochs, loss, 'r', label='Train Loss ')                
plt.plot(epochs, val_loss, 'b', label='Valid Loss')
plt.title('Train and Valid Loss')
plt.legend(loc=0)
plt.figure()                                                                      
plt.show()