from django.template.defaultfilters import register


@register.filter
def get_value(dict_, key):
    return dict_[key]


@register.filter
def calculate_table_number(page_number, for_loop_counter):
    return (page_number - 1) * 10 + for_loop_counter