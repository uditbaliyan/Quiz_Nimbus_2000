# Register your models here.
# blog/admin.py
import nested_admin
from django.contrib import admin

from .models import Choice
from .models import Question
from .models import Quiz
from .models import Subject
from .models import Topic


class ChoiceInline(nested_admin.NestedTabularInline):
    model = Choice
    extra = 3


class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    inlines = [ChoiceInline]
    extra = 2


@admin.register(Quiz)
class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 3


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    inlines = [TopicInline]
