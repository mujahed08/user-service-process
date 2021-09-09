import os
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    run_env:str = Field(..., env='RUN_ENV')
    user_svc_sys_host:str = Field(..., env='USER_SVC_SYS_HOST')
    producer_host:str = Field(..., env='PRODUCER_HOST')

    class Config:
        env_file = None
        env_file_encoding = 'utf-8'


def get_settings():
    run_env:str = os.environ['RUN_ENV']
    return Settings(_env_file=f'{run_env}.env', _env_file_encoding='utf-8')
