import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(hash: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hash.encode())

def convert_amount_to_min_denomination(amount: int) -> int:
    return amount * 100