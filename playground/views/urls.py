from django.urls import path
from .code_view import (
    QuestionListCreateView
)

urlpatterns = [
    path('',QuestionListCreateView.as_view(),name='home')
]