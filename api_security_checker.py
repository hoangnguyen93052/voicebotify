import requests
from flask import Flask, request, jsonify
from functools import wraps
import time
import logging
import hashlib
import random
import string
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# API configurations
API_KEY = os.getenv('API_KEY', 'your_api_key_here')
RATE_LIMIT = 5  # requests per minute
RATE_LIMIT_WINDOW = 60  # in seconds

# Store user credentials for simulation
users_db = {
    "user1": "password1",
    "user2": "password2"
}

# Store API call timestamps by user
user_requests = {}

def authenticate_user(username, password):
    return users_db.get(username) == password

def generate_token(username):
    token = hashlib.sha256(f"{username}{random.randint(0, 1000000)}".encode()).hexdigest()
    return token

def verify_token(token):
    # For demonstration purposes, we're just going to check the token structure
    return len(token) == 64

def rate_limiter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        username = request.args.get('username')
        
        if username not in user_requests:
            user_requests[username] = []
        
        # Remove timestamps outside the rate limit window
        current_time = time.time()
        user_requests[username] = [timestamp for timestamp in user_requests[username]
                                   if current_time - timestamp < RATE_LIMIT_WINDOW]

        if len(user_requests[username]) >= RATE_LIMIT:
            return jsonify({"error": "Rate limit exceeded. Try again later."}), 429
        
        user_requests[username].append(current_time)
        return func(*args, **kwargs)
    return wrapper

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if authenticate_user(username, password):
        token = generate_token(username)
        logging.info(f"User {username} logged in successfully.")
        return jsonify({"token": token}), 200
    else:
        logging.warning(f"Failed login attempt for user {username}.")
        return jsonify({"error": "Invalid credentials."}), 401

@app.route('/secure-data', methods=['GET'])
@rate_limiter
def secure_data():
    token = request.headers.get('Authorization')
    
    if not verify_token(token):
        logging.warning("Unauthorized access attempt.")
        return jsonify({"error": "Unauthorized. Invalid token."}), 403
    
    return jsonify({"data": "This is secure data."}), 200

@app.route('/public-data', methods=['GET'])
def public_data():
    return jsonify({"data": "This is public data."}), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_error(e):
    logging.error(f"Internal error: {str(e)}")
    return jsonify(error="Internal server error."), 500

if __name__ == '__main__':
    app.run(debug=True)