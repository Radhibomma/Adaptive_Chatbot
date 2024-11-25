from flask import Flask, render_template, request, jsonify
from textblob import TextBlob  # For sentiment analysis

app = Flask(__name__)

# Chatbot responses based on sentiment
responses = {
    "positive": [
        "That's wonderful! 😊 What else can I assist you with?",
        "I'm so glad to hear that! Keep up the positivity! 🌟",
        "Fantastic! Is there anything else on your mind?"
    ],
    "neutral": [
        "I'm here to help. Please tell me more.",
        "What else can I assist you with today?",
        "Feel free to ask me anything."
    ],
    "negative": [
        "I'm sorry to hear that. How can I make your day better? 💛",
        "That sounds tough. I'm here for you. Let me know how I can help. 🙏",
        "I'm here to support you. Feel free to share more with me."
    ]
}

# Keyword responses
keywords = {
    "weather": "The weather is great today! 🌤️ What do you think?",
    "sports": "I love talking about sports! What's your favorite team? 🏀⚽",
    "news": "The latest news can be overwhelming. Do you want me to summarize something? 📰"
}

# Conversation context
conversation_context = {"expecting_followup": False, "last_topic": None}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    global conversation_context
    user_message = request.json.get('message').lower()

    # Handle follow-up responses
    if conversation_context["expecting_followup"]:
        if conversation_context["last_topic"] == "weather":
            response = "It's sunny here. What's it like where you are?"
            conversation_context["expecting_followup"] = False
            return jsonify({"response": response, "sentiment": "neutral"})
        elif conversation_context["last_topic"] == "sports":
            response = "I'm a fan of many sports! What's your favorite game?"
            conversation_context["expecting_followup"] = False
            return jsonify({"response": response, "sentiment": "positive"})

    # Check for specific keywords
    for keyword, response in keywords.items():
        if keyword in user_message:
            conversation_context["expecting_followup"] = True
            conversation_context["last_topic"] = keyword
            return jsonify({"response": response, "sentiment": "neutral"})

    # Sentiment-based response
    sentiment = analyze_sentiment(user_message)
    bot_response = responses[sentiment][0]  # Pick the first response
    return jsonify({"response": bot_response, "sentiment": sentiment})


def analyze_sentiment(message):
    """Analyze the sentiment of a message."""
    analysis = TextBlob(message)
    polarity = analysis.sentiment.polarity

    if polarity > 0.2:
        return "positive"
    elif polarity < -0.2:
        return "negative"
    else:
        return "neutral"


if __name__ == '__main__':
    app.run(debug=True)