import argparse
from leia import SentimentIntensityAnalyzer

parser = argparse.ArgumentParser()
parser.add_argument("lame4_path", help="Noticias D-10 do ticker LAME4.", type=str)
parser.add_argument("varejo_path", help="Noticias do mercado VAREJO.", type=str)
parser.add_argument("nlp_score_path", help="Score obtido pelo modelo em arquivo.", type=str)
args = parser.parse_args()

"""

Análise de Sentimentos das notícias (D - 10) do ticker LAME4 e do seu mercado de 
atuação (varejo)

Utilização do Algoritmo VADER (Valence Aware Dictionary and sEntiment Reasoner) 
adaptado para textos em português por meio do fork LeIa (Léxico para Inferência Adaptada).

"""

# Contrução do corpus a ser analisado com base nos dois datasets

LAME4_file = open(args.lame4_path, "r")
LAME4_news = LAME4_file.read()
LAME4_file.close()

VAREJO_file = open(args.varejo_path, "r")
VAREJO_news = VAREJO_file.read()
VAREJO_file.close()

corpus = LAME4_news + VAREJO_news

sa = SentimentIntensityAnalyzer()

scores = sa.polarity_scores(corpus)

# Salva o score normalizado para posterior uso do modelo LSTM

score_file = open(args.nlp_score_path, "w")
score_file.write(str(scores["compound"]))
score_file.close()
