from rest_framework.test import APITestCase
from rest_framework import status
from django.core.urlresolvers import reverse
from author.models import Author
from follower.models import Follows
from models import Post, Comment, Image
from django.contrib.staticfiles.templatetags.staticfiles import static


class PostTest(APITestCase):

    def test_create_post(self):
        author_d = Author.objects.create(username="ddd", email="d@404.com", password='0000')
        url = reverse('post-list')
        self.client.force_authenticate(user=author_d)
        post = {
            "title": "t1",
            "content": "c1",
            "privacy_level": "me",
            "privacy_host_only": False
        }
        res = self.client.post(url, post, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["username"], author_d.username)

    def setup(self):
        author_a = Author.objects.create(username="aaa", email="a@404.com", password='0000')
        author_b = Author.objects.create(username="bbb", email="b@404.com", password='0000')
        author_c = Author.objects.create(username="ccc", email="c@404.com", password='0000')
        Follows.objects.create(follower=author_a, followed=author_b).save()
        Follows.objects.create(follower=author_b, followed=author_a).save()

        public_post = Post.objects.create(
            title="public_post",
            author=author_a,
            content="public_post_content",
            privacy_level="pub"

        )
        public_post.save()

        friends_post = Post.objects.create(
            title="friends_post",
            author=author_a,
            content="friends_post_content",
            privacy_level="friends"
        )
        friends_post.save()

        private_post = Post.objects.create(
            title="private_post",
            author=author_a,
            content="private_post_content",
            privacy_level="me"
        )
        private_post.save()
        return [author_a, author_b, author_c]

    def test_public_post(self):
        self.setup()
        url = reverse('visible_posts-list')
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data["count"] == 1)
        title = res.data["posts"][0]['title']
        self.assertEqual(title, "public_post")

    def test_friend_post(self):
        authors = self.setup()
        url = reverse('visible_posts-list')
        self.client.force_authenticate(user=authors[1])
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 2)

    def test_private_post(self):
        authors = self.setup()
        url = reverse('visible_posts-list')
        self.client.force_authenticate(user=authors[0])
        res = self.client.get(url, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        print res.data["count"]
        self.assertEqual(res.data["count"], 3)


class CommentTest(APITestCase):

    def test_post_list_delete(self):
        # post
        author = Author.objects.create(username="ddd", email="d@404.com", password='0000')
        post = Post.objects.create(
            title="public_post",
            author=author,
            content="public_post_content",
            privacy_level="pub"
        )
        post.save()
        commentByPostUrl = reverse('comment_by_post-list', args=(post.id,))
        self.client.force_authenticate(user=author)
        args = {'content': 'my comment content'}
        result = self.client.post(commentByPostUrl, args, format='json')
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        # list
        result = self.client.get(commentByPostUrl)
        self.assertEqual(result.data['count'], 1)
        self.assertEqual(result.data['comments'][0]['content'], 'my comment content')

        # delete
        commentUrl = result.data['comments'][0]['url']
        result = self.client.delete(commentUrl)
        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)
        result = self.client.get(commentByPostUrl)
        self.assertEqual(result.data['count'], 0)

    def test_permission_propogation(self):
        author = Author.objects.create(username="A1", email="A1@404.com", password='0000')
        other_author = Author.objects.create(username="A2", email="A2@404.com", password='0000')
        post = Post.objects.create(title='private post', author=author, content='some content', privacy_level='me')
        post.save()
        commentByPostUrl = reverse('comment_by_post-list', args=(post.id,))
        commentListUrl = reverse('comment-list')
        Comment.objects.create(parent = post, content = 'my comment content')

        self.client.force_authenticate(user=None)

        # cannot create comment for unauthorized post (try both comment creation methods)
        args = {'content': 'my comment content'}
        result = self.client.post(commentByPostUrl, args, format='json')
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)
        args = {'content': 'my comment content', 'parent': reverse('post-detail', args=[post.id])}
        result = self.client.post(commentListUrl, args, format='json')
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)

        # cannot read comment under unauthorized post
        result = self.client.get(commentByPostUrl)
        self.assertEqual(result.data['count'], 0)

        self.client.force_authenticate(user=other_author)

        # STILL cannot create comment for unauthorized post (try both comment creation methods)
        args = {'content': 'my comment content'}
        result = self.client.post(commentByPostUrl, args, format='json')
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)
        args = {'content': 'my comment content', 'parent': reverse('post-detail', args=[post.id])}
        result = self.client.post(commentListUrl, args, format='json')
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)

        # STILL cannot read comment under unauthorized post
        result = self.client.get(commentByPostUrl)
        self.assertEqual(result.data['count'], 0)

        self.client.force_authenticate(user=author)

        # we can read the comment now
        result = self.client.get(commentByPostUrl)
        self.assertEqual(result.data['count'], 1)

class ImageTest(APITestCase):

    def test_post_list_get_delete(self):
        # post
        author = Author.objects.create(username="A1", email="A1@404.com", password='0000')
        self.client.force_authenticate(user=author)
        post = Post.objects.create(title='public post', author=author, content='some content', privacy_level='pub')
        post.save()
        imageListUrl = reverse('image-list')
        image_path = 'post/for_tests/cool.jpg'
        args = {'parent_post': reverse('post-detail', args=[post.id]), 'file_type': 'jpeg', 'image_data': open(image_path, 'rb')}
        result = self.client.post(imageListUrl, args, format='multipart')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        imageUrl = result.data['url']

        self.client.force_authenticate(user=None)

        # list
        result = self.client.get(imageListUrl)
        self.assertEqual(result.data['count'], 1)

        # get
        result = self.client.get(imageUrl)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        result = self.client.get(imageUrl + '?json')
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data['file_type'], 'jpeg')

        self.client.force_authenticate(user=author)

        # delete
        self.client.delete(imageUrl)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        result = self.client.get(imageListUrl)
        self.assertEqual(result.data['count'], 0)

    def test_permission_propogation(self):
        author = Author.objects.create(username="A1", email="A1@404.com", password='0000')
        other_author = Author.objects.create(username="A2", email="A2@404.com", password='0000')
        self.client.force_authenticate(user=author)
        post = Post.objects.create(title='private post', author=author, content='some content', privacy_level='me')
        post.save()
        imageListUrl = reverse('image-list')
        image_path = 'post/for_tests/cool.jpg'
        args = {'parent_post': reverse('post-detail', args=[post.id]), 'file_type': 'jpeg', 'image_data': open(image_path, 'rb')}
        result = self.client.post(imageListUrl, args, format='multipart')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        imageUrl = result.data['url']

        self.client.force_authenticate(user=None)

        # cannot access image
        result = self.client.get(imageListUrl)
        self.assertEqual(result.data['count'], 0)
        result = self.client.get(imageUrl)
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)
        result = self.client.get(imageUrl + '?json')
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=other_author)

        # STILL cannot access image
        result = self.client.get(imageListUrl)
        self.assertEqual(result.data['count'], 0)
        result = self.client.get(imageUrl)
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)
        result = self.client.get(imageUrl + '?json')
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=author)

        # now we can access the image
        result = self.client.get(imageUrl)
        self.assertEqual(result.status_code, status.HTTP_200_OK)