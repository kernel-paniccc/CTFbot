from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import BigInteger

from dotenv import load_dotenv
import os

load_dotenv()

engine = create_async_engine(os.getenv('URL'))

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    flag_count: Mapped[int] = mapped_column()


class Flag(Base):
    __tablename__ = 'submit'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, nullable=False)
    flag: Mapped[str] = mapped_column()


async def async_main():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)