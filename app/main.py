from fastapi import FastAPI

from app.api import main_router
from app.core import create_first_superuser


app = FastAPI()
app.include_router(main_router)


@app.on_event('startup')
async def startup():
    await create_first_superuser()
