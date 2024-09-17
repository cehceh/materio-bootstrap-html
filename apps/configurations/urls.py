from django.urls import path

# from .departments_origin import(
#      add_departments, edit_departments, departments_table
# )

# from .work_type import (
#     add_work_type,
#     edit_work_type,
#     work_type_table,
# )
# from .equipments import (
#     add_equipments,
#     edit_equipments,
#     equipments_table,
# )
# from .tools import (
#     add_tools,
#     edit_tools,
#     tools_table,
# )
# from .payment_method import (
#     add_payment_method,
#     edit_payment_method,
#     payment_method_table,
# )
# from .daily_task import (
#     add_daily_task,
#     edit_daily_task,
#     daily_task_table,
#     unit_pricing,
#     unit_pricing_add,
#     add_uom_sale,
#     add_uom_purchase,
#     ajax_get,
# )

from .views import DoctorView, DoctorUpdateView, DoctorListView  # noqa: F811


app_name = "configurations"


urlpatterns = [
    # ? ------- Doctor Names Urls -------
    path(
        "table/of/all/doctor/names/",
        (DoctorListView.as_view()),
        name="doctors-table",
    ),
    path(
        "add/doctor/names/",
        (DoctorView.as_view()),
        name="add-doctor-names",
    ),
    path(
        "edit/doctor/name/id/<int:id>/",
        (DoctorUpdateView.as_view()),
        name="edit-doctor-names",
    ),
    # ? ------- Branches Urls -------
    # ? ------- Work Types Urls -------
]
