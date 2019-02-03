
def populate_ids_for_indicator(apps, schema_editor):
    """
    Populate primary keys values for migration in CountryIndicator model
    """
    Model = apps.get_model('indicators', 'CountryIndicator')
    for field_id, field in enumerate(Model.objects.all()):
        field.id = field_id + 1
        field.save()


def opposite_letter_case(data_string):
    """
    Change string on opposite case string, if string contains different cases
    return lowercase string

    pre-requirements: must contains only letters
    :param data_string: string
    :return: data_string
    """
    if data_string.islower():
        data_string = data_string.upper()
    else:
        data_string = data_string.lower()
    return data_string
