from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from ..cfg import DB_PASS, DB_IP, DB_NAME


engine = create_async_engine(f"mysql+aiomysql://root:{DB_PASS}@{DB_IP}/{DB_NAME}")
Sessions = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
