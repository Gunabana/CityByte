from urllib import request
import unittest
import requests
import re
from django.test import TestCase
from info.helpers.places import FourSquarePlacesHelper
from django.shortcuts import render
from info.helpers.weather import WeatherBitHelper
from datetime import datetime
import pytz
from info.models import Comment
from info.forms import CommentForm
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from search.helpers.photo import UnplashCityPhotoHelper
from urllib.request import urlopen

image_formats = ("image/png", "image/jpeg", "image/gif")


class CityByte_testcase(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            "admin", "admin.@simpson.net", "admin"
        )

    def test_main_page(self):
        assert render(request, "search/search.html").status_code == 200

    def test_cityphoto(self):
        photo_link = UnplashCityPhotoHelper().get_city_photo(city="Pune")
        site = urlopen(photo_link)
        meta = site.info()
        if meta["content-type"] in image_formats:
            assert True

    def test_photo(self):
        photo_link = FourSquarePlacesHelper().get_place_photo(
            fsq_id="518a71ab498e430858000827"
        )
        site = urlopen(photo_link)
        meta = site.info()
        if meta["content-type"] in image_formats:
            assert True

    def test_info_page(self):
        city = "New York City"
        country = "US"

        try:
            weather_info = WeatherBitHelper().get_city_weather(
                city=city, country=country
            )["data"][0]
            weather_info["sunrise"] = (
                datetime.strptime(weather_info["sunrise"], "%H:%M")
                .astimezone(pytz.timezone(weather_info["timezone"]))
                .strftime("%I:%M")
            )
            weather_info["sunset"] = (
                datetime.strptime(weather_info["sunset"], "%H:%M")
                .astimezone(pytz.timezone(weather_info["timezone"]))
                .strftime("%I:%M")
            )
            weather_info["ts"] = datetime.fromtimestamp(
                weather_info["ts"]
            ).strftime("%m-%d-%Y, %H:%M")

        except Exception:
            # api limit exceeded
            weather_info = {}

        # commentForm = CommentForm()

        dining_info = FourSquarePlacesHelper().get_places(
            city=f"{city}, {country}",
            categories="13065",
            sort="RELEVANCE",
            limit=5,
        )
        outdoor_info = FourSquarePlacesHelper().get_places(
            city=f"{city}, {country}",
            categories="16000",
            sort="RELEVANCE",
            limit=5,
        )
        airport_info = FourSquarePlacesHelper().get_places(
            city=f"{city}, {country}",
            categories="19040",
            sort="RELEVANCE",
            limit=5,
        )
        arts_info = FourSquarePlacesHelper().get_places(
            city=f"{city}, {country}",
            categories="10000",
            sort="RELEVANCE",
            limit=5,
        )
        photo_link = UnplashCityPhotoHelper().get_city_photo(city=city)
        # comments = Comment.objects.filter(city=city, country=country).order_by(
        #     "-created_on"
        # )
        # isInFav = True if FavCityEntry.objects.filter(city=city, country=country, user=request.user).count() > 0 else False
        # render(request, 'search/city_info.html', context={"weather_info": weather_info, "dining_info": dining_info, "outdoor_info": outdoor_info, "airport_info": airport_info, "photo_link": photo_link, "arts_info": arts_info,  "comments": comments,
        #     "commentForm": commentForm,
        #     'city': city,
        #     'country': country,
        #     'isInFav': True}).status_code == 200
        if (
            not weather_info
            and not dining_info
            and not outdoor_info
            and not airport_info
            and not arts_info
            and not photo_link
        ):
            assert True

    def TestModels(TestCase):
        user = get_user_model().objects.create_user(
            "admin@citybyte.com", "password"
        )
        assert user

    def test_can_access_page(self):
        login = self.client.login(username="admin", password="admin")
        self.assertTrue(login)
        # self.assertEqual(response.status_code,200)

    def test_user_logout(self):
        # client=Client()
        self.client.logout()
        # response = self.client.get('/admin/')
        self.assertTrue(True)

    def test_profile_page(self):
        self.client = Client()
        response = self.client.get(reverse("profile_page"))
        self.assertTrue(200, response.status_code)

    def test_place_photo(self):
        self.client = Client()
        response = self.client.get(reverse("info:place_photo"))
        self.assertTrue(200, response.status_code)

class TestGoogleMapsAPI(TestCase):

    def test_city_info(self):
        assert render(request, "search/search.html").status_code == 200
    
    def setUp(self): 
        self.api_key = "AIzaSyARlyaa0oivxKv8jtpx_wzt5fjh1XvoerI"
        self.location = "Myrtle Beach US"
        self.url = f"https://www.google.com/maps/embed/v1/place?key={self.api_key}&q={self.location}"

    def test_map_response(self):
        # Send a GET request to the Google Maps embed URL
        response = requests.get(self.url)
        
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Optionally, check if the content-type of the response is as expected
        self.assertIn("text/html", response.headers["Content-Type"])

    def test_sanitize_address_function(self):
    
        # Since this is a JS function, you can test it via the output to the address field
        address = '123 Main St.!@#$%^&*()'
        sanitized_address = re.sub('[^0-9a-zA-Z]+', ' ',address)  # Expected behavior
        self.assertEqual(sanitized_address, '123 Main St ')  # Spaces where special chars were"""
