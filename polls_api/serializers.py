from rest_framework import serializers
from .models import Question, Answer, Comment, AnswerVote, CommentVote



class AnswerVoteSerializer(serializers.ModelSerializer):
	class Meta:
		model = AnswerVote
		fields = ["id", "user", "answer", "vote"]


class CommentVoteSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommentVote
		fields = ["id", "user", "comment", "choice"]




class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ["id", "comment_text", "comment_author", "answer", "user_choices"]


class AnswerSerializer(serializers.ModelSerializer):
	comments = CommentSerializer(many=True, read_only=True)

	class Meta:
		model = Answer
		fields = ["id", "answer_text", "answer_author", "question", "comments"]


class QuestionSerializer(serializers.ModelSerializer):
	answers = AnswerSerializer(many=True, read_only=True)
	
	class Meta:
		model = Question
		fields = ["id", "question_text", "question_author", "is_solved", "answers"]
















# answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
# answers = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='answer-detail')
# answers = serializers.SlugRelatedField(many=True, read_only=True, slug_field='answer_text')
# answers = serializers.HyperlinkedIdentityField(view_name='answer-detail')