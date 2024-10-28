from datetime import datetime
from copy import deepcopy
from typing import List, NamedTuple

from aiogoogle import Aiogoogle, HTTPError
from fastapi import HTTPException
from http import HTTPStatus

from app.core.config import settings
from app.models import CharityProject



FORMAT = '%Y/%m/%d %H:%M:%S'
MAX_ROWS = 100
MAX_COLS = 50
SPREADSHEET_TITLE = 'Отчет на {date}'
SPREADSHEET_BODY_TEMPLATE = dict(
    properties=dict(
        title=SPREADSHEET_TITLE.format(date=datetime.now().strftime(FORMAT)),
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
    ['Отчет от', datetime.now().strftime(FORMAT)],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


class SpreadsheetInfo(NamedTuple):
       spreadsheet_id: str
       spreadsheet_url: str


async def spreadsheets_create(wrapper_services: Aiogoogle,
                                  spreadsheet_body=None) -> SpreadsheetInfo:
    if spreadsheet_body is None:
        spreadsheet_body = deepcopy(SPREADSHEET_BODY_TEMPLATE)
        spreadsheet_body['properties']['title'] = SPREADSHEET_TITLE.format(
            date=datetime.now().strftime(FORMAT)
        )
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return SpreadsheetInfo(response['spreadsheetId'],
                           response['spreadsheetUrl'])


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
        spreadsheetid: str,
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
    try:
        await wrapper_services.as_service_account(
            service.spreadsheets.values.update(
                spreadsheetId=spreadsheetid, range=f'R1C1:R{rows}C{cols}',
                valueInputOption='USER_ENTERED', json=update_body))
    except (ValueError, HTTPError) as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, 
            detail=f'Ошибка при обновлении данных в таблице: {e}'
        )


async def get_spreadsheet_url(spreadsheet_id: str,
                              wrapper_services: Aiogoogle):
    response = await wrapper_services.spreadsheets.v4.Spreadsheets().get(
        spreadsheetId=spreadsheet_id
    ).execute()
    return response['spreadsheetUrl'] 
