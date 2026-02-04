from django import forms

from quiz_master.assessments.models import Subject


class BookForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name"]
