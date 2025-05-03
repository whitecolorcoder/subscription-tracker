
from src.config import settings
from src.models.base import Base
from sqlalchemy import create_engine

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

Base.metadata.create_all(bind=engine)