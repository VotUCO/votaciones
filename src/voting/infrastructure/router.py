from django.urls import path
from src.voting.infrastructure.controllers.find_private_voting_controller import (
    FindPrivateVotingController,
)
from src.voting.infrastructure.controllers.find_public_voting_controller import (
    FindPublicVotingController,
)
from src.voting.infrastructure.controllers.create_voting_controller import (
    CreateVotingController,
)
from src.voting.infrastructure.controllers.update_voting_controller import (
    UpdateVotingController,
)
from src.voting.infrastructure.controllers.delete_voting_controller import (
    DeleteVotingController,
)
from src.voting.infrastructure.controllers.get_options_voting_controller import (
    GetOptionsVotingController,
)
from src.voting.infrastructure.controllers.active_votings_by_user import FindActiveVotingByUserController
from src.voting.infrastructure.controllers.archived_votings_by_user import FindArchivedVotingByUserController
from src.voting.infrastructure.controllers.draft_votings_by_user import FindDraftVotingByUserController
from src.voting.infrastructure.controllers.publish_voting_controller import PublishVotingController
from src.voting.infrastructure.controllers.get_voting_by_id import GetVotingByIdController

urlpatterns = [
    path("create", CreateVotingController.as_view(), name="voting-creation-controler"),
    path("private", FindPrivateVotingController.as_view(), name="get-private-votings"),
    path("public", FindPublicVotingController.as_view(), name="get-public-votings"),
    path("update", UpdateVotingController.as_view(), name="voting-update-view"),
    path("delete", DeleteVotingController.as_view(), name="voting-delete-view"),
    path(
        "options",
        GetOptionsVotingController.as_view(),
        name="options-by-id",
    ),
    path(
        "active",
        FindActiveVotingByUserController.as_view(),
        name="get-options-voting-controller",
    ),
    path(
        "archived",
        FindArchivedVotingByUserController.as_view(),
        name="get-options-voting-controller",
    ),
    path(
        "draft",
        FindDraftVotingByUserController.as_view(),
        name="get-options-voting-controller",
    ),
    path(
        "publish",
        PublishVotingController.as_view(),
        name="publish-voting-controller"

    ),
    path(
        "id",
        GetVotingByIdController.as_view(),
        name="get-voting-by-id-controller"
    )
]
