from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow Cross-Origin Requests (optional)

worker_status = "idle"
completed_tasks = {"task1": "completed", "task2": "completed"}
pending_tasks = ["task3", "task4"]

@app.after_request
def add_header(response):
    """Disable caching to ensure real-time updates"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/status')
def status():
    return jsonify({
        "worker_status": worker_status,
        "completed_tasks": list(completed_tasks.keys()),
        "pending_tasks": pending_tasks
    })

if __name__ == '__main__':
    app.run(debug=True)
