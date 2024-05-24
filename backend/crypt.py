import bcrypt


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def check_password(entered_password, hashed_password):
    hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(entered_password.encode('utf-8'), hashed_password)