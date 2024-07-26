from flask import Flask, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask_cors import CORS
from functools import lru_cache

app = Flask(__name__)
CORS(app, supports_credentials=True)

try:
    analyzer = SentimentIntensityAnalyzer()
except Exception as e:
    print(f"Error initializing SentimentIntensityAnalyzer: {str(e)}")
    # You might want to raise an exception here or handle it appropriately

@lru_cache(maxsize=1000)
def get_sentiment(text):
    vs = analyzer.polarity_scores(text)
    sentiment = "positive" if vs['compound'] >= 0.05 else "negative" if vs['compound'] <= -0.05 else "neutral"
    return sentiment, vs['compound']

@app.route('/')
def home():
    return "Sentiment Analysis Service is running!"

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
        print(f"Error in analyze_sentiment: {str(e)}")
        return jsonify({'error': str(e)}), 500

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
        print(f"Error in analyze_sentiment_batch: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

# Remove the if __name__ == '__main__': block