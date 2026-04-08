from datetime import datetime
from app.db.session import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, String, func


class Link(Base):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(primary_key=True)
    original_url: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    short_id: Mapped[str] = mapped_column(
        String(10), index=True, unique=True, nullable=False
    )
    visit_counts: Mapped[int] = mapped_column(
        default=0,
        server_default="0",
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now, server_default=func.now()
    )
