from django.views.generic import ListView
from django.views.generic import TemplateView

from quiz_master.assessments.models import Subject

# Create your views here.


class ModelView(TemplateView):
    template_name = ".html"


class SubjectListView(ListView):
    model = Subject
    template_name = "assessments/subjects.html"
    context_object_name = "subjects"
