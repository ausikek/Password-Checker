import requests
import hashlib as hl


def Master(senha):
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
        response2 = request_api_data(usable)
        return getpsswrd_leaks_count(response2, nonusable)

    def inputpass(senha):
        L = []
        L.append(senha)
        return L

    def main(senha):
        for password in inputpass(senha):
            count = api_check_pwned(password)
            securepass = len(password) * '*'
            if count:
                return f'{securepass} was found {count} times. Oh Oh!'
            else:
                return f'{securepass} was not found. Congratulations!'
    return main(senha)