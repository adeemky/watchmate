from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from . import models


# STREAM
class StreamPlatformTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="adem", password="kaya")
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        self.stream = models.StreamPlatform.objects.create(
            name="Youtube", about="#1 Platform", website="https://www.youtube.com"
        )

    def test_streamplatform_create(self):
        data = {
            "name": "Youtube",
            "about": "Most famous video site",
            "website": "https://www.youtube.com",
        }

        response = self.client.post(reverse("streamplatform-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_streamplatform_list(self):
        response = self.client.get(reverse("streamplatform-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_ind(self):
        response = self.client.get(
            reverse("streamplatform-detail", args=(self.stream.id,))
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# WATCH LIST
class WatchListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="adem", password="kaya")
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        self.stream = models.StreamPlatform.objects.create(
            name="Netflix", about="#1 Platform", website="https://www.netflix.com"
        )

        self.watchlist = models.WatchList.objects.create(
            platform=self.stream, title="Example Movie", storyline="Example Story"
        )

    def test_watchlist_create(self): # If there is an error comment platform variable in WatchListSerializer
        data = {
            "platform": self.stream.id,
            "title": "Example Movie",
            "storyline": "Example Story",
        }

        response = self.client.post(reverse("movie-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_watchlist_list(self):
        response = self.client.get(reverse("movie-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_ind(self):
        response = self.client.get(reverse("movie-detail", args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(), 1)
        self.assertEqual(models.WatchList.objects.get().title, "Example Movie")


# REVIEW
class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="adem", password="kaya")
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        self.stream = models.StreamPlatform.objects.create(
            name="Netflix", about="#1 Platform", website="https://www.netflix.com"
        )

        self.watchlist = models.WatchList.objects.create(
            platform=self.stream, title="Example Movie", storyline="Example Story"
        )
        self.watchlist2 = models.WatchList.objects.create(
            platform=self.stream, title="Example Movie", storyline="Example Story"
        )

        self.review = models.Review.objects.create(
            review_user=self.user,
            rating=5,
            description="Great Movie",
            watchlist=self.watchlist2,
        )

    def test_review_create(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Good Movie",
            "watchlist": self.watchlist,
        }

        response = self.client.post(
            reverse("review-create", args=(self.watchlist.id,)), data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)

    def test_review_create_unauth(self):

        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Good Movie",
            "watchlist": self.watchlist,
        }

        self.client.force_authenticate(user=None)
        response = self.client.post(
            reverse("review-create", args=(self.watchlist.id,)), data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            "review_user": self.user,
            "rating": 4,
            "description": "Good Movie - Updated",
            "watchlist": self.watchlist,
        }

        response = self.client.put(
            reverse("review-detail", args=(self.review.id,)), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(reverse("review-list", args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_ind(self):
        response = self.client.get(reverse("review-detail", args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_delete(self):  # If there is an error comment the RevievDetail views
        response = self.client.delete(reverse("review-detail", args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_review_user(self):
        response = self.client.get(
            "/watch/user-reviews/?username=" + self.user.username
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
