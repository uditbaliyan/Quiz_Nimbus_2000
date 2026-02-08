import nested_admin
from django.contrib import admin

from .models import Choice
from .models import Question
from .models import Quiz
from .models import Subject
from .models import Topic

# ---------- Inlines ----------


class ChoiceInline(nested_admin.NestedTabularInline):
    model = Choice
    extra = 2


class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    inlines = [ChoiceInline]
    extra = 1
    show_change_link = True


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1


# ---------- Admins ----------


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")

    search_fields = ("name", "description")

    prepopulated_fields = {"slug": ("name",)}

    inlines = [TopicInline]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "difficulty", "created_at")

    list_filter = ("difficulty", "subject")

    search_fields = ("name", "description", "subject__name")

    autocomplete_fields = ("subject",)

    list_select_related = ("subject",)

    prepopulated_fields = {"slug": ("name",)}


@admin.register(Quiz)
class QuizAdmin(nested_admin.NestedModelAdmin):
    list_display = (
        "name",
        "topic",
        "difficulty",
        "question_count",
        "created_at",
    )

    list_filter = ("difficulty", "topic")

    search_fields = (
        "name",
        "description",
        "topic__name",
    )

    autocomplete_fields = ("topic",)

    list_select_related = ("topic",)

    prepopulated_fields = {"slug": ("name",)}

    inlines = [QuestionInline]

    @admin.display(description="Questions")
    def question_count(self, obj):
        return obj.questions.count()
