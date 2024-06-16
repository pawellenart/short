import secrets
import os
from fastapi import FastAPI, Depends, HTTPException, Body, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import RedirectResponse
from app.database import Base, engine, get_db
from app.models import URL
from app.utils import generate_numeric_key, generate_random_string, is_custom_keyword_available, set_option, get_option


app = FastAPI()
security = HTTPBasic()


def verify_basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = os.getenv("BASIC_AUTH_USERNAME")
    correct_password = os.getenv("BASIC_AUTH_PASSWORD")
    if not (secrets.compare_digest(credentials.username, correct_username) and secrets.compare_digest(credentials.password, correct_password)):
        raise HTTPException(
            status_code=401, detail="Incorrect username or password")


@app.get("/")
def read_root():
    return {"detail": "ok"}


@app.post("/install")
def install(credentials: HTTPBasicCredentials = Depends(verify_basic_auth), db: Session = Depends(get_db)):
    try:
        # Create the database tables
        Base.metadata.create_all(bind=engine)
        return {"message": "Database schema created successfully."}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/generate-api-key")
def generate_api_key(credentials: HTTPBasicCredentials = Depends(verify_basic_auth), db: Session = Depends(get_db)):
    new_api_key = secrets.token_hex(16)
    set_option(db, "api_key", new_api_key)
    return {"api_key": new_api_key}


@app.post("/")
def create_short_url(
    url: str = Body(...),
    # Default key_type to "numeric"
    key_type: str = Body("numeric", embed=True),
    custom_key: str = Body(None),
    api_key: str = Header(None, alias="X-Api-Key"),
    db: Session = Depends(get_db)
):
    stored_api_key = get_option(db, "api_key")
    if not stored_api_key or stored_api_key.options_value != api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")

    shortkey = None

    if key_type == "numeric":
        shortkey = generate_numeric_key(db)
    elif key_type == "random":
        shortkey = generate_random_string()
    elif key_type == "custom":
        if custom_key and is_custom_keyword_available(db, custom_key):
            shortkey = custom_key
        else:
            raise HTTPException(
                status_code=400, detail="Custom key is not available or not provided")
    else:
        raise HTTPException(status_code=400, detail="Invalid key type")

    new_url = URL(shortkey=shortkey, url=url)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return {
        "shortkey": new_url.shortkey,
        "url": new_url.url,
        "date_created": new_url.date_created  # Include date_created in the response
    }


@app.get("/{shortkey}")
def redirect_short_url(shortkey: str, db: Session = Depends(get_db)):
    db_url = db.query(URL).filter(URL.shortkey == shortkey).first()
    if db_url:
        return RedirectResponse(url=str(db_url.url))
    else:
        raise HTTPException(status_code=404, detail="Short URL not found")
