import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import json
import uuid
import collections
from flask import jsonify
from Quiz import Quiz

class Question:

	def path_to_file_question(self):
		with open('config.json', 'r') as file:
			file = json.load(file)
		return file["questions_path"]
	
	def read_question_file(self):
		path_to_file = self.path_to_file_question()
		with open(path_to_file, 'r') as json_file:
			questions_json_file = json.load(json_file)
		return questions_json_file

	def write_questions_json_file(self, questions_json_file):
		path_to_file = self.path_to_file_question()
		with open(path_to_file, 'w') as file_question:
			json.dump(questions_json_file, file_question)

	def show_question(self, question_id):
		try:
			question_file = self.read_question_file()
			for dic_quest in question_file:
				if dic_quest['id'] == question_id:
					return jsonify({
						'id': dic_quest['id'],
						'name': dic_quest['name'],
						'options': dic_quest['options'],
						'correct_option':dic_quest['correct_option'],
						'quiz':dic_quest['quiz'],
						'points': dic_quest['points']
					}), 200
			return {}, 404
		except:
			return jsonify({
                'status': 'failure',
                'reason': 'Something went wrong'
            }), 400
	
	def get_all_questions_for_quizid(self, quiz_id):
		questions_list = []
		question_file = self.read_question_file()
		for question in question_file:
			if question['quiz'] == quiz_id:
				questions_list.append(question)
		if len(questions_list) == 0:
			return {}, 404
		quiz = Quiz().get_quiz(quiz_id)
		return jsonify({
			'name': quiz['name'],
			'description': quiz['description'],
			'questions': questions_list
		}), 200

	def create_question(self, que_input):
		que_input['id'] = int(uuid.uuid4())
		for key in ["name", "options", "correct_option", "quiz", "points"]:
			if key not in que_input:
				return jsonify({
					'status': 'failure',
                    'reason': 'Input is not correct'
				}), 400
		if (Quiz().check_if_quiz_exists(que_input['quiz']) == False):
			return jsonify({
				'status': 'failure',
				'reason': "Quiz Key doesn't exist"
			}), 400
			
		que_json_file = self.read_question_file()
		que_json_file.append(que_input)
		self.write_questions_json_file(que_json_file)
		return jsonify({
            'id': que_input['id'],
			'name': que_input['name'],
			'options': que_input['options'],
			'correct_option':que_input['correct_option'],
			'quiz':que_input['quiz'],
			'points': que_input['points']
        }), 201