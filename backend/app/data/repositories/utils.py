import bcrypt
from decimal import Decimal

def hashPassword(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def checkPassword(hash: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hash.encode())

def convertAmountToMinDenomination(amount: Decimal) -> Decimal:
    return amount * 100