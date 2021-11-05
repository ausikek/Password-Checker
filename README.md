
# 💻 Password Checker
This program checks if a password has been compromised using the pwnedpasswords API with K-Anonimity model.

## 🤔Motivation
I am really interested in getting into the field of Computer Science and particularly Cybersecurity and Criptography. Buiding Password Checker to me was a brief introduction of some tools that can be used on that field.

This project also taught me a lot about the work of a back-end developer.

## ❗ How it works

### Using Flask 

```python
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passwords.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from mainapp import routes
```
In the init file we will import an instance of Flask. We also set the Flask-SQLAlchemy and Bcrypt instances here.

### Flask Routes

```python
from collections import Counter
from flask import render_template, request, redirect
from mainapp.password import Verifier
from mainapp.models import Passwords, PassStorer
from mainapp.forms import PasswordReceiver
from mainapp import bcrypt, db, app


def hash_comparator(item):
    passwords = Passwords.query.all()
    for password in passwords:
        validator = bcrypt.check_password_hash(str(password), item)
    if validator:
        x = Passwords.query.filter_by(password=str(password)).first()
        storer = PassStorer(senhas=x, nome=str(item))
        db.session.add(storer)
        db.session.commit()

    return PassStorer.query.all()


def table_shower():
    pass_counter = PassStorer.query.all()
    pass_final = []
    for item in pass_counter:
        pass_final.append(str(item))
    pass_sorted = Counter(pass_final).most_common()
    return pass_sorted


@app.route("/", methods=['POST', 'GET'])
def index():
    form = PasswordReceiver()
    if request.method == 'POST':
        senha = request.form["password"]
        count, securepass = Verifier.displayer(senha=senha)
        if count:
            hashed = bcrypt.generate_password_hash(form.password.data)\
                                                .decode('utf-8')
            passw = Passwords(password=str(hashed))
            db.session.add(passw)
            db.session.commit()
            hash_comparator(form.password.data)
            try:
                redirect('/')
                return render_template('password.html', form=form,
                                       count=count, passlenght=securepass,
                                       passlist=table_shower(), listlen=len(table_shower()))
            except:
                return 'Error in saving password'
        try:
            redirect('/')
            return render_template('password.html', passlenght=securepass,
                                   form=form, passlist=table_shower(),
                                   listlen=len(table_shower()))
        except:
            return 'Error in displaying None'

    print(table_shower())
    return render_template('index.html', form=form,
                           passlist=table_shower(), listlen=len(table_shower()))
 ```
 Here, we will finally set our page. 
 
 First, we catch a password through a form and verify it using the PwnedPasswords API:
 
 1. If the password is pwned, we hash it using Flask-Bcrypt and append it to our database.
 2. Else, we just output that the password has not been found.
 3. The saved passwords are displayed from most to least searched in our website.


### The database 

```python
from mainapp import db
from datetime import datetime


class Passwords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(60), nullable=False)
    relacao = db.relationship('PassStorer', backref='senhas', lazy=True)

    def __repr__(self):
        return f'{self.password}'

class PassStorer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    senha_id = db.Column(db.Integer, db.ForeignKey('passwords.id'), nullable=False)
    nome = db.Column(db.String(60), nullable=False)
    tempo = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    
    def __repr__(self):
        return f'{self.nome}'
```
Those are the two tables we have in our database. The first one (Passwords) stores the hashed passwords and the other (PassStorer) has a relationship to the first. That way, we can get the number of times a password has been sent.

### Our Form

```python
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired

class PasswordReceiver(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired()])
    submit = SubmitField('Submit')
```
Simple form :)

### The cool program that check if the password is pwned

```python
import requests
import hashlib as hl


class Verifier:
    
    def request_api_data(query_chars):
        url = 'https://api.pwnedpasswords.com/range/' + str(query_chars)
        Response = requests.get(url)
        if Response.status_code != 200:
            raise RuntimeError(f'Error: {Response.status_code}')
        return Response

    def getpsswrd_leaks_count(hashes, checkhash):
        hashes = (line.split(':') for line in hashes.text.splitlines())
        for h, count in hashes:
            if h == checkhash:
                return count
        return 0

    def api_check_pwned(password):
        sha1passwrd = hl.sha1(password.encode('utf-8')).hexdigest().upper()
        usable, nonusable = sha1passwrd[:5], sha1passwrd[5:]
        response2 = Verifier.request_api_data(usable)
        return Verifier.getpsswrd_leaks_count(response2, nonusable)
    
    def inputpass(senha):
        L = []
        L.append(senha)
        return L
    
    @staticmethod
    def displayer(senha):
        for password in Verifier.inputpass(senha):
            if len(senha) > 0:
                count = Verifier.api_check_pwned(password)
                securepass = len(password) * '*'
                if count:
                    return count, securepass
                else:
                    return None, securepass

```        
In here, the input from the forms will be processed using the PwnedPasswords API. See that we use the K-Anonimity Model to verify the password in the API.

If the password is Pwned, we return a Tuple with the count and the password in asterisks. Else, we return a tuple with None and the password in asterisks.

### Jinja Templating 

```html5
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Password Verifier</title>
  <link href="https://fonts.googleapis.com/css?family=Montserrat" rel="stylesheet">
  <link rel="stylesheet" type="text/css" href="static/style.css">
  <link rel="shortcut icon" href="{{ url_for('static', filename='passwordkey.ico') }}">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
    {% block head %} {% endblock %}
</head>
<body>
    <div class="root">
      <h1 class="header">Here, input a password!</h1>
      <form action="" method="post" name="password">
          <fieldset class="form-group">
            <div class="form-group" >
              {{ form.password(class="form-control form-control-lg") }} 
            </div>
            <div class="form-group">
              {{ form.submit(class="btn btn-outline-info") }}
            </div>
        </fieldset> 
      </form>
    </div>
  {% block content %} {% endblock content %}
    {% if listlen > 5 %}
    <h3>Most common passwords in Password Verifier:</h3>
    <ol>
    <li>{{ passlist[0][0] }}, {{ passlist[0][1] }} time(s).</li>
    <li>{{ passlist[1][0] }}, {{ passlist[1][1] }} time(s).</li>
    <li>{{ passlist[2][0] }}, {{ passlist[2][1] }} time(s).</li>
    <li>{{ passlist[3][0] }}, {{ passlist[3][1] }} time(s).</li>
    <li>{{ passlist[4][0] }}, {{ passlist[4][1] }} time(s).</li>
  </ol>
    {% endif %}
</body>
</html>
```
The connection between the python program variables and the website happens thanks to Jinja 2 Templating. See that we create the form using Flask-Forms and Jinja 2 syntax.

## Credits
Password Checker is one of a series of projects from Andrei's Anagoie course **Complete Python Developer**. 

Outside of the course, I implemented Flask to create a link between the front-end and the back-end of a website.

I'd like to thank Andrei for being a professional, funny and skilled professor. Looking forward to continue learning with you.

I'd also like to thank my great friend Dahrug for giving me help believing and challenging me to be a better professional.







