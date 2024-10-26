from sqlalchemy import select, extract
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import CharityProject
from app.schemas import CharityProjectCreate, CharityProjectUpdate


class CRUDCharityProject(CRUDBase[CharityProject, CharityProjectCreate,
                                  CharityProjectUpdate]):
    async def get_by_name(
        self, name: str, session: AsyncSession
    ) -> CharityProject:
        return (await session.execute(
            select(self.model).where(
                self.model.name == name,
            )
        )).scalars().first()

    async def get_projects_by_completion_rate(
            self, session: AsyncSession) -> list:
        projects = await session.execute(
            select(CharityProject.name, CharityProject.description,
                   (extract('year', CharityProject.close_date) - extract(
                       'year', CharityProject.create_date)) * 365 +
                   (extract('month', CharityProject.close_date) - extract(
                       'month', CharityProject.create_date)) * 30 +
                   (extract('day', CharityProject.close_date) - extract(
                       'day', CharityProject.create_date)))
            .where(CharityProject.fully_invested == 1)
            .order_by((extract('year', CharityProject.close_date) - extract(
                'year', CharityProject.create_date)) * 365 + (
                    extract('month', CharityProject.close_date) - extract(
                        'month', CharityProject.create_date)) * 30 + (extract(
                            'day', CharityProject.close_date) - extract(
                                'day', CharityProject.create_date))))
        return projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
