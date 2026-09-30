import os
import re
import joblib
import torch
from flask import Flask, request, jsonify, render_template
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load trained Classical ML model artifacts
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "sentiment_model.pkl")
tfidf_path = os.path.join(current_dir, "tfidf_vectorizer.pkl")

if not os.path.exists(model_path) or not os.path.exists(tfidf_path):
    raise FileNotFoundError("Missing sentiment_model.pkl or tfidf_vectorizer.pkl in directory.")

print("Loading Classical ML Sentiment Model (Logistic Regression + TF-IDF)...")
model = joblib.load(model_path)
tfidf = joblib.load(tfidf_path)

# Load Sarcasm/Irony Transformer
print("Loading RoBERTa Sarcasm Transformer...")
SARCASM_MODEL_NAME = "cardiffnlp/twitter-roberta-base-irony"
sarcasm_tokenizer = AutoTokenizer.from_pretrained(SARCASM_MODEL_NAME)
sarcasm_model = AutoModelForSequenceClassification.from_pretrained(SARCASM_MODEL_NAME)
sarcasm_model.eval()
print("All models initialized successfully!")

app = Flask(__name__)

SENTIMENT_MAPPING = {0: "Negative", 1: "Neutral", 2: "Positive"}

CONTRACTION_MAP = {
    r"\bdidn't\b": "did not",
    r"\bdoesn't\b": "does not",
    r"\bdon't\b": "do not",
    r"\bisn't\b": "is not",
    r"\bwasn't\b": "was not",
    r"\bweren't\b": "were not",
    r"\bcan't\b": "cannot",
    r"\bcouldn't\b": "could not",
    r"\bwon't\b": "will not",
    r"\bwouldn't\b": "would not",
    r"\bshouldn't\b": "should not",
    r"\bhasn't\b": "has not",
    r"\bhaven't\b": "have not",
    r"\bhadn't\b": "had not"
}

HTML_REGEX = re.compile(r"<.*?>")
URL_REGEX = re.compile(r"http\S+|www\S+")
NON_ALPHA_REGEX = re.compile(r"[^a-z\s]")
MULTI_SPACE_REGEX = re.compile(r"\s+")

def clean_text(text):
    text = str(text).lower()
    for pattern, repl in CONTRACTION_MAP.items():
        text = re.sub(pattern, repl, text)
    text = HTML_REGEX.sub(" ", text)
    text = URL_REGEX.sub(" ", text)
    text = NON_ALPHA_REGEX.sub(" ", text)
    return MULTI_SPACE_REGEX.sub(" ", text).strip()

def detect_sarcasm(text):
    inputs = sarcasm_tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
    with torch.no_grad():
        logits = sarcasm_model(**inputs).logits
        probs = torch.softmax(logits, dim=1).squeeze().tolist()
    
    # Class 0: Non-Irony / Non-Sarcastic
    # Class 1: Irony / Sarcastic
    prob_sarcastic = probs[1] * 100
    is_sarcastic = prob_sarcastic >= 50.0

    return is_sarcastic, prob_sarcastic

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        payload = request.get_json(force=True)
        raw_review = payload.get("review", "").strip()

        if not raw_review:
            return jsonify({"error": "Please enter a review to analyze."}), 400

        # 1. Sentiment Prediction (Logistic Regression + TF-IDF)
        cleaned_text = clean_text(raw_review)
        tfidf_vec = tfidf.transform([cleaned_text])
        raw_pred_code = model.predict(tfidf_vec)[0]
        sentiment_prob = model.predict_proba(tfidf_vec)[0][raw_pred_code] * 100
        sentiment_label = SENTIMENT_MAPPING[raw_pred_code]

        # 2. Sarcasm Detection (RoBERTa Transformer)
        is_sarcastic, sarcasm_confidence = detect_sarcasm(raw_review)

        # 3. Decision Logic
        sarcasm_explanation = "Literal tone detected."
        final_sentiment = sentiment_label

        if is_sarcastic:
            if sentiment_label == "Positive":
                final_sentiment = "Negative (Sarcasm Inverted)"
                sarcasm_explanation = "Positive vocabulary was used sarcastically to describe an unsatisfactory experience."
            elif sentiment_label == "Neutral":
                final_sentiment = "Negative (Sarcasm Inverted)"
                sarcasm_explanation = "Subtle sarcasm detected; sentiment shifted to negative."
            else:
                sarcasm_explanation = "Sarcasm confirms strong dissatisfaction."

        return jsonify({
            "original_ml_sentiment": sentiment_label,
            "final_sentiment": final_sentiment,
            "sentiment_confidence": f"{sentiment_prob:.1f}%",
            "is_sarcastic": "Yes" if is_sarcastic else "No",
            "sarcasm_confidence": f"{sarcasm_confidence:.1f}%",
            "sarcasm_explanation": sarcasm_explanation
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("\nStarting server on http://127.0.0.1:5000 ...")
    app.run(host="127.0.0.1", port=5000, debug=False)