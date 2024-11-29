from django.urls import path

# from .views import (add_category, edit_category,
#                     delete_category, category_table,)
from django.contrib.auth.decorators import login_required
from .views import dashboard, frontpage, error_page  # test_views,
from .gold_page import main_page


# from .my_inertia_vite import (
#     # index_from_inertia,
#     app_page
# )
app_name = "home"

urlpatterns = [
    path("dashboard/", login_required(dashboard), name="dashboard"),
    path("", frontpage, name="frontpage"),
    # path("test-views/", test_views, name="test_views"),
    # path("inertia/", index_from_inertia, name="index_from_inertia"),
    # path("app/", app_page, name="app_page"),
    path("error/page/type/<str:type>/", error_page, name="error_page"),
    #
    # path("select-app/", (select_app), name="select_app"),
    path("main-page/", login_required(main_page), name="main_page"),
    # path('table/of/all/category/', login_required(category_table), name='category_table'),
    # path('delete/category/id/<int:category_id>/', login_required(delete_category), name='delete_category'),
]
