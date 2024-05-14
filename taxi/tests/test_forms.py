from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
)


class FormsTest(TestCase):
    def test_driver_creation_form_with_license_number_first_last_name(self):
        form_data = {
            "username": "some_username",
            "password1": "some_password123",
            "password2": "some_password123",
            "first_name": "some_first_name",
            "last_name": "some_last_name",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_update_form_with_license_number(self):
        form_data = {
            "license_number": "XCS54321",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_search_from_with_username(self):
        form_data = {
            "username": "x" * 256
        }
        form = DriverSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertFalse(form.cleaned_data)
