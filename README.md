# Финальный проект спринта: отчёт в Google Sheets для QRKot
## Описание
Проект QRKot — это приложение для Благотворительного фонда поддержки котиков на FastAPI.
В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.
Проект расширяется с добавлением возможности формирования отчёта в гугл-таблице, который содержит закрытые проекты, отсортированные по скорости сбора средств.
Функционал приложения FastAPI остаётся неизменным, и взаимодействие с Google API включает авторизацию, подключение к сервисам, создание таблицы, выдачу прав и обновление данных.
Это позволит волонтерам благотворительного фонда QRKot быстро определять проекты, которые нуждаются в дополнительной рекламе.

## Технологии и  и библиотеки
```
    Python;
    FastAPI;
    SQLAlchemy;
    Alembic;
    Uvicorn;
    FastAPI Users;
    Aiogoogle;
    Google Sheet API v4;
    Google Drive API v3;
```

### 1. Перед использованием
Клонируйте репозиторий к себе на компьютер:
```
git clone git@github.com:Kirill-kuz/QRkot_spreadsheets.git
```
Перейдите в папку.
```
cd QRkot_spreadsheets
```
В корневой папке создайте виртуальное окружение и установите зависимости.
```
python -m venv venv
```
```
source venv/scripts/activate
```
```
pip install -r requirements.txt
```
### 2. Создайте файл .env, в корне проекта выполните команду:
```
mv .env.example .env
```

В файле появятся: 
```
APP_TITLE = Приложения для сбора пожертвований
APP_DESCRIPTION = Приложение для сбора пожертвований на любые цели, связанные с поддержкой  кошачьей популяции
DATABASE_URL = sqlite+aiosqlite:///./cat_fund.db
SECRET = secretkey
FIRST_SUPERUSER_EMAIL = admin@admin.com
FIRST_SUPERUSER_PASSWORD = admin
TYPE=service_account
PROJECT_ID=atomic-climate-<идентификатор>
PRIVATE_KEY_ID=<id приватного ключа>
PRIVATE_KEY="-----BEGIN PRIVATE KEY-----<приватный ключ>-----END PRIVATE KEY-----\n"
CLIENT_EMAIL=<email сервисного аккаунта>
CLIENT_ID=<id сервисного аккаунта>
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=<ссылка>
EMAIL=<email пользователя>
```
### 3. Примените миграции
```
alembic upgrade head
```
### 4. Запуск проекта
```
uvicorn main:app
```
или запуск сервера с автоматическим рестартом
```
uvicorn main:app --reload
```
### 5. API
Сервис является API, так что может быть интегрирован в вашу систему.

Для регистрации выполните POST запрос на http://127.0.0.1:8000/auth/register:
```
curl -X 'POST' \
  'http://127.0.0.1:8000/auth/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "user@example.com",
  "password": "your_password"
  }'
```
Для аутентификации и получения токена выполните POST запрос на http://127.0.0.1:8000/auth/jwt/login
```
curl -X 'POST' \
  'http://127.0.0.1:8000/auth/jwt/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=username&password=password&scope=&client_id=&client_secret='
```
Пример ответа в случае успешного выполнения:
```
{
  "access_token": "token",
  "token_type": "bearer"
}
```
Далее используйте этот токен при запросах к сервису.

#### *[/swagger](http://127.0.0.1:8000/swagger/)*
#### *[/redoc](http://127.0.0.1:8000/redoc)*
### Автор
[Кирилл Кузнецов](https://github.com/Kirill-kuz)