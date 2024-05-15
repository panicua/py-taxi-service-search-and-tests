from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_manufacturer_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 302)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="Mini", country="UK")

    def test_search_manufacturer_by_name(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "M"})
        self.assertContains(response, "BMW")
        self.assertContains(response, "Mini")
        self.assertNotContains(response, "Ford")

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicCarTest(TestCase):
    def test_car_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 302)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test12",
            password="test12313",
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(
            name="Porsche", country="Germany"
        )
        Car.objects.create(model="GT3", manufacturer=manufacturer)
        Car.objects.create(model="Taycan", manufacturer=manufacturer)

    def test_search_car_by_model(self):
        response = self.client.get(CAR_URL, {"model": "GT"})
        self.assertContains(response, "GT3")
        self.assertNotContains(response, "Taycan")

    def test_retrieve_cars(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PublicDriverTest(TestCase):
    def test_driver_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 302)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test1",
            password="test1231",
        )
        self.client.force_login(self.user)
        get_user_model().objects.create(
            username="driver1", first_name="John",
            last_name="Doe", license_number="ABC22345"
        )
        get_user_model().objects.create(
            username="driver2", first_name="John",
            last_name="Doe", license_number="ABC32345"
        )
        get_user_model().objects.create(
            username="racer1", first_name="John",
            last_name="Doe", license_number="ABC42345"
        )

    def test_search_driver_by_username(self):
        response = self.client.get(DRIVER_URL, {"username": "drive"})
        self.assertContains(response, "driver1")
        self.assertContains(response, "driver2")
        self.assertNotContains(response, "racer1")

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
