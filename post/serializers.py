import base64
import imghdr
from rest_framework import serializers
from permissions import *
from rest_framework import exceptions

from author.api.serializers import UserSerializer
from .models import Post, Image, Comment

class PostWriteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'url', 'title', 'content', 'date_created', 'last_modified', 'privacy_level', 'privacy_host_only')

    def create(self, validated_data):
        author = self.context['request'].user
        validated_data['author'] = author
        post = Post.objects.create(**validated_data)
        return post

    def to_representation(self, obj):
        data = super(PostWriteSerializer, self).to_representation(obj)

        request = self.context['request']
        queryset = Comment.objects.all().order_by('-date_created')
        try:
            queryset = [comment for comment in queryset if comment.parent.id == obj.id]
        except:
            queryset = []
        queryset = [comment for comment in queryset if CanViewComment(comment, request.user)]
        commentSerializer = CommentReadSerializer(data = queryset, many = True, context = {'request': request})
        commentSerializer.is_valid()
        data['comments'] = commentSerializer.data

        data['comments_list'] = data['url'] + 'comments/'

        data['username'] = obj.author.username
        data['source'] = data['url']
        data['origin'] = data['url']
        return data

class PostReadSerializer(PostWriteSerializer):
    author = UserSerializer()

    class Meta:
        model = Post
        fields = ('id', 'url', 'title', 'content', 'author', 'date_created', 'last_modified', 'privacy_level', 'privacy_host_only')

class CommentWriteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('url', 'content', 'remote_author_name', 'remote_author_url', 'parent', 'date_created', 'last_modified')

    def create(self, validated_data):
        local_author = self.context['request'].user
        if not local_author.is_anonymous():
            validated_data['local_author'] = local_author
        comment = Comment.objects.create(**validated_data)
        return comment

    def validate_parent(self, value):
        if not CanViewPost(value, self.context['request'].user):
            raise exceptions.PermissionDenied('Attempted to create Comment with parent you cannot view')
        return value

class CommentReadSerializer(CommentWriteSerializer):
    local_author = UserSerializer()
    class Meta:
        model = Comment
        fields = ('url', 'content', 'local_author', 'remote_author_name', 'remote_author_url', 'parent', 'date_created', 'last_modified')

class CommentByPostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('url', 'content', 'remote_author_name', 'remote_author_url', 'date_created', 'last_modified')

    def create(self, validated_data):
        post_id = self.context['parent']
        parent = Post.objects.get(pk=post_id)
        if not CanViewPost(parent, self.context['request'].user):
            raise exceptions.PermissionDenied('Attempted to create Comment with parent you cannot view')
        validated_data['parent'] = parent
        local_author = self.context['request'].user
        if not local_author.is_anonymous():
            validated_data['local_author'] = local_author
        comment = Comment.objects.create(**validated_data)
        return comment

# http://www.scriptscoop.net/t/7d698c5fe6de/using-django-rest-framework-how-can-i-upload-a-file-and-send-a-json-pa.html
class Base64Field(serializers.Field):
    def to_internal_value(self, data):
        # Check if the base64 string is in the "data:" format
        if 'data:' in data and ';base64,' in data:
            # Break out the header from the base64 content
            header, data = data.split(';base64,')

        # Try to decode the file. Return validation error if it fails.
        try:
            decoded_file = base64.b64decode(data)
        except TypeError:
            self.fail('invalid_image')

        file_ext = imghdr.what('', decoded_file)
        if file_ext == 'jpg':
            file_ext = 'jpeg'

        return decoded_file

    def to_representation(self, value):
        return base64.b64encode(value)

class ImageCreateSerializer(serializers.HyperlinkedModelSerializer):
    image_data = serializers.ImageField()
    class Meta:
        model = Image
        fields = ('url', 'parent_post', 'file_type', 'image_data', 'date_created')

    def create(self, validated_data):
        uploader = self.context['request'].user
        validated_data['uploader'] = uploader
        validated_data['image_data'] = validated_data['image_data'].file.read()
        image = Image.objects.create(**validated_data)
        return image

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    image_data = Base64Field()
    class Meta:
        model = Image
        fields = ('url', 'uploader', 'parent_post', 'file_type', 'image_data', 'date_created')

    def to_representation(self, obj):
        data = super(ImageSerializer, self).to_representation(obj)
        data['json_url'] = data['url'] + '?json'
        return data

class ImageSimpleSerializer(serializers.HyperlinkedModelSerializer):
    """
    Doesn't return image_data at all
    """
    class Meta:
        model = Image
        fields = ('url', 'uploader', 'parent_post', 'file_type', 'date_created')

    def to_representation(self, obj):
        data = super(ImageSimpleSerializer, self).to_representation(obj)
        data['json_url'] = data['url'] + '?json'
        return data