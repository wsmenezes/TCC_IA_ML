from flask import Flask, jsonify, request, Response
from security import oauth, token_required
from keras.models import load_model
import pandas as pd
import numpy as np

class getModel ():
    def __init__(self, file:str)-> object:
        self.fileModel = file

    def model(self):        
        return load_model(self.fileModel)

app = Flask(__name__)
modelFile = "model.h5"
predictModel = getModel(modelFile).model()

# Recuperar nlp score compound processado anteriormente

nlp_score_file = open("score_compound.txt", "r")
nlp_score = nlp_score_file.read()
nlp_score_file.close()

@app.route('/predict', methods=['POST'])
@token_required
def root(user:str) -> object:
    try:
        data = request.json       

        X_test = np.array([[
            float(data['ABERTURA']),
            float(data['VARIACAO_(%)']),
            float(data['MINIMO']),
            float(data['MAXIMO']), 
            float(data['VOLUME']),
            float(nlp_score)
        ]])

        X_test = X_test.reshape(X_test.shape[0], 1, X_test.shape[1])

        predictmodel = predictModel.predict(X_test)
        
        return jsonify({"Predict": str(predictmodel[0])})
    except:
        return Response("erro", status=404, mimetype='application/json')

@app.route('/security', methods=['POST'])
def security() -> object:
    data = request.authorization
    if not data or 'username' not in data or 'password' not in data:
        return Response("erro", status=404, mimetype='application/json')
    else:
        return oauth(data['username'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)