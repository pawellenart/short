import random
import string
from sqlalchemy.orm import Session
from app.models import URL


def generate_numeric_key(db: Session):
    last_url = db.query(URL).order_by(URL.shortkey.desc()).first()
    if last_url and last_url.shortkey.isdigit():
        return str(int(last_url.shortkey) + 1)
    return "1"


def generate_random_string(length=7):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def is_custom_keyword_available(db: Session, keyword: str):
    return db.query(URL).filter(URL.shortkey == keyword).first() is None
