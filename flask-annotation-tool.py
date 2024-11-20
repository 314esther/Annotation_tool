# app.py
from flask import Flask, render_template, jsonify, request
import json
from datetime import datetime
import os

app = Flask(__name__)

# Sample data - in production, this would likely come from a database
SAMPLE_DATA = [
    {
        "id": 1,
        "text": "The Industrial Revolution was a major turning point in human history. It began in Britain in the late 18th century and later spread to other parts of the world. This period marked a shift from manual production methods to machine manufacturing, leading to unprecedented economic growth.",
        "question": "When did the Industrial Revolution begin?",
        "choices": [
            "Early 17th century",
            "Late 18th century",
            "Mid 19th century",
            "Early 20th century"
        ],
        "correctAnswer": 1
    },
    {
        "id": 2,
        "text": "Photosynthesis is the process by which plants convert light energy into chemical energy. This process occurs in the chloroplasts of plant cells, specifically using chlorophyll to capture sunlight. The energy is then used to convert water and carbon dioxide into glucose and oxygen.",
        "question": "Where does photosynthesis occur in plant cells?",
        "choices": [
            "Nucleus",
            "Mitochondria",
            "Chloroplasts",
            "Vacuoles"
        ],
        "correctAnswer": 2
    }
]

# Ensure annotations directory exists
if not os.path.exists('annotations'):
    os.makedirs('annotations')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/questions')
def get_questions():
    return jsonify(SAMPLE_DATA)

@app.route('/api/annotations', methods=['POST'])
def save_annotation():
    annotation = request.json
    filename = 'annotations/annotations.json'
    
    # Load existing annotations
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            annotations = json.load(f)
    else:
        annotations = {}
    
    # Update annotations
    question_id = str(annotation['questionId'])
    annotations[question_id] = {
        'questionId': annotation['questionId'],
        'selectedText': annotation['selectedText'],
        'timestamp': datetime.now().isoformat()
    }
    
    # Save to file
    with open(filename, 'w') as f:
        json.dump(annotations, f, indent=2)
    
    return jsonify({'status': 'success'})

@app.route('/api/annotations', methods=['GET'])
def get_annotations():
    filename = 'annotations/annotations.json'
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return jsonify(json.load(f))
    return jsonify({})

if __name__ == '__main__':
    app.run(debug=True)
