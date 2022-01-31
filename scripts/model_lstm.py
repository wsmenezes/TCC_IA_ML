import pandas as pd
import argparse
from sklearn.model_selection import TimeSeriesSplit
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument("input_path", help="Arquivo input historico ticker (tratado).", type=str)
parser.add_argument("output_path", help="Arquivo output modelo em formato H5", type=str)
args = parser.parse_args()

# Histórico de cotações do ticker LAME4

df_ticker = pd.read_csv(args.input_path)

# Separação de DataFrames para as variáveis features e a variável classe.

features = ['ABERTURA','VARIACAO_(%)','MINIMO','MAXIMO','VOLUME','SCORE_D-10']
df_features = df_ticker[features]
df_classe = df_ticker['FECHAMENTO']

# Definindo o conjunto de treinamento e testes usando TimeSeriesSplit.

timesplit= TimeSeriesSplit(n_splits=10)
for train_index, test_index in timesplit.split(df_features):
        X_train, X_test = df_features[:len(train_index)], df_features[len(train_index): (len(train_index)+len(test_index))]
        y_train, y_test = df_classe[:len(train_index)].values.ravel(), df_classe[len(train_index): (len(train_index)+len(test_index))].values.ravel()

# Transformando a estrutura dos dados para compatibilidade de entrada na RNN LSTM.

trainX =np.array(X_train)
testX =np.array(X_test)
X_train = trainX.reshape(X_train.shape[0], 1, X_train.shape[1])
X_test = testX.reshape(X_test.shape[0], 1, X_test.shape[1])

# Construindo o modelo da RNN LSTM.

lstm = Sequential()
lstm.add(LSTM(32, input_shape=(1, trainX.shape[1]), activation='relu', return_sequences=False))
lstm.add(Dense(1))
lstm.compile(loss='mean_squared_error', optimizer='adam')

# Treinamento da RNN LSTM.

history = lstm.fit(X_train, y_train, epochs=300, batch_size=8, verbose=1, shuffle=False)

# Salvar o modelo e pesos em formato H5 (preparado para chamada API)

lstm.save(args.output_path)
