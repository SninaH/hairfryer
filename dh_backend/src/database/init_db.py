from sqlalchemy.sql import text
from .database import engine
from .models import Base


async def init_db():
    async with engine.begin() as conn:
        # Enable UUID extension
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))

        # Create tables
        await conn.run_sync(Base.metadata.create_all)
