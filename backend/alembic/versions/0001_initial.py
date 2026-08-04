"""initial

Revision ID: 0001_initial
Revises: 
Create Date: 2026-07-31

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create tables via SQLAlchemy metadata (sa) by importing app models
    from app.db import init_db
    init_db()


def downgrade():
    # drop all tables
    from app.db import engine
    from app.models_db import Base
    Base.metadata.drop_all(bind=engine)
