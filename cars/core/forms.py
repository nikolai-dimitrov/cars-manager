from django import forms

from cars.core.mixins import FormControlsMixin


class CarSearchForm(forms.Form, FormControlsMixin):
    classes = {
        'make': 'car-search-form-field',
        'model': 'car-search-form-field',
        'year': 'car-search-form-field',
        'transmission': 'car-search-form-field',
        'fuel_type': 'car-search-form-field',
        'cylinders': 'car-search-form-field',
    }
    placeholders = {
        'make': 'Brand',
        'model': 'Model',
        'year': 'Year',
    }
    TRANSMISSION_CHOICES = (
        ('all', 'All'),
        ('m', 'Manual'),
        ('a', 'Automatic'),
    )
    FUEL_TYPE = (
        ('all', 'All'),
        ('diesel', 'Diesel'),
        ('electricity', 'Electricity'),
        ('gas', 'Gas'),
    )
    CYLINDERS_CHOICES = (
        ('all', 'All'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('8', '8'),
        ('10', '10'),
        ('12', '12'),
        ('16', '16'),
    )

    make = forms.CharField(required=True)
    model = forms.CharField(required=False)
    year = forms.DateField(required=False)
    transmission = forms.ChoiceField(
        choices=TRANSMISSION_CHOICES
    )
    fuel_type = forms.ChoiceField(
        choices=FUEL_TYPE
    )
    cylinders = forms.ChoiceField(
        choices=CYLINDERS_CHOICES
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_classes()
        self.add_place_holders()
