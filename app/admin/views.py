from sqladmin import ModelView
from wtforms.validators import DataRequired

from app.task.models import Task
from app.user.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.ID, User.email, User.tasks]
    name_plural = "Пользователи"
    name = "Пользователь"
    column_details_exclude_list = [User.hashed_password]
    icon = "fa-sharp fa-solid fa-users"
    can_delete = False
    can_edit = False


class TaskAdmin(ModelView, model=Task):

    column_list = [c.name for c in Task.__table__.columns] + [Task.user]
    name_plural = "Задачи"
    name = "Задача"
    icon = "fa-sharp fa-solid fa-list-check"
    form_excluded_columns = [Task.ID]
    form_include_pk = True
