import logging
import sys
from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = ('Приложение для Благотворительного '
                      'фонда поддержки котиков QRKot.')
    app_description: str = ('Приложение фонда для сбора пожертвований'
                            ' кошкам — на любые цели, связанные с поддержкой '
                            'кошачьей популяции')
    database_url: str = 'sqlite+aiosqlite:///./cat_fund.db'
    secret: str = 'secretkey'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = '.env'


logging.basicConfig(
    handlers=[logging.StreamHandler(sys.stdout)],
    format=(
        '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s'),
    level=logging.INFO
)

settings = Settings()
logger = logging.getLogger(__name__)
