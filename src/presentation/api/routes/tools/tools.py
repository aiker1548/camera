# from fastapi import APIRouter, Depends
# from dependency_injector.wiring import Provide, inject

# from application.auth.commands.reset_password import ResetPasswordCommand
# from application.auth.commands.update_user import UpdateUserCommand
# from application.camera.commands.save_camera_command import SaveCameraCommand
# from di.auth import AuthContainer

# from application.auth.dto.auth_dto import (PasswordResetDTO, UserUpdateDTO)
# from di.cameras import CamerasContainer

# from presentation.api.responses.base import OkResponse

# from presentation.api.routes.tools.dependencies.tools_dep import \
#     verify_registration_key

# from shared_kernel.building_blocks.application.mediator import Mediator

# router = APIRouter(prefix="/tools", tags=["Tools"])


# @router.post("/password-reset", response_model=OkResponse[str])
# @inject
# async def reset_password(
#         reset_data: PasswordResetDTO,
#         _: None = Depends(verify_registration_key),
#         mediator: Mediator = Depends(Provide[AuthContainer.mediator]),
# ):
#     command = ResetPasswordCommand(
#         email=reset_data.email,
#         new_password=reset_data.new_password,
#     )
#     await mediator.send(command)

#     return OkResponse(result="Пароль успешно обновлён.")


# @router.put("/users", response_model=OkResponse[str])
# @inject
# async def update_user(
#         id_or_email__eq: str,
#         user_data: UserUpdateDTO,
#         _: None = Depends(verify_registration_key),
#         mediator: Mediator = Depends(Provide[AuthContainer.mediator]),
# ):
#     command = UpdateUserCommand(
#         id_or_email=id_or_email__eq,
#         update_data=user_data,
#     )
#     await mediator.send(command, context="auth")
#     return OkResponse(result="Пользователь успешно обновлён.")

# @router.post("/camera-save", response_model=OkResponse[str])
# @inject
# async def save_camera_data_task(
#         mediator: Mediator = Depends(Provide[CamerasContainer.mediator]),
# ):
#     command = SaveCameraCommand()
#     await mediator.send(command, context="camera")
#     return OkResponse(result="Камеры успешно загружены/обновлены.")
