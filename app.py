from flask import Flask, redirect, render_template, request, url_for, session
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, text
from werkzeug.utils import secure_filename
import os
import imghdr
import datetime
import base64
import cv2
from deepface import DeepFace

app = Flask(__name__)

app.secret_key = "pyFace"

bcrypt = Bcrypt(app)

UPLOAD_FOLDER = "static/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

connection_string = "mysql+mysqlconnector://root:1234@localhost/music_player"
engin = create_engine(connection_string, echo=True)

@app.route("/")
def home():
    return render_template("home.html", title="Home")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.form

        with engin.connect() as conn:

            query = "SELECT * FROM accounts WHERE name = :name"

            result = conn.execute(text(query), {
                "name": data["name"]
            })

            if result.rowcount == 1:
                data1 = result.all();
                hashed_password = data1[0][-1]
                is_valid = bcrypt.check_password_hash(hashed_password, data["password"])
                if is_valid:
                    session['id'] = data1[0][0]
                    return redirect(url_for('home'))
                showAlert = True
                return render_template("login.html", showAlert=showAlert, message="Invalid Password", title="Login")    
            showAlert = True
            return render_template("login.html", showAlert=showAlert, message="Account not found", title="Login")
    elif request.method == 'GET':
        return render_template('login.html')
    else:
        return "Requested Method Not Allowed"

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        data = request.form
        with engin.connect() as conn:

            query = "SELECT * FROM accounts WHERE name = :name"

            result = conn.execute(text(query), {
                "name": data["username"]
            })

            print("row count ", result.rowcount)

            if result.rowcount == 1:
                return render_template('register.html', error="Username aleary taken")


            query = "INSERT INTO accounts(name, birth_date, password) VALUES (:name, :birth_date, :password)"

            password = data['password']
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            result = conn.execute(text(query), {
                "name": data['username'],
                "birth_date": data['birth_date'],
                "password": hashed_password,
            })
            conn.commit()

            if result.rowcount == 1:
                return redirect(url_for("login"))

        return render_template("register.html", title="Register")

    elif request.method == 'GET':
        return render_template('register.html')
    else:
        return "Requested Method Not Allowed"

@app.route('/camera', methods=['POST', 'GET'])
def camera():
    if request.method == 'POST':
        image_data_base64 = request.form['imageData']

        image_data = base64.b64decode(image_data_base64.split(',')[1])

        if not os.path.exists(app.config["UPLOAD_FOLDER"]):
            os.makedirs(app.config["UPLOAD_FOLDER"])

        timestamp = datetime.datetime.now().timestamp() * 1000000
        image_name = str(int(timestamp)) + '.png'
        image_filename = os.path.join(app.config["UPLOAD_FOLDER"], image_name)

        with open(image_filename, 'wb') as f:
            f.write(image_data)

        img = cv2.imread('static/uploads/1712342814765677.png')

        result = DeepFace.analyze(img, actions = ['emotion'])
        
        emotion = result[0]['dominant_emotion']

        print(emotion)

        return render_template('camera.html', image_name=image_name, emotion=emotion)            

    elif request.method == 'GET':
        return render_template('camera.html')
    else:
        return "Requested Method Not Allowed"
if __name__ == '__main__':
   app.run(debug=True)