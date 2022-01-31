import pandas as pd
import argparse
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

parser = argparse.ArgumentParser()
parser.add_argument("input_path", help="Arquivo input historico ticker (tratado).", type=str)
parser.add_argument("output_path", help="Arquivo output modelo em formato pickle", type=str)
args = parser.parse_args()

# Histórico de cotações do ticker LAME4

df_ticker = pd.read_csv(args.input_path)

# Obtenção de novos DataFrames para features e para classe.

features = ['ABERTURA', 'MINIMO','MAXIMO', 'VOLUME']
df_feature = df_ticker[features]
df_classe = df_ticker['FECHAMENTO']

# Separação dos dados para treinamento e teste.

X_treino, X_teste, y_treino, y_teste = train_test_split(df_feature, df_classe, random_state=42)

# Criação do modelo e treinamento.

lr_model = LinearRegression()

lr_model.fit(X_treino, y_treino)

#Salvar modelo em formato pickle (preparado para chamada API)

pickle.dump(lr_model, open(args.output_path, 'wb'))