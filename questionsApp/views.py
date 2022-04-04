from rest_framework import generics, permissions
from . import serializers
from django.contrib.auth.models import User
from .models import Question, Comment
from .serializers import (
    QuestionListSerializer,
    QuestionDetailSerializer,
    QuestionAddSerializer,
)
from .permissions import IsOwnerOrReadOnly
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
    HTTP_204_NO_CONTENT,
)
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import json


class QuestionList(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionListSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class QuestionAdd(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionAddSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=HTTP_403_FORBIDDEN,
            )


class QuestionDetail(generics.RetrieveAPIView):
    context_object_name = "question"
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_context_data(self, **kwargs):
        context = super(QuestionDetail, self).get_context_data(**kwargs)
        context["comment_list"] = Comment.objects.all()
        return context


class CommentList(generics.ListCreateAPIView):
    context_object_name = "comment_list"
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentDetailSerializer
    permission_classes = [permissions.IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = Comment.objects.get(id=request.headers["commentId"])
        self.perform_destroy(instance)
        return Response(status=HTTP_204_NO_CONTENT)


class PublicQuestionList(generics.ListAPIView):
    serializer_class = serializers.QuestionListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Question.objects.filter(public=True).filter(answer__isnull=False)


class UserQuestionList(generics.ListAPIView):
    serializer_class = serializers.QuestionListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Question.objects.filter(owner=self.request.user)


class AnswerQuestionDetail(generics.RetrieveUpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = serializers.AnswerSerializer
    permission_classes = [permissions.IsAdminUser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(
            {"detail": "Answer was successfully given."}, status=HTTP_200_OK
        )


class UpdateQuestionDetail(generics.RetrieveUpdateAPIView):
    context_object_name = "question"
    queryset = Question.objects.all()
    serializer_class = serializers.UpdateQuestionDetailSerializer
    permission_classes = [permissions.IsAdminUser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(
            {"detail": "Category was successfully updated."}, status=HTTP_200_OK
        )


#
