import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_path", help="Arquivo input historico ticker (raw).", type=str)
parser.add_argument("output_path", help="Arquivo output historico ticker (tratado)", type=str)
args = parser.parse_args()

# Histórico de cotações do ticker LAME4

df_ticker = pd.read_csv(args.input_path)

# Limpeza dos nomes das colunas do dataframe

df_ticker.rename(columns={'VARIAÇÃO': 'VARIACAO_(%)', 'MÍNIMO': 'MINIMO', 'MÁXIMO': 'MAXIMO'}, inplace=True)

# Tratamento dos valores numéricos para posterior conversão

df_ticker = df_ticker.replace(',','.', regex=True)
df_ticker['VOLUME'] = df_ticker['VOLUME'].replace('M','',regex=True)
df_ticker['VOLUME'] = df_ticker['VOLUME'].replace('B','',regex=True)

# Remoção de registros incompletos que atrapalham a análise.

# Dataframe stacking

bad_rows = df_ticker.stack().str.contains('n/d', na=False)

# Uso de boolean indexing para extração dos índices

rows_to_del = [x[0] for x in (bad_rows[bad_rows].index)]
df_ticker.drop(rows_to_del, inplace=True)

# Conversão dos dados do Dataframe para tipos apropriados de análise.

df_ticker['DATA'] = pd.to_datetime(df_ticker['DATA'], format='%d/%m/%Y')
df_ticker['ABERTURA'] = df_ticker['ABERTURA'].astype(float)
df_ticker['FECHAMENTO'] = df_ticker['FECHAMENTO'].astype(float)
df_ticker['VARIACAO_(%)'] = df_ticker['VARIACAO_(%)'].astype(float)
df_ticker['MINIMO'] = df_ticker['MINIMO'].astype(float)
df_ticker['MAXIMO'] = df_ticker['MAXIMO'].astype(float)
df_ticker['VOLUME'] = df_ticker['VOLUME'].astype(float)

# Salva Dataframe com dados pré-processados

df_ticker.to_csv(args.output_path, index=False)