!pip install pandas
!pip install numpy
!pip install pickle
!pip install torch
!pip install transformers

import pandas as pd
import numpy as np
import transformers
import os, warnings, pickle, torch
warnings.filterwarnings('ignore')
from transformers import BertTokenizer

def emotion(result):
    emotions_map = {
        "0" : "anger",
        "1" : "boredom",
        "2" : "empty",
        "3" : "enthusiasm",
        "4" : "fear",
        "5" : "fun",
        "6" : "happiness",
        "7" : "happy",
        "8" : "hate",
        "9" : "love",
        "10" : "neutral",
        "11" : "relief",
        "12" : "sadness",
        "13" : "worry"
    }
    
    return emotions_map[str(result[0])]

def normal_ml(selected_model, lyrics):
    # File and folder paths
    model_dir = os.path.join(os.getcwd(), 'models/ml')
    model_dict = {
        "LR_ovr" : "logistic_regression-ovr-c1_emotions.pkl",
        "LR_mn" : "logistic_regression-multinomial-c1_emotions.pkl",
        "NB_MN" : "multinomialNB_emotions.pkl",
        "SVC" : "linear_svc_emotions.pkl",
    }
    vect = "cv (selected) emotions.pkl"
    
    # Load count vectorizer
    cv = pickle.load(open(os.path.join(model_dir, vect), 'rb'))
    
    # Load model 
    model = pickle.load(open(os.path.join(model_dir, model_dict[selected_model]), 'rb'))
    
    # Vectorize lyrics
    lyrics_vect = cv.transform([lyrics]).toarray()
    
    # Predict emotion
    result = model.predict(lyrics_vect)
    return emotion(result)
    

def transformer(selected_model, lyrics):
    model_dir = os.path.join(os.getcwd(), 'models/transformers')
    models = [(transformers.BertForSequenceClassification, transformers.BertTokenizer, 'bert-base-uncased_v2'),
                (transformers.AlbertForSequenceClassification, transformers.AlbertTokenizerFast, 'albert-large-v1_v2'),
                (transformers.AlbertForSequenceClassification, transformers.AlbertTokenizerFast, 'albert-large-v2'),
                (transformers.DistilBertForSequenceClassification, transformers.DistilBertTokenizerFast, 'distilbert-base-uncased_v2'),
                (transformers.RobertaForSequenceClassification, transformers.RobertaTokenizer, 'roberta-base_v2')]
    
    model_class = ""
    tokenizer_class = ""
    pretrained_weights = ""
    for model, tokenizer, model_path in models:
        if selected_model == model_path:
            model_class = model
            tokenizer_class = tokenizer
            pretrained_weights = model_path
        
    saved_dir = os.path.join(model_dir, pretrained_weights)
    # Load pretrained model/tokenizer
    tokenizer = tokenizer_class.from_pretrained(saved_dir)
    model = model_class.from_pretrained(saved_dir)
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    # Copy the model to the GPU.
    model.to(device)
    predict_emotions = []
    
    # Tokenize lyrics
    encoded = tokenizer(lyrics, padding=True, truncation=True)
    
    # Predict emotion
    predict_emotions.append(to_check_result(encoded, model, device))
    return emotion(predict_emotions)
        
def to_check_result(test_encoding, model, device):
    input_ids = torch.tensor(test_encoding["input_ids"]).to(device)
    attention_mask = torch.tensor(test_encoding["attention_mask"]).to(device)
    with torch.no_grad():
        output = model(input_ids.unsqueeze(0), attention_mask=attention_mask.unsqueeze(0))
    return np.argmax(output[0].to("cpu").numpy())
    
