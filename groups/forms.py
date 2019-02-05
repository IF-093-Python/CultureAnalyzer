from django import forms
from django.contrib.auth.models import User
from users.models import Profile
from groups.models import Group


class MyProfile(Profile):
    '''
    Proxy Model for changing __str__ attribute of
    Profile model for proper representation
    of the name of user
    '''
    class Meta:
        proxy = True

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name} \
                ({self.user.username})'


class GroupCreateForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (GroupCreateForm,self ).__init__(*args,**kwargs)
        self.fields['mentor'].queryset =\
            MyProfile.objects.filter(role__name='Mentor').\
            order_by('user__last_name')
        self.fields['mentor'].widget = forms.CheckboxSelectMultiple()

    class Meta:
        model = Group
        fields = ['name', 'mentor']

