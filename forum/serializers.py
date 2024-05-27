from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class ForumSerializer(serializers.ModelSerializer):
    #postImage = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)
    id = serializers.IntegerField(read_only = True)
    user_first_name = serializers.CharField(source='user.first_name',read_only = True)
    user_last_name = serializers.CharField(source='user.last_name',read_only = True)

    class Meta:
        model = forumPost
        #fields = '__all__'
        fields = ['id','postTitle','postDate','postTime','postImage','latitude','longitude','user_first_name','user_last_name']

class ForumCommentSerializer(serializers.ModelSerializer):
    # user_email = serializers.EmailField(source='user.email', read_only=True)
    user_first_name = serializers.CharField(source='user.first_name',read_only = True)
    user_last_name = serializers.CharField(source='user.last_name',read_only = True)
    uploaded_on = serializers.DateTimeField(read_only = True)

    class Meta:
        model = forumComment
        fields = ['comment','uploaded_on','user_first_name','user_last_name']
        

class coordinatesGetSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(read_only = True)
    longitude = serializers.FloatField(read_only = True)
    # postDate = serializers.DateField(read_only = True)
    class Meta:
        model = forumPost
        fields = ['latitude','longitude',]
        