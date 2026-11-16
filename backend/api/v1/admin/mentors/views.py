from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from django.contrib.auth import get_user_model
from mentors.models import MentorOnboardingApplication
from api.v1.auth.permissions import IsAdminRole
from api.v1.mentors.onboarding.serializers import (
    MentorOnboardingApplicationSerializer,
    AdminOnboardingActionSerializer,
)

User = get_user_model()


class AdminMentorApplicationListView(generics.ListAPIView):
    permission_classes = [IsAdminRole]
    serializer_class = MentorOnboardingApplicationSerializer
    queryset = MentorOnboardingApplication.objects.all().order_by("-created_at")

    @extend_schema(
        summary="List mentor onboarding applications",
        responses={
            200: MentorOnboardingApplicationSerializer(many=True),
            403: OpenApiResponse(description="Administrator access required"),
        },
        tags=["Admin - Mentor Onboarding"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AdminMentorApplicationDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAdminRole]
    serializer_class = MentorOnboardingApplicationSerializer
    queryset = MentorOnboardingApplication.objects.all()
    lookup_url_kwarg = "application_id"

    @extend_schema(
        summary="View a mentor onboarding application",
        responses={
            200: MentorOnboardingApplicationSerializer,
            403: OpenApiResponse(description="Administrator access required"),
            404: OpenApiResponse(description="Application not found"),
        },
        tags=["Admin - Mentor Onboarding"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class AdminMentorApplicationActionView(APIView):
    permission_classes = [IsAdminRole]
    
    def get_application(self, application_id):
        try:
            return MentorOnboardingApplication.objects.get(id=application_id)
        except MentorOnboardingApplication.DoesNotExist:
            return None

    def _audit(self, application, actor, action, reason):
        application.reviewed_by = actor
        application.reviewed_at = timezone.now()
        if action == "reject":
            application.status = "REJECTED"
            application.rejection_reason = reason or "No reason provided."
            application.correction_notes = ""
        elif action == "approve":
            application.status = "APPROVED"
            application.approved_at = timezone.now()
            application.rejection_reason = ""
            application.correction_notes = ""
        elif action == "request_correction":
            application.status = "NEEDS_CORRECTION"
            application.correction_notes = reason or "Additional information required."
            application.rejection_reason = ""
        application.save()

    @extend_schema(
        summary="Approve/reject/request-correction mentor application",
        parameters=[
            OpenApiParameter(
                name="application_id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Application ID",
            ),
            OpenApiParameter(
                name="action",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Action: approve, reject, or request_correction",
            ),
        ],
        request=AdminOnboardingActionSerializer,
        responses={
            200: MentorOnboardingApplicationSerializer,
            400: OpenApiResponse(description="Invalid action"),
            403: OpenApiResponse(description="Administrator access required"),
            404: OpenApiResponse(description="Application not found"),
            409: OpenApiResponse(description="Already in target state"),
        },
        tags=["Admin - Mentor Onboarding"],
    )
    def post(self, request, application_id, action):
        application = self.get_application(application_id)
        if not application:
            return Response(
                {"detail": "Application not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = AdminOnboardingActionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        reason = serializer.validated_data.get("reason", "")

        if action == "approve":
            if application.status == "APPROVED":
                return Response(
                    {"detail": "Application is already approved."},
                    status=status.HTTP_409_CONFLICT,
                )
            self._audit(application, request.user, "approve", reason)
        elif action == "reject":
            if application.status == "REJECTED":
                return Response(
                    {"detail": "Application is already rejected."},
                    status=status.HTTP_409_CONFLICT,
                )
            self._audit(application, request.user, "reject", reason)
        elif action == "request_correction":
            if application.status == "NEEDS_CORRECTION":
                return Response(
                    {"detail": "Application already requests correction."},
                    status=status.HTTP_409_CONFLICT,
                )
            self._audit(application, request.user, "request_correction", reason)
        else:
            return Response(
                {"detail": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            MentorOnboardingApplicationSerializer(application).data,
            status=status.HTTP_200_OK,
        )


class AdminMentorSuspendView(APIView):
    permission_classes = [IsAdminRole]
    serializer_class = None

    @extend_schema(
        summary="Suspend a mentor",
        parameters=[
            OpenApiParameter(
                name="mentor_id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Mentor ID",
            ),
        ],
        responses={
            200: OpenApiResponse(description="Mentor suspended"),
            403: OpenApiResponse(description="Administrator access required"),
            404: OpenApiResponse(description="Mentor not found"),
        },
        tags=["Admin - Mentor Onboarding"],
    )
    def post(self, request, mentor_id):
        try:
            mentor = User.objects.get(id=mentor_id, role="mentor")
        except User.DoesNotExist:
            return Response(
                {"detail": "Mentor not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        application = (
            MentorOnboardingApplication.objects.filter(user=mentor)
            .order_by("-created_at")
            .first()
        )
        if application:
            application.status = "SUSPENDED"
            application.reviewed_by = request.user
            application.reviewed_at = timezone.now()
            application.save()
        return Response(
            {"detail": "Mentor suspended."}, status=status.HTTP_200_OK
        )


class AdminMentorReactivateView(APIView):
    permission_classes = [IsAdminRole]
    serializer_class = None

    @extend_schema(
        summary="Reactivate a mentor",
        parameters=[
            OpenApiParameter(
                name="mentor_id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Mentor ID",
            ),
        ],
        responses={
            200: OpenApiResponse(description="Mentor reactivated"),
            403: OpenApiResponse(description="Administrator access required"),
            404: OpenApiResponse(description="Mentor not found"),
        },
        tags=["Admin - Mentor Onboarding"],
    )
    def post(self, request, mentor_id):
        try:
            mentor = User.objects.get(id=mentor_id, role="mentor")
        except User.DoesNotExist:
            return Response(
                {"detail": "Mentor not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        application = (
            MentorOnboardingApplication.objects.filter(user=mentor)
            .order_by("-created_at")
            .first()
        )
        if application:
            application.status = "APPROVED"
            application.reviewed_by = request.user
            application.reviewed_at = timezone.now()
            application.save()
        return Response(
            {"detail": "Mentor reactivated."}, status=status.HTTP_200_OK
        )