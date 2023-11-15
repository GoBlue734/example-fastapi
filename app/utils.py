from passlib.context import CryptContext#imports the CryptContext class from the passlib.context module


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")#creates a CryptContext instance

def hash(password: str):#function to hash a password
    return pwd_context.hash(password)#returns the hashed password

def verify(plain_password: str, hashed_password: str):#function to verify a password
    return pwd_context.verify(plain_password, hashed_password)#returns True if the password is verified, False otherwise