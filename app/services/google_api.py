from datetime import datetime
from copy import deepcopy
from aiogoogle import Aiogoogle
from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'

SPREADSHEET_BODY_TEMPLATE = {
    'properties': {
        'title': '',
        'locale': 'ru_RU'},
    'sheets': [
        {
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Лист1',
                'gridProperties': {
                    'rowCount': 100,
                    'columnCount': 11
                }
            }
        }
    ]
}

async def spreadsheets_create(wrapper_services: Aiogoogle) -> dict:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = deepcopy(SPREADSHEET_BODY_TEMPLATE)
    spreadsheet_body['properties']['title'] = f'Отчет на {now_date_time}'
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body))
    return {'spreadsheetId': response['spreadsheetId'],
            'spreadsheetUrl': response['spreadsheetUrl']}

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

async def spreadsheets_update_value(spreadsheet_id: str, closed_projects: list,
                                     wrapper_services: Aiogoogle) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_info = await wrapper_services.as_service_account(
        service.spreadsheets.get(spreadsheetId=spreadsheet_id,
                                 fields='sheets/properties'))
    sheet_properties = spreadsheet_info['sheets'][0]['properties']
    num_rows = sheet_properties['gridProperties']['rowCount']
    num_cols = sheet_properties['gridProperties']['columnCount']

    table_header = [['Отчет от', now_date_time],
                    ['Топ проектов по скорости закрытия'],
                    ['Название проекта', 'Время сбора', 'Описание']]
    data_values = [list(map(str, project)) for project in closed_projects]
    total_rows = len(table_header) + len(data_values)

    if total_rows > num_rows or len(data_values[0]) > num_cols:
        raise ValueError(
            'Предоставленные данные не помещаются в созданную таблицу')

    table_values = [*table_header, *data_values]
    update_body = {'majorDimension': 'ROWS', 'values': table_values}
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='R1C1:R{0}C{1}'.format(total_rows, num_cols),
            valueInputOption='USER_ENTERED', json=update_body))
