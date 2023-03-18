from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from predict import *

app = Flask(__name__)   
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/model_select", methods=["POST"])
def model_select():
    data = request.get_json(force=True)
    model = data["model_k"]
    lyrics = str(data["lyrics_k"]).lower()
    
    ml_model_list = ["LR_ovr", "LR_mn", "NB_MN", "SVC"]
    transformer_model_list = ["bert-base-uncased_v2", "albert-large-v1_v2", "albert-large-v2", "distilbert-base-uncased_v2", "roberta-base_v2"]
    try:
        if model in ml_model_list:
            result = normal_ml(model, lyrics).capitalize()
        elif model in transformer_model_list:
            result = transformer(model, lyrics).capitalize()
        return jsonify(
            {
                "code": 201,
                "data": result,
                "message": "Success"
            }
        ), 201
    except:
        return jsonify(
            {
                "code": 404,
                "message": "Error"
            }
        ), 404
    
    
if __name__ == "__main__":
    app.run(debug=True)