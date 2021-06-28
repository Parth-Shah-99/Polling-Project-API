from rest_framework import serializers
from .models import Question, Answer, Comment
from datetime import datetime


class CommentSerializer(serializers.ModelSerializer):
    created_on = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ["id", "comment_text", "comment_author", "answer", "like_users", "dislike_users", "created_on"]

    def get_created_on(self, obj):
        return obj.created_on.strftime("%Y-%m-%d %X")


class AnswerSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    created_on = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ["id", "answer_text", "answer_author", "question", "upvote_users", "downvote_users", "comments", "created_on"]
        extra_kwargs = {'answer_text': {'required': False},
        				'answer_author': {'required': False},
        				'question': {'required': False}
        			}

    def get_created_on(self, obj):
        return obj.created_on.strftime("%Y-%m-%d %X")


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    created_on = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = ["id", "question_text", "question_author", "is_solved", "answers", "created_on"]
        extra_kwargs = {'question_text': {'required': False},
        				'question_author': {'required': False},
        				'is_solved': {'required': False}
        			}


    def get_created_on(self, obj):
        return obj.created_on.strftime("%Y-%m-%d %X")

    
















# answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
# answers = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='answer-detail')
# answers = serializers.SlugRelatedField(many=True, read_only=True, slug_field='answer_text')
# answers = serializers.HyperlinkedIdentityField(view_name='answer-detail')