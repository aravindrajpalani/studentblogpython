from django.contrib.auth import update_session_auth_hash

from rest_framework import serializers

from studentzapp.models import Account
from rest_framework import serializers
from .models import BlogPost,Like

class BlogPostSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = BlogPost
        fields = ('id', 'title','content','owner', 'likescount','likes','date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')


class LikeSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    ownername = serializers.ReadOnlyField(source='ownerfbid.displayname')
    ownerfbid = serializers.ReadOnlyField(source='ownerfbid.fbid')
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Like
        fields = ('postid','post','user', 'ownername', 'ownerfbid', 'isliked')



class AccountSerializer(serializers.ModelSerializer):
  

    class Meta:
        model = Account
        fields = ('id', 'email', 'displayname', 'fbid','accesstoken','created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at',)

        def create(self, validated_data):
            return Account.objects.create(**validated_data)
