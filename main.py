from fastapi import FastAPI
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models.models as models
from db.database import SessionLocal, engine
from fastapi.responses import RedirectResponse

from utils.db import create_url, get_url_by_short_id
from utils.common import generate_shorten_url
from models.request import URLRequest

app = FastAPI(
    title="URL Shortener",
    description="URL Shortener API using FastAPI and SQLite",
    version="1.0.0",
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/shorten", tags=["URL Shortener"])
def shorten_url_func(url_request: URLRequest, db: Session = Depends(get_db)):
    try:
        long_url = url_request.url
        short_id = generate_shorten_url()
        db_url = create_url(db, short_id, long_url)
        print("Response from DB: ", db_url)
        print(get_url_by_short_id(db, short_id))
        return {
            "short_url": short_id,
            "status": "success"
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error while trying to shorten the URL")


@app.get("/{short_id}", tags=["URL Shortener"])
def redirect_url(short_id: str, db: Session = Depends(get_db)):
    try:
        db_url = get_url_by_short_id(db, short_id)
        if db_url:
            if not db_url.long_url.startswith("http"):
                db_url.long_url = "https://" + db_url.long_url
            return RedirectResponse(url=db_url.long_url)
        else:
            raise HTTPException(status_code=404, detail="URL not found")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error while calling the redirect URL")
