from flask import Flask, render_template, redirect, request
from password import Master

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        L = []
        senha = request.form["inputPassword5"]
        x = Master(senha=senha)
        L.append(x)

        try:
            redirect('/')
            return render_template('password.html', L=L)
        except:
            return 'Well, it didn\'t work'
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
