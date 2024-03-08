from flask import Flask, jsonify, redirect, render_template, request, url_for, session
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, text

app = Flask(__name__)

app.secret_key = "pyFace"

bcrypt = Bcrypt(app)

UPLOAD_FOLDER = "static/images"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

connection_string = "mysql+mysqlconnector://root:1234@localhost/test_db"
engin = create_engine(connection_string, echo=True)

@app.route("/")
def home():
    # with engin.connect() as conn:

    #     result = conn.execute(text(
    #         "SELECT news.*, reporter_tbl.fname, reporter_tbl.lname FROM news JOIN reporter_tbl ON news.reporter_id = reporter_tbl.reporter_id"))
    #     news = []
    #     for row in result.all():
    #         news.append(row)

    #     print(len(news))

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

            print("row count ", result.rowcount)

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
            query = "INSERT INTO accounts(name, password) VALUES (:name, :password)"

            password = data['password']
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            result = conn.execute(text(query), {
                "name": data['name'],
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

if __name__ == '__main__':
   app.run(debug=True)