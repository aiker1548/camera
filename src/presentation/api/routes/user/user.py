# from fastapi import APIRouter, Depends

# from application.auth.dto import JWTUserPayload
# from application.user import dto
# from application.user.queries.get_user_me import GetUserQuery
# from dependency_injector.wiring import Provide, inject

# from application.user.queries.get_users import GetUsersQuery
# from di.auth import AuthContainer
# from presentation.api.responses.base import OkResponse
# from presentation.api.routes.auth.dependencies.auth_dep import get_current_user
# from shared_kernel.building_blocks.application.dto import DTO
# from shared_kernel.building_blocks.application.mediator import Mediator
# from shared_kernel.building_blocks.application.pagination.dto import UserOrderBy
# from shared_kernel.building_blocks.presentaion.pagination_params import FilterPaginationParams
# from . import users_paramns
# router = APIRouter(tags=["User"], dependencies=[Depends(get_current_user)])


# @router.get("/users/me", response_model=OkResponse[dto.UserDTO])
# @inject
# async def get_me(
#         current_user: JWTUserPayload = Depends(get_current_user),
#         mediator: Mediator = Depends(Provide[AuthContainer.mediator]),
# ) -> OkResponse[dto.UserDTO]:
#     query = GetUserQuery(
#         user_id=current_user.user_id
#     )

#     response: DTO = await mediator.send(query, context="auth")

#     return OkResponse[dto.UserDTO](
#         result=response,
#     )


# @router.get("/users", response_model=OkResponse[dto.UsersDTO])
# @inject
# async def get_users(
#         filter_params: users_paramns.FilterUsersParams = Depends(users_paramns.FilterUsersParams),
#         pagination_params: FilterPaginationParams[UserOrderBy, UserOrderBy.CREATED_AT] = Depends(
#             FilterPaginationParams[UserOrderBy, UserOrderBy.CREATED_AT]),
#         mediator: Mediator = Depends(Provide[AuthContainer.mediator]),
# ) -> OkResponse[dto.UsersDTO]:
#     """Return all users uploaded video with optional filtering and pagination."""

#     filters = filter_params.build_users_filters()

#     query = GetUsersQuery(
#         filters=filters,
#         pagination=pagination_params
#     )

#     response: DTO = await mediator.send(query, context="auth")

#     return OkResponse[dto.UsersDTO](
#         result=response,
#     )
