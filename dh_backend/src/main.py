from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager


from src.api.api_routes import api_router
from src.database.init_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # Runs at startup
    yield
    # You can add cleanup logic here (if needed)

app = FastAPI(lifespan=lifespan)
app.include_router(api_router, prefix="/api/v1")
app.mount('/images', StaticFiles(directory='/data/images'), name='images')
@app.get("/")
def root():
    return {"message": "Hello There!"}