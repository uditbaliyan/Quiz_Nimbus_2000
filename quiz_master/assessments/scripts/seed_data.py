from faker import Faker

from quiz_master.assessments.models import Choice
from quiz_master.assessments.models import Difficulty
from quiz_master.assessments.models import Question
from quiz_master.assessments.models import Quiz
from quiz_master.assessments.models import Subject
from quiz_master.assessments.models import Topic

fake = Faker()

# -------- CONFIG --------
SUBJECTS = 5
TOPICS_PER_SUBJECT = 4
QUIZZES_PER_TOPIC = 3
QUESTIONS_PER_QUIZ = 15
CHOICES_PER_QUESTION = 4
# ------------------------


def run():
    for _ in range(SUBJECTS):
        subject_name = fake.sentence(nb_words=2)
        subject = Subject.objects.create(
            name=subject_name,
            description=fake.sentence(),
        )

        for _ in range(TOPICS_PER_SUBJECT):
            topic_name = fake.sentence(nb_words=3)
            topic = Topic.objects.create(
                name=topic_name,
                description=fake.sentence(),
                difficulty=fake.random_element(Difficulty.values),
                subject=subject,
            )

            for _ in range(QUIZZES_PER_TOPIC):
                quiz_name = fake.sentence(nb_words=3)
                quiz = Quiz.objects.create(
                    name=quiz_name,
                    description=fake.sentence(),
                    difficulty=fake.random_element(Difficulty.values),
                    topic=topic,
                )

                for _ in range(QUESTIONS_PER_QUIZ):
                    question = Question.objects.create(
                        quiz=quiz,
                        text=fake.sentence(),
                    )

                    correct_index = fake.random_int(
                        min=0,
                        max=CHOICES_PER_QUESTION - 1,
                    )

                    for i in range(CHOICES_PER_QUESTION):
                        Choice.objects.create(
                            question=question,
                            text=fake.word().capitalize(),
                            is_correct=(i == correct_index),
                        )
