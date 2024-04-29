from django import forms

from car.models import CarImg


class CarImageForm(forms.ModelForm):

    class Meta:
        model = CarImg
        fields = ['images']
        widgets = {
            'images' : forms.ClearableFileInput(attrs={'miltiple': True})
        }
