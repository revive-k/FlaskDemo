import json
import uuid
import collections
from flask import jsonify

class Quiz:

    def path_to_quiz_file(self):
        with open('config.json', 'r') as file:
            file = json.load(file)
        return file["quiz_path"]

    def read_quiz_file(self):
        path_to_file = self.path_to_quiz_file()
        with open(path_to_file, 'r') as json_file:
            quiz_json_file = json.load(json_file)
        return quiz_json_file

    def write_quiz_json_file(self, quiz_json_file):
        path_to_file = self.path_to_quiz_file()
        with open(path_to_file, 'w') as file_quiz:
            json.dump(quiz_json_file, file_quiz)

    def get_quiz_ids(self):
        quiz_ids = []
        quiz_file = self.read_quiz_file()
        for quiz in quiz_file:
            quiz_ids.append(quiz['id'])
        return quiz_ids

    def get_quiz(self, quiz_id):
        quiz_file = self.read_quiz_file()
        for quiz in quiz_file:
            if(quiz['id']==quiz_id):
                return quiz
        return None

    def check_if_quiz_exists(self, quiz_id):
        quiz_file = self.read_quiz_file()
        for quiz in quiz_file:
            if(quiz['id']==quiz_id):
                return True
        return False

    def create_quiz(self, quiz_input):
        quiz_input['id'] = int(uuid.uuid4())
        for key in ["name", "description"]:
            if key not in quiz_input:
                return jsonify({
					'status': 'failure',
                    'reason': 'Input should contain name and description'
				}), 400

        quiz_json_file = self.read_quiz_file()
        quiz_json_file.append(quiz_input)
        self.write_quiz_json_file(quiz_json_file)
        return jsonify({
            'id': quiz_input['id'],
            'name': quiz_input['name'],
            'description': quiz_input['description']
        }), 201

    def show_quiz(self, quiz_id):
        try:
            quiz_file = self.read_quiz_file()
            for dic_quiz in quiz_file:
                if dic_quiz['id'] == quiz_id:
                    return jsonify({
                        'id': dic_quiz['id'],
                        'name': dic_quiz['name'],
                        'description': dic_quiz['description']
                    }), 200
            return {}, 404
        except:
            return jsonify({
                'status': 'failure',
                'reason': 'Something went wrong'
            }), 400
