from sqlalchemy.orm import Session
import models.models as models


def get_url_by_short_id(db: Session, short_id: str):
    return db.query(models.URLs).filter(models.URLs.short_id == short_id).first()


def create_url(db: Session, short_id: str, long_url: str):
    db_url = models.URLs(short_id=short_id, long_url=long_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url
