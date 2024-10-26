from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import (
    current_superuser,
    current_user,
    get_async_session)
from app.crud import charity_project_crud, donation_crud
from app.models import User
from app.schemas import DonationCreate, DonationDB
from app.services.payment import investment_procces


router = APIRouter()


@router.get(
    path='/',
    response_model=List[DonationDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session=Depends(get_async_session)
):
    return await donation_crud.get_multi(session)


@router.post(
    path='/',
    response_model=DonationDB,
    response_model_exclude={
        'user_id',
        'invested_amount',
        'fully_invested',
        'close_date',
    },
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    new_donation = await donation_crud.create(
        donation, session, user, False)
    session.add_all(
        investment_procces(
            target=new_donation,
            sources=await charity_project_crud.get_opens(session)
        )
    )
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    path='/my',
    response_model=List[DonationDB],
    response_model_exclude={
        'user_id',
        'close_date',
        'fully_invested',
        'invested_amount',
        'close_date'
    }
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(
        get_async_session)):
    donations = await donation_crud.get_user_donations(
        user, session)
    return donations
