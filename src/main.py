from fastapi import FastAPI
from modules.auth import router
from modules.users import router as users_router
from modules.products import router as products_router
from contextlib import asynccontextmanager
from pymongo import AsyncMongoClient
import uvicorn


async def startup_db_client(app: FastAPI):
    app.state.mongo_client = AsyncMongoClient("localhost", 27017)
    app.state.mongo_db = app.state.mongo_client.get_database(
        'evaluasi-sharing-session')

    print('MongoDB Connected')


async def shutdown_db_client(app: FastAPI):
    app.mongodb_client.close()
    print('MongoDB Disconnected')


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_db_client(app)
    yield
    await shutdown_db_client(app)

app = FastAPI(
    # lifespan=lifespan
)

app.include_router(router.router)  
app.include_router(users_router.router)
app.include_router(products_router.router)


@app.get('/')
async def root():
    return {"message": "Hello, world!"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=3000)
