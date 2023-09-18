from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from ..cfg import dbPassword


engine = create_async_engine(f"mysql+aiomysql://root:{dbPassword}@127.0.0.1/vk_to_tg")
Sessions = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
