from sqlalchemy import Column, String, Text

from app.core import Base
from .base import Invested


class CharityProject(Invested, Base):
    name = Column(String(
        length=100),
        unique=True,
        nullable=False)
    description = Column(
        Text,
        nullable=False)

    def __repr__(self):
        return (
            f'{self.name=}, '
            f'{self.description=}, '
            f'{super().__repr__()})')
