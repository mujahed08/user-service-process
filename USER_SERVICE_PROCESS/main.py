"""
FastAPI
"""

import httpx
import json

from fastapi import FastAPI
from USER_SERVICE_PROCESS.commons.logger import get_logger
from USER_SERVICE_PROCESS.pydantic.models import Example, Status
from USER_SERVICE_PROCESS.pydantic.generated.user_svc_sys.models import UserIn

http:str = 'http://'
host:str = 'localhost'
port:str = 8000
url:str = f'{http}{host}:{port}'
logger = get_logger('main.py')
logger.info(Example.schema_json())

logger.info('   Initiliazing Fast API app')
app = FastAPI(title="FastAPI")
logger.info('   Initialized Fast API app')

@app.post("/signup", response_model=Status)
async def signup(user:UserIn):
    logger.info('   signup function is executing')
    url_users = 'http://localhost:8000/users'

    async with httpx.AsyncClient() as client:
        response = await client.post(url_users, json.dumps(user))
        data = response.json()
        logger.info(response.json())
        user_id = data.get('id')
        logger.info(user_id)
        url_assign_roles = f'http://localhost:8000/users/{user_id}/roles'
        response2 = await client.post(url_assign_roles, json.dumps(['ROLE_ADMIN', 'ROLE_USER']))
        if response2.status_code == 200:
            logger.log(response2.json())
            url_send_message = 'http://localhost:8002/producer'
            response3 = await client.post(url_send_message, json.dumps({
                "id" : 1,
                "text" : data
            }))
            logger.log(response3.json())

    return Status(message='Hellow World!')

@app.get("/example", response_model=Status)
async def get_example():
    logger.info('   get_example function is executing')
    message = 'Hello World!'
    return Status(message=f'Returning with message: {message}')

@app.post("/example/ops", response_model=Example)
async def example_ops(example:Example):
    logger.info('   example_ops function is executing')
    logger.info(example.json())
    return Example(id=1, name='Hellow World!')

logger.info('   End of the main file')
