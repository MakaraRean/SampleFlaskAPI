import base64
import hashlib

from passlib.context import CryptContext
import bcrypt

pas =str(123)
secret = "2DF97463AF0944F4F459BC06E5CF8D47"
hash_pas = CryptContext(schemes=['bcrypt'], deprecated="auto").hash(pas)+secret

def verify_password(password: str, hashed_password: str) -> bool:
    if isinstance(password, str):
        password = password.encode()

    verified_hash = hashed_password.replace(secret,"")

    # check_hash = CryptContext(schemes=['bcrypt'], deprecated="auto").hash(password)
    return bcrypt.checkpw(password, verified_hash.encode())

if __name__ == "__main__":
    print(f"password : {pas}\nhash password: {hash_pas}\n")


    print(verify_password(password="123",hashed_password=hash_pas))