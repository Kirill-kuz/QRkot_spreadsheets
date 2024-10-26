from datetime import datetime
from app.core import Base
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Integer)


class Invested(Base):
    __abstract__ = True
    create_date = Column(
        DateTime, default=datetime.now)
    close_date = Column(
        DateTime,
        default=None,
        nullable=True)
    full_amount = Column(Integer, nullable=False)
    fully_invested = Column(
        Boolean,
        default=False,
        nullable=False,
        index=True)
    invested_amount = Column(
        Integer, default=0, nullable=False)

    __table_args__ = (
        CheckConstraint(
            'full_amount > 0',
            name='verifi_full_amount_positive'
        ),
        CheckConstraint(
            'full_amount >= invested_amount >= 0',
            name='verifi_pos_invested_amount'
        ),
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'invested_amount' not in kwargs:
            self.invested_amount = 0

    def __repr__(self):
        return (
            f"<Investment("
            f"{self.full_amount=}, "
            f"{self.invested_amount=}, "
            f"{self.fully_invested=}, "
            f"create_date={self.create_date}, "
            f"close_date={self.close_date})>"
        )
