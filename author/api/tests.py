from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from rest_framework import status

from ..models import Author

#http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
class UserTest(APITestCase):
    count = 0

    def create_a_user(self):
        username = 'user_%d' % self.count
        email = 'u%d@email.com' % self.count
        author = Author.objects.create(username=username, email=email, password='0000')
        author.save()
        self.count += 1
        return author

    def test_create(self):
        url = reverse('author-list')
        data = {
            "username": "user_1",
            "password": "0000",
            "email": "u1@email.com",
            "github": "user1"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 1)
        user = Author.objects.get_by_natural_key('user_1')
        self.assertEqual(user.email, 'u1@email.com')
        self.assertEqual(user.github, 'user1')

    def test_list(self):
        url = reverse('author-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['authors']), 0)
        self.create_a_user()
        self.create_a_user()
        self.create_a_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['authors']), 3)

    def test_authentication(self):
        user = self.create_a_user()
        url = reverse('author-detail', kwargs={'pk': user.id})
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch(self):
        user = self.create_a_user()
        url = reverse('author-detail', kwargs={'pk': user.id})
        data = {
            "first_name": "User",
            "last_name": "One",
            "github": "123123123"
        }
        self.client.force_authenticate(user=user)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = Author.objects.get_by_natural_key(user.username)
        self.assertEqual(user.first_name, 'User')
        self.assertEqual(user.last_name, 'One')
        self.assertEqual(user.github, "123123123")




