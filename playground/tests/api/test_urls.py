from django.urls import reverse,resolve
from rest_framework.test import APISimpleTestCase
from rest_framework import status
from playground.api.views import (
    QuestionGetPostView,QuestionGetPutDeleteView,SolvedGetPostView,SolvedGetPutDelete
)

class TestUrls(APISimpleTestCase):
    def test_question_get_post_url(self):
        response = reverse("question-get-post")
        self.assertEqual(resolve(response).func.view_class,QuestionGetPostView)
    
    def test_question_get_put_delete_url(self):
        response = reverse("question-get-put-delete",args=[1])
        self.assertEqual(resolve(response).func.view_class,QuestionGetPutDeleteView)
    
    def test_question_solved_get_post_url(self):
        response = reverse("question-solved-get-post")
        self.assertEqual(resolve(response).func.view_class,SolvedGetPostView)
    
    def test_question_solved_get_put_delete_url(self):
        response = reverse("question-solved-get-put-delete",args=[1])
        self.assertEqual(resolve(response).func.view_class,SolvedGetPutDelete)