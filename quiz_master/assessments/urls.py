from django.urls import path

from quiz_master.assessments.views import HomeModelView
from quiz_master.assessments.views import QuizListView
from quiz_master.assessments.views import QuizView
from quiz_master.assessments.views import SubjectListView
from quiz_master.assessments.views import TopicListView

app_name = "assessments"

urlpatterns = [
    path("", HomeModelView.as_view(), name="home"),
    path("subjects/", SubjectListView.as_view(), name="subjects"),
    path("<int:subject_id>/topics/", TopicListView.as_view(), name="topics"),
    path("quizes/<str:topic_id>/", QuizListView.as_view(), name="quizes"),
    path("quizes/<str:topic>/<int:quiz_id>", QuizView.as_view(), name="quiz"),
]
