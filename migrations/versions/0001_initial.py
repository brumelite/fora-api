"""Initial schema
Revision ID: 0001
Revises:
"""
from alembic import op
import sqlalchemy as sa
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("languages", sa.Column("code", sa.String(16), primary_key=True), sa.Column("label", sa.String(80), nullable=False), sa.Column("enabled", sa.Boolean(), nullable=False))
    op.create_table("categories", sa.Column("slug", sa.String(40), primary_key=True), sa.Column("label", sa.String(80), nullable=False))
    op.create_table("fortunes", sa.Column("id", sa.String(32), primary_key=True), sa.Column("language_code", sa.String(16), sa.ForeignKey("languages.code"), nullable=False), sa.Column("text", sa.Text(), nullable=False), sa.Column("enabled", sa.Boolean(), nullable=False), sa.Column("eligible_for_daily", sa.Boolean(), nullable=False))
    op.create_index("ix_fortunes_language_code", "fortunes", ["language_code"])
    op.create_table("fortune_categories", sa.Column("fortune_id", sa.String(32), sa.ForeignKey("fortunes.id"), primary_key=True), sa.Column("category_slug", sa.String(40), sa.ForeignKey("categories.slug"), primary_key=True))
    op.create_table("daily_fortunes", sa.Column("date_utc", sa.Date(), primary_key=True), sa.Column("language_code", sa.String(16), sa.ForeignKey("languages.code"), primary_key=True), sa.Column("fortune_id", sa.String(32), sa.ForeignKey("fortunes.id"), nullable=False))

def downgrade():
    op.drop_table("daily_fortunes")
    op.drop_table("fortune_categories")
    op.drop_index("ix_fortunes_language_code", "fortunes")
    op.drop_table("fortunes")
    op.drop_table("categories")
    op.drop_table("languages")
