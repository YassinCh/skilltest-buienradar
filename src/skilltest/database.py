from sqlmodel import create_engine

from .config import settings

engine = create_engine(
    settings.database_url,
    echo=settings.echo_sql,
    connect_args={"check_same_thread": False},  # Needed for SQLite
)
