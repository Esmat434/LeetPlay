from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import (
    IsAuthenticatedAndSuperuserPermission,IsOwnerOrReadOnly
)

from playground.models import (
    Question,Solved
)

from playground.api.serializers import (
    QuestionSerializer,SolvedSerializer
)

class QuestionGetPostView(APIView):
    permission_classes = [IsAuthenticatedAndSuperuserPermission]

    def get(self,request):
        unsolved_question = Question.objects.filter(~Q(solved__user = request.user))
        serializer = QuestionSerializer(unsolved_question,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = QuestionSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class QuestionGetPutDeleteView(APIView):
    permission_classes = [IsAuthenticatedAndSuperuserPermission]

    def get_question(self,pk):
        try:
            question = Question.objects.get(id = pk)
            return question
        except Question.DoesNotExist:
            return None

    def get(self,request,pk):
        question = self.get_question(pk)
        if not question:
            return Response({"error":"question does not exists."},status=status.HTTP_400_BAD_REQUEST)
        serializer = QuestionSerializer(question)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        question = self.get_question(pk)

        if not question:
            return Response({"error":"question does  not exists."},status=status.HTTP_400_BAD_REQUEST)
        
        serializer = QuestionSerializer(question,data = request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        question = self.get_question(pk)
        
        if not question:
            return Response({"error":"question does not exists."},status=status.HTTP_400_BAD_REQUEST)
        
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SolvedGetPostView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get(self,request):
        solved_question = Solved.objects.filter(user = request.user)
        serializer = SolvedSerializer(solved_question,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = SolvedSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class SolvedGetPutDelete(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get_question_solved(self,request,pk):
        try:
            solved_question = Solved.objects.get(id = pk , user = request.user)
            return solved_question
        except Solved.DoesNotExist:
            return None

    def get(self,request,pk):
        solved_question = self.get_question_solved(request,pk)
        if not solved_question:
            return Response({"error":"the question does not exists."},status=status.HTTP_400_BAD_REQUEST)
        serializer = SolvedSerializer(solved_question)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,pk):
        solved_question = self.get_question_solved(request,pk)
        if not solved_question:
            return Response({"error":"question does not exists."},status=status.HTTP_400_BAD_REQUEST)
        serializer = SolvedSerializer(solved_question,data = request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        solved_question = self.get_question_solved(request,pk)
        if not solved_question:
            return Response({"error":"the question does not exists."},status=status.HTTP_400_BAD_REQUEST)
        solved_question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)