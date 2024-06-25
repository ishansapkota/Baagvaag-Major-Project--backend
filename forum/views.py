from django.shortcuts import render
from .models import forumPost
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta

# Create your views here.

#@method_decorator(login_required(login_url="/api/login/"),name='dispatch')#this makes it so that you need to be logged in to access the forums and post in it, if you are not logged in it sends you to login page
# @csrf_exempt
# class forumAPI(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self,request):
#         posts = forumPost.objects.filter(is_approved = True)
#         #posts = forumPost.objects.all()
#         serializer = ForumSerializer(posts,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
#         # else:
#         #      return Response("Invalid Request!",status=status.HTTP_400_BAD_REQUEST)

#     def post(self, request):
#         if request.user.is_authenticated:
#             # user = User.objects.get(id=id)
#             serializer = ForumSerializer(data=request.data)
#             if serializer.is_valid():
#                 result = serializer.validated_data
#                 serializer.save(user=request.user)
#                 # print(result)
#                 return Response('The post has been sent for approval!', status=status.HTTP_202_ACCEPTED)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response('User must log in!', status=status.HTTP_401_UNAUTHORIZED)
        
    # def put(self,request):

    # @login_required(login_url="/api/login/")
    # def post(self,request):
    #         serializer = ForumSerializer(data = request.data)
    #         if serializer.is_valid():
    #             postTitle = serializer.validated_data.get('postTitle')
    #             postDate = serializer.validated_data.get('postDate')
    #             postTime = serializer.validated_data.get('postTime')
    #             postImage = serializer.validated_data.get('postImage')
    #             data = postDetails.objects.create(postTitle=postTitle,postDate=postDate,postTime=postTime,postImage=postImage)
    #             data.save()
    #             return Response('The data of the post has been saved.',status=status.HTTP_202_ACCEPTED)
    #         else:
    #             return Response('Invalid Data sequence!',status=status.HTTP_400_BAD_REQUEST)
            
            
        # else:
        #     return Response('User is not logged in, go to the login page to access this feature',status=status.HTTP_401_UNAUTHORIZED)

# class ForumPostApprovalAPI(APIView):
#     def post(self,request,post_id):
#         if request.user.is_authenticated and request.user.is_staff:
#             post = forumPost.objects.get( id=post_id)
#             post.is_approved = True
#             post.save()
#             return Response('Post has been approved.', status=status.HTTP_200_OK)
#         else:
#             return Response('Permission denied.', status=status.HTTP_403_FORBIDDEN)


