# Sentiment Analysis Service

This is a Flask-based microservice that provides sentiment analysis for text inputs. It's designed to work as part of a larger blog application system, where it analyzes the sentiment of user comments.

## Features

- Single text sentiment analysis
- Batch sentiment analysis
- Caching of results for improved performance
- CORS support for cross-origin requests
- Health check endpoint
- Error handling and logging

## Technology Stack

- Python 3.x
- Flask
- VADER Sentiment Analysis
- Gunicorn (for production deployment)

## Installation

1. Clone the repository:
git clone https://github.com/your-username/sentiment-analysis-service.git
cd sentiment-analysis-service

2. Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate

3. Install the required packages:
pip install -r requirements.txt

## Usage

### Running Locally

To run the service locally for development:
python app.py

The service will be available at `http://localhost:5000`.

### Deployment

This service is configured for deployment on Vercel. The `vercel.json` file contains the necessary configuration.

To deploy:

1. Install the Vercel CLI: `npm i -g vercel`
2. Run `vercel` in the project directory and follow the prompts

## API Endpoints

### 1. Analyze Single Text

- **URL:** `/analyze`
- **Method:** POST
- **Body:**
    ```json```
    {
        "text": "Your text here"
    }
    
Response:
```json```
    {
        "text": "Your text here",
        "sentiment": "positive",
        "compound_score": 0.5423
    }
    
### 2. Analyze Batch of Texts

- **URL:** /analyze_batch
- **Method:** POST
- **Body:**
    ```json
    {
    "texts": ["First text", "Second text", "Third text"]
    }

Response:
    ```json```
    [
        {
            "text": "First text",
            "sentiment": "neutral",
            "compound_score": 0.0
        },
        {
            "text": "Second text",
            "sentiment": "positive",
            "compound_score": 0.6124
        },
        {
            "text": "Third text",
            "sentiment": "negative",
            "compound_score": -0.3412
        }
    ]

### 3. Health Check

- **URL:** /health
- **Method:** GET

Response:
    ```json```
    {
    "status": "healthy"
    }

## Error Handling
In case of errors, the API will return a JSON response with an error message and an appropriate HTTP status code.

## Logging
Logs are written to app.log in the project directory. The log file is rotated when it reaches 10,000 bytes, keeping one backup.
