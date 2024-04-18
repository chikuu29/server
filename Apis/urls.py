from django.urls import path
from Apis.userAuth import *
from Apis.jobResumeView import *

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('logout',LogoutView.as_view(),name='logout'),
    # /session# /session
    path('authTn/dynaQuery', JobResumeDynamicQuery.as_view(), name='dynaQuery'),
    path('authTn/dynaAggregation', JobResumeAggregationQuery.as_view(), name='dynaAggregation'),
    path('session',checkLoginStatus.as_view(),name='session'),
    path('JobsResumeView',JobsResumeView.as_view(),name='JobsResumeView'),
]

