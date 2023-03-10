from django import forms
from django.forms import ModelForm, ValidationError
from .models import Home, Human, Breed, Cat
from django.forms.widgets import DateInput

class HomeForm(ModelForm):
    class Meta:
        model = Home
        fields = '__all__'
    def clean(self):

        name = self.cleaned_data.get('home_name')

        matching_name = Home.objects.filter(home_name=name)
        if self.instance:
            matching_name = matching_name.exclude(pk=self.instance.pk)
        if matching_name.exists():
            msg = u"Home name: %s already exists." % name
            raise ValidationError(msg)
        else:
            return self.cleaned_data
    
class HumanForm(ModelForm):
    class Meta:
        model = Human
        fields = '__all__'
        widgets = {
            'human_date_of_birth': DateInput(attrs={'type':'date'})
        }

class BreedForm(ModelForm):
    class Meta:
        model = Breed
        fields = '__all__'

class CatForm(ModelForm):
    class Meta:
        model = Cat
        fields = '__all__'
        widgets = {
            'cat_date_of_birth': DateInput(attrs={'type':'date'})
        }

class AllForms(ModelForm):
    class Meta:
        def __init__(self, modelw):
            self.model = modelw
        fields = '__all__'
