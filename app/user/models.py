from app.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.task.models import Task


class User(Base):
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(nullable=False, server_default="False")

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="user", lazy="immediate", foreign_keys=Task.assigned_user
    )
