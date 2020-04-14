from Crypto.PublicKey import RSA


def create_RSA():
    key = RSA.generate(2048)
    f = open('mykey.key','wb+')
    f.write(key.export_key('PEM'))
    f.close()
    return'mykey.key'
def RSA_toString():
    f = open('mykey.key', 'r')
    rsa = ""
    for line in f:
        rsa = rsa + line
    return rsa