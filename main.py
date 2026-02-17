import uvicorn
from src.ui.api.fastapi.app import app
from src.ui.api.fastapi.settings import fastapi_settings



if __name__ == "__main__":
     uvicorn.run("main:app",
                 host=fastapi_settings.APP_HOST,
                 port=fastapi_settings.APP_PORT,
                 reload=fastapi_settings.APP_RELOAD
                 )
