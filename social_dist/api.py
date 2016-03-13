from rest_framework import routers
from author.api.views import AuthorViewSet
from post.views import PostViewSet, CommentViewSet, ImageViewSet, PostByAuthor, MyPosts, CommentByPost
from follower.views import FollowViewSet, FriendViewSet, FriendlistViewSet

# http://stackoverflow.com/questions/17496249/in-django-restframework-how-to-change-the-api-root-documentation
class MyRouter(routers.DefaultRouter):
    def get_api_root_view(self):
        api_root_view = super(MyRouter, self).get_api_root_view()
        ApiRootClass = api_root_view.cls

        class MyAPIRoot(ApiRootClass):
            """
            _In general, our API matches Abram's example-article.json_

            ## [Posts](/api/posts) \n
            - create, list, edit, delete: [`/posts`](/api/posts) _<-- try clicking_
            - list all the posts that I authored: [`/author/myposts`](/api/author/myposts)
            - list all the posts I can view: [`/author/posts`](/api/author/posts)
            - list by author: `/author/{author_id}/posts`

            ## [Comments](/api/comments) \n
            - create, list, edit, delete: [`/comments`](/api/comments)
            - list, create by parent post: `/api/posts/{post_id}/comments`

            ## [Images](/api/images) \n
            - create, delete: [`/images`](/api/images)

            ## [Authors](/api/author) \n
            - create, list, edit, delete: [`/author`](/api/author)

            ## [Follow](/api/follow) \n
            - create, list, delete: [`/follow`](/api/follow)

            ## [Friend](/api/friend) \n
            - list, delete: [`/friend/author_id`](/api/friend)

            _Edit this documentation in `social_dist/social_dist/api.py`_

            """
            pass

        return MyAPIRoot.as_view()

router = MyRouter()

# Post views
router.register(r'author/posts', PostViewSet, base_name='visible_posts')
router.register(r'author/myposts', MyPosts, base_name='my_posts') # not required by the spec
router.register(r'posts', PostViewSet)
router.register(r'author/(?P<author_id>[0-9a-f\-]+)/posts', PostByAuthor, base_name='post_by_author')

# Comment views
router.register(r'posts/(?P<post_id>[0-9a-f\-]+)/comments', CommentByPost, base_name='comment_by_post')
router.register(r'comments', CommentViewSet) # not required by the spec

# Image views
router.register(r'images', ImageViewSet)

# Author views
router.register(r'author', AuthorViewSet)

# Friend views TODO
router.register(r'follow', FollowViewSet)

router.register(r'friend/(?P<author_id_1>[0-9a-f\-]+)/(?P<author_id_2>[0-9a-f\-]+)', FriendViewSet)

router.register(r'friends/(?P<author_id>[0-9a-f\-]+)', FriendlistViewSet)

