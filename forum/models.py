from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
# class postDetails(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
#     postTitle = models.CharField(max_length=255)
#     postDate = models.DateField()
#     postTime = models.TimeField()
#     #postImageURL = models.URLField() #pillow library is required
#     postImage = CloudinaryField('image',null = True, blank = True) #this 'image' inside the bracket of CloudinaryField signifies that the input to be taken is of image format


class forumPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    postTitle = models.CharField(max_length=255)
    postDate = models.DateField(null=True)
    postTime = models.TimeField(null=True)
    #postImageURL = models.URLField() #pillow library is required
    #postImage = CloudinaryField('image',null = True, blank = True) #this 'image' inside the bracket of CloudinaryField signifies that the input to be taken is of image format
    postImage = models.TextField(max_length = 200,null=True)
    is_approved = models.BooleanField(null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    def __str__(self):
        if self.is_approved:
            return self.postTitle + ' from '+ self.user.email + " is approved "
        else:
            return self.postTitle + ' from '+ self.user.email + " is not approved "

class forumComment(models.Model):
    post = models.ForeignKey(forumPost,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    comment = models.CharField(max_length = 450)
    uploaded_on = models.DateTimeField(auto_now_add=True)
