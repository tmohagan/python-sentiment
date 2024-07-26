from flask import Flask, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask_cors import CORS
from functools import lru_cache
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
CORS(app, supports_credentials=True)

handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

analyzer = SentimentIntensityAnalyzer()

@lru_cache(maxsize=1000)
def get_sentiment(text):
    vs = analyzer.polarity_scores(text)
    sentiment = "positive" if vs['compound'] >= 0.05 else "negative" if vs['compound'] <= -0.05 else "neutral"
    return sentiment, vs['compound']

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    try:
        data = request.get_json()
        text = data['text']

        sentiment, compound_score = get_sentiment(text)

        return jsonify({
            'text': text,
            'sentiment': sentiment,
            'compound_score': compound_score
        })
    except Exception as e:
        app.logger.error(f"Error in analyze_sentiment: {str(e)}")
        return jsonify({'error': 'An error occurred while analyzing sentiment'}), 500

@app.route('/analyze_batch', methods=['POST'])
def analyze_sentiment_batch():
    try:
        data = request.get_json()
        texts = data['texts']

        results = []
        for text in texts:
            sentiment, compound_score = get_sentiment(text)
            results.append({
                'text': text,
                'sentiment': sentiment,
                'compound_score': compound_score
            })

        return jsonify(results)
    except Exception as e:
        app.logger.error(f"Error in analyze_sentiment_batch: {str(e)}")
        return jsonify({'error': 'An error occurred while analyzing sentiment batch'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)