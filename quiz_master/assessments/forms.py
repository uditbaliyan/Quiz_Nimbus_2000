from django import forms


class QuizForm(forms.Form):
    def __init__(self, *args, quiz=None, **kwargs):
        super().__init__(*args, **kwargs)

        if not quiz:
            return

        questions = quiz.questions.prefetch_related("choices")

        for question in questions:
            self.fields[f"question_{question.id}"] = forms.ModelChoiceField(
                queryset=question.choices.all(),
                widget=forms.RadioSelect,
                label=question.text,
                empty_label=None,
            )
