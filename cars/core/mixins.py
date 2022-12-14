import random
import requests
from cloudinary import uploader
from django.core.files.uploadedfile import InMemoryUploadedFile
from cars.profiles.models import DeleteCode


class FormControlsMixin:
    placeholders = {}
    classes = {}
    required_fields = []

    def add_form_control_class(self):
        for name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''
            field.widget.attrs['class'] += 'form-control'

    def add_place_holders(self):
        for field, placeholder in self.placeholders.items():
            self.fields[field].widget.attrs['placeholder'] = placeholder

    def add_classes(self):
        for field, class_name in self.classes.items():
            if self.fields[field].widget.attrs.get('class') is None:
                self.fields[field].widget.attrs['class'] = ''
            self.fields[field].widget.attrs['class'] += f' {class_name}'

    def disable_fields(self):
        for name, field in self.fields.items():
            field.disabled = True

    def field_required(self):
        for field_name in self.required_fields:
            self.fields[field_name].required = True


class CarApiMixin:
    __URL = 'https://api.api-ninjas.com/v1/cars'

    def parse_data(self, **data):
        parameters = []
        for k, v in data.items():
            if not v or v == 'all':
                continue
            parameters.append(f'{k}={v}')
        return '&'.join(parameters)

    def make_request(self, **data):
        url = self.__URL + f'?{self.parse_data(**data)}&limit=3000'
        headers = {
            'X-Api-Key': 'WNsOo0klVkYBZnAiRIqPWw==2cdefSnle0bZLX45',
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        return data


class AssignDataUpdateAdForm:

    def asign_data(self, ad_obj, form):
        ad_obj.title = form.cleaned_data['title']
        ad_obj.year_of_manufacture = form.cleaned_data['year_of_manufacture']
        ad_obj.fuel = form.cleaned_data['fuel']
        ad_obj.body_type = form.cleaned_data['body_type']
        ad_obj.transmission = form.cleaned_data['transmission']
        ad_obj.horse_power = form.cleaned_data['horse_power']
        ad_obj.price = form.cleaned_data['price']
        ad_obj.mileage = form.cleaned_data['mileage']
        ad_obj.car = form.cleaned_data['car']
        ad_obj.model = form.cleaned_data['model']
        ad_obj.city = form.cleaned_data['city']
        ad_obj.description = form.cleaned_data['description']

    def update_images(self, ad_obj, form):
        if type(form.cleaned_data['image_main']) is InMemoryUploadedFile:
            ad_obj.image_main = uploader.upload_resource(
                form.cleaned_data['image_main'],
                use_filename=True,
                unique_filename=False,
                filename_override=f'{ad_obj.title}_image_main',
                folder=f'/cars/',
            )
        if type(form.cleaned_data['image1']) is InMemoryUploadedFile:
            ad_obj.image1 = uploader.upload_resource(
                form.cleaned_data['image1'],
                use_filename=True,
                unique_filename=False,
                filename_override=f'{ad_obj.title}_image1',
                folder=f'/cars/',
            )
        if type(form.cleaned_data['image2']) is InMemoryUploadedFile:
            ad_obj.image2 = uploader.upload_resource(
                form.cleaned_data['image2'],
                use_filename=True,
                unique_filename=False,
                filename_override=f'{ad_obj.title}_image2',
                folder=f'/cars/',
            )
        if type(form.cleaned_data['image3']) is InMemoryUploadedFile:
            ad_obj.image3 = uploader.upload_resource(
                form.cleaned_data['image3'],
                use_filename=True,
                unique_filename=False,
                filename_override=f'{ad_obj.title}_image3',
                folder=f'/cars/',
            )

    def asign_data_to_profile(self, profile, form):
        profile.first_name = form.cleaned_data['first_name']
        profile.last_name = form.cleaned_data['last_name']
        profile.age = form.cleaned_data['age']
        profile.phone_number = form.cleaned_data['phone_number']

    def update_profile_image(self, profile, form):
        if type(form.cleaned_data['image']) is InMemoryUploadedFile:
            profile.image = uploader.upload_resource(
                form.cleaned_data['image'],
                use_filename=True,
                unique_filename=False,
                filename_override=f'{profile.user.username}',
                folder=f'/profiles/',
            )


def generate_delete_code():
    nums = set()
    while len(nums) < 2:
        nums.add(random.randint(99999, 999999))
    delete_code = nums.pop()
    return delete_code


def add_generated_delete_code_to_profile(delete_code, profile):
    delete_code_obj = DeleteCode.objects.get(profile=profile)
    delete_code_obj.generated_code = delete_code
    delete_code_obj.save()
