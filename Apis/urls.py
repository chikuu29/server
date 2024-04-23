from django.urls import path
from Apis.userAuth import *
from Apis.jobResumeView import *

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('logout',LogoutView.as_view(),name='logout'),
    # /session# /session
    # path('dynaQuery', JobResumeDynamicQuery.as_view(), name='dynaQuery'),
    # path('dynaAggregation', JobResumeAggregationQuery.as_view(), name='dynaAggregation'),
    # path('getJobResumePost', getJobPost.as_view(), name='getJobResumePost'),
    # path('nlpfindtopjobs',getTopTenJobPost.as_view(),name="nlpfindtopjobs"),
    # path('nlpfindtopresumes',getTopTenJobResume.as_view(),name="nlpfindtopresumes"),
    path('session',checkLoginStatus.as_view(),name='session'),
]

