from flask import Flask, jsonify, request
import json
from api.Quiz import Quiz
from api.Question import Question

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/api/quiz/', methods=['POST'])
def create_quiz():
	if not request.is_json:
		return jsonify({
			"status":"failure",
            "reason":"Body must be json"
		}), 400
	post_data = request.data
	data = json.loads(post_data)
	return Quiz().create_quiz(data)

@app.route('/api/quiz/<int:quiz_id>')
def get_quiz(quiz_id):
	return Quiz().show_quiz(quiz_id)

@app.route('/api/questions/', methods=['POST'])
def create_question():
	if not request.is_json:
		return jsonify({
			"status":"failure",
            "reason":"Body must be json"
		}), 400
	post_data = request.data
	data = json.loads(post_data)
	return Question().create_question(data)

@app.route('/api/questions/<int:question_id>')
def get_question(question_id):
	return Question().show_question(question_id)

@app.route('/api/quiz-questions/<int:quiz_id>')
def get_all_questions_for_quizid(quiz_id):
	return Question().get_all_questions_for_quizid(quiz_id)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)