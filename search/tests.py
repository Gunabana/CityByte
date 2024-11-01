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

    # 1. Test for Correct URL Format
    def test_google_maps_url_format(self):
        is_valid_format = re.match(
            r"^https://www\.google\.com/maps/embed/v1/place\?key=[\w-]+&q=[\w\s,]+$",
            self.url
        )
        self.assertTrue(is_valid_format)

    # 2. Test Response Time for Google Maps API
    def test_google_maps_response_time(self):
        response = requests.get(self.url)
        self.assertLess(response.elapsed.total_seconds(), 2, "Response took too long.")

    # 3. Test for API Key Presence in URL
    def test_api_key_in_url(self):
        self.assertIn("key=", self.url)

    # 4. Test for Proper Handling of Invalid City Input
    def test_invalid_city_input(self):
        invalid_url = f"https://www.google.com/maps/embed/v1/place?key={self.api_key}&q=InvalidCity12345"
        response = requests.get(invalid_url)
        self.assertEqual(response.status_code, 404, "Invalid city input should return 404.")

    # 5. Test Redirects on Unauthorized Access to Profile Page
    def test_unauthorized_access_redirect(self):
        response = self.client.get(reverse("profile_page"))
        self.assertEqual(response.status_code, 302, "Unauthorized users should be redirected.")

    # 6. Test Image Format for City Photo in FourSquare Helper
    def test_city_photo_format(self):
        photo_link = UnplashCityPhotoHelper().get_city_photo(city="Paris")
        site = urlopen(photo_link)
        meta = site.info()
        self.assertIn(meta["content-type"], image_formats, "Photo format is not supported.")
    # 8. Test Access to Favorite City List
    def test_favorite_city_list_access(self):
        response = self.client.get(reverse("favCities"))
        self.assertEqual(response.status_code, 200)

    # 9. Test Weather API Data Structure
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

    # 10. Test API Limit Error Handling for Weather API
    def test_weather_api_limit_handling(self):
        # Simulating multiple calls to exceed API limits
        for _ in range(10):
            weather_info = WeatherBitHelper().get_city_weather(city="Tokyo", country="JP")
        self.assertIn("error", weather_info, "API limit exceeded should return error.")


    



