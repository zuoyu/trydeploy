from rest_framework.test import APITestCase
from rest_framework import status
from django.core.urlresolvers import reverse
from author.models import Author
from follower.models import Follows

class FriendTest(APITestCase):

        def test_follow(self):
                url = reverse("follows-list")
                author_a_sampel = Author.objects.create(username="aaa", email="a@404.com", password='0000')
                author_a = Author.objects.get(username="aaa")
                author_b = Author.objects.create(username="bbb", email="b@404.com", password='0000')
                #Follows.objects.create(follower=author_a, followed=author_b).save()
                print author_a
                self.client.force_authenticate(user=author_a)
                data = {
                        "follower": author_a.id,
                        "following": author_b.id}
                response= self.client.post(url, data)