# Template Settings
# ------------------------------------------------------------------------------

# ? try to get patient Id
# from app.patientdata.models import Patient
# from apps.patientdata.models import Patients
# patients_id = Patients.objects.values_list("id")

# Theme Variables
# ? Personalize template by changing theme variables (For ex: Name, URL Version etc...)
THEME_VARIABLES = {
    "creator_name": "Amr Amer",  # "ThemeSelection",
    "creator_url": "#",  # "https://themeselection.com/",
    "template_name": "KMA-Clinic",  # "Materio",
    "template_suffix": "Django Admin Template",
    "template_version": "1.0.0",
    "template_free": True,
    "template_description": "Materio is a modern, clean and fully responsive admin template built with Bootstrap 5, Django 5, HTML, CSS, and JavaScript. It has a huge collection of reusable UI components. It can be used for all types of web applications like System Error pages, Authentication pages, admin dashboard.",
    "template_keyword": "django, django admin, dashboard, bootstrap 5 dashboard, bootstrap 5 design, bootstrap 5",
    "facebook_url": "https://www.facebook.com/ThemeSelections/",
    "twitter_url": "https://twitter.com/Theme_Selection",
    "github_url": "https://github.com/themeselection",
    "dribbble_url": "https://dribbble.com/themeselection",
    "instagram_url": "https://www.instagram.com/themeselection/",
    "license_url": "https://themeselection.com/license/",
    "live_preview": "https://demos.themeselection.com/materio-html-django-admin-template/demo-1/",
    "product_page": "https://themeselection.com/item/materio-bootstrap-django-admin-template/",
    "support": "https://themeselection.com/support/",
    "more_themes": "https://themeselection.com/",
    "documentation": "https://demos.themeselection.com/materio-bootstrap-html-admin-template/documentation/django-introduction.html",
    "changelog": "https://demos.themeselection.com/materio-bootstrap-html-django-admin-template/changelog.html",
    "git_repository": "https://github.com/themeselection/materio-bootstrap-html-django-admin-template-free",
    "git_repo_access": "https://tools.themeselection.com/github/github-access",
    "live_preview_free": "https://demos.themeselection.com/materio-html-django-admin-template-free/",
    "product_page_free": "https://themeselection.com/item/materio-free-bootstrap-html-django-admin-template/",
    # ? /* ------------ My New URLs Variables --------- */
    # ? Patients URLs -----------------------------
    "add_patient_url": "/patients/add/new/patient/",
    "all_patients_url": "/patients/list/all/patients/from/patient-view-class/",
    "patients_dashboard_url": "/patients/list/all/patients/",
    "history_patient_url": "/patients/choose/history/for/patient-id/{patient_id}/",
    # ? Reservaation URLs ----------------------------
    "reservations_url": "/patients/reservation/area/",
    # ? Visits URLs --------------------------------------
    "visits_table_url": "/visits/table/list/every/visits/",
    # ? Doctor Names URLs
    "add_doctor_name_url": "/config/add/doctor/name/",
    "edit_doctor_name_url": "/config/edit/doctor/name/id/{id}/",
    "all_doctor_name_url": "/config/table/of/all/doctor/names/",
}

# ! Don't change THEME_LAYOUT_DIR unless it's required
THEME_LAYOUT_DIR = "layout"
