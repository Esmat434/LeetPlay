from django.urls import path
from .views import (
    QuestionGetPostView,QuestionGetPutDeleteView,SolvedGetPostView,SolvedGetPutDelete
)

urlpatterns = [
    path('api/question/',QuestionGetPostView.as_view(),name='question-get-post'),
    path('api/question/<int:pk>/',QuestionGetPutDeleteView.as_view(),name="question-get-put-delete"),
    path('api/question/solved/',SolvedGetPostView.as_view(),name='question-solved-get-post'),
    path('api/question/solved/<int:pk>/',SolvedGetPutDelete.as_view(),name='question-solved-get-put-delete')
]