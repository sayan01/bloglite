# helper function
def hashpass(username, password):
    from hashlib import sha512
    converter = sha512()
    token = username*len(password)+password*len(username)
    converter.update(token.encode('utf-8'))
    return converter.hexdigest()
