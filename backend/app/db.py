import os

from sqlalchemy import create_engine

from sqlalchemy.orm import (
    sessionmaker,
    declarative_base
)





# =====================================================
# Database URL
# =====================================================

# Render/Supabase:
# DATABASE_URL will come from environment variables
#
# Local development:
# fallback to SQLite


DATABASE_URL = os.getenv(

    "DATABASE_URL",

    "sqlite:///./dev.db"

)








# =====================================================
# Normalize PostgreSQL URL
# =====================================================

def _normalize_database_url(
    url: str
) -> str:


    # Supabase / Render usually provide:
    # postgresql://...


    if url.startswith(
        "postgresql://"
    ) and "+psycopg" not in url:


        return url.replace(

            "postgresql://",

            "postgresql+psycopg://",

            1

        )




    # Some providers use:
    # postgres://...


    if url.startswith(

        "postgres://"

    ):


        return url.replace(

            "postgres://",

            "postgresql+psycopg://",

            1

        )



    return url







SQLALCHEMY_DATABASE_URL = _normalize_database_url(

    DATABASE_URL

)








# =====================================================
# SQLAlchemy Engine
# =====================================================


if SQLALCHEMY_DATABASE_URL.startswith(

    "sqlite"

):


    engine = create_engine(

        SQLALCHEMY_DATABASE_URL,


        connect_args={

            "check_same_thread": False

        }

    )


else:


    # PostgreSQL
    # Supabase / Render


    engine = create_engine(

        SQLALCHEMY_DATABASE_URL,


        pool_pre_ping=True,

        pool_recycle=300

    )









# =====================================================
# Session
# =====================================================


SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine

)






# =====================================================
# Base Model
# =====================================================


Base = declarative_base()









# =====================================================
# Initialize Database
# =====================================================


def init_db():


    # Import models to register tables

    from . import models_db



    Base.metadata.create_all(

        bind=engine

    )