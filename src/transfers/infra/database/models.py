import uuid
from sqlalchemy import String, Numeric, Text
from sqlalchemy.orm import mapped_column, declarative_base, Mapped

Base = declarative_base()


__all__ = ["Base", "Transfer"]


class Transfer(Base):
    __tablename__ = 'transfers'

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    external_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    amount: Mapped[str] = mapped_column(Numeric(30, 18), nullable=False)
    destination: Mapped[str] = mapped_column(String(255), nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
