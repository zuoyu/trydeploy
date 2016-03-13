from follower.models import Follows, FollowManager
from author.models import  Author 
from author.api.serializers import UserSerializer
from django.http import HttpResponse
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from follower.serializers import FollowSerializer
from django.contrib.auth.models import User
from models import Follows
from collections import OrderedDict

class FollowViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows followers to be viewed by author

    Usage: \n
      - `/follow/{author_id}/followers`
        - GET: list all author's followers
        - you cannot POST to this url
      - `/follow/{author_id}/followings`
        - GET: list all author's following author
        - you cannot POST to this url
    """
    queryset = Follows.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [AllowAny, ]
    authentication_classes = [BasicAuthentication, TokenAuthentication, SessionAuthentication]


    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ]
        return super(FollowViewSet, self).get_permissions()


    def create(self, request, *args, **kwargs):
        username = unicode(request.user)

        me = Author.objects.get(username = request.user)

        following = Author.objects.get(id= request.data["followed"].split("/")[-2])
        follow = Follows.objects.follow(me, following)
        follow_serializer = FollowSerializer(follow, context={'request': request})
        return Response(follow_serializer.data)


    @detail_route(methods=["GET"])
    def followers(self, request, **kwargs):
        queryset = Follows.objects.getFollowers(self.kwargs['pk'])
        serializer = FollowSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


    @detail_route(methods=["GET"])
    def followings(self, request, **kwargs):
        queryset = Follows.objects.getFollowing(self.kwargs['pk'])
        print queryset
        serializer = FollowSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


    @detail_route(methods=["GET"])
    def friends(self, request, **kwargs):
        #get all author follower
        follower = Follows.objects.getFollowing(self.kwargs['pk'])
        #get all author follower
        followed = Follows.objects.getFollowers(self.kwargs['pk'])
        print followed[0]
        friend_list = list()

        for i in range(len(followed)):
            for j in range(len(follower)):  
                if followed[i].follower.username == follower[j].followed.username:
                    friend_list.append(followed[i].follower.id)
        print friend_list
        return Response(OrderedDict([
            ('query', 'friends'),
            ('author', self.kwargs['pk']),
            # Array of Author UUIDs who are friends
            ('authors', friend_list)
            ]))



class FriendViewSet(viewsets.ModelViewSet):
    """
    API endpoint that checks two users relation

    Usage: \n
      - `/friend/{author_id_1}/{author_id_2}}`
        - GET: result of two users are friends
    """
    queryset = Follows.objects.all()
    serializer_class = FollowSerializer

    def list(self, request, author_id_1, author_id_2):
        #set default result is false
        result = False
        user_1 = Author.objects.get(pk = author_id_1)
        user_2 = Author.objects.get(pk = author_id_2)


        #check if two user are friends
        result_case_one = Follows.objects.isFollowing(user_1, user_2)
        result_case_two = Follows.objects.isFollowing(user_2, user_1)

        authors = [author_id_1, author_id_2]
        if result_case_one and result_case_two:
            result = True
        else:
            result = False
        return Response(OrderedDict([
            ('query', 'friends'),
            ('authors', authors),
            # boolean true or false
            ('friends', result)
            ]))


class FriendlistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that returns a list of friends.

    Usage: \n
      - `/friends/{author_id}`
        - GET: result of two users are friends
    """
    queryset = Follows.objects.all()
    serializer_class = FollowSerializer

    def list(self, request, author_id):
        #get all author follower
        follower = Follows.objects.getFollowing(author_id)
        #get all author follower
        followed = Follows.objects.getFollowers(author_id)
        print followed[0]
        friend_list = list()

        for i in range(len(followed)):
            for j in range(len(follower)):  
                if followed[i].follower.username == follower[j].followed.username:
                    friend_list.append(followed[i].follower.id)
        print friend_list
        return Response(OrderedDict([
            ('query', 'friends'),
            ('author', author_id),
            # Array of Author UUIDs who are friends
            ('authors', friend_list)
            ]))