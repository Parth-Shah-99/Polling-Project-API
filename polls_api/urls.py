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

    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('login_api/', views.LoginAPIView.as_view(), name='login_api'),
    path('logout_api/', views.LogoutAPIView.as_view(), name='logout_api'),

    path('question/', views.QuestionAPIView.as_view(), name='question_view'),
    path('question/<int:pk>/', views.QuestionDetailAPIView.as_view(), name='question_detail'),

    path('answer/', views.AnswerAPIView.as_view(), name='answer_view'),
    path('answer/<int:pk>/', views.AnswerDetailAPIView.as_view(), name='answer_detail'),

    path('comment/', views.CommentAPIView.as_view(), name='comment_view'),
    path('comment/<int:pk>/', views.CommentDetailAPIView.as_view(), name='comment_detail'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
