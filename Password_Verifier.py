import requests
import hashlib


def request_api_data(query_chars):
    url = 'https://api.pwnedpasswords.com/range/' + str(query_chars)
    Response = requests.get(url)
    if Response.status_code != 200:
        raise RuntimeError(f'Error: {Response.status_code}, check the API and try again.')
    return Response

def getpsswrd_leaks_count(hashes, checkhash):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == checkhash:
            return count
    return 0

def api_checkpwned(password):
    sha1passwrd = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    usable, nonusable = sha1passwrd[:5], sha1passwrd[5:]
    response2 = request_api_data(usable)
    return getpsswrd_leaks_count(response2, nonusable)

def inputpass():
    password_storer = []
    clientpass = input('Please input your password: ')
    with open('./Password.txt', 'w+') as createuserpassword:
        createuserpassword.write(f'{clientpass}')
    
    with open('./Password.txt', 'r') as userpassword:
        userpass = userpassword.read()
        password_storer.append(userpass)
    return password_storer

def main():
    for password in inputpass():
        count = api_checkpwned(password)
        securepass = len(password) * '*'
        if count:
            print(f'{securepass} was found {count} times.')
        else:
            print(f'{securepass} was not found.')
    
    with open('./Password.txt', 'w+') as final:
        encrypted = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        final.write(f'{encrypted}')

if __name__ == '__main__':
    main()