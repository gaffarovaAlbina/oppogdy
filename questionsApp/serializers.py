from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Question, Comment
import datetime


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]
        read_only_fields = ["first_name", "last_name"]

    def to_representation(self, instance):
        result = super(PersonSerializer, self).to_representation(instance)
        new_result = "{} {}".format(result["first_name"], result["last_name"])
        return new_result


class QuestionListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.get_category_display()

    class Meta:
        model = Question
        fields = ["id", "title", "answer", "category", "owner", "public"]


class QuestionAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "title", "answer", "category"]
        read_only_fields = ["id", "answer"]


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Comment
        fields = ["id", "body", "owner", "created", "question"]


class CommentDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    question = serializers.ReadOnlyField(source="question.title")

    class Meta:
        model = Comment
        fields = ["id", "body", "owner", "created", "question"]


class QuestionDetailSerializer(serializers.ModelSerializer):
    owner = PersonSerializer()
    comments = CommentSerializer(many=True, read_only=True)
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.get_category_display()

    class Meta:
        model = Question
        fields = [
            "id",
            "title",
            "createdQuestion",
            "owner",
            "category",
            "answer",
            "createdAnswer",
            "comments",
        ]
        depth = 1


class AnswerSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.get_category_display()

    class Meta:
        model = Question
        fields = ["id", "title", "category", "answer", "createdAnswer"]
        read_only_fields = ["id", "title", "category"]

    def update(self, instance, validated_data):
        instance.answer = validated_data.get("answer", instance.answer)
        instance.createdAnswer = datetime.datetime.now() + datetime.timedelta(hours=3)
        instance.save()
        return instance


class UpdateQuestionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "title", "category", "answer"]
        read_only_fields = ["id", "title", "answer"]

    def update(self, instance, validated_data):
        instance.category = validated_data.get("category", instance.category)
        print(instance.category)
        instance.save()
        return instance
