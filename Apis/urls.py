from django.urls import path
from Apis.userAuth import *
from Apis.jobResumeView import *

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    # /session
    path('authTn/dynaQuery', JobResumeDynamicQuery.as_view(), name='dynaQuery'),
]