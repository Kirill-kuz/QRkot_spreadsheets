from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def verifi_name_allready_exists(
    charity_project_name: str, session: AsyncSession
) -> None:
    charity_project_db = await charity_project_crud.get_by_name(
        charity_project_name, session
    )
    if charity_project_db:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail='Проект с таким именем уже существует!'
        )


async def verifi_charity_project_before_update(
    update_data: CharityProjectUpdate,
    charity_project: CharityProject,
    session: AsyncSession
) -> None:
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail='Закрытый проект нельзя редактировать!'
        )
    if update_data.name:
        await verifi_name_allready_exists(
            update_data.name, session
        )
    if (update_data.full_amount and
            update_data.full_amount < charity_project.invested_amount):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail=f'В {charity_project.name} уже '
                   f'проинвестировано {charity_project.invested_amount}'
        )


async def get_charity_project_by_id(
    charity_project_id: int, session: AsyncSession
) -> CharityProject:
    charity_project_db = await charity_project_crud.get(
        charity_project_id, session
    )
    if not charity_project_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail='Проект не найден!'
        )
    return charity_project_db


def verifi_for_zero_invested_amount(
    charity_project: CharityProject
) -> None:
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail='Закрытый проект нельзя редактировать!'
        )