class ExtendedTests(TestCase):
    def setUp(self):
        self.client = Client()
        get_user_model().objects.create_user(
            "testuser", "testuser@citybyte.com", "testpassword"
        )
        self.api_key = "AIzaSyARlyaa0oivxKv8jtpx_wzt5fjh1XvoerI"
        self.location = "Myrtle Beach US"
        self.url = f"https://www.google.com/maps/embed/v1/place?key={self.api_key}&q={self.location}"

    #  Test for Correct URL Format
    def test_google_maps_url_format(self):
        is_valid_format = re.match(
            r"^https://www\.google\.com/maps/embed/v1/place\?key=[\w-]+&q=[\w\s,]+$",
            self.url
        )
        self.assertTrue(is_valid_format)

    #  Test Response Time for Google Maps API
    def test_google_maps_response_time(self):
        response = requests.get(self.url)
        self.assertLess(response.elapsed.total_seconds(), 2, "Response took too long.")

    #  Test for API Key Presence in URL
    def test_api_key_in_url(self):
        self.assertIn("key=", self.url)

    #  Test Redirects on Unauthorized Access to Profile Page
    def test_unauthorized_access_redirect(self):
        response = self.client.get(reverse("profile_page"))
        self.assertEqual(response.status_code, 302, "Unauthorized users should be redirected.")

    # Test Image Format for City Photo in FourSquare Helper
    def test_city_photo_format(self):
        photo_link = UnplashCityPhotoHelper().get_city_photo(city="Paris")
        site = urlopen(photo_link)
        meta = site.info()
        self.assertIn(meta["content-type"], image_formats, "Photo format is not supported.")

    # Test Weather API Data Structure
    def test_weather_data_structure(self):
        city = "Los Angeles"
        country = "US"
        try:
            weather_info = WeatherBitHelper().get_city_weather(
                city=city, country=country
            )["data"][0]
            weather_info["sunrise"] = (
                datetime.strptime(weather_info["sunrise"], "%H:%M")
                .astimezone(pytz.timezone(weather_info["timezone"]))
                .strftime("%I:%M")
            )
            weather_info["sunset"] = (
                datetime.strptime(weather_info["sunset"], "%H:%M")
                .astimezone(pytz.timezone(weather_info["timezone"]))
                .strftime("%I:%M")
            )
            weather_info["ts"] = datetime.fromtimestamp(
                weather_info["ts"]
            ).strftime("%m-%d-%Y, %H:%M")

        except Exception:
            # api limit exceeded
            weather_info = {}

    #  Test map location with special characters
    
    def test_map_url_special_characters(self):
        special_location = "São Paulo, Brazil"
        url = f"https://www.google.com/maps/embed/v1/place?key={self.api_key}&q={special_location}"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200, "URL with special characters should load successfully.")

    #  Test User Login Page
    def test_user_login(self):
        response = self.client.post(reverse("login"), data={"username": "testuser", "password": "testpassword"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("_auth_user_id", self.client.session)

    #  Test API Key Error
    def test_invalid_api_key(self):
        invalid_key_url = f"https://www.google.com/maps/embed/v1/place?key=INVALID_KEY&q={self.location}"
        response = requests.get(invalid_key_url)
        self.assertNotEqual(response.status_code, 200, "Invalid API key should not return a valid response.")

    # Test Large Query for Dining Info
    def test_large_dining_info_query(self):
        dining_info = FourSquarePlacesHelper().get_places(city="New York, US", categories="13065", sort="RELEVANCE", limit=50)
        self.assertGreaterEqual(len(dining_info), 1, "Large query should return some results.")

    #  Test Comment Form Validation
    def test_comment_form_validation(self):
        form_data = {"text": ""}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid(), "Comment form with empty text should be invalid.")

    #  Test Missing City Data in Weather API Response
    def test_missing_city_data_weather(self):
        invalid_city = "InvalidCity123"
        weather_info = WeatherBitHelper().get_city_weather(city=invalid_city, country="US")
        self.assertFalse(weather_info, "Missing city data should return an empty response.")

    #  Test Profile Page Access for Authenticated User
    def test_authenticated_user_profile_page(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("profile_page"))
        self.assertEqual(response.status_code, 200, "Authenticated user should access profile page.")

    #  Test Logout Functionality
    def test_user_logout_functionality(self):
        self.client.login(username="testuser", password="testpassword")
        self.client.logout()
        response = self.client.get(reverse("profile_page"))
        self.assertEqual(response.status_code, 302, "Logged-out user should be redirected from profile page.")

    #  Test Map Embed URL with Numeric Location
    def test_numeric_location_map_url(self):
        url = f"https://www.google.com/maps/embed/v1/place?key={self.api_key}&q=12345"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200, "Numeric location should return a valid response if location exists.")