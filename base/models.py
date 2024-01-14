from django.db import models
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.text import slugify


class Soha(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True)
    questions = models.ManyToManyField("Question", blank=True)

    class Meta:
        verbose_name_plural = "Soha"

    def __str__(self):
        return self.name

class Reyting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    soha = models.ForeignKey(Soha, on_delete=models.CASCADE)
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    percentage = models.FloatField()

    class Meta:
        verbose_name_plural = "Ratings"

    def __str__(self):
        return f"{self.user.username}'s Rating"

class Question(models.Model):
    question_name = models.CharField(max_length=120)

    class Meta:
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.question_name

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    correct = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Answers"

    def __str__(self):
        return self.answer
    
@receiver(post_save, sender=Soha)
def post_save_category(instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
        instance.save()