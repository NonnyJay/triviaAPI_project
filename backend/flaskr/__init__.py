import os
import sys
from flask import Flask, request, abort, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import werkzeug
from sqlalchemy import func, exc


from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
def paginate_questions(request, query_value):
    page = request.args.get('page', 1, type=int)
    start = (page -1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    all_questions = [question.format() for question in query_value]
    current_questions = all_questions[start : end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    #CORS(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def retrieve_categories():
        try:
            query_value = Category.query.order_by('id').all()
            #print(query_value)
            data= {category.id  : category.type for category in query_value}
            #print(data)
            return jsonify({
                'success' : True,
                'categories': data
            })
        except:
            print(sys.exc_info())
            abort(500)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def retrieve_questions():
        try:
            query_value = Question.query.order_by('id').all()
            #print(query_value)
            current_questions = paginate_questions(request, query_value)
            if len(current_questions) == 0:
                raise werkzeug.exceptions.NotFound
                #raise werkzeug.exceptions.Unauthorized
            category_values = Category.query.order_by('id').all()
            #print(query_value)
            data= {category.id  : category.type for category in category_values}

            return jsonify({
                'success' : True,
                'questions': current_questions,
                'total_questions' : len(query_value),
                'categories': data,
                "current_category" : None
            })
            #except TypeError:
        except werkzeug.exceptions.NotFound:
            print(sys.exc_info())
            abort(404)
        except :
            print(sys.exc_info())
            abort(400)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        print(question_id)
        try:
            del_question = Question.query.filter(Question.id == question_id).one_or_none()
            if del_question is None:
                #abort(400)
                raise werkzeug.exceptions.NotFound
            del_question.delete()
            return jsonify({
                'success': True
            })
        except werkzeug.exceptions.NotFound:
            print(sys.exc_info())
            abort(404)
        except:
            print(sys.exc_info())
            print(sys.exc_info()[1])
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        print(body)
        #{'question': 'Hie', 'answer': 'whay', 'difficulty': '2', 'category': '3'} {'searchTerm': 'title'}
        new_qstn = body.get("question", None)
        new_ans = body.get("answer", None)
        new_diff = body.get("difficulty", None)
        new_cat = body.get("category", None)
        print(new_qstn)
        try:
            if new_qstn is  None:
                #abort(400)
                raise werkzeug.exceptions.BadRequest

            add_qstn = Question(
                question = new_qstn,
                answer = new_ans,
                difficulty = new_diff,
                category = new_cat
            )
            add_qstn.insert()
            return jsonify(
                {
                    "success": True
                }
            )
        except werkzeug.exceptions.BadRequest:
            print(sys.exc_info())
            abort(400)
        except:
            print(sys.exc_info())
            abort(422)



    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        print("Testing search")
        search_term = request.get_json().get("searchTerm", None)
        print(search_term)
        query_value = Question.query.filter(Question.question.ilike(f"%{search_term}%")).order_by('id').all()
        #print(query_value)

        try:
            current_questions = paginate_questions(request, query_value)
            print(current_questions)
            print(len(current_questions))
            #if len(current_questions) == 0:
            #    abort(404)
            return jsonify({
                'success' : True,
                'questions': current_questions,
                'total_questions' : len(query_value),
                "current_category" : None
            })
        except:
            print(sys.exc_info())
            abort(422)
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def retrieve_category_questions(category_id):
        
        try:
            query_value = Question.query.filter(Question.category == category_id).order_by('id').all()
            current_questions = paginate_questions(request, query_value)
            print(current_questions)
            if len(current_questions) == 0:
                raise werkzeug.exceptions.NotFound
            
            current_category = Category.query.filter(Category.id == category_id).one_or_none()
            #print(current_category)
            #print(current_category.type)
            return jsonify({
                'success' : True,
                'questions': current_questions,
                'total_questions' : len(query_value),
                "current_category" : current_category.type
            })
        except werkzeug.exceptions.NotFound:
            print(sys.exc_info())
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            body = request.get_json()
            print(body)
            prev_qstn = body.get('previous_questions', None)
            print(prev_qstn)
            quiz_cat = body.get('quiz_category', None)
            print(quiz_cat)
            if type(quiz_cat) is not dict:
                raise werkzeug.exceptions.BadRequest
            
            print(quiz_cat['id'])
            print(quiz_cat['type'])
            
            if (len(prev_qstn) == 0 and quiz_cat['id'] == 0) :
                print("Case 0")
                #quiz = Question.query.first()
                quiz = Question.query.order_by(func.random()).limit(1).one_or_none()
            elif (len(prev_qstn) > 0 and quiz_cat['id'] == 0) :
                print("Case 1")
                #quiz = Question.query.filter(~Question.id.in_(prev_qstn)).first()
                quiz = Question.query.filter(~Question.id.in_(prev_qstn)).order_by(func.random()).limit(1).one_or_none()
            elif (len(prev_qstn) == 0 and quiz_cat['id'] != 0) :
                print("Case 2")
                #quiz = Question.query.filter(Question.category == quiz_cat['id']).first()
                quiz = Question.query.filter(Question.category == quiz_cat['id']).order_by(func.random()).limit(1).one_or_none()
            else:
                print("Case 3")
                #quiz = Question.query.filter(Question.category == quiz_cat['id'], ~Question.id.in_(prev_qstn)).first()
                quiz = Question.query.filter(Question.category == quiz_cat['id'], ~Question.id.in_(prev_qstn)).order_by(func.random()).limit(1).one_or_none()
            print(quiz)
            print(type(quiz))
            if quiz is None:
                return jsonify({
                    'success': False
                })
            #print(quiz.id)
            #prev_qstn.append(quiz.id)
            #print(prev_qstn)
            #print(quiz.answer)
            data = {
                "id": quiz.id,
                "question": quiz.question,
                "answer": quiz.answer,
                "difficulty": quiz.difficulty,
                "category": quiz.category,
            }
            #print(data)
            #'questions': quiz.format(),
            #'previous_questions': prev_qstn,
            #'quiz_category': quiz_cat['type']
            return jsonify({
                'success': True,
                'question': data
            })
        except werkzeug.exceptions.BadRequest:
            print(sys.exc_info())
            print(sys.exc_info()[1])
            abort(400)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({
            'success' : False,
            'error' : 400,
            'message' : "The request was invalid"
        }), 400

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'success' : False,
            'error' : 404,
            'message' : "The request is not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable_error(error):
        return jsonify({
            'success' : False,
            'error' : 422,
            'message' : "The request cannot be processed"
        }), 422

    @app.errorhandler(405)
    def method_not_allowed_error(error):
        return jsonify({
            'success' : False,
            'error' : 405,
            'message' : "Request Method not Allowed"
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success' : False,
            'error' : 500,
            'message' : "Server Error has occured"
        }), 500

    return app

