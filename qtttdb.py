from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from sqlalchemy import MetaData


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    metadata = MetaData()


class Users(Base):
    __tablename__ = "users"
    name: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    
    def __repr__(self) -> str:
        return f"{self.name=}, {self.password=}"
    
    