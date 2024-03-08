from flask import request, render_template

class Auth:
    def login(_self):
        if request.method == 'POST':
            return "Post"
        elif request.method == 'GET':
            return render_template('login.html')
        else:
            return "Requested Method Not Allowed"
        
    def register(_self):
        if request.method == 'POST':
            return "Post"
        elif request.method == 'GET':
            return render_template('register.html')
        else:
            return "Requested Method Not Allowed"