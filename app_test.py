from flask import Flask 

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'How are you?'

# export FLASK_APP=app_test.py (run this in terminal)

# set FLASK_APP=app_test.py (run this in the terminal)

