from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class ForumSerializer(serializers.ModelSerializer):
    #postImage = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)
    class Meta:
        model = forumPost
        fields = ['postTitle','postDate','postTime','postImage']
        #fields = ['postTitle','postImage']

class ForumCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = forumComment
        fields = ['comment']
        