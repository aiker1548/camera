# from fastapi import Query
# from pydantic import BaseModel

# from application.user.interfaces.persistence.reader import UserFilters


# class FilterUsersParams(BaseModel):
#     user_fullname__subtext: str | None = Query(None, description="Фильтр по ФИО")

#     def build_users_filters(self) -> UserFilters:
#         return UserFilters(
#             user_fullname__subtext=self.user_fullname__subtext,
#         )
