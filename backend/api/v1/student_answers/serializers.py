from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from quizzes.models import StudentAnswer, QuizAttempt, Question, Option


class StudentAnswerSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    quiz_attempt = serializers.PrimaryKeyRelatedField(
        queryset=QuizAttempt.objects.all()
    )

    question = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all()
    )

    selected_option = serializers.PrimaryKeyRelatedField(
        queryset=Option.objects.all()
    )

    class Meta:
        model = StudentAnswer
        fields = [
            "id",
            "quiz_attempt",
            "question",
            "selected_option",
            "is_correct",
            "marks_obtained",
            "answered_at",
        ]

        read_only_fields = [
            "id",
            "answered_at",
            "is_correct",
            "marks_obtained",
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_id(self, obj):
        return str(obj.id)

    def validate(self, attrs):
        question = attrs["question"]
        option = attrs["selected_option"]

        if option.question != question:
            raise serializers.ValidationError(
                "Selected option does not belong to this question."
            )

        return attrs

    def create(self, validated_data):
        question = validated_data["question"]
        option = validated_data["selected_option"]

        validated_data["is_correct"] = option.is_correct

        if option.is_correct:
            validated_data["marks_obtained"] = question.marks
        else:
            validated_data["marks_obtained"] = 0

        return super().create(validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["quiz_attempt"] = str(instance.quiz_attempt.id)

        data["question"] = {
            "id": str(instance.question.id),
            "question_text": instance.question.question_text,
        }

        data["selected_option"] = {
            "id": str(instance.selected_option.id),
            "option_text": instance.selected_option.option_text,
        }

        return data