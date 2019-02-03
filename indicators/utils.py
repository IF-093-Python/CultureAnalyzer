
def populate_ids_for_indicator(apps, schema_editor):
    """
    Populate primary keys values for migration in CountryIndicator model
    """
    Model = apps.get_model('indicators', 'CountryIndicator')
    for field_id, field in enumerate(Model.objects.all()):
        field.id = field_id + 1
        field.save()
