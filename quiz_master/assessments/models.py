import itertools

from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

SLUG_GENERATION_ERROR = "Failed to generate unique slug"


def generate_unique_slug(instance, field, slug_field="slug") -> str:
    base = slugify(field)
    slug = base
    model = instance.__class__

    for i in itertools.count(1):
        qs = model.objects.filter(**{slug_field: slug}).exclude(pk=instance.pk)

        if not qs.exists():
            return slug

        slug = f"{base}-{i}"

    raise RuntimeError(SLUG_GENERATION_ERROR)


class Difficulty(models.TextChoices):
    EASY = "E", "Easy"
    MEDIUM = "M", "Medium"
    HARD = "H", "Hard"


class Subject(models.Model):
    name = models.CharField(max_length=50, validators=[MinLengthValidator(3)])
    description = models.CharField(max_length=100, validators=[MinLengthValidator(20)])
    slug = models.SlugField(unique=True, blank=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.name)
        super().save(*args, **kwargs)


class Topic(models.Model):
    name = models.CharField(max_length=50, validators=[MinLengthValidator(3)])
    description = models.CharField(max_length=100, validators=[MinLengthValidator(20)])
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
            self.slug = generate_unique_slug(self, self.name)
        super().save(*args, **kwargs)


class Quiz(models.Model):
    name = models.CharField(max_length=50, validators=[MinLengthValidator(3)])
    slug = models.SlugField(unique=True, blank=False)
    difficulty = models.CharField(max_length=1, choices=Difficulty, default="E")
    description = models.CharField(max_length=100, validators=[MinLengthValidator(20)])

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="quizzes")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.name)
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
        constraints = [
            models.UniqueConstraint(
                fields=["question"],
                condition=models.Q(is_correct=True),
                name="unique_correct_choice_per_question",
            )
        ]
        verbose_name = "Choice"
        verbose_name_plural = "Choices"

    def __str__(self):
        return self.text
