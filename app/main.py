from datetime import datetime, timezone
from random import SystemRandom
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from .db import get_session
from .models import Category, DailyFortune, Fortune, Language

app = FastAPI(title="Fortune Rabbit API", version="0.1.0", description="API publique de phrases — V1 locale")
rng = SystemRandom()
DB = Annotated[Session, Depends(get_session)]

def err(code, message, status=404):
    raise HTTPException(status_code=status, detail={"code":code,"message":message})

@app.exception_handler(HTTPException)
async def http_error(_request: Request, exc: HTTPException):
    detail = exc.detail if isinstance(exc.detail, dict) else {"code":"HTTP_ERROR","message":str(exc.detail)}
    return JSONResponse(status_code=exc.status_code, content={"error": detail})

def pack(f: Fortune, *, date=None):
    data = {"id":f.id,"text":f.text,"language":f.language_code,"categories":sorted(c.slug for c in f.categories)}
    if date is not None:
        data["date"] = date.isoformat()
    return {"data": data, "meta":{"source":"api","api_version":"1"}}

def ensure_language(db, lang):
    l = db.get(Language, lang)
    if l is None or not l.enabled:
        err("FORTUNE_NOT_FOUND", "Langue indisponible.")

def pick(db, lang, categories=None):
    ensure_language(db, lang)
    stmt = select(Fortune).where(Fortune.language_code==lang, Fortune.enabled.is_(True))
    if categories:
        known = set(db.scalars(select(Category.slug)).all())
        if any(c not in known for c in categories):
            err("INVALID_PARAMETER","Catégorie inconnue.",400)
        stmt = stmt.where(Fortune.categories.any(Category.slug.in_(categories)))
    choices = db.scalars(stmt).unique().all()
    if not choices:
        err("FORTUNE_NOT_FOUND","Aucune phrase ne correspond aux critères demandés.")
    return pack(rng.choice(choices))

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/v1/fortunes/random")
def random_fortune(db: DB, lang: str="fr", category: list[str] | None=Query(default=None)):
    return pick(db,lang,category)

@app.get("/v1/fortunes/daily")
def daily(db: DB, lang: str="fr"):
    ensure_language(db,lang)
    today=datetime.now(timezone.utc).date()
    entry = db.get(DailyFortune, (today,lang))
    if entry is None:
        err("FORTUNE_NOT_FOUND","Calendrier officiel indisponible pour cette date.")
    return pack(entry.fortune,date=today)

@app.get("/v1/fortunes/answer")
def answer(db: DB, lang: str="fr"):
    return pick(db,lang,["reponses"])

@app.get("/v1/fortunes/{id}")
def by_id(id: str, db: DB):
    f=db.get(Fortune,id)
    if f is None or not f.enabled:
        err("FORTUNE_NOT_FOUND","Phrase introuvable.")
    return pack(f)

@app.get("/v1/categories")
def categories(db: DB):
    rows=db.scalars(select(Category).order_by(Category.slug)).all()
    return {"data":[{"slug":r.slug,"label":r.label} for r in rows],"meta":{"source":"api","api_version":"1"}}

@app.get("/v1/languages")
def languages(db: DB):
    rows=db.scalars(select(Language).where(Language.enabled.is_(True)).order_by(Language.code)).all()
    return {"data":[{"code":r.code,"label":r.label} for r in rows],"meta":{"source":"api","api_version":"1"}}
