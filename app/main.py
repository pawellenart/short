from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from app.database import get_db
from app.models import URL
from app.utils import generate_numeric_key, generate_random_string, is_custom_keyword_available


app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:8765",  # React app URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"detail": "ok"}


@app.post("/")
def create_short_url(
    url: str = Body(...),
    # Default key_type to "numeric"
    key_type: str = Body("numeric", embed=True),
    custom_key: str = Body(None),
    db: Session = Depends(get_db)
):

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
def get_all_urls(db: Session = Depends(get_db)):
    urls = db.query(URL).order_by(URL.date_created.desc()).all()
    return urls


@app.get("/{shortkey}")
def redirect_short_url(shortkey: str, db: Session = Depends(get_db)):
    db_url = db.query(URL).filter(URL.shortkey == shortkey).first()
    if db_url:
        return RedirectResponse(url=str(db_url.url))
    else:
        raise HTTPException(status_code=404, detail="Short URL not found")
