# services/topics.py

from django.db.models import QuerySet

from quiz_master.assessments.models import Question
from quiz_master.assessments.models import Quiz
from quiz_master.assessments.models import Topic


def get_topics_for_subject(subject: str) -> QuerySet[Topic]:
    return Topic.objects.filter(subject__name=subject)


def get_quizes_for_topic(topic: str) -> QuerySet[Quiz]:
    return Quiz.objects.filter(topic__name=topic)


def get_ques_for_quiz(quiz: str) -> QuerySet[Quiz]:
    return Question.objects.filter(quiz__name=quiz)
