from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Extra,
    PositiveInt)


class DonationBase(BaseModel):
    comment: Optional[str]
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationUpdate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    user_id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
