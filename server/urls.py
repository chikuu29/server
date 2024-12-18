"""
URL configuration for server project.

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
# from django.contrib import admin
from django.urls import path,include
from db.mongo import db
from Apis.jobResumeView import *

urlpatterns = [
    # path('admin/', admin.site.urls),
     path('api/', include([
        path('auth/', include('Apis.urls')),
        path('getAllResume',getallResume.as_view()),
        path('getallJob',getallJob.as_view()),
        path('syncAllResumeJobs',syncAllResumeJobs.as_view()),
        path('dynaQuery', JobResumeDynamicQuery.as_view(), name='dynaQuery'),
        path('dynaAggregation', JobResumeAggregationQuery.as_view(), name='dynaAggregation'),
        path('getJobResumePost', getJobPost.as_view(), name='getJobResumePost'),
        path('nlpfindtopjobs',getTopTenJobPost.as_view(),name="nlpfindtopjobs"),
        path('nlpfindtopresumes',getTopTenJobResume.as_view(),name="nlpfindtopresumes")
    ])),
]
