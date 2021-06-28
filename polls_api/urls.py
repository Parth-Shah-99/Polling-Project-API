from django.urls import path, include
from polls_api import views
from rest_framework.routers import DefaultRouter


# Creating Router object
# router = DefaultRouter()

# Registering routers for Question, Answer, Comment
# router.register('question', views.QuestionViewSet, basename='question')
# router.register('answer', views.AnswerViewSet, basename='answer')
# router.register('comment', views.CommentViewSet, basename='comment')

# urls
urlpatterns = [
    # path('', include(router.urls)),
    path('question/', views.QuestionAPIView.as_view(), name='question_view'),
    path('question/<int:pk>/', views.QuestionDetailAPIView.as_view(), name='question_detail'),
    path('question/<int:pk>/vote/', views.QuestionDetailAPIView.as_view(), name='question_vote'),

    path('answer/', views.AnswerAPIView.as_view(), name='answer_view'),
    path('answer/<int:pk>/', views.AnswerDetailAPIView.as_view(), name='answer_detail'),
    path('answer/<int:pk>/vote/', views.AnswerDetailAPIView.as_view(), name='answer_vote'),

    path('comment/', views.CommentAPIView.as_view(), name='comment_view'),
    path('comment/<int:pk>/', views.CommentDetailAPIView.as_view(), name='comment_detail'),
    path('comment/<int:pk>/vote/', views.CommentDetailAPIView.as_view(), name='comment_vote'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
