from base64 import b64decode, b64encode
import rsa

def generate_license(email, private_key):
    return b64encode(rsa.sign(email.encode(), private_key, 'SHA-1')).decode()

def new_rsa():
    public, private = rsa.newkeys(512)
    return (public, private)

def valid(email, license_key, public_key):
    with open(public_key, 'rb') as file:
        key = rsa.PublicKey.load_pkcs1(file.read())
    try:
        rsa.verify(email.encode(), b64decode(license_key), key)
    except rsa.VerificationError:
        return False
    else:
        return True
