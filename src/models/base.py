from typing import List
from datetime import datetime
from sqlalchemy import ForeignKey, String, Boolean, DateTime, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass