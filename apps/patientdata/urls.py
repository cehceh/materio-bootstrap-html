from django.urls import path  # defs

# from clinic.views.home import homepage

# from .views import PatientListView, PatientUpdateView
from . import views

app_name = "patientdata"
urlpatterns = [
    # ? CBV
    path(
        "add/new/patient/",
        views.PatientView.as_view(),  # (template_name="save_patient.html"),
        name="save-patient",
    ),
    path(
        "reservation/area/",
        views.PatientView.as_view(
            template_name="reservations/reservations.html"
        ),  # (template_name="save_patient.html"),
        name="reservations",
    ),
    path(
        "list/all/patients/",
        views.PatientListView.as_view(),  # (template_name="save_patient.html"),
        name="patients-cards",
    ),
    path(
        "choose/history/for/patient-id/<int:patient_id>/",
        views.PatientListView.as_view(
            template_name="patients_cards/patient_history.html"
        ),  # (),
        name="patient-history",
    ),
    path(
        "edit/patient-id/<int:patient_id>/",
        views.PatientUpdateView.as_view(),  # (template_name="save_patient.html"),
        name="edit-patient",
    ),
    path(
        "list/all/patients/from/patient-view-class/",
        views.PatientView.as_view(
            template_name="patients_table.html"
        ),  # (template_name="save_patient.html"),
        name="all-patients",
    ),
    # * for patient
    # path("create/patient/", save_patient, name="save_patient"),
    # path("edit/patient/<int:id>/", edit_patient, name="edit_patient"),
    # path("table/patients/", table_patient, name="table_patient"),
    # path(
    #     "patient/details/by/barcode/<str:barcode>/",
    #     patient_details,
    #     name="patient_details",
    # ),
    # for visit
    # path('create/visit/', visits.save_visits, name='save_visits'),
    # path('edit/visit/<int:id>/patient/<int:patient_id>/', visits.visits_patient_id, name='visits_patient_id'),
    # path('edit/visit/<int:id>/', visits.edit_visits, name='edit_visits'),
    # path('table/visits/', visits.table_visits, name='table_visits'),
    # path('export/table/', visits.export_table, name='export_table'),
    #
    # path('drug/patient/<int:patient_id>/visit/<int:visit_id>/',
    #     medicine.save_medicine, name='save_medicine'),
    #
    # path('add/prescription/patient/<int:patient_id>/visit/<int:visit_id>/',
    #     medicine.add_new, name='add_new'),
    #
    # path('patient/<int:patient_id>/visit/<int:visit_id>/drug/<int:id>/',
    #     medicine.edit_medicine, name='edit_medicine'),
    #
    # path('patient/<int:patient>/visit/<int:visit>/delete/drug/<int:id>/', medicine.delete_medicine, name='delete_medicine'),
    # path('table/medicine/', medicine.table_medicine, name='table_medicine'),
    #
    # path('search/patient/', search_patient, name='search_patient'),
    # path('search/visit/', search_visit, name='search_visit'),
    # path('search/date/', search_date, name='search_date'),
    # path('search/only/date/', search_only, name='search_only'),
    #
    # path('income/day/<int:day>/<int:month>/<int:year>/', calculate_income, name='day_income'),
    # path('income/month/<int:day>/<int:month>/<int:year>/', calculate_income, name='month_income'),
    # path('income/year/<int:year>/', calculate_income, name='year_income'),
    # # path('income/day/', calculate_income, name='calculate_day_income'),
    # # path('income/month/', calculate_income, name='calculate_month_income'),
    # path('income/day/', calculate_day_income, name='calculate_day_income'),
    # path('income/month/', calculate_month_income, name='calculate_month_income'),
    # path('income/year/', calculate_year_income, name='calculate_year_income'),
    # #
    # path('prescription/visit/<int:visit_id>/', prescription.get_pdf, name='get_pdf'),
    # # This is a good one for printing prescription
    # path('print/visit/<int:visit_id>/', prescription.print_html, name='print_html'),
    # #
    # path('pdf/', prescription.some_view, name='some_view'),
]
