from flask import Flask, jsonify, request, Response
from configuration import getModel
from security import oauth, token_required

app = Flask(__name__)
modelFile = open("model.pkl", 'rb')
predictModel = getModel(modelFile).model()

@app.route('/predict', methods=['POST'])
@token_required
def root(user:str) -> object:
    try:
        data = request.json
        predictmodel = predictModel.predict([[
            float(data['ABERTURA']), 
            float(data['MINIMO']), 
            float(data['MAXIMO']), 
            float(data['VOLUME'])
        ]])
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