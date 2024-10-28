from datetime import datetime
from copy import deepcopy
from typing import List, Tuple

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models import CharityProject

FORMAT = '%Y/%m/%d %H:%M:%S'
MAX_ROWS = 100
MAX_COLS = 50
SPREADSHEET_TITLE = 'Отчет на {date}'
SPREADSHEET_BODY_TEMPLATE = dict(
    properties=dict(
        title='',
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=MAX_ROWS,
            columnCount=MAX_COLS,
        )
    ))]
)
TABLE_HEADER = [
    ['Отчет от'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(
        wrapper_services: Aiogoogle, spreadsheet_body=None) -> Tuple[str, str]:
    if spreadsheet_body is None:
        spreadsheet_body = deepcopy(SPREADSHEET_BODY_TEMPLATE)
        spreadsheet_body['properties']['title'] = SPREADSHEET_TITLE.format(
            date=datetime.now().strftime(FORMAT)
        )
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId'], response['spreadsheetUrl']


async def set_user_permissions(spreadsheet_id: str,
                               wrapper_services: Aiogoogle) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id, json=permissions_body, fields='id'))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: List[CharityProject],
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    table_header = deepcopy(TABLE_HEADER)
    table_header[0][1] = datetime.now().strftime(FORMAT)
    table_values = [
        *table_header,
        *[list(map(str, [
            attr.name, attr.close_date - attr.create_date, attr.description
        ])) for attr in projects],
    ]
    rows = len(table_values)
    cols = max(map(len, table_values))
    if rows > MAX_ROWS or cols > MAX_COLS:
        raise ValueError(
            f'Предоставленные данные не помещаются в созданную таблицу '
            f'Сформированно строк {rows}. Допустимо строк {MAX_ROWS}. '
            f'Сформированно столбцов {cols}. Допустимо строк {MAX_COLS}. '
        )
    update_body = {
        'majorDimension': 'ROWS', 'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id, range=f'R1C1:R{rows}C{cols}',
            valueInputOption='USER_ENTERED', json=update_body))
