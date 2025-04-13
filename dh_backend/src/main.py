from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Replace with your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(api_router, prefix="/api/v1")
app.mount('/images', StaticFiles(directory='/data/images'), name='images')
@app.get("/")
def root():
    return {"message": "Hello There!"}