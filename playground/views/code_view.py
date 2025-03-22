import json
from django.shortcuts import render,HttpResponse
from django.db.models import Q
from django.views import View
from playground.models import (
    Question
)

class QuestionListCreateView(View):
    def get(self,request):
        unsolved_questions = Question.objects.filter(category='Easy',tag = 'Array')
        # تبدیل به JSON
        questions_data = [
            {"title": question.title, "link": question.link}
            for question in unsolved_questions
        ]
        return render(request,'home/playground.html',{'questions_json': json.dumps(questions_data)})
    
    def post(self,request):
        data = request.POST
        category = data.get('category')
        tag = data.get('tag')
        unsolved_questions = Question.objects.filter(~Q(solved__user = request.user),
                                                     category = category,tag = tag)
        # تبدیل به JSON
        questions_data = [
            {"title": question.title, "link": question.link}
            for question in unsolved_questions
        ]
        return render(request,'home/playground.html',{'questions_json': json.dumps(questions_data)})