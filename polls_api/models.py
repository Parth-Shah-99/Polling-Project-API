from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    question_author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_solved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text

    def __unicode__(self):
        return __str__(self)


class Answer(models.Model):
    answer_text = models.CharField(max_length=1000)
    answer_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answer_author")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    upvote_users = models.ManyToManyField(User, blank=True, related_name="upvote_users")
    downvote_users = models.ManyToManyField(User, blank=True, related_name="downvote_users")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer_text

    def __unicode__(self):
        return __str__(self)



class Comment(models.Model):
    comment_text = models.CharField(max_length=100)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="comments")
    like_users = models.ManyToManyField(User, blank=True, related_name="like_users")
    dislike_users = models.ManyToManyField(User, blank=True, related_name="dislike_users")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_text

    def __unicode__(self):
        return __str__(self)


