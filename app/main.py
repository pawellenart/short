from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import RedirectResponse
from app.database import Base, engine, get_db
from app.models import URL
from app.utils import generate_numeric_key, generate_random_string, is_custom_keyword_available


app = FastAPI()


@app.get("/")
def read_root():
    return {"detail": "ok"}


@app.post("/")
def create_short_url(url: str = Body(...), key_type: str = Body("numeric", embed=True), custom_key: str = Body(None), db: Session = Depends(get_db)):
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
    return new_url


@app.post("/install")
def install(db: Session = Depends(get_db)):
    try:
        # Create the database tables
        Base.metadata.create_all(bind=engine)
        return {"message": "Database schema created successfully."}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/{shortkey}")
def redirect_short_url(shortkey: str, db: Session = Depends(get_db)):
    db_url = db.query(URL).filter(URL.shortkey == shortkey).first()
    if db_url:
        return RedirectResponse(url=str(db_url.url))
    else:
        raise HTTPException(status_code=404, detail="Short URL not found")
