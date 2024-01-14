from rest_framework.serializers import ModelSerializer
from .models import *

class ReytingSerializer(ModelSerializer):
    class Meta:
        model = Reyting
        fields = '__all__'

class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class SohaSerializer(ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Soha
        fields = '__all__'

class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'