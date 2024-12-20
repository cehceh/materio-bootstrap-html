# import django_tables2 as tables

# from apps.presenthistory.models import PresentHistory
# from apps.pasthistory.models import PastHistory

# from django.core.exceptions import ValidationError


def render_footer(bound_column, table):
    return sum(bound_column.accessor.resolve(row) for row in table.data)
    # s = sum(bound_column.accessor.resolve(row) for row in table.data)
    # return s


# class VisitsTable(tables.Table):
#     # def render_id(self, **kwargs):
#     #     return kwargs['value'].id

#     # def render_forid(self, value, record):
#     #     return mark_safe('''<a href=%s>%s</a>''' % (record['id'], value))
#     # return "%s" % value

#     id = tables.TemplateColumn(
#         "<a href=\"{% url 'visits:visits_patient_id' record.id record.patient_id %}\">{{ record.id }}</a>",
#         verbose_name="Visits ID",
#         template_name="django_tables2/bootstrap4.html",
#     )
#     patient = tables.TemplateColumn(
#         "<a href=\"{% url 'visits:visits_patient_id' record.id record.patient_id %}\">{{ record.patient }}</a>",
#         verbose_name="Patient Name",
#         template_name="django_tables2/bootstrap4.html",
#     )

#     visitdate = tables.TemplateColumn(
#         "<a href=\"{% url 'visits:visits_patient_id' record.id record.patient_id %}\">{{ record.visitdate }}</a>",
#         verbose_name="Visit Date",
#     )

#     diagnosis = tables.TemplateColumn(
#         "<a href=\"{% url 'visits:visits_patient_id' record.id record.patient_id %}\">{{ record.diagnosis }}</a>",
#         verbose_name="Daignosis",  # footer=len(tables.rows)
#     )
#     amount = tables.TemplateColumn(
#         "<a href=\"{% url 'visits:visits_patient_id' record.id record.patient_id %}\">{{ record.amount }}</a>",
#         verbose_name="Amount",
#         footer=render_footer,
#     )

#     addlab = tables.TemplateColumn(
#         '<a class="btn btn-outline-dark" href="{% url \'labs:add_lab_visit\' record.patient_id record.id %}">Add Analysis</a>',
#         verbose_name="Add Analysis",
#     )

#     addpresent = tables.TemplateColumn(
#         '<a class="btn btn-outline-primary" href="{% url \'presenthistory:save_present_hist\' record.patient_id record.id %}">Add Present History</a>',
#         verbose_name="Add Present History",
#     )

#     addrevis = tables.TemplateColumn(
#         '<a class="btn btn-outline-dark" href="{% url \'revisits:save_revisit\' record.patient_id record.id %}">Add Revisit</a>',
#         verbose_name="Add Revisit",
#     )

#     class Meta:
#         model = Visits
#         attrs = {
#             "id": "visits-table",
#         }
#         template_name = "django_tables2/bootstrap4.html"
#         fields = (
#             "id",
#             "patient",
#             "visitdate",
#             "diagnosis",
#             "amount",
#             "addrevis",
#             "addlab",
#         )
#
# exclude columns while creating the TableExport instance:
# exporter = TableExport("csv", table, exclude_columns=("image", "buttons"))
