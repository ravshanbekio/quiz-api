from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters, permissions
from django.db.models import Avg
from .serializers import *
from .models import *

class ReytingViewSet(ModelViewSet):
    serializer_class = ReytingSerializer
    queryset = Reyting.objects.select_related().order_by('-percentage')
    permission_classes = [permissions.IsAuthenticated]

    allowed_methods = ['GET','POST','PUT']
    http_method_names = ['get','post','put']

class SohaViewSet(ModelViewSet):
    serializer_class = SohaSerializer
    queryset = Soha.objects.select_related()
    permission_classes = [permissions.IsAuthenticated]

    allowed_methods = ['GET','POST','PUT']
    http_method_names = ['get','post','put']

    #making queries with slug field
    lookup_field = 'slug'

    filter_backends = [filters.SearchFilter,]
    search_fields = ['id','name','age','country','city','username',]

    @action(detail=True, methods=['GET','POST'])
    def questions(self, request, slug):
        soha = Soha.objects.get(slug=slug)
        questions = soha.question.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def submit_answers(self, request, slug):
        soha = self.get_object()
        user = request.user
        answers_data = request.data.get('answers', [])

        total_questions = soha.questions.count()
        correct_answers = 0

        for answer_data in answers_data:
            answer = answer_data.get('answer')

            try:
                answer = Answer.objects.get(answer=answer)
                if answer.correct:
                    correct_answers += 1
            except Answer.DoesNotExist:
                pass

        percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

        # Check if a Reyting instance already exists for the user and Soha
        reyting_instance = Reyting.objects.filter(user=user, soha=soha).first()

        if reyting_instance:
            # Update the existing record
            reyting_instance.total_questions = total_questions
            reyting_instance.correct_answers = correct_answers
            reyting_instance.percentage = percentage
            reyting_instance.save()
        else:
            # Create a new record
            Reyting.objects.create(user=user, soha=soha, total_questions=total_questions, correct_answers=correct_answers, percentage=percentage)

        # Calculate the average percentage for the specified Soha across all users
        average_percentage = Reyting.objects.filter(soha=soha).aggregate(Avg('percentage'))['percentage__avg']

        result_data = {
            'total': total_questions,
            'found': correct_answers,
            'in_percent': round(percentage, 2),
        }

        return Response(result_data)

class QuestionViewSet(ModelViewSet):
    serializer_class = ReytingSerializer
    queryset = Question.objects.select_related()
    permission_classes = [permissions.IsAuthenticated]

    allowed_methods = ['GET','POST','PUT']
    http_method_names = ['get','post','put']
    filter_backends = [filters.SearchFilter,]
    search_fields = ['id','name','age','country','city','username',]

class AnswerViewSet(ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.select_related()
    permission_classes = [permissions.IsAuthenticated]

    allowed_methods = ['GET','POST','PUT']
    http_method_names = ['get','post','put']
    filter_backends = [filters.SearchFilter,]
    search_fields = ['id','name','age','country','city','username',]