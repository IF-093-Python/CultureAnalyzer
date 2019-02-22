from django import forms
from groups.models import Group, CustomUser


class GroupCreateForm(forms.ModelForm):
    mentor = forms.ModelMultipleChoiceField(
        label='Mentors of group:', queryset=CustomUser.objects.all(),
        required=False)

    class Meta:
        model = Group
        fields = ['name', 'mentor']


class GroupUpdateForm(forms.ModelForm):
    user = forms.ModelMultipleChoiceField(
        label='Users in group:',queryset=CustomUser.objects.all(),required=False)

    class Meta:
        model = Group
        fields = ['user']
