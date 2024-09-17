from os import name
from django.core.checks import messages
from django.urls import path

# from django.contrib.auth import views as auth_views
from .views import (
    edit_message,
    # edit_user_profile,
    is_read_changes,
    list_messages,
    list_user_messages,
    mark_all_is_read,
    sent_message,
)
from django.contrib.auth.decorators import login_required

# UserProfilePageView,

app_name = "users"

urlpatterns = [
    ###############??????????? not needed here oin accounts app
    # path(
    #     "profile/for/user/id/<user_id>/",
    #     login_required(edit_user_profile),
    #     name="edit_user_profile",
    # ),  # profile page views
    path("messages/", login_required(sent_message), name="sent_message"),
    path("messages/<int:id>/", login_required(edit_message), name="edit_message"),
    path("list/messages/", login_required(list_messages), name="list_messages"),
    path(
        "list/user/<str:sender>/messages/",
        login_required(list_user_messages),
        name="list_user_messages",
    ),
    # for changes of is_read field
    path(
        "update/is-read/id/<int:id>/",
        login_required(is_read_changes),
        name="is_read_changes",
    ),
    path(
        "mark/all/messages/as/read/",
        login_required(mark_all_is_read),
        name="mark_all_is_read",
    ),
]
