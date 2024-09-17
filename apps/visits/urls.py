from django.urls import path
from . import views

# VisitView


app_name = "visits"
urlpatterns = [
    # ? for CBV
    path(
        "add/new/visit/for/patient-id/<int:patient_id>/",  # <int:patient_id>/
        views.VisitView.as_view(),
        name="add-visit",
    ),
    path(
        "edit/visit-id/<int:visit_id>/for/patient-id/<int:patient_id>/",
        views.VisitUpdateView.as_view(),
        name="edit-visit",
    ),
    path(
        "list/all/visits/for/patient-id/<int:patient_id>/",  # <int:patient_id>/
        views.VisitListView.as_view(
            template_name="visits/visits_cards/patient_visits_cards.html"
        ),
        name="patient-visits-cards",
    ),
    path(
        "table/visits/for/patient-id/<int:patient_id>/",  #
        views.VisitListView.as_view(),
        name="patient-visits-table",
    ),
    path(
        "table/list/every/visits/",  #
        views.VisitListView.as_view(),
        name="visits-table",
    ),
    # for visit
    path(
        "create/visit/patient/<int:id>/", views.pass_patient_id, name="pass_patient_id"
    ),
    path(
        "edit/visit/<int:id>/patient/<int:patient_id>/",
        views.visits_patient_id,
        name="visits_patient_id",
    ),
    # path('edit/visit/<int:id>/', visits.edit_visits, name='edit_visits'),
    path("table/list/all/visits/", views.table_visits, name="table_visits"),
    path("export/table/", views.export_table, name="export_table"),
]
