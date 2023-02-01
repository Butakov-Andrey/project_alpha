import bcrypt


def hash_password(password: str):
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    password_hash = password_hash.decode()
    return password_hash


def check_password(pass_from_user: str, hashed_pass_from_db: str):
    return bcrypt.checkpw(pass_from_user.encode(), hashed_pass_from_db.encode())
