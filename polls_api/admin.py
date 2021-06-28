from django.contrib import admin
from .models import Question, Answer, Comment

# Register your models here.

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	list_display = ("id", "question_text", "question_author", "is_solved", "created_on")
	list_display_links = ("id", "question_text")

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
	list_display = ["id", "answer_text", "answer_author", "question", "created_on"]
	list_display_links = ("id", "answer_text")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ["id", "comment_text", "comment_author", "answer", "created_on"]
	list_display_links = ("id", "comment_text")
