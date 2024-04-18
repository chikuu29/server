from django.urls import path
from Apis.userAuth import *
from Apis.jobResumeView import *

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('logout',LogoutView.as_view(),name='logout'),
    # /session
    path('auth/dynaQuery', JobResumeDynamicQuery.as_view(), name='dynaQuery'),
]