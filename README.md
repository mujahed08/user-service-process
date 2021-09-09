
.pylintrc has been created with following command
pylint --generate-rcfile > .pylintrc

pytest.ini is a configuration file for pytest having higest configuration precedence. -s argument says python print() function 
prints to the console.


To generate pydantic model for API

user-process-service>datamodel-codegen --url http://localhost:8000/openapi.json --output USER_SERVICE_PROCESS\pydantic_models\generated\user_svc_sys\models.py

user-process-service>datamodel-codegen --url http://localhost:8002/openapi.json --output USER_SERVICE_PROCESS\pydantic_models\generated\producer\models.py

To Start applicationuse the following command
user-service-process>uvicorn USER_SERVICE_PROCESS.main:app --port 8002 --log-config log4py.yaml --reload --reload-dir USER_SERVICE_PROCESS