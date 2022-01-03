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

