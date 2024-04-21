from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from app.config import settings


class Base(DeclarativeBase):
    __abstract__ = True
    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


engin = create_async_engine(url=settings.DATABASE_URL, echo=True)

get_async_session = async_sessionmaker(engin, expire_on_commit=False)
