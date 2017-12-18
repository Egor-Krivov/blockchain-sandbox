from Crypto import Random
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
random_generator = Random.new().read

RSAkey = RSA.generate(1024, random_generator)   # This will take a while...
text = 'abcdefgh'

print(RSAkey.publickey())

plaintext = str(text).encode('utf-8')
hash = plaintext#MD5.new(plaintext).digest()
signature = RSAkey.sign(hash, '')
print(signature)

print(RSAkey.verify(hash, signature))     # This sig will check out
print(RSAkey.verify(hash[:-1], signature)) # This sig will fail

RSA.exp()

pubkey = 'MIGfMA0GCSqGSIb3DQEBA3UAA4GNADCBiQKBgQC35eMaYoJXEoJt5HxarHkzDBEMU3qIWE0HSQ77CwP/8UbX07W2XKwngUyY4k6Hl2M/n9TOZMZsiBzer/fqV+QNPN1m9M94eUm2gQgwkoRj5battRCaNJK/23GGpCsTQatJN8PZBhJBb2Vlsvw5lFrSdMT1R7vaz+2EeNR/FitFXwIDAQAB'
msg = "test"
keyDER = b64decode(pubkey)
keyPub = RSA.importKey(keyDER)
