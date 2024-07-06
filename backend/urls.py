"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user_auth.views import *
from forum.views import *
from charity.views import *
from khalti.views import *
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register',Registration.as_view()),
    path('api/verify/<int:id>/<str:token>',EmailVerification.as_view()),
    path('api/login/',handleLogin.as_view()),
    path('api/logout',handleLogout.as_view()),
    path('api/forgotpassword',ForgotPassword.as_view()),
    path('api/reset_password/<int:id>/<str:token>',ResetPassword.as_view()),
    path('api/forum',forumViewAPI.as_view()),
    path('api/forum/post',forumPostingAPI.as_view()),
    path('api/post/<int:id>/comments',forumCommentAPI.as_view()),
    path('api/post_coordinates',coordinatesGetAPI.as_view()),
    path('api/forum/unapproved',unapprovedPostAPI.as_view()),
    path('api/forum/approval/<int:id>',postApprovalDeletionAPI.as_view()),
    path('api/kyc/<int:id>',KYCAPI.as_view()),
    path('api/admin/add_ranger',AddRanger.as_view()),
    path('api/change_to_admin/<int:id>',ChangeToAdmin.as_view()),
    path('api/admin/list_user',ListUsers.as_view()),
    path('api/admin/list_ranger',ListRangers.as_view()),
    path('api/admin/delete_user/<int:id>',DeleteUserAdmin.as_view()),
    path('api/admin/delete_ranger/<int:id>',DeleteRangerAdmin.as_view()),
    path('api/ranger/adddangerzone',AddDangerZoneAPI.as_view()),
    path('api/ranger/forum/post',RangerForumPostingAPI.as_view()),
    path('api/iot/forum/post',ForumPostingIoTAPI.as_view()),
    path('api/iot/image/fetch',IOTImageFetchAPI.as_view()),
    path('api/iot/image/unapproved',IOTUnApprovedImageViewAPI.as_view()),
    path('api/iot/image/approval/<int:id>',IOTImageApprovalAPI.as_view()),
    path('api/iot/image/rejection/<int:id>',IOTImageRejectionAPI.as_view()),
    path('api/iot/image',IOTApprovedImageViewAPI.as_view()),
    path('api/admin/victim/add',AddVictim.as_view()),
    path('api/admin/victim/list',ViewVictim.as_view()),
    path('api/admin/victim/edit/<int:id>',EditVictimInfo.as_view()),
    path('api/admin/victim/delete/<int:id>',DeleteVictimInfo.as_view()),
    path('api/khalti/try/<int:id>',KhaltiInitiation.as_view()),
    path('api/khalti/verify',KhaltiVerification.as_view()),
]
