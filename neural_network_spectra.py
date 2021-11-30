# -*- coding: utf-8 -*-
"""neural_network_spectra.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JjhURiSrRWfcXoWZI1pS5TCgC3iW5vm1
"""

'''Importar bibliotecas necessárias'''
import numpy as np
import matplotlib.pyplot as pp
from tensorflow import keras
from keras.models import Sequential
from keras.layers.core import Dense

'''Carregar dados de arquivo CSV, e separar fração para treino e teste'''
input_data = np.genfromtxt('input_noiseless.csv', delimiter=';')
output_data = np.genfromtxt('output_noiseless.csv', delimiter=';')
print("Tamanho de dados de entrada: ", len(input_data))
print("Tamanho de dados de saída: ", len(output_data))
x_train = input_data[:100]
x_test = input_data[100:]
print("Tamanho de matriz de treino: ", len(x_train))
print("Tamanho de matriz de teste: ", len(x_test))
print("Tamanho total de dados de treino: ", x_train.size)
print("Tamanho total de dados de teste: ", x_test.size)
y_train = output_data[:100]
y_test = output_data[100:]
input_shape_size = int(x_train.size/len(x_train))
print(input_shape_size)

'''Configurar parâmetros da rede neural'''
# change these values to experiment
epochs = 200         # number of times the full data trains the network params
batch_size = 100    # the amount of data which goes into the network at once
num_neurons = 25     # number of neurons required in middle layer

''' Criar modelo de rede neural, adicionando camadas, definindo número de neuros, ativação, medidas de erro e otimização'''
def get_model():
  model = Sequential()
  model.add(Dense(num_neurons, input_shape=(input_shape_size, ),  activation='relu'))
  model.add(Dense(num_neurons, input_shape=(num_neurons,), activation='relu'))
  model.add(Dense(num_neurons, input_shape=(num_neurons,), activation='relu'))
  model.add(Dense(2))
  print(model.summary())
  model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
  return model

''' Treinar modelo a partir de parâmetros especificados'''
def train_model(X, y, model, epochs, batch_size):
  h = model.fit(X, y, validation_split=0.2,
               epochs=epochs,
               batch_size=batch_size,
               verbose=1)
  pp.figure(figsize=(15,2.5))
  pp.plot(h.history['loss'])
  pp.title('Training loss wrt time')
  return model

''' Fazer a previsão de valores a partir de rede treinada e comparar valores com o esperado'''
def predict_model(X):
  prediction = model.predict(X)
  print("Valores: \n", y_test[:]/prediction*100)
  print("Média", np.mean(y_test[:]/prediction*100, axis=0))
  print("Desvio", np.std(y_test[:]/prediction*100, axis=0))

'''Gerar modelo'''
model = get_model()

'''Treinar modelo'''
model = train_model(x_train, y_train, model, epochs, batch_size)

'''Avaliar modelo'''
predict_model(x_test)