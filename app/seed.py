"""Idempotent import and immutable precomputed daily schedule (2026-2030)."""
import json
from datetime import date, timedelta
from pathlib import Path
from sqlalchemy import select
from .db import make_engine
from .models import Category, DailyFortune, Fortune, Language
from sqlalchemy.orm import Session

def seed():
    payload = json.loads((Path(__file__).resolve().parent.parent / "data/sample.json").read_text(encoding="utf-8"))
    with Session(make_engine()) as db:
        for row in payload["languages"]:
            if db.get(Language,row["code"]) is None:
                db.add(Language(**row, enabled=True))
        for row in payload["categories"]:
            if db.get(Category,row["slug"]) is None:
                db.add(Category(**row))
        db.flush()
        for row in payload["fortunes"]:
            if db.get(Fortune,row["id"]) is None:
                db.add(Fortune(id=row["id"],text=row["text"],language_code=row["language"],enabled=True,eligible_for_daily=True,categories=[db.get(Category,c) for c in row["categories"]]))
        db.flush()
        # Fixed calendar: insert missing days only; never rewrite existing choices.
        for lang in payload["languages"]:
            ids = sorted(f["id"] for f in payload["fortunes"] if f["language"]==lang["code"])
            day = date(2026,1,1)
            end = date(2030,12,31)
            existing = set(db.scalars(select(DailyFortune.date_utc).where(DailyFortune.language_code==lang["code"])).all())
            offset = 0
            while day <= end:
                if day not in existing:
                    db.add(DailyFortune(date_utc=day, language_code=lang["code"], fortune_id=ids[offset % len(ids)]))
                offset += 1
                day += timedelta(days=1)
        db.commit()
    print("Sample catalogue and daily calendar seeded.")

if __name__ == "__main__":
    seed()
