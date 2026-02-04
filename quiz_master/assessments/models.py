from django.db import models
from django.utils.translation import gettext_lazy as _


class Subject(models.Model):
    name = models.CharField(_("Subject Name"), max_length=50)

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(_("Topic Name"), max_length=50)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="topics"
    )

    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"

    def __str__(self):
        return self.name


class Quiz(models.Model):
    name = models.CharField(_("Quiz Name"), max_length=50)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="quizzes")

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")

    text = models.CharField(_("Question"), max_length=255)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )

    text = models.CharField(_("Option"), max_length=100)
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Choice"
        verbose_name_plural = "Choices"

    def __str__(self):
        return self.text
