import os
import secrets
import bcrypt
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Body, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from starlette.responses import RedirectResponse
from app.database import get_db
from app.models import URL, ApiKey
from app.utils import generate_numeric_key, generate_random_string, is_custom_keyword_available
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:8765",  # Frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic()


def verify_basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = os.getenv("BACKEND_USERNAME", None)
    correct_password = os.getenv("BACKEND_PASSWORD", None)
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password")


def hash_api_key(api_key: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(api_key.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_api_key(api_key: str, db: Session):
    api_key_entry = db.query(ApiKey).filter(
        ApiKey.api_key != None).all()  # Retrieve all non-null keys
    for entry in api_key_entry:
        if bcrypt.checkpw(api_key.encode('utf-8'), entry.api_key.encode('utf-8')):
            return True
    raise HTTPException(status_code=403, detail="Invalid API key")


@app.get("/")
def read_root():
    return {"detail": "ok"}


@app.post("/api")
def generate_api_key(
    db: Session = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(verify_basic_auth)
):
    new_api_key = secrets.token_hex(32)
    hashed_api_key = hash_api_key(new_api_key)
    api_key_entry = ApiKey(api_key=hashed_api_key)
    db.add(api_key_entry)
    db.commit()
    db.refresh(api_key_entry)
    return {"api_key": new_api_key}


@app.post("/")
def create_short_url(
    url: str = Body(...),
    # Default key_type to "numeric"
    key_type: str = Body("numeric", embed=True),
    custom_key: str = Body(None),
    api_key: str = Query(...),
    db: Session = Depends(get_db)
):
    verify_api_key(api_key, db)

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


@app.get("/urls")
def get_all_urls(
    api_key: str = Query(...),
    db: Session = Depends(get_db),
    page: int = Query(1, alias="page", ge=1),
    page_size: int = Query(10, alias="page_size", ge=1, le=100),
    sort_by: str = Query("date_created", alias="sort_by"),
    sort_order: str = Query("desc", alias="sort_order")
):
    verify_api_key(api_key, db)

    # Determine the sorting order
    sort_column = getattr(URL, sort_by, None)
    if not sort_column:
        raise HTTPException(
            status_code=400, detail=f"Invalid sort_by value: {sort_by}")

    if sort_order == "desc":
        sort_column = desc(sort_column)
    elif sort_order == "asc":
        sort_column = asc(sort_column)
    else:
        raise HTTPException(
            status_code=400, detail=f"Invalid sort_order value: {sort_order}")

    # Query the database with pagination and sorting
    offset = (page - 1) * page_size
    urls_query = db.query(URL).order_by(
        sort_column).offset(offset).limit(page_size)
    urls = urls_query.all()

    total_urls = db.query(URL).count()
    total_pages = (total_urls // page_size) + \
        (1 if total_urls % page_size != 0 else 0)

    return {
        "total": total_urls,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "urls": urls
    }


@app.get("/{shortkey}")
def redirect_short_url(shortkey: str, db: Session = Depends(get_db)):
    db_url = db.query(URL).filter(URL.shortkey == shortkey).first()
    if db_url:
        return RedirectResponse(url=str(db_url.url))
    else:
        raise HTTPException(status_code=404, detail="Short URL not found")
