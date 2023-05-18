from base64 import b64decode, b64encode
import rsa

def generate_license(email, private_key):
    key = rsa.PrivateKey.load_pkcs1(private_key)
    return b64encode(rsa.sign(email.encode(), key, 'SHA-1')).decode()

def new_rsa():
    public, private = rsa.newkeys(512)
    return public.save_pkcs1().decode(), private.save_pkcs1().decode()

def validate_signature(email, license_key, public_key):
    print(email)
    print(license_key)
    print(public_key)

    key = rsa.PublicKey.load_pkcs1(public_key)
    try:
        rsa.verify(email.encode(), b64decode(license_key), key)
    except rsa.VerificationError:
        return False
    else:
        return True
