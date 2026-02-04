from django.urls import path

from quiz_master.assessments.views import SubjectListView

urlpatterns = [path("subjects/", SubjectListView.as_view(), name="")]
