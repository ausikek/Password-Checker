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
