from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from pymongo import MongoClient
import os
from datetime import datetime

app = Flask(__name__)

# Configuration
app.config['STATIC_FOLDER'] = 'static'
current_year = datetime.now().year

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Update this URI if using MongoDB Atlas
db = client['portfolio_db']
contact_collection = db['contact_messages']

# Routes
@app.route('/')
def home():
    return render_template('index.html', current_year=current_year)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    if name and email and message:
        contact_collection.insert_one({
            'name': name,
            'email': email,
            'message': message,
            'timestamp': datetime.now()
        })
        return redirect(url_for('home'))
    else:
        return "Please fill out all fields", 400

# Run
if __name__ == '__main__':
    os.makedirs(os.path.join(app.config['STATIC_FOLDER'], 'images'), exist_ok=True)
    os.makedirs(os.path.join(app.config['STATIC_FOLDER'], 'docs'), exist_ok=True)
    
    app.run(debug=True)
