from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    question_author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_solved = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text

    def __unicode__(self):
        return __str__(self)


class Answer(models.Model):
    answer_text = models.CharField(max_length=1000)
    answer_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answer_author")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    user_votes = models.ManyToManyField(User, through="AnswerVote", related_name="user_votes")

    def __str__(self):
        return self.answer_text

    def __unicode__(self):
        return __str__(self)


class AnswerVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    vote = models.BooleanField(blank=True)

    def __str__(self):
        return self.user.username + " " + self.answer.answer_text

    def __unicode__(self):
        return __str__(self)

    class Meta:
    	verbose_name = "Answer Vote"
    	verbose_name_plural = "Answer Votes"


class Comment(models.Model):
    comment_text = models.CharField(max_length=100)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="comments")
    user_choices = models.ManyToManyField(User, through="CommentVote", related_name="user_choices")

    def __str__(self):
        return self.comment_text

    def __unicode__(self):
        return __str__(self)


class CommentVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    choice = models.BooleanField(blank=True)

    def __str__(self):
        return self.user.username + " " + self.comment.comment_text

    def __unicode__(self):
        return __str__(self)

    class Meta:
    	verbose_name = "Comment Choice"
    	verbose_name_plural = "Comment Choices"
