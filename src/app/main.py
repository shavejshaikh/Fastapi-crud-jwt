import uvicorn
from fastapi import FastAPI
from app.controllers import include_routers
from app.data import models
from app.data.database import engine

app = FastAPI(title="Fastapi-CRUD")

''' Automatically create table in database if any model is created '''
models.Base.metadata.create_all(bind=engine) 

@app.get("/")
def home():
    return ":("

include_routers(app)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port = 8000)