class forumViewAPI(APIView):
    def get(self,request):
        three_days_ago = timezone.now().date() - timedelta(days=3)

        posts = forumPost.objects.filter(is_approved = True,postDate__gte=three_days_ago)
        # iotposts = forumPost.objects.filter(user_id=None)
        serializer = ForumSerializer(posts,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class forumPostingAPI(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        if request.user.is_authenticated:
        # user = User.objects.get(id=request.user.id)
        # object = forumPost.objects.create(user=request.user,postTitle = request.data['postTitle'],postDate=request.data['postDate'],postTime = request.data['postTime'],postImage=request.data['postImage'])
        # object.save()
        # return Response("balla bhayo myaa",status=status.HTTP_201_CREATED)

            serializer = ForumSerializer(data=request.data)
            # default_post_url = "https://asset.cloudinary.com/dzcdirj0l/bd1ba18b679f153c73de442c6ea9beb1"
            # if not serializer.initial_data['postImageURL']:
            #     serializer.data['postImageURL'] = default_post_url
            print(serializer.initial_data)
            if serializer.is_valid():
                result = serializer.validated_data
                serializer.save(user=request.user)
                print(result)
                return Response({"message":'The post has been sent for approval!'}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"message":"Invalid attempt"}, status=status.HTTP_400_BAD_REQUEST)
        else:
                return Response({"message":'User must log in!'}, status=status.HTTP_401_UNAUTHORIZED)
        #add image column in this

class forumCommentAPI(APIView):
    def post(self,request,id):
        post = forumPost.objects.get(id = id)
        # user = User.objects.get(id = id)
        if request.user.is_authenticated:
            serializer = ForumCommentSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save(post=post,user=request.user)
                return Response({"message":"Comment has been made!"},status=status.HTTP_201_CREATED)
            else:
                return Response({"message":"Invalid attempt"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"User must log in!"}, status=status.HTTP_401_UNAUTHORIZED)
        
    def get(self,request,id):
        comments = forumComment.objects.filter(post_id=id)
        serializers = ForumCommentSerializer(comments,many=True)
        return Response({"message":serializers.data},status=status.HTTP_200_OK)


class coordinatesGetAPI(APIView):
    def get(self,request):
        one_day_ago = timezone.now().date() - timedelta(days=1)
        coordinates = forumPost.objects.filter(postDate__gte =one_day_ago)#only approved post's coordinates
        serializer = coordinatesGetSerializer(coordinates,many=True)
        
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    #get this from a table where the admin post coordinates in danger zone tab
    
class unapprovedPostAPI(APIView):
    def get(self,request):
        posts = forumPost.objects.filter(is_approved = None )
        serializers = ForumSerializer(posts,many=True)
        return Response({"message":serializers.data},status=status.HTTP_200_OK)
    
class postApprovalDeletionAPI(APIView):
    def post(self,request,id):
        post = forumPost.objects.get(id = id)
        print(post)
        if request.user.is_superuser == False and request.user.is_staff == True:
            post.is_approved = True
            post.save()
            return Response({"message":"The post has been approved by the admin"},status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"message":"Only admin can approve the post!"},status=status.HTTP_401_UNAUTHORIZED)
        

    def delete(self,request,id):
        post = forumPost.objects.get(id = id)
        if request.user.is_superuser == False and request.user.is_staff == True:
            post.delete()
            return Response("The post has been deleted and has been removed from database.",status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Only admin can delete the post!",status=status.HTTP_401_UNAUTHORIZED)
        
class AddDangerZoneAPI(APIView):
    def post(self,request):
        if request.user.is_superuser == False and request.user.is_staff == True:
             serializer = dangerZoneAddSerializer(data=request.data)
             if serializer.is_valid():
                 serializer.save()
                 return Response("The coordinates have been saved!",status=status.HTTP_200_OK)
             else:
                 return Response("Invalid Response!",status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You must have admin perms",status=status.HTTP_400_BAD_REQUEST)
        

class RangerForumPostingAPI(APIView):
    def post(self,request):
        if request.user.is_superuser == False and request.user.is_staff == True:
            serializer = ForumSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user,is_approved = True)
                return Response({"message":"The post has been posted!"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"message":"Invalid Attempt"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"You must have admin perms"},status=status.HTTP_400_BAD_REQUEST)


class ForumPostingIoTAPI(APIView):
    def post(self,request):
        serializer = ForumSerializer(data=request.data)
        if serializer.is_valid():
                serializer.save(user=None,is_approved = True)
                return Response({"message":"The post has been posted!"}, status=status.HTTP_202_ACCEPTED)
        else:
                return Response({"message":"Invalid Attempt"}, status=status.HTTP_400_BAD_REQUEST)
        
class IOTImageFetchAPI(APIView):
    def post(self,request):
        try:
            serializer = IoTImageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"The images from IoT have been saved!"},status=status.HTTP_200_OK)
            else:
                return Response({"message":"Invalid Attempt"},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message":"Exception occured!"},status=status.HTTP_400_BAD_REQUEST)


class IOTUnApprovedImageViewAPI(APIView):
    def get(self,request):
        try:
            photos = IOTPhotos.objects.filter(is_approved = None)
            serializer = IoTImageSerializer(photos,many=True)
            return Response(serializer.data,status= status.HTTP_200_OK)
        except:
            return Response({"message":"IoT Photos exception!"},status=status.HTTP_400_BAD_REQUEST)
        


class IOTImageApprovalAPI(APIView):
    def put(self,request,id):
        try:
            approvephotos = IOTPhotos.objects.get(id=id)
            if request.user.is_superuser:
                approvephotos.is_approved = True
                approvephotos.save()
                return Response({"message":"The image from IoT has been approved!"},status=status.HTTP_200_OK)
            else:
                return Response({"message":"Only admin can approve the image."},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message":"ImageApproval exception"},status=status.HTTP_400_BAD_REQUEST)
        

class IOTImageRejectionAPI(APIView):
    def delete(self,request,id):
        try:
            approvephotos = IOTPhotos.objects.get(id=id)
            if request.user.is_superuser:
                approvephotos.delete()
                return Response({"message":"The image from IoT has been rejected!"},status=status.HTTP_200_OK)
            else:
                return Response({"message":"Only admin can rejected the image."},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message":"ImageRejection exception"},status=status.HTTP_400_BAD_REQUEST)

class IOTApprovedImageViewAPI(APIView):
    def get(self,request):
        try:
            photos = IOTPhotos.objects.filter(is_approved = True)
            serializer = IoTImageSerializer(photos,many=True)
            return Response(serializer.data,status= status.HTTP_200_OK)
        except:
            return Response({"message":"IoT Photos exception!"},status=status.HTTP_400_BAD_REQUEST)