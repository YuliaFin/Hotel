from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Request, Room
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .models import occupancy_of_rooms

class RequestForm(ModelForm):
    room = forms.ModelChoiceField(label='',queryset=Room.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control',
        'placeholder': 'Выберите комнату'
    }), empty_label=None)

    main_place = forms.IntegerField(label='', min_value=1, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Количество гостей'
    }))

    additional_place = forms.IntegerField(label='', min_value = 0, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Количество дополнительных мест'
    }))

    date_of_arrival = forms.DateField(label='', widget=DatePickerInput(format='%d/%m/%Y', attrs={
        'placeholder': 'Выберите дату заезда',
         'class': 'form-control datepicker'
    }))

    date_of_departure = forms.DateField(label='', widget=DatePickerInput(format='%d/%m/%Y', attrs={
        'placeholder': 'Выберите дату выезда',
        'class': 'form-control datepicker'
    }))

    def clean_main_place(self):
        main_place = self.cleaned_data['main_place']
        if main_place < 1:
            raise ValidationError("Количество гостей должно быть не менее 1")
        return main_place

    def clean_additional_place(self):
        additional_place = self.cleaned_data['additional_place']
        if additional_place < 0:
            raise ValidationError("Количество дополнительных мест не может быть отрицательным")
        return additional_place

    class Meta:
        model = Request
        fields = ['room', 'main_place', 'additional_place', 'date_of_arrival', 'date_of_departure']


class RoomAvailabilityForm(forms.Form):
    room_number = forms.IntegerField(label='Номер комнаты')
    date_of_arrival = forms.DateField(label='Дата заезда')
    date_of_departure = forms.DateField(label='Дата выезда')




