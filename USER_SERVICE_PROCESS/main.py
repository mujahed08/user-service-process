"""
FastAPI
"""

import json
import httpx

from fastapi import FastAPI
from USER_SERVICE_PROCESS.commons.logger import get_logger
from USER_SERVICE_PROCESS.pydantic_models.enviornment import get_settings
from USER_SERVICE_PROCESS.pydantic_models.models import Response
from USER_SERVICE_PROCESS.pydantic_models.generated.user_svc_sys.models import UserIn, UserUp

logger = get_logger('main.py')

settings = get_settings()

url_send_message = f'{settings.producer_host}/producer'
url_users = f'{settings.user_svc_sys_host}/users'

def get_url_user(user_id:int):
    return f'{settings.user_svc_sys_host}/users/{user_id}'

def get_url_assign_roles(user_id:str):
    return f'{settings.user_svc_sys_host}/users/{user_id}/roles'

logger.info('   Initiliazing Fast API app')
app = FastAPI(title="FastAPI")
logger.info('   Initialized Fast API app')

@app.post("/signup", response_model=Response)
async def signup(user:UserIn):
    logger.info('   signup function is executing')
    logger.info(user.json())
    async with httpx.AsyncClient() as client:
        response = await client.post(url_users, data=user.json())
        data1 = response.json()
        logger.info(data1)
        user_id = data1.get('id')
        logger.info(user_id)
        url_assign_roles = get_url_assign_roles(user_id)
        response2 = await client.post(url_assign_roles,
            data=json.dumps(['ROLE_ADMIN', 'ROLE_USER']))
        if response2.status_code == 200:
            logger.info(response2.json())
            response3 = await client.post(url_send_message, data=json.dumps({
                "id" : 1,
                "text" : data1
            }))
            logger.info(response3.json())

    return Response(code=200, message='SUCCESS', data=response2.dict())

@app.get("/deactivate/{user_id}", response_model=Response)
async def deactivate(user_id:int):
    logger.info('   deactivate function is executing')
    return await toggle_enabled(user_id, False)

@app.get("/activate/{user_id}", response_model=Response)
async def activate(user_id:int):
    logger.info('   activate function is executing')
    return await toggle_enabled(user_id, True)

async def toggle_enabled(user_id:int, enabled: bool):
    async with httpx.AsyncClient() as client:
        url_user = get_url_user(user_id)
        response = await client.get(url_user)
        data1 = response.json()
        logger.info(data1)
        updates:UserUp = UserUp(name=data1['name'], enabled=enabled)
        logger.info(updates)
        if response.status_code == 200:
            response2 = await client.put(url_user, data=updates.json())
            if response2.status_code == 200:
                data2 = response2.json()
                logger.info(data2)
                return Response(code=200, message='SUCCESS', data=data2)

logger.info('   End of the main file')
