from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from rest_framework.parsers import JSONParser
from .models import Question, Answer, Comment
from .serializers import QuestionSerializer, AnswerSerializer, CommentSerializer
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

class QuestionAPIView(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        # question_text necessary to pass
        if request.data.get('question_text', None) in [None, ""]:
            return Response({"error": "Please provide question text to create new question."}, status=status.HTTP_400_BAD_REQUEST)
        
        # question_author default to user who is logged in
        request.data.update({"question_author": request.user.id})

        # is_solved default to False even if True is passed
        request.data.update({"is_solved": False})

        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailAPIView(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        serializer = QuestionSerializer(self.get_object(pk))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):

        # can update [question_text, is_solved] by author
        if self.get_object(pk).question_author.id != request.user.id:
            return Response({"detail": "You are not authorized to edit this question."}, status=status.HTTP_401_UNAUTHORIZED)

        changes = 0

        # question_text possible to change
        if request.data.get('question_text', None) not in [None, ""]:
            changes += 1

        # question_author not possible to change
        if request.data.get('question_author', None):
            del request.data['question_author']

        # is_solved possible to change
        if request.data.get('is_solved', None):
            changes += 1

        if changes == 0:
            return Response({"error": "Please provide valid data to edit question."}, status=status.HTTP_400_BAD_REQUEST)
        

        serializer = QuestionSerializer(self.get_object(pk), data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response({"detail": "Question deleted successfully !!"}, status=status.HTTP_204_NO_CONTENT)


class AnswerAPIView(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        answers = Answer.objects.all()
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        # answer_text necessary to pass
        if request.data.get('answer_text', None) in [None, ""]:
            return Response({"error": "Please provide answer text to create new answer."}, status=status.HTTP_400_BAD_REQUEST)

        # answer_author default to user who is logged in
        request.data.update({"answer_author": request.user.id})

        # question necessary to pass
        if request.data.get('question', None) in [None, ""]:
            return Response({"error": "Please provide question id to create new answer."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = AnswerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerDetailAPIView(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        serializer = AnswerSerializer(self.get_object(pk))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):

        answer = self.get_object(pk)

        # answer_text possible to change only by author
        if answer.answer_author.id == request.user.id:
            if request.data.get('answer_text', None):
                answer.answer_text = request.data.get('answer_text')
                answer.save()
                return Response({"message": "Answer Text updated successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Please provide valid data to edit answer."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.data.get('answer_text', None):
                 return Response({"detail": "You are not authorized to edit this answer text."}, status=status.HTTP_401_UNAUTHORIZED)
        

        # answer_author not possible to change
        if request.data.get('answer_author', None):
            del request.data['answer_author']


        # vote possible to change by any user other than author (after text update i am returning)
        if answer.upvote_users.all().filter(id=request.user.id).exists():
            current = "upvote"
        elif answer.downvote_users.all().filter(id=request.user.id).exists():
            current = "downvote"
        else:
            current = "neither"

        if request.data.get('vote') == "upvote":
            new = "upvote"
        elif request.data.get('vote') == "downvote":
            new = "downvote"
        else:
            return Response({"error": "Please provide valid vote to edit answer."}, status=status.HTTP_400_BAD_REQUEST)
       

        user = request.user
        if current == "neither" and new == "upvote":
            answer.upvote_users.add(user)
            return Response({"detail": "You have successfully upvoted in this Answer."}, status=status.HTTP_200_OK)
        elif current == "neither" and new == "downvote":
            answer.downvote_users.add(user)
            return Response({"detail": "You have successfully downvoted in this Answer."}, status=status.HTTP_200_OK)
        elif current == "upvote" and new == "downvote":
            answer.upvote_users.remove(user)
            answer.downvote_users.add(user)
            return Response({"detail": "You have successfully downvoted in this Answer."}, status=status.HTTP_200_OK)
        elif current == "downvote" and new == "upvote":
            answer.downvote_users.remove(user)
            answer.upvote_users.add(user)
            return Response({"detail": "You have successfully upvoted in this Answer."}, status=status.HTTP_200_OK)
        elif current == "upvote" and new == "upvote":
            return Response({"detail": "You have already upvoted in this Answer."}, status=status.HTTP_400_BAD_REQUEST)
        elif current == "downvote" and new == "downvote":    
            return Response({"detail": "You have already downvoted in this Answer."}, status=status.HTTP_400_BAD_REQUEST)


        return Response({"error": "Some Error Occured."}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response({"detail": "Answer deleted successfully !!"}, status=status.HTTP_204_NO_CONTENT)



class CommentAPIView(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):

        # necessary = [comment_text, answer]
        request.data.update({"comment_author": request.user.id})
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailAPIView(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        serializer = CommentSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = CommentSerializer(self.get_object(pk), data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response({"detail": "Comment deleted successfully !!"}, status=status.HTTP_204_NO_CONTENT)


def login_user(request):

    if request.user.is_authenticated:
        return render(request, 'home.html')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are successfully Logged In!!")
            return render(request, 'home.html')
        else:
            messages.warning(request, "Incorrect Username/Password!!")

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return render(request, 'logout.html')