from django import forms
from groups.models import Group,MyProfile


class GroupCreateForm(forms.ModelForm):
    mentor=forms.ModelMultipleChoiceField(label='Mentors of group:',
        queryset=None,required=False)

    def __init__(self,*args,**kwargs):
        #List of all mentors with checkboxes
        super (GroupCreateForm,self ).__init__(*args,**kwargs)
        self.fields['mentor'].queryset =\
            MyProfile.objects.filter(role__name='Mentor').\
            order_by('user__last_name')
        self.fields['mentor'].widget = forms.CheckboxSelectMultiple()

    class Meta:
        model = Group
        fields = ['name', 'mentor']


class GroupUpdateForm(forms.ModelForm):
#     all_users=forms.ModelMultipleChoiceField(label='Add users:',
#         queryset=None,required=False)
    user=forms.ModelMultipleChoiceField(label='Users in group:',
        queryset=MyProfile.objects.all(),required=False)
#
#     def __init__(self,*args,**kwargs):
#         group = kwargs['instance']
#         super (GroupUpdateForm,self ).__init__(*args,**kwargs)
#         self.fields['user'].queryset = MyProfile.objects.\
#             filter(user_in_group__name=group.name).\
#             filter(user__is_active=True).\
#             order_by(('user__last_name'))
#         self.fields['all_users'].queryset = MyProfile.objects.\
#             filter(role__name='Trainee').\
#             filter(user__is_active=True).\
#             exclude(user_in_group__name=group.name).\
#             order_by(('user__last_name'))
#         self.fields['user'].widget = forms.CheckboxSelectMultiple()
#         self.fields['all_users'].widget = forms.CheckboxSelectMultiple()
#
#     def save(self, commit=True):
#         #Merging accepted users from two fields
#         #print(self.cleaned_data['user'])
#         self.cleaned_data['user']=\
#             self.cleaned_data['user']|self.cleaned_data['all_users']
#         return super(GroupUpdateForm, self).save(commit=commit)

    class Meta:
        model = Group
        fields = ['user']#,'all_users']