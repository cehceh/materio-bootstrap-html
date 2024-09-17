from django.utils.safestring import mark_safe
from django import template
from web_project.template_helpers.theme import TemplateHelper

register = template.Library()


# Register tags as an adapter for the Theme class usage in the HTML template


# @register.simple_tag
# def get_theme_variables(scope):
#     return mark_safe(TemplateHelper.get_theme_variables(scope))


# * FROM CHATGPT
@register.simple_tag
def get_theme_variables(scope, *args, **kwargs):
    return mark_safe(TemplateHelper.get_theme_variables(scope, *args, **kwargs))


# @register.simple_tag
# def get_theme_variables(key, *args, **kwargs):
#     theme_variables = settings.THEME_VARIABLES
#     url = theme_variables.get(key, '')

#     if args or kwargs:
#         try:
#             url = url.format(*args, **kwargs)
#         except KeyError as e:
#             # Handle missing keys if necessary
#             print(f"KeyError: Missing key {e}")

#     return url
