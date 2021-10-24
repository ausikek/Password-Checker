
# 💻 Password Checker
This program checks if a password has been compromised using the pwnedpasswords API with K-Anonimity model.

## 🤔Motivation
I am really interested in getting into the field of Computer Science and particularly Cybersecurity and Criptography. Buiding Password Checker to me was a brief introduction of some tools that can be used on that field.

## ❗ How it works

### Using Flask 

```python
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
```
We will be using Flask to create a server. With Flask, we can get the user's input and send it to our password verifier function.

### What happens in the back-end?

The back-end will be called with the Master() Function. It simply contains all the functions below.

### The inputpass() Function

```python
def inputpass(senha):
        L = []
        L.append(senha)
        return L
```
This function simply catches the user's "password" and returns a list with it.

### The displayer() Function

```python
def displayer(senha):
        for password in inputpass(senha):
            count = api_check_pwned(password)
            securepass = len(password) * '*'
            if count:
                return f'{securepass} was found {count} times. Oh Oh!'
            else:
                return f'{securepass} was not found. Congratulations!'

```        
This function gets the password from inputpass() and creates "count", that will be the number of times the password was found.

It then prints the number of time it was found.

### The api_checkpwned() Function

```python
def api_checkpwned(password):
    sha1passwrd = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    usable, nonusable = sha1passwrd[:5], sha1passwrd[5:]
    response2 = request_api_data(usable)
    return getpsswrd_leaks_count(response2, nonusable)
```
This function will encrypt the password using SHA-1, and crop the first 5 characters of the SHA-1 encrypted string. Then, it will send those 5 characters to request_api_data() and return getpsswrd_leaks_count()

### The request_api_data() Function 

```python
def request_api_data(query_chars):
    url = 'https://api.pwnedpasswords.com/range/' + str(query_chars)
    Response = requests.get(url)
    if Response.status_code != 200:
        raise RuntimeError(f'Error: {Response.status_code}, check the API and try again.')
    return Response
```
This function will give us the number of times the password has been found using the pwnedpasswords API. It will search using the first five characters of the SHA-1 encrypted password (K-Anonimity).

### The get_psswrd_leaks_count()
```python
def getpsswrd_leaks_count(hashes, checkhash):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == checkhash:
            return count
    return 0
```
As the name suggests, this function will finally return us the count that will be displayed to the user. It compares the output of request_api_data() with the rest of the encrypted strings (that is, everything but the first five characters). If that comparison is true, we output the count. If not, we output 0.

## Credits
Password Checker is one of a series of projects from Andrei's Anagoie course **Complete Python Developer**.

I'd like to thank Andrei for being a professional, funny and skilled professor. Looking forward to continue learning with you.






