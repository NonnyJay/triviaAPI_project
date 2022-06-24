# UDACITY TRIVIA APP

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

Open and view the Project using the `.zip` file provided or at my [GitHub Repository](https://github.com/NonnyJay/triviaAPI_project)

## Project Overview
The project contains a frontend and backend directory that holds the code and  other system files to allow the for the running of the project. Below shows the project structure:

```
triviaAPI_project/
┣ .github/
┃ ┗ workflows/
┣ backend/
┃ ┣ flaskr/
┃ ┣ __pycache__/
┃ ┣ models.py
┃ ┣ README.md
┃ ┣ requirements.txt
┃ ┣ test_flaskr.py
┃ ┗ trivia.psql
┣ frontend/
┃ ┣ node_modules/
┃ ┣ public/
┃ ┣ src/
┃ ┣ package-lock.json
┃ ┣ package.json
┃ ┗ README.md
┣ .gitignore
┣ CODEOWNERS
┣ LICENSE.txt
┣ Project_Doc_README.md
┗ README.md
```


## How to start and setup the project

In this session, you will find instruction on how to get the project setup on your local machine. Dependencies and tools required for both the frontend and backend are discussed below.

### Frontend  - Trivia App

> _tip_: the frontend is designed to work with [Flask-based Backend](.\triviaAPI_project\backend) so it will not load successfully if the backend is not working or not connected. We recommend that you **start up the backend first**, test using Postman or curl, update the endpoints in the frontend, and then the frontend should integrate smoothly.

#### Installing Dependencies

1. **Installing Node and NPM**
   This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

> _tip_: `npm i`is shorthand for `npm install``

#### Required Tasks

##### Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.

```bash
npm start
```

### Backend  - Trivia App

#### Installing Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `backend/flaskr/__init__.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.


#### Set up the Database

With Postgres running, create a `trivia` database:

**Mac and Unix systems**

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

**Windows systems**

You will need to login to your postgres server using a superuser user like `postgres` or the one you created and carry out the followinf steps:

1. Login to postgres server. You will be prompted for password, if your user has a password setup. Here my user is "postgres" and my existing database is "postgres".

```command
psql -U postgres -d postgres
```
2. Now you have logged in to your DB and on your psql shell. Use the following command to create a new database.

```command
    DROP DATABASE IF EXISTS trivia;
    CREATE DATABASE trivia OWNER postgres;
    GRANT ALL PRIVILEGES ON DATABASE trivia TO postgres;
```

3. Populate the database using the `trivia.psql` file provided. From the `backend` folder in cmd terminal run:

```command
psql -U postgres -d trivia <  trivia.psql
```
if you are not on the `backend` directory path on your CMD, then you should use the absolute path. 

Example: C:\Users\PUT YOUR FILE COMPLETE PATH\trivia.psql

#### Required Tasks

##### Running Your Backend in Dev Mode

From within the `./backend` directory run the following command on your terminals. It is important to check you have activated your virtual environment is you running from a created virtual environment.

**Mac, Unix and Gitbash**

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

**Windows CMD**

```command
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

**Windows Powershell**

```command
$env:FLASK_APP=flaskr
$env:FLASK_ENV=development
flask run
```


## Testing

To test the APIs using the unittest library, you the above described steps to create and populate your `trivia_test` Database. 

The run the test script from the `./backend` directory.

```command
python test_flaskr.py
```


## API Reference

### Getting Started
- Base URL: This application is not hosted and currently running locally. The backend app will run on localhost and port 5000. Note, `http://127.0.0.1:5000` has been configured as the proxy for the frontend, changing this base URL at the backend will require same on the frontend configuration for the app to work.

- Authentication: This app version does not require authentication or API keys to function.


### Error Handling
All errors known errors has been handled and returned as JSON objects in the below format:

```json
{
  "error": 422,
  "message": "The request cannot be processed",
  "success": False
}
```

The API will return the listed five errors when the requests fail:
- 400: The request was invalid
- 404: The request is not found
- 405: Request Method not Allowed
- 422: The request cannot be processed
- 500: Server Error has occured


### Endpoints

#### GET /categories
- General:
    - Returns a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category and success value.
- Sample: `curl http://127.0.0.1:5000/categories`

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

#### GET /questions?page={integer}
- General:
    - Returns an object with 10 paginated questions, total questions, object including all categories, and current category string
- Sample : `curl http://127.0.0.1:5000/questions?page=1`

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 22
}
```

#### GET /categories/{id}/questions
- General:
    - Returns an object with questions for the specified category, total questions, and current category string
- Sample : `curl http://127.0.0.1:5000/categories/1/questions`

```json
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

#### DELETE /questions/{id}
- General:
    - Deletes the question associated with the given ID if it exists. This only returns the HTTP status code to help identify if the deletion was successful or not.
- Sample : `curl -X DELETE http://127.0.0.1:5000/questions/4`

```json
{
  "success": true
}
```


#### POST /quizzes
- General:
    - Returns a single new question object every time the service is called that is among the previous questions.
- Sample : `curl -H "Content-Type: application/json" -X POST -d "{'previous_questions': [], 'quiz_category': {'type': 'Science', 'id': '1'}}" http://127.0.0.1:5000/quizzes`

```json
{
  "question": {
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}
```


#### POST /questions
- General:
    - Creates a new question using the category,difficulty, answer and question. Returns the success value.
- Sample : `curl -H "Content-Type: application/json" -X POST -d "{'question' : 'Who painted monalisa portrait', 'answer' : 'Vincent Black', 'difficulty' : 3, 'category' : 4}"  http://127.0.0.1:5000/questions`

```json
{
  "success": true
}
```


#### POST /questions/search
- General:
    - Returns any array of questions,a number of totalQuestions that met the search term and the current category string.
- Sample : `curl -H "Content-Type: application/json" -X POST -d "{\"searchTerm\": \"world\"}"  http://127.0.0.1:5000/questions/search`

```json
{
  "current_category": null,
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

## Authors

#### Chinonso Aguonye and Udacity
* [GitHub](https://github.com/NonnyJay)
* [LinkedIn](https://www.linkedin.com/in/cyber-dummy/)
* [Udacity](https://www.udacity.com/)

## Acknowledgments

I will like to acknowledge the scholarships offered by the Africa Leadership group(ALG) and the mentors,community leaders and instructors of the Udacity programme for their guidance.

- [Udacity](https://www.udacity.com/) provided the based code and instructions for the project.
I also reference some ways to handle some of the APIs from the below platforms:
- [StackOverflow](https://stackoverflow.com/questions/60805/getting-random-row-through-sqlalchemy)
- [ProgramCreek](https://www.programcreek.com/python/example/88978/sqlalchemy.func.random)


## License

`Udacity Trivia App` is open source application [licensed as Udacity](https://www.udacity.com/)

