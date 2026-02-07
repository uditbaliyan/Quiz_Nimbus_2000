from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import View

from quiz_master.assessments.models import Quiz
from quiz_master.assessments.models import Subject
from quiz_master.assessments.models import Topic

from .forms import QuizForm


class HomeModelView(View):
    template_name = "assessments/home.html"

    def get(self, request):
        return render(request, self.template_name)


class SubjectListView(ListView):
    model = Subject
    template_name = "assessments/subjects.html"
    context_object_name = "subjects"


class TopicListView(ListView):
    template_name = "assessments/topics.html"
    context_object_name = "topics"

    def get_queryset(self):
        subject_id = self.kwargs["subject_id"]

        return Topic.objects.filter(subject_id=subject_id).select_related("subject")


class QuizListView(ListView):
    template_name = "assessments/quizes.html"
    context_object_name = "quizzes"

    def get_queryset(self):
        topic_id = self.kwargs["topic_id"]

        return Quiz.objects.filter(topic_id=topic_id).select_related("topic")


class QuizView(FormView):
    template_name = "assessments/quiz.html"
    form_class = QuizForm

    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(
            Quiz.objects.prefetch_related("questions__choices"),
            pk=self.kwargs["quiz_id"],
        )
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["quiz"] = self.quiz
        return kwargs

    def form_valid(self, form):
        score = 0

        for selected_choice in form.cleaned_data.values():
            if selected_choice.is_correct:
                score += 1

        return render(
            self.request,
            "assessments/result.html",
            {"score": score, "quiz": self.quiz},
        )


class SubjectCreateView(CreateView):
    model = Subject
    fields = ["name"]
    template_name = "assessments/form.html"
    success_url = reverse_lazy("subject_list")
