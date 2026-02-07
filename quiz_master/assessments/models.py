from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Difficulty(models.TextChoices):
    EASY = "E", "Easy"
    MEDIUM = "M", "Medium"
    HARD = "H", "Hard"


class Subject(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Topic(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=1, choices=Difficulty, default="E")
    slug = models.SlugField(unique=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="topics"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Quiz(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=False)
    difficulty = models.CharField(max_length=1, choices=Difficulty, default="E")
    description = models.CharField(max_length=100)

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="quizzes")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


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
