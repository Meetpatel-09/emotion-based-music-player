from flask import Flask
import auth

app = Flask(__name__)

authObject = auth.Auth()

def hello_world():
   return 'Hello World'

app.add_url_rule('/', '', hello_world)
app.add_url_rule('/register', 'register', authObject.register, methods = ['POST', 'GET'])
app.add_url_rule('/login', 'login', authObject.login, methods = ['POST', 'GET'])

if __name__ == '__main__':
   app.run(debug=True)