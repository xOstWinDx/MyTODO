import datetime
from sqlalchemy import DateTime
from datetime import date

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Task(Base):
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    created_by: Mapped[int] = mapped_column(ForeignKey("user.ID", ondelete="CASCADE"))
    Deadline: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))

    assigned_user: Mapped[int] = mapped_column(
        ForeignKey("user.ID", ondelete="CASCADE"), nullable=True
    )

    user: Mapped["User"] = relationship(
        back_populates="tasks", foreign_keys=assigned_user
    )