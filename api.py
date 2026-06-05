from flask import Flask, jsonify
import os
app = Flask(__name__)
todos = [
    {"id": 1, "tache": "Apprendre Docker", "faite": False},
    {"id": 2, "tache": "Faire le pipeline CI/CD", "faite": False}
]
@app.route('/')
def home():
    return jsonify({"message": "Bienvenue sur mon API!", "todos": todos})

@app.route('/health')
def health():
    return jsonify({"status": "OK"})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    

