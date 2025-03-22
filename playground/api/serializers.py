from rest_framework import serializers
from playground.models import Question,Solved

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"
    
class SolvedSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = "user.username")
    class Meta:
        model = Solved
        fields = ("id","user","question")