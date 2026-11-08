from datetime import date
from sqlalchemy import Boolean, Date, ForeignKey, ForeignKeyConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base

class Language(Base):
    __tablename__ = "languages"
    code: Mapped[str] = mapped_column(String(16), primary_key=True)
    label: Mapped[str] = mapped_column(String(80))
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)

class Category(Base):
    __tablename__ = "categories"
    slug: Mapped[str] = mapped_column(String(40), primary_key=True)
    label: Mapped[str] = mapped_column(String(80))

class FortuneCategory(Base):
    __tablename__ = "fortune_categories"
    fortune_id: Mapped[str] = mapped_column(ForeignKey("fortunes.id"), primary_key=True)
    category_slug: Mapped[str] = mapped_column(ForeignKey("categories.slug"), primary_key=True)

class Fortune(Base):
    __tablename__ = "fortunes"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    language_code: Mapped[str] = mapped_column(ForeignKey("languages.code"), index=True)
    text: Mapped[str] = mapped_column(Text)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    eligible_for_daily: Mapped[bool] = mapped_column(Boolean, default=True)
    categories = relationship("Category", secondary="fortune_categories", lazy="selectin")

class DailyFortune(Base):
    __tablename__ = "daily_fortunes"
    date_utc: Mapped[date] = mapped_column(Date, primary_key=True)
    language_code: Mapped[str] = mapped_column(ForeignKey("languages.code"), primary_key=True)
    fortune_id: Mapped[str] = mapped_column(ForeignKey("fortunes.id"))
    fortune = relationship("Fortune", lazy="selectin")
