import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('project:project@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_trivia_1 = {"question" : "Who painted monalisa portrait", "answer" : "Vincent Black", "difficulty" : 3, "category" : 2}
        self.new_trivia_2 = {"question" : None, "answer" : "Vincent Black", "difficulty" : 4, "category" : 1}
        self.new_trivia_3 = {"question" : "When was the first Lunar esclipse recorded", "answer" : "Vincent Black", "difficulty" : "Science", "category" : 4}
        
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # Testcase for successful and error operation for retrieve category
    def test_retrieve_categories_success(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_500_database_not_accessible(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message', 'Server Error has occured'])


    # Testcase for successful and error operation for retrieve questions
    def test_retrieve_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertEqual(data['current_category'], None)
        
    def test_404_request_beyond_page(self):
        res = self.client().get('/questions?page=50')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The request is not found')



    # Testcase for successful and error operation for delete questions
    def test_delete_question_success(self):
        res = self.client().delete('/questions/20')
        data = json.loads(res.data)
        qstn = Question.query.filter(Question.id == 20).one_or_none()

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertEqual(qstn, None)

    def test_404_delete_question_not_exist(self):
        res = self.client().delete('/questions/50')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The request is not found')


    # Testcase for successful and error operation for question creation
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_trivia_1)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_incomplete_question_data(self):
        res = self.client().post('/questions', json=self.new_trivia_2)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The request was invalid')



    # Testcase for successful and error operation for question search
    def test_search_questions(self):
        res = self.client().post('/questions/search', json={'searchTerm' : 'title'})
        data =json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']), 8)
        self.assertEqual(data['current_category'], None)
    
    def test_search_does_not_match(self):
        res = self.client().post('/questions/search', json={'searchTerm' : 'yellow'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['current_category'], None)



    # Testcase for successful and error operation on retrieving questions by category
    def test_retrieve_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['current_category'], "Art")
        
    def test_404_no_question_for_category(self):
        res = self.client().get('/categories/10/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The request is not found')
        
        
    # Testcase for successful and error operation on playing quiz
    def test_quiz_game(self):
        res = self.client().post('/quizzes', json={'previous_questions': [2], 'quiz_category': {'type': 'Science', 'id': '1'}})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        

    def test_no_question_in_category(self):
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'type': 'Science', 'id': '10'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)

    def test_400_quiz_game(self):
        res = self.client().post('/quizzes', json={'previous_questions' : [], 'quiz_category' : 3})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The request was invalid')
        
    def test_405_quiz_method_not_allowed(self):
        res = self.client().get('/quizzes', json={'previous_questions' : [], 'quiz_category' : 3})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Request Method not Allowed')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()