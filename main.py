from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from dependencies.database import connect_to_mongodb
from routers import home

app = FastAPI(lifespan=connect_to_mongodb)

app.include_router(home.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", reload=True)