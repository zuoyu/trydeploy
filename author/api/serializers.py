from rest_framework import serializers
from ..models import Author
from django.core.urlresolvers import reverse


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'url', 'username', 'email', 'password', 'is_active', 'first_name', 'last_name',
                  'date_joined', 'github', 'picture')
        read_only_fields = ('id', 'url', 'is_active', 'date_joined')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Author.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super(UserSerializer, self).update(instance, validated_data)
        user.save()
        return user

    def to_representation(self, obj):
        data = super(UserSerializer, self).to_representation(obj)
        request = self.context['request']
        data['posts'] = request.build_absolute_uri(reverse('post_by_author-list', args=(obj.id,)))
        data['displayName'] = data['username']
        if data['github'].find('github.com/') == -1:
            data['github'] = 'https://api.github.com/users/' + data['github'] + '/events'
        data['host'] = request.get_host()
        return data
