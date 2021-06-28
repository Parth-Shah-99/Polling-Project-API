from django.contrib import admin
from .models import Question, Answer, Comment, AnswerVote, CommentVote

# Register your models here.

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	list_display = ["id", "question_text", "question_author", "is_solved"]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
	list_display = ["id", "answer_text", "answer_author", "question"]

@admin.register(AnswerVote)
class AnswerVoteAdmin(admin.ModelAdmin):
	list_display = ["id", "user", "answer", "vote"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ["id", "comment_text", "comment_author", "answer"]

@admin.register(CommentVote)
class CommentVoteAdmin(admin.ModelAdmin):
	list_display = ["id", "user", "comment", "choice"]