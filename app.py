from flask import Flask, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

analyzer = SentimentIntensityAnalyzer()

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    text = data['text']

    vs = analyzer.polarity_scores(text)
    sentiment = "positive" if vs['compound'] >= 0.05 else "negative" if vs['compound'] <= -0.05 else "neutral"

    return jsonify({
        'text': text,
        'sentiment': sentiment,
        'compound_score': vs['compound']
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 