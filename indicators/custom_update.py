from django.views.generic.edit import ProcessFormView, ModelFormMixin,\
    BaseUpdateView
from django.views.generic import UpdateView
from django.shortcuts import get_object_or_404


class CustomProcessFormView(ProcessFormView):

    def post(self, request, *args, **kwargs):

        """Update record in model. Delete and create new record with new
        updated fields. If form isn't valid restore with previous fields
        record into db."""

        model_obj = get_object_or_404(self.model, pk=kwargs.get('pk'))
        tmp_pk = model_obj.pk
        model_obj.delete()
        is_deleted_obj = True
        model_obj.pk = tmp_pk

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            if is_deleted_obj:
                model_obj.save()
            return self.form_invalid(form)


class CustomBaseUpdateView(BaseUpdateView,
                           ModelFormMixin,
                           CustomProcessFormView):
    pass


class CustomUpdateView(UpdateView, CustomBaseUpdateView):
    pass
