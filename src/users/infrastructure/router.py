from django.urls import path
from src.users.infrastructure.controllers.find_user_by_user_pass_controller import (
    FindUserByUserPasswordController,
)
from src.users.infrastructure.controllers.find_user_by_id import FindUserByIdController
from src.users.infrastructure.controllers.create_user_controller import (
    CreateUserController,
)
from src.users.infrastructure.controllers.google_login_callback_controller import (
    GoogleLoginCallbackController,
)
from src.users.infrastructure.controllers.google_login_redirect_controller import (
    GoogleLoginRedirectController,
)
from src.users.infrastructure.controllers.get_all_users_controller import FindAllUsersController
from src.users.infrastructure.controllers.delete_user_by_id import DeleteUserController

urlpatterns = [
    path("login", FindUserByUserPasswordController.as_view(), name="login-view"),
    path("register", CreateUserController.as_view(), name="register-view"),
    path("public", FindUserByIdController.as_view(), name="find-user-by-id"),
    path("google", GoogleLoginRedirectController.as_view()),
    path("google/callback", GoogleLoginCallbackController.as_view()),
    path("all", FindAllUsersController.as_view()),
    path("delete", DeleteUserController.as_view(), name="delete-user")
]
