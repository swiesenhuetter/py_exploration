from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["sha256_crypt"])

secret_password = "password_123456"

def get_password_hash(password):
    hashed_pw = pwd_context.hash(password)
    return hashed_pw

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


if __name__ == "__main__":
    print(get_password_hash(secret_password))
    print(verify_password(secret_password, get_password_hash(secret_password)))
    
    print(verify_password("wrong_password", get_password_hash(secret_password)))
    print(verify_password(secret_password, get_password_hash("wrong_password")))