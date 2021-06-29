from django.contrib import admin
from .models import Question, Answer, Comment

# Register your models here.

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	list_display = ("id", "question_text", "question_author", "is_solved", "no_of_answers")
	list_display_links = ("id", "question_text")

	def no_of_answers(self, obj):
		return obj.answers.all().count()


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
	list_display = ("id", "answer_text", "answer_author", "question", "upvotes", "downvotes", "no_of_comments")
	list_display_links = ("id", "answer_text")

	def upvotes(self, obj):
		return obj.upvote_users.count()
	def downvotes(self, obj):
		return obj.downvote_users.count()
	def no_of_comments(self, obj):
		return obj.comments.all().count()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ("id", "comment_text", "comment_author", "answer", "likes", "dislikes")
	list_display_links = ("id", "comment_text")

	def likes(self, obj):
		return obj.like_users.count()
	def dislikes(self, obj):
		return obj.dislike_users.count()
