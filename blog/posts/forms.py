from django import forms

from . import models


class CreatePost(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title','body','banner']

class MembersForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['username'].required = True     

    class Meta:
        model = models.Members
        fields = ['username','email','avatar','age']
        

class AddressForm(forms.ModelForm):
    class Meta:
        models = models.Post
        field = ['member_id','street','city','country']