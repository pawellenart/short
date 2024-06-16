import random
import string
from sqlalchemy.orm import Session
from app.models import URL, Options


def generate_numeric_key(db: Session):
    last_url = db.query(URL).order_by(URL.shortkey.desc()).first()
    if last_url and last_url.shortkey.isdigit():
        return str(int(last_url.shortkey) + 1)  # type: ignore
    return "1"


def generate_random_string(length=7):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def is_custom_keyword_available(db: Session, keyword: str):
    return db.query(URL).filter(URL.shortkey == keyword).first() is None


def set_option(db: Session, key: str, value: str):
    option = db.query(Options).filter(Options.options_key == key).first()
    if option:
        option.options_value = value  # type: ignore
    else:
        option = Options(options_key=key, options_value=value)
        db.add(option)
    db.commit()
    db.refresh(option)
    return option


def get_option(db: Session, key: str):
    return db.query(Options).filter(Options.options_key == key).first()
