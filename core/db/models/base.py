from datetime import datetime

from sqlalchemy import BigInteger, DateTime, SmallInteger, String, text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()


class User(Base):
    """User model."""

    __tablename__ = "users"
    __table_args__ = {"schema": "raw"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="Unique user id")
    tg_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, index=True, nullable=False, comment="Unique Telegram user id"
    )
    tg_username: Mapped[str | None] = mapped_column(String(256), nullable=True, comment="Telegram username")
    subscription: Mapped[int] = mapped_column(SmallInteger, default=0, comment="Subscription key")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"), comment="User created at (UTC)"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=text("CURRENT_TIMESTAMP"),
        server_default=text("CURRENT_TIMESTAMP"),
        comment="User updated at (UTC)",
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, subscription={self.subscription})"
